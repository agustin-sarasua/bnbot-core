from abc import ABC, abstractmethod
from app.model import Message, System, CustomerContext, Conversation
from app.task_resolver.tasks import create_task_router_task, create_select_business_task
from app.integrations import TwilioMessagingAPI
from app.task_resolver.engine import Task
from app.utils import logger, remove_spanish_special_characters
import traceback

class HandleMessageUseCase:

    def __init__(self, system: System, twilio_integration: TwilioMessagingAPI):
        self.twilio_integration = twilio_integration
        self.system = system

    def main_flow(self, message: Message, customer_number: str) -> Message: 

        if message.text == "exit":
            self.system.save_context(CustomerContext(customer_number, Conversation(), create_task_router_task()))
            return Message.assistant_message("Conversacion reiniciada. Puedes comenzar de nuevo!")
        
        message.text = remove_spanish_special_characters(message.text)
        
        customer_context: CustomerContext = self.system.get_context(customer_number)
        conversation: Conversation = customer_context.conversation
        current_task: Task = customer_context.current_task
        
        if current_task.is_done():
            if current_task.get_next_task() is not None:
                logger.debug(f"Moving to the next Task -> {current_task.get_next_task().name}")
                current_task = current_task.get_next_task()
            else:
                self.system.save_context(CustomerContext(customer_number, Conversation(), create_task_router_task()))
                return Message.assistant_message("Gracias, la conversacion fue reiniciada. Si deseas realizar otra tarea vuelve a escribirnos.")

        if message is not None:
            conversation._add_message(message)
        task_result: Message = current_task.run(conversation.get_messages())
        if current_task.is_done():
            if not current_task.steps[-1].reply_when_done:
                current_task = current_task.get_next_task()
                if current_task is not None:
                    customer_context.current_task = current_task
                    task_result: Message = current_task.run(conversation.get_messages())
                    if task_result is not None:
                        conversation._add_message(task_result)
                    self.system.save_context(customer_context)
                else:
                    # Reset Conversation
                    self.system.save_context(CustomerContext(customer_number, Conversation(), create_task_router_task()))
                    return Message.assistant_message("Gracias, la conversacion fue reiniciada. Si deseas realizar otra tarea vuelve a escribirnos.")
        return task_result
    

    def execute(self, user_message: Message, customer_number: str):
        try:
            response = self.main_flow(message=user_message, customer_number=customer_number)
            if response is not None and response != "":
                self.twilio_integration.send_message(customer_number, response.text)
            return response
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Exception {str(e)}")
            if customer_number is not None:
                self.twilio_integration.send_message(customer_number, "Lo siento, tuvimos un problema :(. Intenta mas tarde.")
                self.system.save_context(CustomerContext(customer_number, Conversation(), create_task_router_task()))
            return None

        
        
