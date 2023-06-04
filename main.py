# This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_CODE = "NYC"

data_manager = DataManager()
sheet_data = data_manager.get_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

if sheet_data[0]['iataCode'] == "":
    for city in sheet_data:
        flight_search = FlightSearch()
        city['iataCode'] = flight_search.destination_code(city['city'])

    data_manager.destination_data = sheet_data
    data_manager.add_data_to_row()

for destination in sheet_data:
    flight = flight_search.search_flights(
        ORIGIN_CITY_CODE,
        destination["iataCode"])

    if flight and flight.price < destination["lowestPrice"]:
        notification_manager.notify_about_deals(
            message=f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )
