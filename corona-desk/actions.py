# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
import requests
import json
import textwrap


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_get_news"

    def run(self, dispatcher, tracker, domain):
        country = tracker.get_slot('country')
        print(country)
        try:
            if country == 'world' or country is None:
                url = 'https://api.thevirustracker.com/free-api?global=stats'
                response = requests.get(url).text
                json_data = json.loads(response)['results'][0]
                message = 'Total Cases: {}\nTotal Recovered: {}\nTotal Unresolved: {}\nTotal Deaths: {}\nTotal New ' \
                          'Cases Today: {}\nTotal New Deaths Today: {}\nTotal Active Cases: {}\nTotal Serious Cases: ' \
                          '{}\nTotal Affected Countries: {}\n'.format(json_data['total_cases'],
                                                                      json_data['total_recovered'],
                                                                      json_data['total_unresolved'],
                                                                      json_data['total_deaths'],
                                                                      json_data['total_new_cases_today'],
                                                                      json_data['total_new_deaths_today'],
                                                                      json_data['total_active_cases'],
                                                                      json_data['total_serious_cases'],
                                                                      json_data['total_affected_countries'])
                dispatcher.utter_message(text=message)

            else:
                url = 'https://api.thevirustracker.com/free-api?countryTotal={country}'.format(country=country)
                response = requests.get(url).text
                json_data = json.loads(response)['countrydata'][0]
                message = 'Total Cases: {}\nTotal Recovered: {}\nTotal Unresolved: {}\nTotal Deaths: {}\nTotal New ' \
                          'Cases Today: {}\nTotal New Deaths Today: {}\nTotal Active Cases: {}\nTotal Serious Cases: ' \
                          '{}\nTotal Danger Rank: {}\n'.format(json_data['total_cases'],
                                                               json_data['total_recovered'],
                                                               json_data['total_unresolved'],
                                                               json_data['total_deaths'],
                                                               json_data['total_new_cases_today'],
                                                               json_data['total_new_deaths_today'],
                                                               json_data['total_active_cases'],
                                                               json_data['total_serious_cases'],
                                                               json_data['total_danger_rank'])
                dispatcher.utter_message(text=message)
        except Exception as e:
            print('Error {}'.format(e))
