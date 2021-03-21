import pickle

import gspread
from django.shortcuts import render, redirect

from sheeter.models import UserGoogle
from starling.models import Starling


def home(request):
    context = {}
    if 'Google' in request.session.keys():
        context['google_login'] = True

    if 'Starling' in request.session.keys():
        context['starling_login'] = True

    return render(request, 'hitter/index.html', context)


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

        workbook = gc.create("Bankspread")

        # Transaction History
        transaction_history_sheet = workbook.sheet1
        transaction_history_sheet.update_title("Transaction History")
        transaction_history_sheet.append_rows(user_starling.get_full_transaction_history())

        # Saving Spaces
        saving_spaces = user_starling.get_saving_spaces()
        saving_spaces_sheet = workbook.add_worksheet("Saving Spaces", len(saving_spaces[0]), len(saving_spaces))
        saving_spaces_sheet.append_rows(saving_spaces)

    return redirect('hitter:home')


def privacy(request):
    return render(request, 'hitter/privacy.html')


def terms_of_service(request):
    return render(request, 'hitter/terms-of-service.html')
