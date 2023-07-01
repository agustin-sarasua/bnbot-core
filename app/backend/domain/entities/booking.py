from typing import List, Any
# from app.model import Conversation
from datetime import datetime
from pydantic import BaseModel


class Reservation(BaseModel):
    id: int = None

    # Booking Info
    check_in: str
    check_out: str
    num_guests: int
    property_id: str
    price_per_night: float
    total_price: float
    currency: str
    chat_id: str

    # Customer Info
    customer_number: str
    customer_name: str
    customer_email: str
    
    # = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp: str = None