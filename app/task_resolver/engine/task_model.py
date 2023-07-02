from abc import ABC, abstractmethod
from typing import List, Any, Optional
from app.utils import logger
import uuid
import copy
from datetime import datetime
from app.model import Message

class StepResolver(ABC):
    
    data: dict

    def __init__(self):
        self.data = dict()
    
    @abstractmethod
    def run(self, messages: List[Message], previous_steps_data: dict, step_chat_history: List[Message] = None) -> Message:
        pass
    
    @abstractmethod
    def is_done(self):
        pass
    
    def build_chat_history(self, messages: List[Message]):
        chat_history = ""
        for msg in messages:
            chat_history += f"{msg.role}: {msg.text}\n"
        return chat_history[:-1]

class StepData:
    input_messages: List[Message]
    previous_steps_data: dict
    result: dict
    resolver_data: dict
    step_chat_history: List[Message]

    def __init__(self):
        self.step_chat_history = []
        self.resolver_data = {}

    def __str__(self):
        return f"""StepData(result={self.result}, 
        resolver_data={self.resolver_data}, 
        input_messages={self.input_messages}),
        step_chat_history={self.step_chat_history}"""


class Step:
    name: str
    data: StepData
    reply_when_done: bool # Wether to respond to user with text generated of jump right to the next Step
    resolver: StepResolver
    force_execution: bool
    execution_log: List[StepData]
    post_process_router_resolver: StepResolver

    def __init__(self, name: str, 
                 resolver: StepResolver, 
                 post_process_router_resolver: StepResolver = None, 
                 force_execution: bool=False, reply_when_done: bool=True):
        self.name = name
        self.resolver = resolver
        self.data = StepData()
        self.reply_when_done = reply_when_done
        self.force_execution = force_execution
        self.post_process_router_resolver = post_process_router_resolver
        self.execution_log = []

    def is_done(self) -> bool:
        return self.resolver.is_done()
    
    def _is_step_first_exection(self) -> bool:
        return len(self.execution_log) == 0
    
    def _resolve(self, input_messages: List[Message], previous_steps_data: dict) -> Message:
        result = self.resolver.run(messages=input_messages, 
                                   previous_steps_data=previous_steps_data, 
                                   step_chat_history=self.data.step_chat_history)
        return result

    def resolve(self, input_messages: List[Message], previous_steps_data: dict) -> Message:
        logger.debug(f"Resolving Step: {self.name}")

        self.data.step_chat_history.append(input_messages[-1])
        self.data.input_messages = input_messages
        self.data.previous_steps_data = previous_steps_data
        
        self.resolver.data["step_first_execution"] = self._is_step_first_exection()

        result = self._resolve(input_messages, previous_steps_data)
        
        self.data.resolver_data = self.resolver.data
        self.data.result = result
        self.data.step_chat_history.append(result)

        logger.debug(f"Step: {self.name} - Resolver Result: {result}")
        logger.debug(f"Step: {self.name} - is_done {self.is_done()}")
        logger.debug(f"Step: {self.name} - Data: {self.data}")
        
        # Save Execution Log
        self.execution_log.append(copy.deepcopy(self.data))
        return result

class Task(ABC):
    name: str
    steps: List[Step]
    data: dict

    def __init__(self, name: str, steps: List[Step]):
        self.name = name
        self.steps = steps
    
    @abstractmethod
    def get_next_task(self) -> Optional['Task']:
        pass

    def is_done(self) -> bool:
        for step in self.steps:
            if not step.is_done():
                return False
        return True
    
    def _reset_previous_steps(self, step_name):
        step_names = [step.name for step in self.steps]
        if step_name in step_names:
            for step in reversed(self.steps):
                step.resolver.data = {}
                if step.name == step_name:
                    # Reset Step
                    break
        else:
            logger.error(f"""You are trying to route to an step that does not exists! 
                         Step Name: {step_name}
                         Steps available: {step_names}""")

    def run(self, conversation_messages: List[Message]) -> Message:
        logger.debug(f"Running Task: {self.name}")
        if self.is_done():
            logger.error(f"Task {self.name} DONE, returning None")
            return None
        
        previous_steps_data = {}
        
        for step in self.steps:
            previous_steps_data[step.name] = step.data
            if not step.is_done() or step.force_execution:
                logger.debug(f"Task: {self.name} - Resolving Step {step.name}")
                response = step.resolve(conversation_messages, previous_steps_data)
                if step.is_done() and not step.reply_when_done:
                    continue

                return response
            else:
                logger.debug(f"Task: {self.name} - Skipping Step {step.name} - it is DONE")  
