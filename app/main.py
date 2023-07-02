import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from fastapi import FastAPI, Form

from app.system import System
from app.system import Conversation, CustomerContext
from app.system import System
from app.task_resolver.tasks import create_make_reservation_task, create_task_router_task, create_select_business_task
from app.task_resolver.engine import Task
from app.model import Message
from app.utils import logger
from app.integrations import TwilioMessagingAPI, OpenAIClient

from app.backend.presentation.routers import reservation_router, business_router
from app.backend.main_backend import init_backend
import traceback

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get('TWILIO_NUMBER')
openai_token = os.environ.get('OPENAI_API_KEY')

# init_backend()

app = FastAPI()

##### BACKEND #####
app.include_router(reservation_router.reservation_api_router)
app.include_router(business_router.business_api_router)
##### BACKEND #####

system = System()
twilio_integration = TwilioMessagingAPI(account_sid, auth_token, twilio_number)
openai_integration = OpenAIClient(openai_token)

def create_task(task_name):
    if task_name == "MAKE_RESERVATION_TASK":
        return create_select_business_task()
    else:
        return create_task_router_task()

def main_flow(message: Message, customer_number: str) -> Message: 

    if message.text == "exit":
        system.save_context(CustomerContext(customer_number, Conversation(), create_task_router_task()))
        return Message.assistant_message("Conversacion reiniciada. Puedes comenzar de nuevo!")

    customer_context: CustomerContext = system.get_context(customer_number)
    conversation: Conversation = customer_context.conversation
    current_task: Task = customer_context.current_task
    
    conversation._add_message(message)
    logger.debug(f"Conversation: {conversation.get_messages()}")
    task_result: Message = current_task.run(conversation.get_messages())
    if current_task.name == "TASK_ROUTER_TASK":
        if task_result.key == "CONVERSATION_DONE":
            # Reset Conversation
            logger.debug(f"Conversation finished, reseting conversation.")
            system.save_context(CustomerContext(customer_number, Conversation(), create_task_router_task()))
            return None
        elif task_result.key != "OTHER":
            # Here I know already that he wants to make a reservation.
            new_task = create_task(task_result.key)
            response: Message = new_task.run(conversation.get_messages())             
            conversation._add_message(response)
            customer_context.current_task = new_task
            # customer_context.conversation = conversation
            system.save_context(customer_context)
            return response
        else:
            conversation.add_assistant_message(task_result.text)
            system.save_context(customer_context)
            return task_result
    else:
        if task_result is not None:
            conversation._add_message(task_result)
            system.save_context(customer_context)
        if current_task.is_done():
            if current_task.next_task is not None:
                logger.debug(f"Current Task {current_task.name} is DONE, moving to next Task {current_task.next_task.name}")
                customer_context.current_task = current_task.next_task
                system.save_context(customer_context)
        return task_result


@app.get("/")
async def root():
    return {"message": "Hello World 2"}    


@app.post("/message")
async def reply(Body: str = Form(), To: str = Form(), From: str = Form(), ProfileName: str = Form()):
    # Call the OpenAI API to generate text with GPT-3.5
    try:
        
        user_message = Message.user_message(Body)
        response = main_flow(message=user_message, customer_number=From)
        if response is not None and response != "":
            twilio_integration.send_message(From, response)

        response = {"statusCode": 200}
        return response
        
    except Exception as e:
        # Exception handling and returning a 200 OK response
        # Print the stack trace
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        if From is not None:
            twilio_integration.send_message(From, "Lo siento, tuvimos un problema :(. Intenta mas tarde.")
        response = {"statusCode": 200}
        return response