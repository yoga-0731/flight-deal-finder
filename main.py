# This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_CODE = "NYC"

print("Welcome to Aurora Flight Club 😀\nWe'll find the best flight deals and email you")
first_name = input("What is your first name?: ")
last_name = input("What is your last name?: ")
email = input("Email address: ")
confirm_email = input("Confirm email address again: ")

if email == confirm_email:
    data_manager = DataManager()
    sheet_data = data_manager.get_data()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    data_manager.add_new_user(first_name, last_name, email)

    if sheet_data[0]['iataCode'] == "":
        for city in sheet_data:
            flight_search = FlightSearch()
            city['iataCode'] = flight_search.destination_code(city['city'])

        data_manager.destination_data = sheet_data
        data_manager.add_flight_data()

    for destination in sheet_data:
        flight = flight_search.search_flights(
            ORIGIN_CITY_CODE,
            destination["iataCode"])

        if flight and flight.price < destination["lowestPrice"]:
            message = f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."

            if flight.stop_overs > 0:
                message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

            notification_manager.send_emails(message, email)
            notification_manager.notify_about_deals(message)
            print("""You would've received Low Price Alerts if there were lower prices available! 😎\n\nPlease check your email or messages for more info!""")

else:
    print("Email doesn't match!")
