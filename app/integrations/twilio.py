# Third-party imports
from twilio.rest import Client
from app.utils import logger, decode_form_url_encoded
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

class TwilioMessagingAPI:

    def __init__(self, account_sid, auth_token, twilio_number):
        self.client = Client(account_sid, auth_token)
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_number = twilio_number
        
    
    # Sending message logic through Twilio Messaging API
    def send_message(self, to_number, body_text):
        try:
            message = self.client.messages.create(
                from_=f"whatsapp:{self.twilio_number}",
                body=body_text,
                to=to_number
            )
            logger.debug(f"Message sent to {to_number}: {message.body}")
        except Exception as e:
            logger.error(f"Error sending message to {to_number}: {e}")
    
    def parse_request(self, body) -> dict:
        decoded_msg = decode_form_url_encoded(body)
        #  {'SmsMessageSid': 'SM972e3263b5b0ff982848c4103ecbe45a',
        #  'NumMedia': '0',
        #  'ProfileName': 'Agustin',
        #  'SmsSid': 'SM972e3263b5b0ff982848c4103ecbe45a',
        #  'WaId': '59899513718',
        #  'SmsStatus': 'received',
        #  'Body': 'Hola cómo va',
        #  'To': 'whatsapp:+14155238886',
        #  'NumSegments': '1',
        #  'ReferralNumMedia': '0',
        #  'MessageSid': 'SM972e3263b5b0ff982848c4103ecbe45a',
        #  'AccountSid': 'AC4658a3628d77a893e89f8454a2c5e1ed',
        #  'From': 'whatsapp:+59899513718',
        #  'ApiVersion': '2010-04-01'}
        return {
            # "customer_number": decoded_msg["WaId"],
            "profile_name": decoded_msg["ProfileName"],
            "messgae": decoded_msg["Body"],
            "from": decoded_msg["From"],
            "to": decoded_msg["To"],
        }