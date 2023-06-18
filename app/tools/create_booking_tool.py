from typing import Optional
from langchain.tools import BaseTool
from datetime import datetime

from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

import requests
from langchain.tools import StructuredTool


from typing import Optional, Type

import aiohttp
import requests

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, BaseSettings, Field

from datetime import datetime, timedelta
# from app.utils import Cache, read_json_from_s3
from ..utils import Cache, read_json_from_s3

class PropertiesFilterToolSchema(BaseModel):
    checkin_date: str = Field(default="", description="check-in date")
    checkout_date: str = Field(default="", description="check-out date")
    num_guests: str = Field(default="1", description="number of guests staying")
    num_nights: str = Field(default="1", description="number of nights staying")
    house_picked: str = Field(default="", description="the house id of the user picked by the user")
    booking_email: str = Field(default="", description="email for the booking")
    booking_name: str = Field(default="", description="the name for the booking")
    booking_phone: str = Field(default="", description="the phone for the booking")
    booking_price: str = Field(default="", description="the total price for the booking")
    # available_properties: dict = Field(default=dict(), description="available properties") 
    # query_params: Optional[dict] = Field(
    #     default=None, description="Optional search parameters"
    # )


class CreateBookingTool(BaseTool, BaseSettings):
    """Create booking in the system tool."""

    name = "create_booking"
    description = "useful for when you need to create a booking in the system."

    args_schema: Type[PropertiesFilterToolSchema] = PropertiesFilterToolSchema

    def _run(
        self, 
        checkin_date: str, 
        checkout_date: str,
        num_guests: str,
        num_nights: str,
        house_picked: str,
        booking_email: str,
        booking_name: str,
        booking_phone: str,
        booking_price: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        
        if checkin_date == "" or (num_nights == "" and checkout_date == ""):
            return dict()

        booking = {
            "checkin_date":checkin_date,
            "checkout_date":checkout_date,
            "num_guests":num_guests,
            "num_nights":num_nights,
            "house_picked":house_picked,
            "booking_email":booking_email,
            "booking_name":booking_name,
            "booking_phone":booking_phone,
            "booking_price":booking_price,
        }
        return booking

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
