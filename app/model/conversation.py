from typing import List, Any
import uuid
from datetime import datetime

class Message:

    def __init__(self, role: str, text: str, key: str = None):
        self.key = key
        self.text = text
        self.role = role
        self.id = uuid.uuid4()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def assistant_message(text):
        return Message("assistant", text)
    
    @staticmethod
    def route_message(text: str, key: str):
        return Message("route", text, key)
    
    @staticmethod
    def user_message(text):
        return Message("user", text)
    
    def __str__(self):
        return f"{self.role}: {self.text}"
    
    def __repr__(self):
        return str(self)

    
class Conversation:
    messages: List[Message]

    def __init__(self):
        self.messages = []

    def get_messages(self) -> List[Message]:
        return self.messages
    
    def save_messages(self, messages):
        self.messages = messages

    def get_messages_string(self):
        result =""
        for msg in self.messages:
            result += f"{msg.role}: {msg.text}\n"
        return result[:-1]

    def text_preprocessing(self, msg: str) -> str:
        return msg.replace("\n", "  ")

    def _add_message(self, msg: Message):
        self.messages.append(msg)

    def add_user_message(self, msg_text: str):
        self._add_message(Message('user', self.text_preprocessing(msg_text)))

    def add_assistant_message(self, msg_text: str):
        self._add_message(Message('assistant', self.text_preprocessing(msg_text)))                