import os
from twilio.rest import Client


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

        print(message.sid)
