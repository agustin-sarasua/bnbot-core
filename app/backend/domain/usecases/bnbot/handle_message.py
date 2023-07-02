from abc import ABC, abstractmethod
from app.model import Message, System, CustomerContext, Conversation
from app.task_resolver.tasks import create_task_router_task, create_select_business_task
from app.integrations import TwilioMessagingAPI
from app.task_resolver.engine import Task
from app.utils import logger
import traceback

class HandleMessageUseCase:

    def __init__(self, system: System, twilio_integration: TwilioMessagingAPI):
        self.twilio_integration = twilio_integration
        self.system = system

    def create_task(self, task_name):
        if task_name == "MAKE_RESERVATION_TASK":
            return create_select_business_task()
        else:
            return create_task_router_task()

    def main_flow(self, message: Message, customer_number: str) -> Message: 

        if message.text == "exit":
            self.system.save_context(CustomerContext(customer_number, Conversation(), create_task_router_task()))
            return Message.assistant_message("Conversacion reiniciada. Puedes comenzar de nuevo!")

        customer_context: CustomerContext = self.system.get_context(customer_number)
        conversation: Conversation = customer_context.conversation
        current_task: Task = customer_context.current_task
        
        conversation._add_message(message)
        logger.debug(f"Conversation: {conversation.get_messages()}")
        task_result: Message = current_task.run(conversation.get_messages())
        if current_task.name == "TASK_ROUTER_TASK":
            if task_result.key == "CONVERSATION_DONE":
                # Reset Conversation
                logger.debug(f"Conversation finished, reseting conversation.")
                self.system.save_context(CustomerContext(customer_number, Conversation(), create_task_router_task()))
                return None
            elif task_result.key != "OTHER":
                # Here I know already that he wants to make a reservation.
                new_task = self.create_task(task_result.key)
                response: Message = new_task.run(conversation.get_messages())             
                conversation._add_message(response)
                customer_context.current_task = new_task
                # customer_context.conversation = conversation
                self.system.save_context(customer_context)
                return response
            else:
                conversation.add_assistant_message(task_result.text)
                self.system.save_context(customer_context)
                return task_result
        else:
            if task_result is not None:
                conversation._add_message(task_result)
                self.system.save_context(customer_context)
            if current_task.is_done():
                if current_task.next_task is not None:
                    logger.debug(f"Current Task {current_task.name} is DONE, moving to next Task {current_task.next_task.name}")
                    customer_context.current_task = current_task.next_task
                    self.system.save_context(customer_context)
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
            return None

        
        
