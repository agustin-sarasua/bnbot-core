from task_resolver.model import StepResolver
from typing import List, Any
from utils import get_completion_from_messages
from tools import UserInformationExtractorChain
from datetime import datetime, timedelta

delimiter = "####"



class GatherUserInfoResolver(StepResolver):

    def __init__(self):
        pass

    def build_chat_history(self, messages):
        chat_history = ""
        for msg in messages:
            chat_history += f"{msg['role']}: {msg['content']}\n"
        return chat_history

    def run(self, step_data: dict, messages: List[str], previous_steps_data: List[Any]) -> str:

        chat_history = self.build_chat_history(messages)
        
        info_extractor = UserInformationExtractorChain()
        user_info = info_extractor(chat_history)
        
        step_data["user_information"] = user_info

        return user_info["text"]
    
    def is_done(self, step_data: dict):
        if "user_information" not in step_data:
            return False
        
        user_information = step_data["user_information"]

        return (user_information["user_name"] != "" and user_information["user_name"] is not None and
                user_information["email"] != "" and user_information["email"] is not None)