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
        # print(f"Check flights triggered for {destination_city_code}")
        today = datetime.today()
        from_date = (today + timedelta(days=1)).strftime("%d/%m/%Y")
        to_date = (today + timedelta(weeks=24)).strftime("%d/%m/%Y")
        headers = {"apikey": os.environ["TEQUILA_API_KEY"]}
        parameters = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_date,
            "date_to": to_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 30,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search",  headers=headers, params=parameters)

        try:
            data = response.json()["data"][0]

        except IndexError:
            parameters["max_stopovers"] = 1
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=headers,
                params=parameters,
            )
            # pprint(response.json())
            try:
                data = response.json()["data"][0]
            except IndexError:
                # print(f"No flights found for {destination_city_code}.")
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                # print(f"{flight_data.destination_city}: ${flight_data.price}")
                return flight_data

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            # print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data
