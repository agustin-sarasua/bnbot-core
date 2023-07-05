from app.utils import Cache
from app.task_resolver.tasks import create_task_router_task
from app.task_resolver.engine import Task
from .conversation import Conversation


class CustomerContext:

    def __init__(self, customer_number: str, conversation: Conversation, current_task: Task):
        self.customer_number = customer_number
        self.conversation = conversation
        self.current_task = current_task


class System:

    def __init__(self):
        self.context_cache: Cache = Cache(60*24*60) # 24 hours

    def get_context(self, customer_number: str) -> CustomerContext:
        return self.context_cache.get(customer_number, CustomerContext(customer_number, Conversation(), create_task_router_task()))
    
    def save_context(self, context: CustomerContext):
        self.context_cache.set(context.customer_number, context)