import time
from typing import List, Any
import boto3
import json
from .utils import Cache, read_json_from_s3
from .task_resolver import Task, Step, StepResolver


class Conversation:
    
    task: Task # e.g: the user is making a reservation
    messages_cache: Cache

    def __init__(self, task: Task):
        self.messages_cache = Cache(60*1*60) # 1 hour
        self.task = task

    def get_messages(self, customer_number) -> List[Any]:
        return self.messages_cache.get(customer_number)
    
    def save_messages(self, customer_number, conversation):
        self.messages_cache.set(customer_number, conversation)

    def get_messages_string(self, customer_number):
        conversation = self.get_messages(customer_number)
        result =""
        for msg in conversation:
            result += f"{msg['role']}: {msg['content']}\n"
        return result

    def _add_message(self, msg, customer_number, role):
        messages = self.get_messages(customer_number)
        messages.append({'role':role, 'content': msg})
        self.save_messages(customer_number, messages)

    def add_user_message(self, msg, customer_number):
        self._add_message(msg, customer_number, 'user')

    def add_assistant_message(self, msg, customer_number):
        self._add_message(msg, customer_number, 'assistant')


class System:
    
    conversations_cache: Cache
    assistant_number: str

    def __init__(self, assistant_number="test-number"):
        self.assistant_number = assistant_number
        self.conversations_cache = Cache(60*24*60) # 24 hours

    def get_conversation(self, customer_number:str) -> Conversation:
        return self.conversations_cache.get(customer_number)
    
    def save_conversation(self, customer_number, conversation: Conversation):
        self.conversations_cache.set(customer_number, conversation)