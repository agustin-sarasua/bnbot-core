from abc import ABC, abstractmethod
from typing import List, Any

class StepResolver(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def run(self, step_data: dict, messages: List[str]):
        pass
    
    @abstractmethod
    def is_done(self, step_data: dict):
        pass


class Step:
    name: str
    data: dict
    status: str

    resolver: StepResolver
    
    def __init__(self, name, resolver):
        self.name = name
        self.status = "TODO"
        self.resolver = resolver
        self.data = dict()
    
    def is_done(self) -> bool:
        return self.status == "DONE"
    
    def resolve(self, messages: List[Any]):
        result = self.resolver.run(self.data, messages)
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