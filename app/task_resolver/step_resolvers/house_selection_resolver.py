from app.task_resolver.model import StepResolver
from typing import List, Any
from app.tools import PropertiesFilterTool, HousePickedExtractorChain
from app.utils import logger

class HouseSelectionResolver(StepResolver):

    def __init__(self):
        pass
    
    def _format_json(self, properties):
        formatted_string = ''
        idx = 1
        for property_name, property_data in properties.items():
            formatted_string += f"{idx}. {property_name}:\n"
            for key, value in property_data.items():
                formatted_string += f"{key}: {value}\n"
            formatted_string += "\n"

            idx +=1
        return formatted_string

    def run(self, step_data: dict, messages: List[str], previous_steps_data: dict) -> str:
        
        booking_info = previous_steps_data["GATHER_BOOKING_INFO"]["booking_information"]

        property_loader = PropertiesFilterTool()
        if "properties_available" not in step_data:
            properties_available = property_loader.run(tool_input=booking_info)
            logger.debug(f"{self.__class__.__name__} - Properties available: {properties_available}")
            step_data["properties_available"]=properties_available
        properties_available = step_data["properties_available"]

        if len(properties_available.items()) == 0:
            properties_info = "Unfortunately there are no properties available."
        else:
            properties_info = self._format_json(properties_available)
        
        chat_history = self.build_chat_history(messages)

        info_extractor = HousePickedExtractorChain()
        house_info = info_extractor(chat_history, properties_info)

        if house_info["property_id"] != "":
            step_data["property_picked_info"] = {
                "property_id": house_info["property_id"],
                # "price_per_night": properties_info[house_info["property_id"]]["price"],
                # "total_price": f"{int(properties_info[house_info['property_id']]['price']) * int(booking_info['num_nights'])}"
            }
        return house_info["text"]
    
    def is_done(self, step_data: dict):
        if "property_picked_info" not in step_data:
            return False
        
        # TODO validate that the property_picked is valid agains the properties_available.
        return (step_data["property_picked_info"]["property_id"] != "" and step_data["property_picked_info"]["property_id"] is not None)