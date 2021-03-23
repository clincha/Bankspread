from .base import *

BANKSPREAD_VERSION = os.getenv("BANKSPREAD_VERSION")
STARLING_CLIENT_ID = "awwfD5ijdU7lilHuSHbH"
STARLING_CLIENT_SECRET = os.getenv("STARLING_CLIENT_SECRET")
STARLING_REDIRECT_URL = "https://bankspread.com/starling/callback"
STARLING_BASE_URL = "https://api-sandbox.starlingbank.com"
STARLING_API_URL = STARLING_BASE_URL + "/api/v2"
STARLING_OAUTH_URL = "https://oauth-sandbox.starlingbank.com"
GOOGLE_REDIRECT_URL = "https://bankspread.com/sheeter/callback"

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = [
    "web"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
