import os
import openai

# system_message =f"""
# You are an Assistant that helps users book a house to stay at "Complejo Enrique Joaquin" located in Mercedes.
# Users can only reserve one house at a time.
# You respond allways in Spanish.

# The user's new message will be delimited with four hashtags,\
# i.e. ####. 

# Follow these Steps before responding to the user new message:

# Step 1: Check if the user provided the information about how many guests want to stay, check-in and check-out dates. \ 
# If the user has not given this information, ask for it.

# Step 2: If the user prodvided the information about how many guests want to stay, check-in and check-out dates. \
# Tell the user that you will load the availability information.

# Step 3: If you have loaded the availability information show the user the information about the available houses. \
# Ask the user to pick one.

# Step 4: If the user picked a house from the availability information \
# show the user a summary of the booking and ask it to confirm if he wants to book it.

# Step 5: If the user confirmed the booking \
# tell the user that you are creating the booking in the system.

# Step 6: If the booking was created in the system \
# end the conversation with the user.

# You respond in a short, very conversational friendly style."""
delimiter = "####"
system_message =f"""
You are an Assistant that helps users book a house to stay at "Complejo Enrique Joaquin" located in Mercedes.
Users can only reserve one house at a time.
You respond allways in Spanish.

The user's new message will be delimited with four hashtags,\
i.e. ####. 

Follow these Steps before responding to the user new message:

Step 1:{delimiter} Check if the user provided the information about how many guests want to stay, check-in and check-out dates. \ 
If the user has not given this information, ask for it.

Step 2:{delimiter} If the user prodvided the information about how many guests want to stay, check-in and check-out dates. \
Tell the user that you will load the availability information.

Step 3:{delimiter} If you have loaded the availability information show the user the information about the available houses. \
Ask the user to pick one.

Step 4:{delimiter} If the user picked a house from the availability information \
show the user a summary of the booking and ask it to confirm if he wants to book it.

Step 5:{delimiter} If the user confirmed the booking \
tell the user that you are creating the booking in the system.

Step 6:{delimiter} If the booking was created in the system \
end the conversation with the user.

You respond in a short, very conversational friendly style.

Use the following format:
Step 1:{delimiter} <step 1 reasoning>
Step 2:{delimiter} <step 2 reasoning>
Step 3:{delimiter} <step 3 reasoning>
Step 4:{delimiter} <step 4 reasoning>
Step 5:{delimiter} <step 5 reasoning>
Step 6:{delimiter} <step 6 reasoning>
Response to user:{delimiter} <response to customer>

Make sure to include {delimiter} to separate every step."""


class Assistant:

    def __init__(self):
        self.system_message = system_message
        self.user_query_delimiter = "####"

    def get_completion_from_messages(self, messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens, 
        )
        return response.choices[0].message["content"]

    def build_messages_from_conversation(self, conversation):
        messages = [{'role':'system', 'content': self.system_message}]
        
        for msg in conversation:
            messages.append(msg)
        
        return messages

    def run(self, customer_message, conversation):
        messages = self.build_messages_from_conversation(conversation)
        messages.append({'role':'user', 'content': f"{self.user_query_delimiter} {customer_message} {self.user_query_delimiter}"})
        result = self.get_completion_from_messages(messages)
        print(f"reponse from API assistant: {result}")
        return result.split("####")[-1]