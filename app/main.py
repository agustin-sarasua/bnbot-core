import json
import requests

import os
import openai
from system import System
from system import Conversation
from system import System
from task_resolver.tasks import create_make_reservation_task, create_task_router_task

from utils import logger


openai.api_key = os.environ.get('OPEN_AI_TOKEN')
whatsapp_token = os.environ.get('WHATSAPP_TOKEN')
whatsapp_url = os.environ.get('WHATSAPP_URL')

system = System()

def send_response_to_client(client_number="59899513718", message="hola"):
    url = whatsapp_url
    headers = {
        'Authorization': f"Bearer {whatsapp_token}",
        'Content-Type': 'application/json'
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": client_number,
        "type": "text",
        "text": { 
            "preview_url": False,
            "body": message
        }
    }
    logger.debug(f"Replying to customer: {message}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    response_data = response.json()
    formatted_response = json.dumps(response_data, indent=4)
    logger.debug(f"Response from WhatsApp API: {formatted_response}")

def create_task(task_name):
    if task_name == "MAKE_RESERVATION_TASK":
        return create_make_reservation_task()
    else:
        return create_task_router_task()

def main_flow(message: str, customer_number: str): 

    if message == "exit":
        system.save_conversation(Conversation(customer_number, create_task_router_task()))
        return "Conversacion reiniciada. Puedes comenzar de nuevo!"

    conversation = system.get_conversation(customer_number)
    conversation.add_user_message(message)
    logger.debug(f"Conversation: {conversation.get_messages()}")
    task_result = conversation.task.run(conversation.get_messages())
    if conversation.task.name == "TASK_ROUTER_TASK":
        if task_result["task_id"] != "OTHER":
            # Here I know already that he wants to make a reservation.
            task = create_task(task_result["task_id"])
            conversation.task = task
            response = task.run(conversation.get_messages())
            # if not task.steps[-1].reply_when_done:
            #     return main_flow()                
            conversation.add_assistant_message(response)
            system.save_conversation(conversation)
            return response
        else:
            conversation.add_assistant_message(task_result["text"])
            system.save_conversation(conversation)
            return task_result["text"]
    else:
        conversation.add_assistant_message(task_result)
        system.save_conversation(conversation)
        return task_result


def handler(event, context):
    customer_number = None
    try:
        logger.debug(f"Event: {event}")

        if event["queryStringParameters"] is not None and 'hub.challenge' in event["queryStringParameters"]:
            verify_token = event['queryStringParameters']['hub.verify_token']
            assert verify_token == "holacarola"
            challenge =  event['queryStringParameters']['hub.challenge']

            response = {
                "statusCode": 200,
                "body": challenge
            }
            return response
        else:

            # Parse the JSON body
            body = json.loads(event['body'])

            # Extract the text body, profile name, and wa_id
            text_body = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            profile_name = body['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
            customer_number = body['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']

            response = main_flow(message=text_body, customer_number=customer_number)
            send_response_to_client(customer_number, response)

            response = {
                "statusCode": 200,
                "body": "hola"
            }
            return response
        
    except Exception as e:
        # Exception handling and returning a 200 OK response
        logger.debug(f"Conversation: {str(e)}")
        if customer_number is not None:
            send_response_to_client(customer_number, "Ups... Tuvimos un problema procesando tu mensaje. Por favor contactate directo con Gonzalo: 099386573 ")
        response = {
                "statusCode": 200,
                "body": "hola"
        }
        return response