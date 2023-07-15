from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import date

class Location(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]

class BusinessOwner(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]

class PaymentOption(BaseModel):
    payment_method: Optional[str]
    instructions: Optional[str]

class CalendarConfig(BaseModel):
    currency: Optional[str]
    base_price: Optional[float]
    weekend_price: Optional[float]
    special_day_prices: Optional[dict]
    extra_per_person: Optional[float]
    open_days: Optional[List[date]]

class DayConfig(BaseModel):
    date: date
    price: float
    is_open: bool

class CalendarLink(BaseModel):
    source: str
    link: str

class Property(BaseModel):
    property_id: Optional[str]
    name: Optional[str]
    calendar_config: Optional[CalendarConfig]
    calendar_links: Optional[List[CalendarLink]]
    description: Optional[str]
    amenities: Optional[List[str]]
    max_guests: Optional[int]
    pick_up_keys_instructions: Optional[str]

class Business(BaseModel):
    id: Optional[str]
    user_id: str
    bnbot_id: Optional[str]
    business_name: Optional[str]
    description: Optional[str]
    bnbot_configuration: Optional[Dict[str, float]]
    location: Optional[Location]
    business_owners: Optional[List[BusinessOwner]]
    payment_options: Optional[List[PaymentOption]]
    how_to_arrive_instructions: Optional[str]
    properties: Optional[List[Property]]


class LoadBusinesses(BaseModel):
    bnbot_id: Optional[str]
    location: Optional[str]
    business_name: Optional[str]
    business_owner: Optional[str]