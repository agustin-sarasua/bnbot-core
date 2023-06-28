import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from fastapi import FastAPI, Form, Depends
import openai
openai.api_key = os.environ.get('OPENAI_API_KEY')


from app.system import System
from app.system import Conversation
from app.system import System
from app.task_resolver.tasks import create_make_reservation_task, create_task_router_task
from app.task_resolver.engine import Message
from app.utils import logger
from app.integrations import TwilioMessagingAPI
import traceback


account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get('TWILIO_NUMBER')

app = FastAPI()

system = System()
twilio_integration = TwilioMessagingAPI(account_sid, auth_token, twilio_number)

def create_task(task_name):
    if task_name == "MAKE_RESERVATION_TASK":
        return create_make_reservation_task()
    else:
        return create_task_router_task()

def main_flow(message: Message, customer_number: str) -> Message: 

    if message.text == "exit":
        system.save_conversation(Conversation(customer_number, create_task_router_task()))
        return Message.assistant_message("Conversacion reiniciada. Puedes comenzar de nuevo!")

    conversation = system.get_conversation(customer_number)
    conversation._add_message(message)
    logger.debug(f"Conversation: {conversation.get_messages()}")
    task_result: Message = conversation.task.run(conversation.get_messages())
    if conversation.task.name == "TASK_ROUTER_TASK":
        if task_result.key == "CONVERSATION_DONE":
            # Reset Conversation
            logger.debug(f"Conversation finished, reseting conversation.")
            system.save_conversation(Conversation(customer_number, create_task_router_task()))
            return None
        elif task_result.key != "OTHER":
            # Here I know already that he wants to make a reservation.
            task = create_task(task_result.key)
            conversation.task = task
            response: Message = task.run(conversation.get_messages())             
            conversation._add_message(response)
            system.save_conversation(conversation)
            return response
        else:
            conversation.add_assistant_message(task_result.text)
            system.save_conversation(conversation)
            return task_result
    else:
        if task_result is not None:
            conversation._add_message(task_result)
            system.save_conversation(conversation)
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