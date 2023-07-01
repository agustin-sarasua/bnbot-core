# # Extract the text body, profile name, and wa_id
# text_body = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
# profile_name = body['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
# customer_number = body['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']

# def send_response_to_client(client_number="59899513718", message="hola"):
#     url = whatsapp_url
#     headers = {
#         'Authorization': f"Bearer {whatsapp_token}",
#         'Content-Type': 'application/json'
#     }
#     data = {
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": client_number,
#         "type": "text",
#         "text": { 
#             "preview_url": False,
#             "body": message
#         }
#     }
#     logger.debug(f"Replying to customer: {message}")
#     response = requests.post(url, headers=headers, data=json.dumps(data))
    
#     response_data = response.json()
#     formatted_response = json.dumps(response_data, indent=4)
#     logger.debug(f"Response from WhatsApp API: {formatted_response}")