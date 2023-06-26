from app.task_resolver.engine import Task, Message
from typing import List, Any

class Conversation:
    
    customer_number: str
    task: Task # e.g: the user is making a reservation
    messages: List[Message]

    def __init__(self, customer_number: str, task: Task):
        self.messages = []
        self.task = task
        self.customer_number = customer_number

    def get_messages(self) -> List[Message]:
        return self.messages
    
    def save_messages(self, messages):
        self.messages = messages

    def get_messages_string(self):
        result =""
        for msg in self.messages:
            result += f"{msg.role}: {msg.text}\n"
        return result[:-1]

    def _add_message(self, msg: Message):
        self.messages.append(msg)

    def add_user_message(self, msg_text: str):
        self._add_message(Message('user', msg_text))

    def add_assistant_message(self, msg_text: str):
        self._add_message(Message('assistant', msg_text))                