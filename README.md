# flight-deal-finder

A flight deal low price alerting app hosted on [pythonanywhere](https://www.pythonanywhere.com/)
Getting name, email and mobile number as input and alerting the user when a low flight price is reached.

**Tech Stack / Tools** - Python, smtplib, Tequila flight search API, Sheety google sheet API, Twilio API

**1. Add users to Google sheet**  
  - The user is asked to enter the name, mail ID.
  - It is then stored in google sheet using Sheety API.

**2. Add city codes and expected flight price to Google sheet**
  - A list of city codes are stored in the google sheet.
  - The expected flight ticket price is stored alongside city codes.

**3. Flight search**  
  - Set a constant Departure city.
  - Searching flights through Tequila external API from the departure city to other cities by iterating through the 2nd google sheet (flight data)
  - Searching flights within a time range of 6 months from today.
  - Searching for roundtrip details.

**4. Sending mail**
  - If the flight price reaches the expected price from the flight data sheet, sending mail and message to the user.

**References**  
https://tequila.kiwi.com/portal/docs/tequila_api/search_api  
https://sheety.co/docs/requests
