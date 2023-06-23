import time
from typing import List, Any
import boto3
import json
from app.utils import Cache, read_json_from_s3
from app.task_resolver import Task, Step, StepResolver
from app.task_resolver.tasks import create_task_router_task

class Conversation:
    
    customer_number: str
    task: Task # e.g: the user is making a reservation
    messages: List[Any]

    def __init__(self, customer_number: str, task: Task):
        self.messages = []
        self.task = task
        self.customer_number = customer_number

    def get_messages(self) -> List[Any]:
        return self.messages
    
    def save_messages(self, messages):
        self.messages = messages

    def get_messages_string(self):
        result =""
        for msg in self.messages:
            result += f"{msg['role']}: {msg['content']}\n"
        return result[:-1]

    def _add_message(self, msg, role):
        self.messages.append({'role':role, 'content': msg})

    def add_user_message(self, msg):
        self._add_message(msg, 'user')

    def add_assistant_message(self, msg):
        self._add_message(msg, 'assistant')


class System:
    
    conversations_cache: Cache
    assistant_number: str

    def __init__(self, assistant_number="test-number"):
        self.assistant_number = assistant_number
        self.conversations_cache = Cache(60*24*60) # 24 hours

    def get_conversation(self, customer_number: str) -> Conversation:
        return self.conversations_cache.get(customer_number, Conversation(customer_number, create_task_router_task()))
    
    def save_conversation(self, conversation: Conversation):
        self.conversations_cache.set(conversation.customer_number, conversation)