from app.task_resolver.task_model import StepResolver
from typing import List, Any
from datetime import datetime, timedelta


class PromptInjectionResolver(StepResolver):

    def run(self, step_data: dict, messages: List[Any], previous_steps_data: List[Any]) -> str:
        pass
        
    def is_done(self, step_data: dict):
        return True