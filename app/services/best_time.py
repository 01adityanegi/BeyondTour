"""
app/services/best_time.py
--------------------------
"Best Time to Visit" engine for BeyondTour destination pages.

Combines:
  - Weather forecast (next 7 days) — scores good weather
  - Crowd baseline + festival calendar — projects forward crowd tier
  - Produces a single human-readable recommendation sentence
"""
from __future__ import annotations
from datetime import datetime, timedelta


_MONTH_NAMES = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def _weather_score(day_forecast: dict | None) -> float:
    """0–50: clear sky + comfortable temp = high score."""
    if not day_forecast:
        return 25.0
    rain = day_forecast.get('rain_mm', 0) or 0
    high = day_forecast.get('high', 22)
    # Rain penalty
    rain_score = max(0, 50 - rain * 4)
    # Temperature comfort (10–25°C ideal for hills)
    if 10 <= high <= 25:
        temp_bonus = 10
    elif 5 <= high < 10 or 25 < high <= 32:
        temp_bonus = 5
    else:
        temp_bonus = 0
    return min(50, rain_score * 0.8 + temp_bonus)


def _crowd_score_forward(destination_id: int, district: str | None,
                          target_date: datetime) -> float:
    """
    0–50: low projected crowd = high score.
    Uses DestinationBaseline + CultureEntry festival overlap.
    """
    base_score = 25.0
    try:
        from app.models import DestinationBaseline
        day_type = 'weekend' if target_date.weekday() >= 5 else 'weekday'
        baseline = DestinationBaseline.query.filter_by(
            destination_id=destination_id,
            month=target_date.month,
            day_type=day_type,
        ).first()
        if baseline:
            # tier 1 → score 50 (quietest), tier 5 → score 10 (busiest)
            base_score = 50 - (baseline.expected_tier - 1) * 10
    except Exception:
        pass

    # Festival penalty
    try:
        from app.models import CultureEntry
        festivals = CultureEntry.query.filter(
            CultureEntry.month_number == target_date.month,
            CultureEntry.entry_type == 'festival',
        )
        if district:
            festivals = festivals.filter(CultureEntry.district.ilike(f'%{district}%'))
        if festivals.count() > 0:
            base_score = max(0, base_score - 15)
    except Exception:
        pass

    return max(0, min(50, base_score))


def _active_festivals(district: str | None, target_date: datetime) -> list[str]:
    """Return festival titles active during target month."""
    try:
        from app.models import CultureEntry
        q = CultureEntry.query.filter(
            CultureEntry.month_number == target_date.month,
            CultureEntry.entry_type == 'festival',
        )
        if district:
            q = q.filter(CultureEntry.district.ilike(f'%{district}%'))
        return [f.title for f in q.limit(2).all()]
    except Exception:
        return []


def compute_best_time(destination_id: int, district: str | None = None,
                       weather_daily: list | None = None) -> dict:
    """
    Returns:
      {
        'recommendation': str,        # human-readable sentence
        'best_window': str,           # e.g. 'This Sunday' or 'Weekday mornings'
        'score': float,               # combined quality score
        'festivals_to_avoid': list,   # festival names crowding the window
      }
    """
    today = datetime.utcnow()
    best_score = -1.0
    best_date = None
    best_weather = None
    festivals_to_avoid = []

    # Score each of the next 7 days
    for i in range(7):
        target = today + timedelta(days=i)
        w_day = weather_daily[i] if (weather_daily and i < len(weather_daily)) else None
        w_score = _weather_score(w_day)
        c_score = _crowd_score_forward(destination_id, district, target)
        combined = w_score + c_score
        if combined > best_score:
            best_score = combined
            best_date = target
            best_weather = w_day

    # Build human-readable recommendation
    if best_date is None:
        return {
            'recommendation': 'Weekday mornings are typically quieter here.',
            'best_window': 'Weekday mornings',
            'score': 50,
            'festivals_to_avoid': [],
        }

    # Check for festivals in the coming week
    for i in range(7):
        d = today + timedelta(days=i)
        fests = _active_festivals(district, d)
        for f in fests:
            if f not in festivals_to_avoid:
                festivals_to_avoid.append(f)

    # Format best window label
    days_ahead = (best_date - today).days
    if days_ahead == 0:
        window = 'Today'
    elif days_ahead == 1:
        window = 'Tomorrow'
    else:
        window = best_date.strftime('This %A')

    day_type = 'weekend' if best_date.weekday() >= 5 else 'weekday'
    time_hint = 'morning' if day_type == 'weekday' else 'early morning'

    # Weather phrase
    weather_phrase = ''
    if best_weather:
        rain = best_weather.get('rain_mm', 0)
        desc = best_weather.get('desc', '')
        if rain == 0:
            weather_phrase = f'Clear skies expected on {window}.'
        elif rain < 5:
            weather_phrase = f'Light showers possible on {window} — carry a light raincoat.'
        else:
            weather_phrase = f'Rain expected on {window} — consider an alternative day.'

    # Festival warning
    fest_warn = ''
    if festivals_to_avoid:
        fest_warn = f' Expect larger crowds during {festivals_to_avoid[0]} this month.'

    rec = f'Best time to visit: {window} {time_hint}s are ideal.{fest_warn} {weather_phrase}'.strip()

    return {
        'recommendation': rec,
        'best_window': window,
        'score': round(best_score),
        'festivals_to_avoid': festivals_to_avoid,
    }
