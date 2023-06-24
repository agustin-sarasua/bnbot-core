from abc import ABC, abstractmethod
from typing import List, Any
from app.utils import logger

class StepResolver(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def run(self, step_data: dict, messages: List[Any], previous_steps_data: List[Any]):
        pass
    
    @abstractmethod
    def is_done(self, step_data: dict):
        pass
    
    def build_chat_history(self, messages):
        chat_history = ""
        for msg in messages:
            chat_history += f"{msg['role']}: {msg['content']}\n"
        return chat_history[:-1]

class Step:
    name: str
    data: dict
    status: str
    reply_when_done: bool # Wether to respond to user with text generated of jump right to the next Step
    resolver: StepResolver
    force_execution: bool

    def __init__(self, name, resolver, force_execution=False, reply_when_done=True):
        self.name = name
        self.status = "TODO"
        self.resolver = resolver
        self.data = dict()
        self.reply_when_done = reply_when_done
        self.force_execution = force_execution
    
    def save_step_data(self, data):
        self.data["result"] = data

    def is_done(self) -> bool:
        return self.status == "DONE"
    
    def resolve(self, messages: List[Any], previous_steps_data: List[Any]):
        logger.debug(f"Resolving Step: {self.name}")
        result = self.resolver.run(self.data, messages, previous_steps_data)
        logger.debug(f"Step {self.name} - Resolver Result: {result}")
        if self.resolver.is_done(self.data):
            self.status = "DONE"
        else:
            self.status = "IN_PROGRESS"
        logger.debug(f"Step: {self.name} - Status {self.status}")
        logger.debug(f"Step: {self.name} - Data: {self.data}")
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
            logger.info(f"Task {self.name} DONE, returning None")
            return None
        previous_steps_data = {}
        for step in self.steps:
            step.data["current_task_name"] = self.name
            previous_steps_data[step.name] = step.data
            if step.force_execution:
                logger.debug(f"Task: {self.name} - Forced Step Execution {step.name}")
                response = step.resolve(conversation_messages, previous_steps_data)
                if step.is_done() and step.reply_when_done:
                    # Respond to the user when the task finished with the "text" in response.
                    return response
            else:
                if step.is_done():
                    logger.debug(f"Task: {self.name} - Skipping Step {step.name} - it is DONE")
                    continue
                else: 
                    logger.debug(f"Task: {self.name} - Resolving Step: {step.name}")
                    response = step.resolve(conversation_messages, previous_steps_data)
                    if step.is_done() and not step.reply_when_done:
                        continue
                    return response
                    # if self.steps[-1].name == step.name:
                    #     logger.debug(f"Task: {self.name} - Reached Final Step")
                    #     return response
                    # if step.is_done() and not step.reply_when_done:
                    #     logger.debug(f"Task: {self.name} - Step : {step.name} - Not replying, calling recursive.")
                    #     return self.run(conversation_messages)
                    # return response
