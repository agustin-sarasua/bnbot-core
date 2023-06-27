from app.task_resolver.engine import StepResolver, Message
from app.task_resolver.engine import StepData
from typing import List, Any
from app.tools import PropertiesFilterTool, HousePickedExtractorChain
from app.utils import logger

class HouseSelectionResolver(StepResolver):
    
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

    def run(self, messages: List[Message], previous_steps_data: dict):

        # exit_task_step_data: StepData = previous_steps_data["EXIT_TASK_STEP"]
        # if exit_task_step_data.resolver_data["conversation_finished"] == True:
        #     logger.debug("Conversation finished. Responding None")
        #     return None

        gather_booking_info_step_data: StepData = previous_steps_data["GATHER_BOOKING_INFO"]
        booking_info = gather_booking_info_step_data.resolver_data["booking_information"]

        property_loader = PropertiesFilterTool()
        if "properties_available" not in self.data:
            logger.debug(f"Calling tool with: {booking_info}")
            properties_available = property_loader.run(booking_info["check_in_date"], booking_info["check_out_date"], booking_info["num_guests"])
            logger.debug(f"{self.__class__.__name__} - Properties available: {properties_available}")
            self.data["properties_available"] = properties_available

        properties_available = self.data["properties_available"]

        if len(properties_available.items()) == 0:
            properties_info = "Unfortunately there are no properties available."
        else:
            properties_info = self._format_json(properties_available)
        
        chat_history = self.build_chat_history(messages)

        info_extractor = HousePickedExtractorChain()
        house_info = info_extractor(chat_history, properties_info)

        if "property_id" in house_info and  house_info["property_id"] is not None and house_info["property_id"] != "":
            self.data["property_picked_info"] = {
                "property_id": house_info["property_id"],
                "price_per_night": f"{properties_available[house_info['property_id']]['currency']} {float(properties_available[house_info['property_id']]['price'])}",
                "total_price": f"{properties_available[house_info['property_id']]['currency']} {float(properties_available[house_info['property_id']]['price']) * float(booking_info['num_nights'])}"
            }
        return house_info["text"]
    
    def is_done(self):
        if "property_picked_info" not in self.data:
            return False
        
        # TODO validate that the property_picked is valid agains the properties_available.
        return (self.data["property_picked_info"]["property_id"] != "" and 
                self.data["property_picked_info"]["property_id"] is not None)