import pickle

import gspread
from django.shortcuts import render, redirect

from sheeter.models import UserGoogle
from starling import Starling


def home():
    redirect('hitter:welcome')


def welcome(request):
    context = {}
    if 'Google' in request.session.keys():
        context['google_login'] = True

    if 'Starling' in request.session.keys():
        context['starling_login'] = True

    return render(request, 'hitter/templates/hitter/index.html', context)


def make_sheet(request):
    context = {}
    if 'Google' in request.session.keys():
        context['google_login'] = True

    if 'Starling' in request.session.keys():
        context['starling_login'] = True

    if context['google_login'] and context['starling_login']:
        user_google = UserGoogle.objects.filter(id=request.session['Google']).only().first()
        user_starling = Starling.objects.filter(id=request.session['Starling']).only().first()

        gc = gspread.authorize(pickle.loads(user_google.credentials))

        gc.create("test").sheet1.append_rows(user_starling.get_full_transaction_history())

    return redirect('hitter:welcome')
