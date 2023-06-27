from app.task_resolver.engine import StepResolver, Message
from typing import List, Any
from datetime import datetime, timedelta


class PromptInjectionResolver(StepResolver):

    def run(self, messages: List[Message], previous_steps_data: dict, step_chat_history: List[Message] = None) -> Message:
        pass
        
    def is_done(self):
        return True