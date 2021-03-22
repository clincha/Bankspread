from .base import *

BANKSPREAD_VERSION = 'dev'
STARLING_CLIENT_ID = "M7V5p9X3Bjj3HikiIfGE"
STARLING_CLIENT_SECRET = os.getenv("STARLING_CLIENT_SECRET")
STARLING_REDIRECT_URL = "https://bankspread.com/starling/callback"
STARLING_BASE_URL = "https://api-sandbox.starlingbank.com"
STARLING_API_URL = STARLING_BASE_URL + "/api/v2"
STARLING_OAUTH_URL = "https://oauth-sandbox.starlingbank.com"
GOOGLE_REDIRECT_URL = "https://lvh.me:8000/sheeter/callback"

SECRET_KEY = 'KBDauwhdiuh7yT*632urg3qj4hblgUYGLO*&TFAFGE*&Fevfkuw4vr4tQ£%Y$%&£%^UGGbhwegbbiu'
DEBUG = True
ALLOWED_HOSTS = [
    "lvh.me",
    "127.0.0.1",
    "localhost"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
