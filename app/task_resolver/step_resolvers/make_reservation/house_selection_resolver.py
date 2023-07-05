from app.task_resolver.engine import StepResolver
from app.task_resolver.engine import StepData
from typing import List, Any
from app.tools import PropertiesFilterTool, PropertySelectedExtractor, HouseSelectionAssistantTool
from app.utils import logger
import json
from app.model import Message

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

    def _format_property_json(self, properties):
        data = []
        idx = 1
        for _, property_data in properties.items():
            data.append({
                "property_id": property_data['property_id'],
                "name": property_data['name']
            })
        return json.dumps(data)

    def run(self, messages: List[Message], previous_steps_data: dict, step_chat_history: List[Message] = None) -> Message:

        logger.debug(f"Previous Step Data HEREEEE: {previous_steps_data}")
        # exit_task_step_data: StepData = previous_steps_data["EXIT_TASK_STEP"]
        # if exit_task_step_data.resolver_data["conversation_finished"] == True:
        #     logger.debug("Conversation finished. Responding None")
        #     return None
        gather_business_info_step_data: StepData = previous_steps_data["BUSINESS_SELECTION"]
        gather_booking_info_step_data: StepData = previous_steps_data["GATHER_BOOKING_INFO"]
        booking_info = gather_booking_info_step_data.resolver_data["booking_information"]

        property_loader = PropertiesFilterTool()
        if "properties_available" not in self.data:
            logger.debug(f"Calling tool with: {booking_info}")
            bnbot_id = gather_business_info_step_data["business_info"]["bnbot_id"]
            logger.debug(f"Loading properties available for {bnbot_id}")
            properties_available = property_loader.run(bnbot_id, booking_info["check_in_date"], booking_info["check_out_date"], booking_info["num_guests"])
            logger.debug(f"{self.__class__.__name__} - Properties available: {properties_available}")
            self.data["properties_available"] = properties_available

        properties_available = self.data["properties_available"]

        if len(properties_available.items()) == 0:
            properties_info = "Unfortunately there are no properties available."
        else:
            properties_info = self._format_json(properties_available)

        chat_history = self.build_chat_history(messages)
        assistant = HouseSelectionAssistantTool()
        assistant_response = assistant.run(chat_history, properties_info)

        
        if not self.data["step_first_execution"]:
            # There is not need to execute the PropertySelected if it is the first time executing this step.
            prop_extractor = PropertySelectedExtractor()
            prop_extractor_result = prop_extractor.run(messages, properties_info)

            if prop_extractor_result["user_has_selected"]:
                if "property_id" in prop_extractor_result and prop_extractor_result["property_id"] is not None and prop_extractor_result["property_id"] != "":
                    self.data["property_picked_info"] = {
                        "property_id": prop_extractor_result["property_id"],
                        "price_per_night": f"{properties_available[prop_extractor_result['property_id']]['currency']} {float(properties_available[prop_extractor_result['property_id']]['price_per_night'])}",
                        "total_price": f"{properties_available[prop_extractor_result['property_id']]['currency']} {float(properties_available[prop_extractor_result['property_id']]['price_per_night']) * float(booking_info['num_nights'])}"
                    }
        return Message.assistant_message(assistant_response)
    
    def is_done(self):
        if "property_picked_info" not in self.data:
            return False
        
        # TODO validate that the property_picked is valid agains the properties_available.
        return (self.data["property_picked_info"]["property_id"] != "" and 
                self.data["property_picked_info"]["property_id"] is not None)