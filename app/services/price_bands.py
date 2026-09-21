"""
app/services/price_bands.py
----------------------------
Fair-Price Engine for BeyondTour.

Computes median ± 1.5×IQR price bands per category/district from live listings.
Flags listings priced above the upper fence with a transparency notice.
Called on-demand (lazy computation) or via nightly scheduled job.
"""
from __future__ import annotations
import statistics
from datetime import datetime


def _compute_iqr_bounds(prices: list[float]) -> tuple[float, float, float]:
    """Returns (median, lower_fence, upper_fence)."""
    if not prices:
        return (0.0, 0.0, 0.0)
    prices_sorted = sorted(prices)
    n = len(prices_sorted)
    median = statistics.median(prices_sorted)
    if n < 4:
        # Too few samples — use simple ±40% of median
        return (median, median * 0.6, median * 1.4)
    q1 = statistics.median(prices_sorted[:n // 2])
    q3 = statistics.median(prices_sorted[n // 2 + (n % 2):])
    iqr = q3 - q1
    return (median, q1 - 1.5 * iqr, q3 + 1.5 * iqr)


def compute_price_bands():
    """
    Recompute PriceBand for all category/district combos from live listings.
    Upserts results into the price_bands table.
    Safe to call repeatedly — idempotent.
    """
    from app.extensions import db
    from app.models import Hotel, Guide, PriceBand

    # ── Hotels ──────────────────────────────────────────
    hotel_prices: dict[str, list[float]] = {}
    for h in Hotel.query.filter_by(status='live').all():
        if h.district and h.price_min:
            hotel_prices.setdefault(h.district, []).append(float(h.price_min))

    for district, prices in hotel_prices.items():
        median, low, high = _compute_iqr_bounds(prices)
        _upsert_band(db, PriceBand, 'hotel', district, median, low, high, len(prices))

    # ── Guides ──────────────────────────────────────────
    guide_prices: dict[str, list[float]] = {}
    for g in Guide.query.filter_by(status='live').all():
        if g.district and g.daily_rate:
            guide_prices.setdefault(g.district, []).append(float(g.daily_rate))

    for district, prices in guide_prices.items():
        median, low, high = _compute_iqr_bounds(prices)
        _upsert_band(db, PriceBand, 'guide', district, median, low, high, len(prices))

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()


def _upsert_band(db, PriceBand, category, district, median, low, high, count):
    band = PriceBand.query.filter_by(category=category, district=district).first()
    if not band:
        band = PriceBand(category=category, district=district)
        db.session.add(band)
    band.median_price = round(median, 2)
    band.iqr_low = round(low, 2)
    band.iqr_high = round(high, 2)
    band.sample_count = count
    band.computed_at = datetime.utcnow()


def check_price(category: str, district: str | None, price: float) -> dict:
    """
    Returns a flag dict:
    {
      'is_above_band': bool,
      'is_below_band': bool,
      'median': float | None,
      'band_high': float | None,
      'label': str,
    }
    """
    if not district or not price:
        return {'is_above_band': False, 'is_below_band': False,
                'median': None, 'band_high': None, 'label': ''}
    try:
        from app.models import PriceBand
        band = PriceBand.query.filter_by(category=category, district=district).first()
        if not band or band.sample_count < 2:
            # Re-compute if no data
            compute_price_bands()
            band = PriceBand.query.filter_by(category=category, district=district).first()
        if not band:
            return {'is_above_band': False, 'is_below_band': False,
                    'median': None, 'band_high': None, 'label': ''}

        is_above = price > band.iqr_high
        is_below = band.iqr_low > 0 and price < band.iqr_low
        label = ''
        if is_above:
            label = f'Above typical price for {district} ({category}s usually ₹{band.iqr_low:,.0f}–₹{band.iqr_high:,.0f}/night)'
        return {
            'is_above_band': is_above,
            'is_below_band': is_below,
            'median': band.median_price,
            'band_high': band.iqr_high,
            'label': label,
        }
    except Exception:
        return {'is_above_band': False, 'is_below_band': False,
                'median': None, 'band_high': None, 'label': ''}
