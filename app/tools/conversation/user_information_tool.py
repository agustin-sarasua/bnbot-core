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
{input}"""


class UserInfoExtractorChain:

    def __init__(self):

        llm = OpenAI(temperature=0.)

        prompt_template = PromptTemplate(
            input_variables=["input"],
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=True,
                              output_key="booking_information")

    def __call__(self, query):

        info = self.chain({"input": input})
        return info["booking_information"]
    

class UserInfoExtractorTool(BaseTool):
    name = "user_information_extractor"
    description = "useful for when you need to extract the email, name and phone_number for the booking."

    booking_info_extractor = UserInfoExtractorChain()

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.booking_info_extractor(query)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")