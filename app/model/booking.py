from app.task_resolver.engine import Message
from typing import List, Any
# from app.model import Conversation
from datetime import datetime


class Establishment:

    def __init__(self, id: str):
        pass


class Booking:

    def __init__(self, 
                 check_in: str, 
                 check_out: str, 
                 num_guests: int, 
                 property_id: str, 
                 price_per_night: float, 
                 total_price: float, 
                 currency: str,
                 chat_history: List[Message],
                 establishment_id: str,
                 customer_number: str,
                 customer_name: str,
                 customer_email: str):
        
        # Establishment
        self.establishment_id = establishment_id

        # Booking Info
        self.check_in = check_in
        self.check_out = check_out
        self.num_guests = num_guests
        self.property_id = property_id
        self.price_per_night = price_per_night
        self.total_price = total_price
        self.currency = currency
        
        self.chat_history = chat_history

        # Customer Info
        self.customer_number = customer_number
        self.customer_name = customer_name
        self.customer_email = customer_email

        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def validate_availability(self):
        pass

    def pre_book(self):
        pass