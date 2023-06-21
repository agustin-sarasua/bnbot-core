import time
import boto3
import json
import os
import openai


def get_completion_from_messages(messages, 
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


def read_json_from_s3(bucket_name, file_name):
    s3 = boto3.resource('s3')
    try:
        obj = s3.Object(bucket_name, file_name)
        data = obj.get()['Body'].read().decode('utf-8')
        json_data = json.loads(data)
        return json_data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        
        return None


class Cache:
    def __init__(self, timeout=120):
        self.cache_data = {}
        self.timeout = timeout

    def get(self, key, default_value):
        value, timestamp = self.cache_data.get(key, (default_value, None))
        if self.timeout > 0:
            if timestamp and time.time() - timestamp > self.timeout:
                self.delete(key)
                return default_value
        return value

    def set(self, key, value):
        timestamp = time.time()
        self.cache_data[key] = (value, timestamp)

    def delete(self, key):
        if key in self.cache_data:
            del self.cache_data[key]
