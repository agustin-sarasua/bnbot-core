from app.task_resolver.model import StepResolver
from typing import List, Any
from datetime import datetime, timedelta


class PromptInjectionResolver(StepResolver):

    def __init__(self):
        pass

    def run(self, step_data: dict, messages: List[str], previous_steps_data: List[Any]) -> str:
        pass
        
    def is_done(self, step_data: dict):
        return True