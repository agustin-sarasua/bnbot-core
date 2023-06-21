from task_resolver.model import StepResolver
from typing import List
from tools import BookingConfirmationChain
from utils import logger

class BookingConfirmationResolver(StepResolver):

    def __init__(self):
        pass
    
    def build_chat_history(self, messages):
        chat_history = ""
        for msg in messages:
            chat_history += f"{msg['role']}: {msg['content']}\n"
        return chat_history

    def _build_booking_info(self, previous_steps_data: dict):
        booking_info = previous_steps_data["GATHER_BOOKING_INFO"]["booking_information"]
        property_picked = previous_steps_data["HOUSE_SELECTION"]["property_picked_info"]
        user_info = previous_steps_data["GATHER_USER_INFO"]["user_information"]
        merged_dict = booking_info.copy()
        merged_dict.update(property_picked)
        merged_dict.update(user_info)
        return merged_dict


    def run(self, step_data: dict, messages: List[str], previous_steps_data: dict) -> str:
        
        booking_info = self._build_booking_info(previous_steps_data)
        
        
        step_chat_history = []    
        if "step_chat_history" in step_data:
            step_chat_history = step_data.get("step_chat_history")
            step_chat_history.append({"role":"user", "content": messages[-1]})

        chat_history = self.build_chat_history(step_chat_history)

        booking_confirmator = BookingConfirmationChain()
        result = booking_confirmator(booking_info, chat_history)
        step_chat_history = step_data.get("step_chat_history", [])
        step_chat_history.append({"role": "assistant", "content": result["text"]})
        step_data["step_chat_history"] = step_chat_history

        if result["booking_placed"] != "":
            step_data["booking_confirmed"] = result["booking_placed"]

        # if result["confirmed"] == "True":
        #     # TODO save booking in database.
        #     pass
        return result["text"]
    
    def is_done(self, step_data: dict):
        if "booking_confirmed" not in step_data:
            return False
        
        return (step_data["booking_confirmed"] != "" and step_data["booking_confirmed"] is not None)