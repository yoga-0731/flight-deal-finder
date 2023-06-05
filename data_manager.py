import os
import requests

PRICE_GET_ENDPOINT = os.environ.get('SHEETY_GET_ENDPOINT')
PRICE_PUT_ENDPOINT = os.environ.get('SHEETY_PUT_ENDPOINT')
SHEETY_API_KEY = os.getenv('SHEETY_API_KEY')
HEADERS = {"Authorization": SHEETY_API_KEY}
USER_POST_ENDPOINT = os.getenv('SHEETY_USER_ENDPOINT')


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_data(self):
        response = requests.get(url=PRICE_GET_ENDPOINT, headers=HEADERS)
        response.raise_for_status()
        self.destination_data = response.json()['prices']
        return self.destination_data

    def add_flight_data(self):
        for city in self.destination_data:
            parameters = {
                "price": {
                    "iataCode": city['iataCode']
                }
            }
            response = requests.put(url=f"{PRICE_PUT_ENDPOINT}/{city['id']}", headers=HEADERS, json=parameters)
            response.raise_for_status()

    def add_new_user(self, first_name, last_name, email):
        parameters = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }
        response = requests.post(url=USER_POST_ENDPOINT, json=parameters, headers=HEADERS)
        # print(response.text)
