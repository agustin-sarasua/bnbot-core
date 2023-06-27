from typing import List
from app.task_resolver.engine import Message
import openai
import os
import json
from app.utils import logger
from datetime import datetime, timedelta

openai.api_key = os.environ.get('OPENAI_API_KEY')

json_fn = {
    "name": "set_property_selected",
    "description": "Extract the property selected by the user from the available properties",
    "parameters": {
        "type": "object",
        "properties": {
            "user_has_selected": {
                "type": "boolean",
                "description": "Wether the user has explicitly selected a property from the available options"
            },
            "property_name": {
                "type": "string",
                "description": "The name of the property selected by the user"
            },
        },
        "required": ["user_has_selected", "property_name"]
    }
}

property_id_selection_fn = {
    "name": "save_property_id_selected",
    "description": "Saves the property id based on the property name.",
    "parameters": {
        "type": "object",
        "properties": {
            "property_id": {
                "type": "string",
                "description": "The property_id from the list of available properties."
            },
        },
        "required": ["property_id"]
    }
}

class PropertySelectedExtractor:

    def run(self, messages: List[Message]):
        
        messages_input = [{"role": "system", "content": "What is the property that the user wants to book?"}]
        for msg in messages:
            messages_input.append({"role": msg.role, "content": msg.text})
        # messages_input.append("role")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages_input,
            functions=[json_fn],
            function_call={"name": "set_property_selected"},
            temperature=0., 
            max_tokens=500, 
        )
        fn_parameters = json.loads(response.choices[0].message["function_call"]["arguments"])
        logger.debug(f"set_property_selected fn_parameters {fn_parameters}")
        return fn_parameters
    
    def run_load_property_id(self, available_properties, property_name):
        system_prompt = f"""Save the property_id of the property with name: {property_name}?
        Here are the properties available:
        {available_properties}
        """
        messages_input = [{"role": "system", "content": system_prompt}]

        # messages_input.append("role")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages_input,
            functions=[property_id_selection_fn],
            function_call={"name": "save_property_id_selected"},
            temperature=0., 
            max_tokens=500, 
        )
        fn_parameters = json.loads(response.choices[0].message["function_call"]["arguments"])
        logger.debug(f"get_property_id_selected fn_parameters {fn_parameters}")
        return fn_parameters