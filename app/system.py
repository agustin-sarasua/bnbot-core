import time
from typing import List, Any
import boto3
import json
from .utils import Cache, read_json_from_s3


class System:
    
    conversations_cache = Cache(60*15)

    properties_info_cache = Cache(-1)

    def __init__(self, assistant_number="test-number"):
        self.assistant_number = assistant_number

    def get_conversation(self, customer_number) -> List[Any]:
        return self.conversations_cache.get(customer_number)
    
    def save_conversation(self, customer_number, conversation):
        self.conversations_cache.set(customer_number, conversation)
    
    def _add_message(self, msg, customer_number, role):
        conversation = self.get_conversation(customer_number)
        conversation.append({'role':role, 'content': msg})
        self.save_conversation(customer_number, conversation)

    def add_user_message(self, msg, customer_number):
        self._add_message(msg, customer_number, 'user')

    def add_system_message(self, msg, customer_number):
        self._add_message(msg, customer_number, 'system')
    
    def add_assistant_message(self, msg, customer_number):
        self._add_message(msg, customer_number, 'assistant')

    def get_properties_availabe(self):
        result = self.properties_info_cache.get(self.assistant_number)        
        if result is None:
            result = self.load_properties_information(self)
        return result

    def get_conversation_string(self, customer_number):
        conversation = self.get_conversation(customer_number)
        result =""
        for msg in conversation:
            result += f"{msg['role']}: {msg['content']}\n"
        return result
    # def load_properties_information(self):
    #     availability = read_json_from_s3("bnbot-bucket", f"availability_{self.assistant_number}.json")
    #     self.properties_info_cache.set(self.assistant_number, availability)
    #     return availability
        