from typing import List, Dict, Optional
from pydantic import BaseModel

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

class Property(BaseModel):
    property_id: Optional[str]
    name: Optional[str]
    other_calendar_links: Optional[List[str]]
    description: Optional[str]
    amenities: Optional[List[str]]
    price_per_night: Optional[float]
    currency: Optional[str]
    max_guests: Optional[int]
    pick_up_keys_instructions: Optional[str]

class Business(BaseModel):
    business_id: Optional[str]
    business_name: Optional[str]
    description: Optional[str]
    bnbot_id: Optional[str]
    bnbot_configuration: Optional[Dict[str, float]]
    location: Optional[Location]
    business_owners: Optional[List[BusinessOwner]]
    payment_options: Optional[List[PaymentOption]]
    how_to_arrive_instructions: Optional[str]
    properties: Optional[List[Property]]
