from abc import ABC, abstractmethod
from typing import List, Any

class StepResolver(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def run(self, step_data: dict, messages: List[str], previous_steps_data: List[Any]):
        pass
    
    @abstractmethod
    def is_done(self, step_data: dict):
        pass


class Step:
    name: str
    data: dict
    status: str
    reply_when_done: bool
    resolver: StepResolver
    
    def __init__(self, name, resolver, reply_when_done=True):
        self.name = name
        self.status = "TODO"
        self.resolver = resolver
        self.data = dict()
        self.reply_when_done = reply_when_done
    
    def save_step_data(self, data):
        self.data["result"] = data

    def is_done(self) -> bool:
        return self.status == "DONE"
    
    def resolve(self, messages: List[Any], previous_steps_data: List[Any]):
        result = self.resolver.run(self.data, messages, previous_steps_data)
        if self.resolver.is_done(self.data):
            self.status = "DONE"
        else:
            self.status = "IN_PROGRESS"
        
        return result

class Task:
    name: str
    steps: List[Step]
    data: dict

    current_step: Step
    
    def __init__(self, name: str, steps: List[Step]):
        self.name = name
        self.steps = steps
        self.current_step = self.steps[0]

    def get_current_step_data(self, key):
        return self.current_step.data[key]
    
    def is_done(self) -> bool:
        for step in self.steps:
            if not step.is_done():
                return False
        return True

    def run(self, conversation_messages: List[Any]) -> str:
        if self.is_done():
            return None
        previous_steps_data = {}
        for step in self.steps:
            if step.is_done():
                previous_steps_data[step.name] = step.data
                continue
            else:
                current_step = step 
                print(f"Resolving Step: {current_step.name}")
                response = step.resolve(conversation_messages, previous_steps_data)
                if step.is_done() and not step.reply_when_done :
                    return self.run(conversation_messages)
                return response
                    