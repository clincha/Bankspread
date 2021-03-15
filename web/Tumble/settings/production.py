from .base import *

STARLING_CLIENT_ID = "awwfD5ijdU7lilHuSHbH"
STARLING_CLIENT_SECRET = os.getenv("STARLING_CLIENT_SECRET")
STARLING_REDIRECT_URL = "https://bankspread.com/starling/callback"
STARLING_BASE_URL = "https://api-sandbox.starlingbank.com"
STARLING_API_URL = STARLING_BASE_URL + "/api/v2"
STARLING_OAUTH_URL = "https://oauth-sandbox.starlingbank.com"
GOOGLE_REDIRECT_URL = "https://bankspread.com/sheeter/callback"

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = [
    "web"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
