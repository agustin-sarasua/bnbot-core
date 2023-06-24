import time
from typing import List, Any
import boto3
import json
from app.utils import Cache, read_json_from_s3
from app.task_resolver import Task, Step, StepResolver
from app.task_resolver.tasks import create_task_router_task
from app.model import Conversation


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