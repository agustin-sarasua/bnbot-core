from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from langchain.chat_models import ChatOpenAI
from app.utils import chain_verbose

template="""You are an Assistant that helps users choose a house based on its preferences. 
Your task is only to help users pick a house for booking and answer any question about the properties, any other task must not be handled by you.

Follow these Steps before responding to the user new message:

Step 1: Show the user a summary of the available properties including a brief description, amenities and the price per night for each property. 
Here is the list of available properties:
{properties_info}

Step 2: If the user makes any question about the properties after showing the summary, answer it based on the available properties information. 

Step 3: Make sure that the user select one property for making the booking. 
When there are no properties available, you must ask the user if he wants to look for different dates. 

Step 4: If the user does not want any of the available properties, \
you apologize and tell the user that you will notify him if you have something new available in the future.

Here is the conversation: 
{chat_history}

{format_instructions}"""

response_schemas = [
    ResponseSchema(name="property_id", description="The property_id of the property that the user explicitly choose after looking at the options. If the user has not explicitly selected one, set an empty string i.e ''"),
    ResponseSchema(name="text", description="The response to the user"),
]


class HousePickedExtractorChain:

    def __init__(self):

        llm = ChatOpenAI(temperature=0.)
        
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions =self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=["chat_history", "properties_info"], 
            partial_variables={"format_instructions": format_instructions},
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=chain_verbose,
                              output_key="house_picked")

    def __call__(self, chat_history, properties_info):

        info = self.chain({"properties_info": properties_info, "chat_history": chat_history})
        return self.output_parser.parse(info["house_picked"])
    