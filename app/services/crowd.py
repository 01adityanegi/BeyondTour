"""
app/services/crowd.py
----------------------
Honest, explainable crowd-score model for BeyondTour.

Score = weighted blend of:
  a) Baseline seasonality (DestinationBaseline table)       — 50 pts max
  b) Festival calendar overlap (CultureEntry date ranges)   — 25 pts max
  c) Live community check-ins in last 6h (CommunityPost)    — 25 pts max

Maps to: 0-33 → green ("Quiet"), 34-66 → yellow ("Moderate"), 67-100 → red ("Crowded")

Results are cached in-process for 15 minutes (simple dict cache).
"""
from __future__ import annotations
import time
from datetime import datetime, timedelta

# In-process cache: {destination_id: (score_dict, expiry_epoch)}
_cache: dict[int, tuple[dict, float]] = {}
_CACHE_TTL = 900  # 15 minutes

EXPLANATION = (
    "This is a modelled estimate — not a surveillance feed. "
    "It blends seasonal tourism patterns (curated by tourism staff), "
    "active local festivals, and recent community check-ins from BeyondTour users. "
    "It updates every 15 minutes."
)


def _tier_to_base_score(tier: int) -> float:
    """Convert 1–5 tier to 0–50 score."""
    return max(0, min(50, (tier - 1) * 12.5))


def _festival_boost(destination_id: int, district: str | None) -> float:
    """
    Return 0–25 boost if today falls inside any active festival date range
    for this destination's district.
    Uses month_number as proxy (full date parsing would need date columns).
    """
    try:
        from app.models import CultureEntry
        today_month = datetime.utcnow().month
        # Festivals active this month in the district
        q = CultureEntry.query.filter(
            CultureEntry.month_number == today_month,
            CultureEntry.entry_type == 'festival',
        )
        if district:
            q = q.filter(CultureEntry.district.ilike(f'%{district}%'))
        festivals = q.count()
        if festivals >= 2:
            return 25.0
        elif festivals == 1:
            return 15.0
    except Exception:
        pass
    return 0.0


def _checkin_score(destination_id: int, district: str | None) -> float:
    """
    Count community posts tagged to this destination in the last 6 hours.
    Weighted: each post = 3 pts, capped at 25.
    """
    try:
        from app.models import CommunityPost
        cutoff = datetime.utcnow() - timedelta(hours=6)
        q = CommunityPost.query.filter(
            CommunityPost.created_at >= cutoff,
            CommunityPost.is_hidden == False,
        )
        if district:
            q = q.filter(CommunityPost.district_tag.ilike(f'%{district}%'))
        count = q.count()
        return min(25.0, count * 3.0)
    except Exception:
        return 0.0


def _score_to_tier(score: float) -> dict:
    if score <= 33:
        return {
            'score': round(score),
            'tier': 'green',
            'label': 'Quiet right now',
            'color_class': 'bg-green-500',
            'text_class': 'text-green-700',
            'bg_light': 'bg-green-50',
            'border': 'border-green-200',
            'dot': 'circle',
        }
    elif score <= 66:
        return {
            'score': round(score),
            'tier': 'yellow',
            'label': 'Moderately busy',
            'color_class': 'bg-yellow-400',
            'text_class': 'text-yellow-700',
            'bg_light': 'bg-yellow-50',
            'border': 'border-yellow-200',
            'dot': 'circle',
        }
    else:
        return {
            'score': round(score),
            'tier': 'red',
            'label': 'Very crowded',
            'color_class': 'bg-red-500',
            'text_class': 'text-red-700',
            'bg_light': 'bg-red-50',
            'border': 'border-red-200',
            'dot': 'circle',
        }


def compute_crowd_score(destination_id: int, district: str | None = None) -> dict:
    """
    Main entry point. Returns a dict with score, tier, label, color classes,
    and the explanation text shown in the UI tooltip.
    """
    now = time.time()
    cached = _cache.get(destination_id)
    if cached and cached[1] > now:
        return cached[0]

    # a) Baseline tier for this month and day_type
    base_score = 25.0  # default mid-range if no data
    try:
        from app.models import DestinationBaseline
        today = datetime.utcnow()
        day_type = 'weekend' if today.weekday() >= 5 else 'weekday'
        baseline = DestinationBaseline.query.filter_by(
            destination_id=destination_id,
            month=today.month,
            day_type=day_type,
        ).first()
        if baseline:
            base_score = _tier_to_base_score(baseline.expected_tier)
    except Exception:
        pass

    # b) Festival boost
    fest_score = _festival_boost(destination_id, district)

    # c) Live check-in score
    live_score = _checkin_score(destination_id, district)

    total = min(100, base_score + fest_score + live_score)
    result = _score_to_tier(total)
    result['explanation'] = EXPLANATION
    result['breakdown'] = {
        'baseline': round(base_score),
        'festivals': round(fest_score),
        'checkins': round(live_score),
    }

    _cache[destination_id] = (result, now + _CACHE_TTL)
    return result


def invalidate_cache(destination_id: int | None = None):
    """Call this when a new community post is added to refresh scores."""
    if destination_id:
        _cache.pop(destination_id, None)
    else:
        _cache.clear()
