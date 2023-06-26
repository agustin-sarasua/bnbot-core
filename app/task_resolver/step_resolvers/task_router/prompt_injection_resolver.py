from app.task_resolver.engine import StepResolver, Message
from typing import List, Any
from datetime import datetime, timedelta


class PromptInjectionResolver(StepResolver):

    def run(self, messages: List[Message], previous_steps_data: List[Any]) -> str:
        pass
        
    def is_done(self):
        return True