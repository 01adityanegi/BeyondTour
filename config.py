import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'beyond-tour-sih-secret-dev-key-2024')
    # SQLite for dev — switch to MySQL URI for production
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(BASE_DIR, 'beyond_tour.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    # External Services (stub mode — set in .env for production)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
    CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '')

    # Weather Intelligence
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY', '')
    WEATHER_CACHE_TTL_MINUTES = int(os.environ.get('WEATHER_CACHE_TTL_MINUTES', 60))

    # Safety
    SOS_SMS_GATEWAY_KEY = os.environ.get('SOS_SMS_GATEWAY_KEY', '')
    FCM_SERVER_KEY = os.environ.get('FCM_SERVER_KEY', '')
    LOCATION_SHARE_TTL_HOURS = int(os.environ.get('LOCATION_SHARE_TTL_HOURS', 4))

    # App settings
    ITEMS_PER_PAGE = 12
    STUB_AI = not bool(os.environ.get('GEMINI_API_KEY', ''))
    STUB_MAPS = not bool(os.environ.get('GOOGLE_MAPS_API_KEY', ''))
    STUB_WEATHER = not bool(os.environ.get('OPENWEATHERMAP_API_KEY', ''))

