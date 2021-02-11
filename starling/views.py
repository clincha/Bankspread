import datetime
import random
import string
from csv import reader

import gspread
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from gspread_formatting import *

from starling.models import Starling


def welcome(request):
    client_id = settings.STARLING_CLIENT_ID
    state = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    return redirect("https://oauth-sandbox.starlingbank.com/"
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
    response = requests.post("https://api-sandbox.starlingbank.com/oauth/access-token", data)
    print(response.text)
    response_json = response.json()

    starling = Starling(access_token=response_json['access_token'],
                        refresh_token=response_json['refresh_token'],
                        token_expires=datetime.datetime.now() + datetime.timedelta(seconds=response_json['expires_in']))
    starling.save()
    return HttpResponse("saved %s" % starling.id)


def get_accounts(personal_access_token):
    """
    Get an account holder's bank accounts
    :param personal_access_token: Users Personal Access token
    :return: An array containing all the users accounts. Account object keys:
        - accountUid
        - accountType
        - defaultCategory
        - currency
        - createdAt
        - name
    """
    headers = {
        'Authorization': "Bearer " + personal_access_token
    }
    response = requests.get("https://api.starlingbank.com/api/v2/accounts", headers=headers)
    return response.json()['accounts']


def get_statement_periods(personal_access_token, account_uid):
    """
    Get list of statement periods which are available for an account
    :param personal_access_token: Users Personal Access token
    :param account_uid: The accounts unique identifier
    :return: An array containing the statement periods. Statement period object keys:
        - period
        - partial
    """
    headers = {
        'Authorization': "Bearer " + personal_access_token
    }
    response = requests.get(
        "https://api.starlingbank.com/api/v2/accounts/" + account_uid + "/statement/available-periods",
        headers=headers)
    return response.json()['periods']


def get_statement(personal_access_token, account_uid, period):
    """
    Download a statement for a given statement period
    :param personal_access_token: Users Personal Access token
    :param account_uid: The accounts unique identifier
    :param period: The year month string for the statement
    :return: A csv string with the headers:
        - Date
        - Counter Party
        - Reference
        - Type
        - Amount (GBP)
        - Balance (GBP)
        - Spending Category
    """
    headers = {
        'Authorization': "Bearer " + personal_access_token,
        'Accept': "text/csv"
    }
    params = {
        'yearMonth': period
    }
    response = requests.get(
        "https://api.starlingbank.com/api/v2/accounts/" + account_uid + "/statement/download",
        headers=headers,
        params=params)
    return response.text


def get_full_transaction_history(personal_access_token):
    """
    Gets the entire transaction history for all accounts associated with the personal access token provided
    :param personal_access_token: The Starling Personal Access Token
    :return: A list of transaction lines, which are in turn a list of strings
    """
    accounts = get_accounts(personal_access_token)
    statement_lines = []
    for account in accounts:
        statement_periods = get_statement_periods(personal_access_token, account['accountUid'])
        for statement_period in statement_periods:
            statement = get_statement(personal_access_token, account['accountUid'], statement_period['period'])
            statement = statement.split("\n")
            if statement_lines:
                statement = statement[1:]  # Remove heading row if this isn't the first statement
            for line in reader(statement):
                statement_lines.append(line)
    return list(filter(None, statement_lines))  # Remove the blank lines


def clear_and_fill_sheet(workbook_id, sheet_name, data):
    """
    Clears a sheet in a workbook and populates the sheet with the data, highlights and freezes the first row
    :param workbook_id: Identifier of the workbook in Google Drive
    :param sheet_name: Identifier of the worksheet in the workbook
    :param data: Data to be inserted
    """
    gc = gspread.service_account("service_account.json")
    workbook = gc.open_by_key(workbook_id)
    sheet = workbook.worksheet(sheet_name)
    sheet.clear()
    sheet.append_rows(data, 'USER_ENTERED')

    # Formatting

    fmt = CellFormat(
        textFormat=textFormat(bold=True),
        horizontalAlignment='CENTER'
    )
    format_cell_range(sheet, '1:1', fmt)
    set_frozen(sheet, rows=1)


def get_saving_spaces_for_account(personal_access_token):
    """
    Gets all the saving spaces associated with the given personal access token
    :param personal_access_token: The personal access token for the Starling account
    :return: A list of saving spaces which in turn are a list of strings
    """
    headers = {
        'Authorization': "Bearer " + personal_access_token
    }
    accounts = get_accounts(personal_access_token)
    all_goals = [['Account Name',
                  'Space Name',
                  'Target Amount',
                  'Saved Amount',
                  'Saved Percentage']]
    for account in accounts:
        response = requests.get(
            "https://api.starlingbank.com/api/v2/account/" + account['accountUid'] + "/savings-goals",
            headers=headers)
        for goal in response.json()['savingsGoalList']:
            all_goals.append([account['name'],
                              goal['name'],
                              '£' + str(goal['target']['minorUnits'] / 100),
                              '£' + str(goal['totalSaved']['minorUnits'] / 100),
                              str(goal['savedPercentage']) + '%'])
    return all_goals
