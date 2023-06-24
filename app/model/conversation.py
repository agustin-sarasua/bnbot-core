from app.task_resolver import Task
from typing import List, Any

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