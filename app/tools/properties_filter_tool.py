from typing import Optional
from langchain.tools import BaseTool
from datetime import datetime

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, BaseSettings, Field

from datetime import datetime, timedelta
from utils import Cache, read_json_from_s3

class PropertiesFilterToolSchema(BaseModel):
    checkin_date: str = Field(default="", description="check-in date")
    checkout_date: str = Field(default="", description="check-out date")
    num_guests: str = Field(default="1", description="number of guests staying")
    num_nights: str = Field(default="1", description="number of nights staying")


class PropertiesFilterTool(BaseTool, BaseSettings):
    """My custom Properties filter tool."""

    name = "properties_filter"
    description = "useful for when you need to load the properties information based on the check-in date, check-out date and number of guests. Do not use this tool if any of this information is missing."

    args_schema: Type[PropertiesFilterToolSchema] = PropertiesFilterToolSchema
    
    properties_info_cache = Cache(-1)

    assistant_number = "test-number"

    def _run(
        self, 
        checkin_date: str, 
        checkout_date: str,
        num_guests: str,
        num_nights: str,
        # available_properties: dict,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        
        if checkin_date == "" or (num_nights == "" and checkout_date == ""):
            return dict()

        num_nights = int(num_nights)
        if num_nights > 0:
           checkout_date_from_nights = self._calculate_checkout_date(checkin_date, num_nights)
           if checkout_date != checkout_date_from_nights:
               print("There is something wrong with the dates here {checkout_date} - {checkout_date_from_nights}")
               checkout_date = max(checkout_date, checkout_date_from_nights)

        num_guests = int(num_guests)
        available_properties = self.load_properties_information()
        return self._filter_properties(available_properties, checkin_date, checkout_date, num_guests)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

    def _calculate_checkout_date(self, checkin_date, num_nights):
        checkin_datetime = datetime.strptime(checkin_date, '%Y-%m-%d')
        checkout_datetime = checkin_datetime + timedelta(days=num_nights)
        checkout_date = checkout_datetime.strftime('%Y-%m-%d')
        return checkout_date
    
    def _filter_properties(self, properties, checkin_date, checkout_date, num_guests):
        filtered_properties = {}
        for property_id, property_info in properties.items():
            availability = property_info.get('availability', [])
            for avail in availability:
                avail_checkin = avail.get('checkin_from')
                avail_checkout = avail.get('checkout_to')
                avail_capacity = int(property_info.get('max_guests', 0))
                if (
                    avail_checkin <= checkin_date
                    and avail_checkout >= checkout_date
                    and num_guests <= avail_capacity
                ):
                    # Remove multiple keys
                    del property_info["calendar_link"], property_info["source"], property_info["availability"]
                    filtered_properties[property_id] = property_info
                    break  # Stop further iteration if a match is found
        return filtered_properties

    def get_properties_availabe(self):
        result = self.properties_info_cache.get(self.assistant_number)        
        if result is None:
            result = self.load_properties_information()
        return result

    def load_properties_information(self):
        availability = read_json_from_s3("bnbot-bucket", f"availability_{self.assistant_number}.json")
        self.properties_info_cache.set(self.assistant_number, availability)
        return availability