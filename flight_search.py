import os
import requests
from datetime import datetime, timedelta
from flight_data import FlightData
from pprint import pprint

TEQUILA_ENDPOINT = os.environ.get('TEQUILA_ENDPOINT')
TEQUILA_API_KEY = os.environ.get('TEQUILA_API_KEY')
HEADERS = {"apikey": TEQUILA_API_KEY}


class FlightSearch:
    def destination_code(self, city):
        parameters = {"term": city, "location_types": "city"}
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", headers=HEADERS, params=parameters)
        response.raise_for_status()
        data = response.json()
        return data['locations'][0]['code']

    def search_flights(self, origin_city_code, destination_city_code):
        today = datetime.today()
        from_date = (today + timedelta(days=1)).strftime("%d/%m/%Y")
        to_date = (today + timedelta(weeks=24)).strftime("%d/%m/%Y")
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        parameters = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "dateFrom": from_date,
            "dateTo": to_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }
        response = requests.get(url=search_endpoint, params=parameters, headers=HEADERS)
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: ${flight_data.price}")
        return flight_data
