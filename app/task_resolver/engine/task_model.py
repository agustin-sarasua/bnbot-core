from abc import ABC, abstractmethod
from typing import List, Any
from app.utils import logger
import uuid
import copy

class Message:

    def __init__(self, role, text):
        self.text = text
        self.role = role
        self.id = uuid.uuid4()

    @staticmethod
    def assistant_message(text):
        return Message("assistant", text)
    
    @staticmethod
    def user_message(text):
        return Message("user", text)
    
    def __str__(self):
        return f"{self.role}: {self.text}"
    
    def __repr__(self):
        return str(self)

class StepResolver(ABC):
    
    data: dict

    def __init__(self):
        self.data = dict()
    
    @abstractmethod
    def run(self, messages: List[Message], previous_steps_data: dict):
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
    
    def _resolve(self, input_messages: List[Message], previous_steps_data: dict):
        result = self.resolver.run(input_messages, previous_steps_data)
        return result

    def resolve(self, input_messages: List[Message], previous_steps_data: dict):
        logger.debug(f"Resolving Step: {self.name}")

        self.data.step_chat_history.append(input_messages[-1])
        self.data.input_messages = input_messages
        self.data.previous_steps_data = previous_steps_data
        
        result = self._resolve(input_messages, previous_steps_data)
        
        self.data.resolver_data = self.resolver.data
        self.data.result = result
        self.data.step_chat_history.append(Message.assistant_message(result))

        logger.debug(f"Step: {self.name} - Resolver Result: {result}")
        logger.debug(f"Step: {self.name} - is_done {self.is_done()}")
        logger.debug(f"Step: {self.name} - Data: {self.data}")
        
        # Save Execution Log
        self.execution_log.append(copy.deepcopy(self.data))
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
    
    def is_done(self) -> bool:
        for step in self.steps:
            if not step.is_done():
                return False
        return True
    
    def _reset_previous_steps(self, step_name):
        for step in reversed(self.steps):
            step.resolver.data = {}
            if step.name == step_name:
                # Reset Step
                break

    def run(self, conversation_messages: List[Message], recursive_step: int=0) -> str:
        if recursive_step > 1:
            logger.error(f"Task {self.name}: we entered in a loop!")
            return None
        if self.is_done():
            logger.info(f"Task {self.name} DONE, returning None")
            return None
        previous_steps_data = {}
        route_to_previous_step = False
        for step in self.steps:
            # step.data["current_task_name"] = self.name
            previous_steps_data[step.name] = step.data

            if not step.is_done() or step.force_execution:
                logger.debug(f"Task: {self.name} - Resolving Step {step.name}")
                response = step.resolve(conversation_messages, previous_steps_data)
                if step.is_done() and not step.reply_when_done:
                    continue
                # Check post process router
                if step.post_process_router_resolver is not None:
                    logger.debug(f"Task: {self.name} - Do we have to route to other space?")
                    next_step = step.post_process_router_resolver.run(step.data.step_chat_history, previous_steps_data)
                    if next_step["step"] != "CONTINUE":
                        logger.debug(f"Task: {self.name} - Routing to {next_step['step']}")
                        self._reset_previous_steps(next_step["step"])
                        route_to_previous_step = True
                        break
                return response
            else:
                logger.debug(f"Task: {self.name} - Skipping Step {step.name} - it is DONE")
            
        if route_to_previous_step:
            logger.debug(f"Task: {self.name} - Routing to previous Step")
            recursive_step += 1
            return self.run(conversation_messages, recursive_step)
        