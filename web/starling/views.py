import datetime
import random
import string

import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils import timezone

from starling.models import Starling


def welcome(request):
    client_id = settings.STARLING_CLIENT_ID
    state = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

    request.session.set_expiry(0)  # Session lasts until the browser is closed
    request.session['state'] = state
    return redirect(settings.STARLING_OAUTH_URL +
                    "?client_id=" + client_id +
                    "&response_type=code" +
                    "&state=" + state)


def callback(request):
    client_id = settings.STARLING_CLIENT_ID
    client_secret = settings.STARLING_CLIENT_SECRET
    starling_redirect_url = settings.STARLING_REDIRECT_URL

    if request.session['state'] != request.GET['state']:
        return HttpResponseBadRequest('State received from Starling was incorrect')

    request.session.pop('state')
    code = request.GET['code']

    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': starling_redirect_url
    }
    response_json = requests.post(settings.STARLING_BASE_URL + "/oauth/access-token", data).json()
    headers = {
        'Authorization': "Bearer " + response_json['access_token']
    }
    account_uuid = requests.get(settings.STARLING_API_URL + "/account-holder", headers=headers) \
        .json()['accountHolderUid']

    starling = Starling(id=account_uuid,
                        access_token=response_json['access_token'],
                        refresh_token=response_json['refresh_token'],
                        token_expires=datetime.datetime.now(tz=timezone.utc) +
                                      datetime.timedelta(seconds=response_json['expires_in']))
    starling.save()
    request.session['Starling'] = starling.id

    return redirect('hitter:home')


def transactions(request):
    starling = Starling.objects.last()
    return JsonResponse(starling.get_full_transaction_history(), safe=False)
