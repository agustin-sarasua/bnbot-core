from app.task_resolver.model import StepResolver
from app.utils import logger
from app.utils import get_completion_from_messages
from app.tools import InfoExtractorChain
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

    def __init__(self):
        pass

    def _calculate_checkout_date(self, checkin_date, num_nights):
        checkin_datetime = datetime.strptime(checkin_date, '%Y-%m-%d')
        checkout_datetime = checkin_datetime + timedelta(days=num_nights)
        checkout_date = checkout_datetime.strftime('%Y-%m-%d')
        return checkout_date
    
    def build_messages_from_conversation(self, conversation):
        messages = [{'role':'system', 'content': system_message}]
        for msg in conversation:
            messages.append(msg)
        return messages
    
    def build_chat_history(self, messages):
        chat_history = ""
        for msg in messages:
            chat_history += f"{msg['role']}: {msg['content']}\n"
        return chat_history

    def run(self, step_data: dict, messages: List[str], previous_stes_data: List[Any]) -> str:
        chat_input = self.build_messages_from_conversation(messages)
        result = get_completion_from_messages(chat_input)

        chat_history = self.build_chat_history(messages)
        
        info_extractor = InfoExtractorChain()
        booking_info = info_extractor("", chat_history)
        
        checkin_date = booking_info["checkin_date"]
        checkout_date = booking_info["checkout_date"]
        num_nights = booking_info["num_nights"]
        num_guests = booking_info["num_guests"]

        if checkin_date == "" or (booking_info["num_nights"] == "" and checkout_date == ""):
            return result

        num_nights = int(num_nights)
        if num_nights > 0:
           checkout_date_from_nights = self._calculate_checkout_date(checkin_date, num_nights)
           if checkout_date != checkout_date_from_nights:
               logger.error("There is something wrong with the dates here {checkout_date} - {checkout_date_from_nights}")
               checkout_date = max(checkout_date, checkout_date_from_nights)

        num_guests = int(num_guests)

        step_data["booking_information"] = {
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "num_nights": num_nights,
            "num_guests": num_guests
        }

        return result
    
    def is_done(self, step_data: dict):
        if "booking_information" not in step_data:
            return False
        
        booking_information = step_data["booking_information"]

        return (booking_information["checkin_date"] != "" and 
                booking_information["checkout_date"] != "" and 
                booking_information["num_guests"] > 0)