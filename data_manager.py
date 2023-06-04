import os
import requests

GET_ENDPOINT = os.environ.get('SHEETY_GET_ENDPOINT')
PUT_ENDPOINT = os.environ.get('SHEETY_PUT_ENDPOINT')
HEADERS = {"Authorization": os.environ.get('SHEETY_API_KEY')}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_data(self):
        response = requests.get(url=GET_ENDPOINT, headers=HEADERS)
        response.raise_for_status()
        self.destination_data = response.json()['prices']
        return self.destination_data

    def add_data_to_row(self):
        for city in self.destination_data:
            parameters = {
                "price": {
                    "iataCode": city['iataCode']
                }
            }
            response = requests.put(url=f"{PUT_ENDPOINT}/{city['id']}", headers=HEADERS, json=parameters)
            response.raise_for_status()

