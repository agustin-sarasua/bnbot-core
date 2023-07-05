import time
import boto3
import json
import os
import openai
from datetime import datetime
from typing import List, Any
from app.model import Message


class OpenAIClient:
    
    def __init__(self, api_token: str):
        self.api_token = api_token

    @staticmethod
    def build_messages_from_conversation(system_message, messages: List[Message]):
        result = [{'role':'system', 'content': system_message}]
        for msg in messages:
            result.append({'role': msg.role, 'content': msg.text})
        return result
    
    def get_completion_from_messages(self,
                                     messages, 
                                     model="gpt-3.5-turbo", 
                                     temperature=0, 
                                     max_tokens=500):
    
        openai.api_key = self.api_token

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens, 
        )
        return response.choices[0].message["content"]

    