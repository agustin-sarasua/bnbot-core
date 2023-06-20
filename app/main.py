import json
import requests

import os
import openai
from langchain.memory import ConversationBufferMemory

import time

openai.api_key = os.environ.get('OPEN_AI_TOKEN')

def send_response_to_client(client_number="59899513718", message="hola"):
    url = 'https://graph.facebook.com/v17.0/102195312913032/messages'
    headers = {
        'Authorization': 'Bearer EAAJASfMaTY4BAPoqWvo7fG3AgLffAM5ZBkVbdtSP9mZBZAEcUw6fB6ghi1pDx2cvpzZAFUzgd2mJaZCtb34w8f0LgBa88MT2ZAzdElbqcJzlZAQG0zztG1J1AZBbXM1mPHNHoWbVX1iZA5TSBu2YZCHR2reDQbSZAFSDS7RIZBqZBZCrTYuRn0PfZCtCe4ZC4RCiXs4MwYKKSeZAYj1aGegDOfITnkF0lCXZBfkwrWxJwZD',
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
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response)


def handler(event, context):
    try:
        print(event)

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
            wa_id = body['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']

            
            send_response_to_client(wa_id, response)

            response = {
                "statusCode": 200,
                "body": "hola"
            }
            return response
        
    except Exception as e:
        # Exception handling and returning a 200 OK response
        error_message = str(e)
        print(e)
        response = {
                "statusCode": 200,
                "body": "hola"
            }
        return response