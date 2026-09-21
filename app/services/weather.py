"""
app/services/weather.py
------------------------
Real-time weather layer for BeyondTour.

- Uses OpenWeatherMap One Call API 3.0 (or 2.5 fallback)
- Caches results in WeatherCache table for WEATHER_CACHE_TTL_MINUTES (default 60)
- Provides human-readable hill-travel advisories from raw forecast data
- Stub mode: returns realistic demo Uttarakhand weather when API key absent
"""
import json
import requests
from datetime import datetime, timedelta
from flask import current_app

# Icon code → Lucide icon name mapping for UI
OWM_ICON_MAP = {
    '01': 'sun',
    '02': 'cloud-sun',
    '03': 'cloud',
    '04': 'cloud',
    '09': 'cloud-rain',
    '10': 'cloud-rain',
    '11': 'cloud-lightning',
    '13': 'snowflake',
    '50': 'cloud-fog',
}

# ────────────────────────────────────────────────
# Hill-specific advisory generator
# ────────────────────────────────────────────────
_RAIN_ADVISORIES = [
    (20,  "Heavy rain expected — mountain roads may be slippery. Check road conditions before travel."),
    (10,  "Moderate rain likely — carry rain gear and waterproof footwear."),
    (3,   "Light showers possible — pack a compact umbrella."),
]
_TEMP_ADVISORIES = [
    (5,   "Very cold — pack heavy woolens, thermal innerwear, and windproof jacket."),
    (12,  "Cold nights — bring a warm fleece or pullover even if days are mild."),
    (30,  "Pleasant temperatures — light layers are ideal for Himalayan altitude changes."),
    (36,  "Warm — stay hydrated; sun can be intense at altitude despite the breeze."),
]


def _icon_emoji(icon_code: str) -> str:
    return OWM_ICON_MAP.get(icon_code[:2], 'thermometer')


def _hill_advisory(daily_forecasts: list) -> list[str]:
    """Produce plain-language travel advisories from tomorrow's forecast."""
    advisories = []
    if not daily_forecasts:
        return advisories
    tomorrow = daily_forecasts[0] if daily_forecasts else {}
    rain_mm = tomorrow.get('rain', 0) or 0
    temp_min = tomorrow.get('temp', {}).get('min', 20) if isinstance(tomorrow.get('temp'), dict) else 20

    for threshold, msg in _RAIN_ADVISORIES:
        if rain_mm >= threshold:
            advisories.append(msg)
            break
    for threshold, msg in _TEMP_ADVISORIES:
        if temp_min <= threshold:
            advisories.append(msg)
            break

    # Snow warning
    if tomorrow.get('snow', 0):
        advisories.append("Snow possible — check road clearance status before heading to higher elevations.")

    return advisories


# ────────────────────────────────────────────────
# Stub data — realistic Uttarakhand autumn weather
# ────────────────────────────────────────────────
def _get_stub_weather() -> dict:
    now = datetime.utcnow()
    return {
        'current': {
            'temp': 18,
            'feels_like': 15,
            'humidity': 62,
            'description': 'Partly cloudy',
            'icon': 'cloud-sun',
            'wind_kph': 12,
        },
        'daily': [
            {'day': 'Today',     'icon': 'cloud-sun', 'high': 21, 'low': 10, 'rain_mm': 0,  'desc': 'Partly cloudy'},
            {'day': 'Tomorrow',  'icon': 'cloud-rain', 'high': 18, 'low': 9,  'rain_mm': 4,  'desc': 'Light showers'},
            {'day': (now + timedelta(days=2)).strftime('%a'),  'icon': 'sun', 'high': 23, 'low': 11, 'rain_mm': 0, 'desc': 'Clear skies'},
        ],
        'advisories': ['Light showers possible — pack a compact umbrella.'],
        'is_stub': True,
    }


# ────────────────────────────────────────────────
# Cache helpers
# ────────────────────────────────────────────────
def _get_cached(location_key: str) -> dict | None:
    """Return parsed forecast if cache is fresh, else None."""
    from app.models import WeatherCache
    ttl = current_app.config.get('WEATHER_CACHE_TTL_MINUTES', 60)
    cutoff = datetime.utcnow() - timedelta(minutes=ttl)
    entry = WeatherCache.query.filter_by(location_key=location_key).first()
    if entry and entry.fetched_at >= cutoff:
        try:
            return json.loads(entry.forecast_json)
        except Exception:
            return None
    return None


def _store_cache(location_key: str, lat: float, lng: float, raw_json: dict):
    """Upsert a WeatherCache row."""
    from app.extensions import db
    from app.models import WeatherCache
    entry = WeatherCache.query.filter_by(location_key=location_key).first()
    if not entry:
        entry = WeatherCache(location_key=location_key, lat=lat, lng=lng,
                             forecast_json=json.dumps(raw_json), fetched_at=datetime.utcnow())
        db.session.add(entry)
    else:
        entry.forecast_json = json.dumps(raw_json)
        entry.fetched_at = datetime.utcnow()
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()


# ────────────────────────────────────────────────
# OpenWeatherMap fetcher
# ────────────────────────────────────────────────
def _fetch_owm(lat: float, lng: float, api_key: str) -> dict | None:
    """
    Call OWM One Call API 3.0.
    Falls back to 2.5 endpoint automatically if 3.0 returns 401.
    Returns raw JSON or None on failure.
    """
    base_params = {
        'lat': lat, 'lon': lng,
        'exclude': 'minutely,hourly,alerts',
        'units': 'metric',
        'appid': api_key,
    }
    for version in ('3.0', '2.5'):
        url = f'https://api.openweathermap.org/data/{version}/onecall'
        try:
            resp = requests.get(url, params=base_params, timeout=6)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 401:
                continue   # try older version
        except requests.RequestException:
            pass
    return None


# ────────────────────────────────────────────────
# Parse raw OWM response → display-ready dict
# ────────────────────────────────────────────────
def _parse_owm(raw: dict) -> dict:
    days_raw = raw.get('daily', [])[:3]
    current_raw = raw.get('current', {})

    current = {
        'temp': round(current_raw.get('temp', 20)),
        'feels_like': round(current_raw.get('feels_like', 18)),
        'humidity': current_raw.get('humidity', 60),
        'description': current_raw.get('weather', [{}])[0].get('description', 'Clear').capitalize(),
        'icon': _icon_emoji(current_raw.get('weather', [{}])[0].get('icon', '01d')),
        'wind_kph': round(current_raw.get('wind_speed', 0) * 3.6),
    }

    daily = []
    for i, d in enumerate(days_raw):
        ts = d.get('dt', 0)
        label = datetime.utcfromtimestamp(ts).strftime('%a') if ts else ['Today', 'Tomorrow', 'Day 3'][i]
        if i == 0:
            label = 'Today'
        elif i == 1:
            label = 'Tomorrow'
        temp = d.get('temp', {})
        daily.append({
            'day': label,
            'icon': _icon_emoji(d.get('weather', [{}])[0].get('icon', '01d')),
            'high': round(temp.get('max', 22) if isinstance(temp, dict) else temp),
            'low': round(temp.get('min', 10) if isinstance(temp, dict) else temp),
            'rain_mm': round(d.get('rain', 0) or 0, 1),
            'desc': d.get('weather', [{}])[0].get('description', 'Clear').capitalize(),
        })

    advisories = _hill_advisory(days_raw)
    return {'current': current, 'daily': daily, 'advisories': advisories, 'is_stub': False}


# ────────────────────────────────────────────────
# Public API
# ────────────────────────────────────────────────
def get_weather(lat: float | None, lng: float | None,
                location_key: str | None = None) -> dict:
    """
    Main entry point — returns weather display dict.
    Uses DB cache; calls OWM only when cache is stale.
    Falls back gracefully to stub if no API key or OWM is unreachable.
    """
    # Normalise coordinates — default to Almora if missing
    lat = lat or 29.5892
    lng = lng or 79.6467
    location_key = location_key or f'{round(lat, 3)},{round(lng, 3)}'

    api_key = current_app.config.get('OPENWEATHERMAP_API_KEY', '')
    if not api_key:
        return _get_stub_weather()

    # Try cache first
    cached = _get_cached(location_key)
    if cached:
        return _parse_owm(cached)

    # Fetch fresh
    raw = _fetch_owm(lat, lng, api_key)
    if raw:
        _store_cache(location_key, lat, lng, raw)
        return _parse_owm(raw)

    # Graceful fallback
    return _get_stub_weather()
