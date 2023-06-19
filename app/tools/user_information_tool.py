from typing import Optional
from langchain.tools import BaseTool
from datetime import datetime

from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

template = """Given a conversation between a user and an assistant about booking a house for short-term stay. \
Your job is to extract the name, the user email and the user phone_number \
from the conversation.

Here is the conversation: 
{chat_history}
{input}

{format_instructions}"""

response_schemas = [
    ResponseSchema(name="booking_name", description="The name of the person for the booking. "),
    ResponseSchema(name="booking_email", description="The email for the booking."),
    ResponseSchema(name="booking_phone_number", description="The phone number used for the booking."),
]


class UserInfoExtractorChain:

    def __init__(self):

        llm = OpenAI(temperature=0.)
        
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions =self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=["input", "chat_history"], 
            partial_variables={"format_instructions": format_instructions},
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=True,
                              output_key="booking_information")

    def __call__(self, query, chat_history):

        info = self.chain({"input": input, "chat_history": chat_history})
        return self.output_parser.parse(info["booking_information"])
    

class UserInfoExtractorTool(BaseTool):
    name = "user_information_extractor"
    description = "useful for when you need to extract the email, name and phone_number for the booking."

    booking_info_extractor = UserInfoExtractorChain()

    def _run(
        self, input: str, chat_history: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.booking_info_extractor(input, chat_history)

    async def _arun(
        self, input: str, chat_history: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")