from typing import Optional
from langchain.tools import BaseTool
from datetime import datetime

from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from app.utils import chain_verbose
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

template = """Given a conversation between a user and an assistant about booking a house for short-term stay. \
Your job is to extract the check-in date, checkout-date and number of nights \
from the query.
If the year is not specified in the query, assume it is after today, \
same year or at most next year if the month is before current month.
Today is {time}.

Here is the conversation: 
{chat_history}

{format_instructions}"""

response_schemas = [
    ResponseSchema(name="checkin_date", description="reservation Check-In date formated as YYYY-MM-DD i.e: 2023-09-24. If not present, set an empty string."),
    ResponseSchema(name="checkout_date", description="reservation Check-Out date formated as YYYY-MM-DD i.e: 2023-09-24. If not present, set an empty string."),
    ResponseSchema(name="num_nights", description="Number of nights the customer is staying. If not present, set 0."),
    ResponseSchema(name="num_guests", description="Number of guests staying in the house. If not present, set 0."),
]


class InfoExtractorChain:

    def __init__(self):

        llm = OpenAI(temperature=0.)
        
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions =self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=["time", "chat_history"], 
            partial_variables={"format_instructions": format_instructions},
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=chain_verbose,
                              output_key="booking_information")

    def __call__(self, chat_history):

        today = datetime.today()
        formatted_date = today.strftime("%A, %d %B %Y")
        info = self.chain({"time":formatted_date, "chat_history": chat_history})
        return self.output_parser.parse(info["booking_information"])