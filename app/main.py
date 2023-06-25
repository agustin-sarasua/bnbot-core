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

from app.utils import logger
from app.integrations import TwilioMessagingAPI


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

def main_flow(message: str, customer_number: str) -> str: 

    def message_preprocessing(msg: str) -> str:
        return msg.replace("\n", "  ")

    message = message_preprocessing(message)
    if message == "exit":
        system.save_conversation(Conversation(customer_number, create_task_router_task()))
        return "Conversacion reiniciada. Puedes comenzar de nuevo!"

    conversation = system.get_conversation(customer_number)
    conversation.add_user_message(message)
    logger.debug(f"Conversation: {conversation.get_messages()}")
    task_result = conversation.task.run(conversation.get_messages())
    if conversation.task.name == "TASK_ROUTER_TASK":
        if task_result["task_id"] == "CONVERSATION_DONE":
            # Reset Conversation
            logger.debug(f"Conversation finished, reseting conversation.")
            system.save_conversation(Conversation(customer_number, create_task_router_task()))
            return None
        elif task_result["task_id"] != "OTHER":
            # Here I know already that he wants to make a reservation.
            task = create_task(task_result["task_id"])
            conversation.task = task
            response = task.run(conversation.get_messages(), )
            # if not task.steps[-1].reply_when_done:
            #     return main_flow()                
            conversation.add_assistant_message(message_preprocessing(response))
            system.save_conversation(conversation)
            return response
        else:
            conversation.add_assistant_message(message_preprocessing(task_result["text"]))
            system.save_conversation(conversation)
            return task_result["text"]
    else:
        if task_result is not None:
            conversation.add_assistant_message(message_preprocessing(task_result))
            system.save_conversation(conversation)
        return task_result


# def handler(event, context):
#     customer_number = None
#     try:
#             # Parse the JSON body
#         body = json.loads(event['body'])
        
#         if 'isBase64Encoded' in event and event['isBase64Encoded']:
#             body = decode_base64(body)

#         request = twilio_integration.parse_request(body)
#         customer_number = request["from"]

#         response = main_flow(message=request["message"], customer_number=customer_number)
#         if response is not None and response != "":
#             twilio_integration.send_message(request["to"], response)

#         response = {"statusCode": 200}
#         return response
        
#     except Exception as e:
#         # Exception handling and returning a 200 OK response
#         logger.error(f"Exception {str(e)}")
#         if customer_number is not None:
#             twilio_integration.send_message(customer_number, "Lo siento, tuvimos un problema :(. Intenta mas tarde.")
#         response = {"statusCode": 200}
#         return response

@app.get("/")
async def root():
    return {"message": "Hello World 2"}    


@app.post("/message")
async def reply(Body: str = Form(), To: str = Form(), From: str = Form(), ProfileName: str = Form()):
    # Call the OpenAI API to generate text with GPT-3.5
    try:

        response = main_flow(message=Body, customer_number=From)
        if response is not None and response != "":
            twilio_integration.send_message(From, response)

        response = {"statusCode": 200}
        return response
        
    except Exception as e:
        # Exception handling and returning a 200 OK response
        logger.error(f"Exception {str(e)}")
        if From is not None:
            twilio_integration.send_message(From, "Lo siento, tuvimos un problema :(. Intenta mas tarde.")
        response = {"statusCode": 200}
        return response