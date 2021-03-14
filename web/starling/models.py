from _csv import reader

import requests
from django.conf import settings
from django.db import models


class Starling(models.Model):
    id = models.CharField(max_length=4000, primary_key=True)
    access_token = models.CharField(max_length=4000)
    refresh_token = models.CharField(max_length=4000)
    token_expires = models.DateTimeField()

    def get_full_transaction_history(self):
        """
        Gets the entire transaction history for all accounts associated with the personal access token provided
        :return: A list of transaction lines, which are in turn a list of strings
        """
        accounts = self.__get_accounts()
        statement_lines = []
        for account in accounts:
            statement_periods = self.__get_statement_periods(account['accountUid'])
            for statement_period in statement_periods:
                statement = self.__get_statement(account['accountUid'], statement_period['period'])
                statement = statement.split("\n")
                if statement_lines:
                    statement = statement[1:]  # Remove heading row if this isn't the first statement
                for line in reader(statement):
                    statement_lines.append(line)
        return list(filter(None, statement_lines))  # Remove the blank lines

    def get_saving_spaces(self):
        """
        Gets all the saving spaces associated with the given personal access token
        :return: A list of saving spaces which in turn are a list of strings
        """
        headers = {
            'Authorization': "Bearer " + self.access_token
        }
        accounts = self.__get_accounts()
        all_goals = [['Account Name',
                      'Space Name',
                      'Target Amount',
                      'Saved Amount',
                      'Saved Percentage']]
        for account in accounts:
            response = requests.get(settings.STARLING_API_URL + "/account/" + account['accountUid'] + "/savings-goals",
                                    headers=headers)
            for goal in response.json()['savingsGoalList']:
                all_goals.append([account['name'],
                                  goal['name'],
                                  '£' + str(goal['target']['minorUnits'] / 100),
                                  '£' + str(goal['totalSaved']['minorUnits'] / 100),
                                  str(goal['savedPercentage']) + '%'])
        return all_goals

    def __get_accounts(self):
        """
        Get an account holder's bank accounts
        :return: An array containing all the users accounts. Account object keys:
            - accountUid
            - accountType
            - defaultCategory
            - currency
            - createdAt
            - name
        """
        headers = {
            'Authorization': "Bearer " + self.access_token
        }
        response = requests.get(settings.STARLING_API_URL + "/accounts", headers=headers)
        print(response.status_code)
        print(response.text)
        return response.json()['accounts']

    def __get_statement_periods(self, account_uid):
        """
        Get list of statement periods which are available for an account
        :param account_uid: The accounts unique identifier
        :return: An array containing the statement periods. Statement period object keys:
            - period
            - partial
        """
        headers = {
            'Authorization': "Bearer " + self.access_token
        }
        response = requests.get(
            settings.STARLING_API_URL + "/accounts/" + account_uid + "/statement/available-periods",
            headers=headers)
        return response.json()['periods']

    def __get_statement(self, account_uid, period):
        """
        Download a statement for a given statement period
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
            'Authorization': "Bearer " + self.access_token,
            'Accept': "text/csv"
        }
        params = {
            'yearMonth': period
        }
        response = requests.get(settings.STARLING_API_URL + "/accounts/" + account_uid + "/statement/download",
                                headers=headers,
                                params=params)
        return response.text
