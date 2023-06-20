from app.task_resolver.model import StepResolver
from typing import List, Any
from datetime import datetime, timedelta
from app.tools import TaskExtractorChain


class TaskIdentifierResolver(StepResolver):

    def __init__(self):
        pass

    def run(self, step_data: dict, messages: List[str], previous_steps_data: List[Any]) -> str:
        chat_history = self.build_chat_history(messages)

        task_extractor = TaskExtractorChain()
        task_info = task_extractor(chat_history)

        if task_info["task_id"] != "":
            step_data["task_info"] = task_info

        print(f"Assistant Response: {task_info}")
        return task_info
        
    def is_done(self, step_data: dict):
        if "task_info" not in step_data:
            return False
         
        return (step_data["task_info"]["task_id"] != "" and 
                step_data["task_info"]["task_id"] is not None and 
                step_data["task_info"]["task_id"] != "OTHER")