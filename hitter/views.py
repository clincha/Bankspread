import pickle

import gspread
from django.shortcuts import render

from sheeter.models import UserGoogle


def welcome(request):
    context = {}
    if 'Google' in request.session.keys():
        context['google_login'] = True
        user_google = UserGoogle.objects.filter(id=request.session['Google']).only().first()
        gc = gspread.authorize(pickle.loads(user_google.credentials))
        print(gc.open("Finance").sheet1.cell(1, 1).value)

    if 'Starling' in request.session.keys():
        context['starling_login'] = True

    return render(request, 'hitter/index.html', context)
