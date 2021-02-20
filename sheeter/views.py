import gspread
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

GOOGLE_SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/userinfo.email',
                 'openid']

flow = Flow.from_client_secrets_file(
    'sheeter/credentials.json',
    scopes=GOOGLE_SCOPES,
    redirect_uri=settings.GOOGLE_REDIRECT_URL
)


# Create your views here.
def welcome(request):
    authorisation_url, _ = flow.authorization_url(access_type='offline',
                                                  include_granted_scopes='true')
    return redirect(authorisation_url)


def callback(request):
    flow.fetch_token(code=request.GET['code'])
    service = build(serviceName='oauth2',
                    version='v2',
                    credentials=flow.credentials)
    user_info = service.userinfo().get().execute()
    gc = gspread.authorize(flow.credentials)
    return HttpResponse(gc.open("Finance").sheet1.cell(1, 1))
