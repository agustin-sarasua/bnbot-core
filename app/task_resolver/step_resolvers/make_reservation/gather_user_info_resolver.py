from app.task_resolver.engine import StepResolver, StepData
from typing import List, Any
from app.utils import get_completion_from_messages, logger
from app.tools import UserInformationExtractorChain
from app.model import Message

delimiter = "####"

class GatherUserInfoResolver(StepResolver):

    def run(self, messages: List[Message], previous_steps_data: List[Any], step_chat_history: List[Message] = None) -> Message:

        # exit_task_step_data: StepData = previous_steps_data["EXIT_TASK_STEP"]
        # if exit_task_step_data.resolver_data["conversation_finished"] == True:
        #     logger.debug("Conversation finished. Responding None")
        #     return None

        chat_history = self.build_chat_history(messages)
        
        info_extractor = UserInformationExtractorChain()
        user_info = info_extractor(chat_history)
        
        self.data["user_information"] = user_info

        return Message.assistant_message(user_info["text"])
    
    def is_done(self):
        if "user_information" not in self.data:
            return False
        
        user_information = self.data["user_information"]

        return (user_information["user_name"] != "" and 
                user_information["user_name"] is not None and
                user_information["email"] != "" and 
                user_information["email"] is not None)