from app.task_resolver.engine import StepResolver, StepData, Message
from app.tools import BookingConfirmationChain
from app.utils import logger
from typing import List, Any

class BookingConfirmationResolver(StepResolver):

    def _build_booking_info(self, previous_steps_data: dict):
        gather_booking_info_step_data: StepData = previous_steps_data["GATHER_BOOKING_INFO"]
        booking_info = gather_booking_info_step_data.resolver_data["booking_information"]

        house_selection_step_data: StepData = previous_steps_data["HOUSE_SELECTION"]
        property_picked = house_selection_step_data.resolver_data["property_picked_info"]

        gather_user_info_step_data: StepData = previous_steps_data["GATHER_USER_INFO"]
        user_info = gather_user_info_step_data.resolver_data["user_information"]

        merged_dict = booking_info.copy()
        merged_dict.update(property_picked)
        merged_dict.update(user_info)
        return merged_dict


    def run(self, messages: List[Message], previous_steps_data: dict, step_chat_history: List[Message] = None) -> Message:
        
        # exit_task_step_data: StepData = previous_steps_data["EXIT_TASK_STEP"]
        # if exit_task_step_data.resolver_data["conversation_finished"] == True:
        #     logger.debug("Conversation finished. Responding None")
        #     return None
        
        booking_info = self._build_booking_info(previous_steps_data)
        
        chat_history = self.build_chat_history(step_chat_history)

        booking_confirmator = BookingConfirmationChain()
        result = booking_confirmator.run(booking_info, chat_history)

        if result["booking_placed"] != "":
            self.data["booking_confirmed"] = result["booking_placed"]

        # if result["confirmed"] == "True":
        #     # TODO save booking in database.
        #     pass
        return Message.assistant_message(result["text"])
    
    def is_done(self):
        if "booking_confirmed" not in self.data:
            return False
        
        return (self.data["booking_confirmed"] != "" and 
                self.data["booking_confirmed"] is not None)