from app.task_resolver.engine import StepResolver, StepData, Message
from app.utils import logger
from app.utils import get_completion_from_messages
from app.tools import SearchDataExtractor
from typing import List, Any
from datetime import datetime, timedelta

delimiter = "####"
system_message =f"""
You are an Assistant that gathers information from the user about booking an accommodation. 
You respond allways in Spanish.
The only information you need is: check-in date, check-out date and number of guests staying.

Follow these Steps before responding to the user new message:

Step 1: Make sure the user provided the check-in date.

Step 2: Make sure the user has provided the check-out date or the number of nights they are staying.

Step 3: Make sure the user has provided the number of guests that are staying.

You respond in a short, very conversational friendly style.

REMEMBER: Only asked for the information needed, nothing else."""


class GatherBookingInfoResolver(StepResolver):

    def _calculate_checkout_date(self, checkin_date, num_nights):
        checkin_datetime = datetime.strptime(checkin_date, '%Y-%m-%d')
        checkout_datetime = checkin_datetime + timedelta(days=num_nights)
        checkout_date = checkout_datetime.strftime('%Y-%m-%d')
        return checkout_date
    
    def build_messages_from_conversation(self, messages: List[Message]):
        result = [{'role':'system', 'content': system_message}]
        for msg in messages:
            result.append({'role': msg.role, 'content': msg.text})
        return result
    
    def run(self, messages: List[Message], previous_steps_data: dict):
        
        # exit_task_step_data: StepData = previous_steps_data["EXIT_TASK_STEP"]
        # if exit_task_step_data.resolver_data["conversation_finished"] == True:
        #     logger.debug("Conversation finished. Responding None")
        #     return None

        # chat_history = self.build_chat_history(messages)
        
        search_data_extractor = SearchDataExtractor()
        booking_info = search_data_extractor.run(messages)
        # {
        #     "check_in_date": check_in_date,
        #     "check_out_date": check_out_date,
        #     "num_guests": num_guests
        # }
        checkin_date = booking_info["check_in_date"]
        checkout_date = booking_info["check_out_date"]
        # num_nights = booking_info["num_nights"]
        num_guests = booking_info["num_guests"]

        chat_input = self.build_messages_from_conversation(messages)
        assistant_response = get_completion_from_messages(chat_input)
        
        if checkin_date is None or checkout_date is None or num_guests == 0:
            # Get response message from Assistant
            return assistant_response

        self.data["booking_information"] = booking_info
        return assistant_response
    
    def is_done(self):
        if "booking_information" not in self.data:
            return False
        
        booking_information = self.data["booking_information"]

        return (booking_information["check_in_date"] is not None and 
                booking_information["check_out_date"] is not None and 
                booking_information["num_guests"] > 0)