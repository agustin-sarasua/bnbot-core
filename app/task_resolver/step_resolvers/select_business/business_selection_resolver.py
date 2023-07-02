from app.task_resolver.engine import StepResolver, Message
from app.task_resolver.engine import StepData
from typing import List, Any
from app.tools import PropertiesFilterTool, BusinessSelectedExtractor, HouseSelectionAssistantTool
from app.utils import logger
import json
from app.integrations.backend import BackendAPIClient
from app.utils import get_completion_from_messages

system_message = """You are an Assistant that helps the user select an business \
from a list of available businesses that rent houses for short stays.
Your task is only to help the user find the business he is looking for.

These are the available businesses to choose from:
{businesses_info}

Follow these steps before responding to the user:

Step 1: Count the number of available businesses to choose from.

Step 2: If there are no businesses available, tell the user that we have not find the business \
and suggest him to visit the site https://reservamedirecto.com and find the business ID from there.

Step 3: If there is only one business available, ask the user to confirm if that is the business he was looking for \
by showing him a summary of it.

Step 4: If there are multiple business available, ask the user to choose one from the list.

You respond in a short, very conversational friendly style.
response to th user: 
"""

class BusinessSelectionResolver(StepResolver):
    
    def __init__(self, backend_url: str):
        self.backend_api_client = BackendAPIClient(backend_url)
        super().__init__()

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

    def _format_business_json(self, properties):
        data = []
        for _, property_data in properties.items():
            data.append({
                "business_name": property_data['business_name'],
                "business_id": property_data['business_id'],
                "location": property_data['location']
            })
        return json.dumps(data)

    def run(self, messages: List[Message], previous_steps_data: dict, step_chat_history: List[Message] = None) -> Message:

        gather_business_info_step_data: StepData = previous_steps_data["GATHER_BUSINESS_INFO"]
        business_info = gather_business_info_step_data.resolver_data["business_info"]

        logger.debug(f"list_businesses input {business_info}")
        businesses = self.backend_api_client.list_businesses(json.dumps(business_info))

        if len(business_info) == 0:
            # Not found
            businesses_info = "Unfortunately there are no businesses available."
            # Inform, came back to previous step, erase previous step data
            pass
        elif len(business_info) == 1:
            # Confirm
            businesses_info = self._format_business_json(businesses)
            # Stay here and confirm that the property is the correct one
            pass
        else:
            # Select 1
            businesses_info = self._format_business_json(businesses)
            # Select 1 from the list found and confirm.
            pass
        
        formatted_system_message = system_message.format(businesses_info=businesses_info)

        chat_input = self.build_messages_from_conversation(formatted_system_message, messages)
        assistant_response = get_completion_from_messages(chat_input)

        
        if not self.data["step_first_execution"]:
            extractor = BusinessSelectedExtractor()
            extractor_result = extractor.run(messages, businesses_info)

            if extractor_result["user_has_selected"]:
                self.data["business_info"] = extractor_result

        return Message.assistant_message(assistant_response)
    
    def is_done(self):
        if "business_info" not in self.data:
            return False
        
        # TODO validate that the property_picked is valid agains the properties_available.
        return (self.data["business_info"]["business_id"] != "" and 
                self.data["business_info"]["business_id"] is not None)