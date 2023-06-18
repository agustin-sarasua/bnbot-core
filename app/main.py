import json
import requests

import os
import openai
from langchain.memory import ConversationBufferMemory

import time

def read_json_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        raise Exception(f"Failed to retrieve JSON from URL. Status Code: {response.status_code}")

# URL of the JSON file
json_url = "https://bnbot-bucket.s3.amazonaws.com/availability.json"

class Cache:
    def __init__(self):
        self.cache_data = {}

    def get(self, key):
        value, timestamp = self.cache_data.get(key, (None, None))
        if timestamp and time.time() - timestamp > 120:
            self.delete(key)
            return None
        return value

    def set(self, key, value):
        timestamp = time.time()
        self.cache_data[key] = (value, timestamp)

    def delete(self, key):
        if key in self.cache_data:
            del self.cache_data[key]

# Create an instance of the cache
my_cache = Cache()

openai.api_key = os.environ.get('OPEN_AI_TOKEN')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    print(messages)
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


delimiter = "####"


system_message = f"""
You are an assistant to help customers book a house to stay. 
Customers can only reserve one house at a time.
You answer in the same language the user speaks.
Follow these steps to answer the customer queries.
The customer query will be delimited with four hashtags,\
i.e. {delimiter}. 

Use the information about the following to find the house for the customer.\
All Houses are located in Mercedes and they are:
1. Nombre: Cabaña "Sol"
   Descripción: Impresionante villa con vistas panorámicas a las montañas. Esta lujosa propiedad ofrece un ambiente tranquilo y relajante con amplios espacios interiores y exteriores. Cuenta con una piscina privada, jardines exuberantes y una terraza para disfrutar de las maravillosas vistas. Perfecta para escapadas en familia o con amigos.
   Amenities: Wi-Fi, estacionamiento privado, admite mascotas, barbacoa, piscina privada.
   Disponibilidad: 
   - Del 01 de Setiembre de 2023 al 05 de Setiembre de 2023
   - Del 20 de Setiembre de 2023 al 29 de Setiembre de 2023 
   - Del 03 de Octubre de 2023 al 05 de Octubre de 2023
   Precio: $250 por noche.
   Capacidad: Hasta 8 personas.
   Mas informacion: http://google.com

2. Nombre: Cabaña "Luna"
   Descripción: Encantador apartamento ubicado en el pintoresco centro histórico de la ciudad. Esta acogedora propiedad combina encanto tradicional con comodidades modernas. Está rodeada de calles empedradas, restaurantes y tiendas locales. Ideal para aquellos que desean sumergirse en la cultura y la historia de la ciudad.
   Amenities: Wi-Fi, estacionamiento público cercano, no se permiten mascotas, balcón con vistas a la ciudad, acceso a lavandería comunitaria.
   Disponibilidad: 
   - Del 03 de Setiembre de 2023 al 10 de Setiembre de 2023
   Precio: $120 por noche.
   Capacidad: Hasta 4 personas.
   Mas informacion: http://google.com

3. Nombre: Cabaña "Estrella"
   Descripción: Es una linda pero super chica. Tiene lo mismo que la cabaña luna, solo cambia su tamaño.
   Amenities: Wi-Fi, estacionamiento público cercano, no se permiten mascotas, balcón con vistas a la ciudad, acceso a lavandería comunitaria.
   Disponibilidad: 
   - Del 03 de Octubre de 2023 al 05 de Octubre de 2023
   Precio: $60 por noche.
   Capacidad: Hasta 4 personas.
   Mas informacion: http://google.com

Step 1:{delimiter} Decide whether the user wants to book a house. \

Step 2:{delimiter} If the user wants to book a house, identify how many people want to stay, check-in and check-out dates \ 
and check if there are houses available for those conditions.

Step 3:{delimiter} If all the information for the reservation is provided (check-in date, check-out date, house name and number of people), \ 
Make sure the user knows about the available houses that meet its requirements \
and make sure the user chooses one.

Step 4:{delimiter} Once the user selected a house and provided all the information for the reservation, make sure the user agree with the reservation by \ 
showing a summary of the booking, including: \
check-in date, check-out date, house name, number of people and total price. \

Step 5:{delimiter} If the user agreed with the reservation, make sure the you have all the user information needed which are: name and email. \
Finally confirm the reservation to the user and notify the user that a email will be sent.

You respond in a short, very conversational friendly style.
"""


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


def build_current_conversation(new_message: str, customer_number: str) -> ConversationBufferMemory:
    context = my_cache.get(customer_number)
    if context is None:
        context = ConversationBufferMemory()
    
    context.chat_memory.add_user_message(new_message)
    return context

def update_current_conversation(customer_number: str, memory: ConversationBufferMemory):
    my_cache.set(customer_number, memory)


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

            # Read JSON from the URL and save it as a dictionary
            availability_dict = read_json_from_url(json_url)

            # Parse the JSON body
            body = json.loads(event['body'])

            # Extract the text body, profile name, and wa_id
            text_body = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            profile_name = body['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
            wa_id = body['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']

            # Get Current Conversation
            memory = build_current_conversation(text_body, wa_id, profile_name)

            # Call the router chain
            
            response = get_completion_from_messages(context)
            
            context.append({'role':'assistant', 'content':f"{response}"})

            send_response_to_client(wa_id, response)

            my_cache.set(wa_id, context)

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
    

def old_handler(event, context):
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

            # Read JSON from the URL and save it as a dictionary
            availability_dict = read_json_from_url(json_url)

            # Parse the JSON body
            body = json.loads(event['body'])

            # Extract the text body, profile name, and wa_id
            text_body = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            profile_name = body['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
            wa_id = body['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']

            context = my_cache.get(wa_id)
            if context is None:
                context = [{'role':'system', 'content':system_message} ]  # accumulate messages
            
            context.append({'role':'user', 'content':f"{text_body}"})

            response = get_completion_from_messages(context)
            
            context.append({'role':'assistant', 'content':f"{response}"})

            send_response_to_client(wa_id, response)

            my_cache.set(wa_id, context)

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