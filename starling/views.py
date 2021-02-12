import datetime
import random
import string

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

from starling.models import Starling


def welcome(request):
    client_id = settings.STARLING_CLIENT_ID
    state = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    return redirect(settings.STARLING_OAUTH_URL +
                    "?client_id=" + client_id +
                    "&response_type=code" +
                    "&state=" + state)


def callback(request):
    # Must compare the state
    print(request.GET['state'])

    code = request.GET['code']
    client_id = settings.STARLING_CLIENT_ID
    client_secret = settings.STARLING_CLIENT_SECRET
    starling_redirect_url = settings.STARLING_REDIRECT_URL

    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': starling_redirect_url
    }
    response = requests.post(settings.STARLING_BASE_URL + "/oauth/access-token", data)
    response_json = response.json()

    starling = Starling(access_token=response_json['access_token'],
                        refresh_token=response_json['refresh_token'],
                        token_expires=datetime.datetime.now() + datetime.timedelta(seconds=response_json['expires_in']))
    starling.save()
    return HttpResponse("saved %s" % starling.id)


def transactions(request):
    starling = Starling.objects.last()
    return JsonResponse(starling.get_full_transaction_history(), safe=False)
