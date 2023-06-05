import os
from twilio.rest import Client
import smtplib

USER = os.environ.get('PYTHON_TEST_EMAIL')
PASSWORD = os.environ.get('PASSWORD')

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    def notify_about_deals(self, message):
        client = Client(self.account_sid, self.auth_token)

        message = client.messages.create(
            body=message,
            from_=os.environ.get('TWILIO_FROM_NUMBER'),
            to=os.environ.get('TWILIO_TO_NUMBER')
        )

        # print(message.sid)

    def send_emails(self, message, to_email):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=USER, password=PASSWORD)
            connection.sendmail(
                from_addr=USER,
                to_addrs=to_email,
                msg=f"Subject: Flight Deal Alert!\n\n{message}"
            )
