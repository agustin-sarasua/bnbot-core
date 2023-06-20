from typing import Optional
from langchain.tools import BaseTool

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

template = """Given a list of available properties for rent in json format, \
your job is to summarize the information. You allways respond in Spanish.

Here is the information about the properties: 
{properties_available}

{format_instructions}"""

response_schemas = [
    ResponseSchema(name="properties_summary", description="Summary of properties that are available for the user to book."),
]

class PropertiesSummarizerChain:

    def __init__(self):

        llm = OpenAI(temperature=0.)

        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions =self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=["properties_available"],
            partial_variables={"format_instructions": format_instructions},
            template=template
        )
   
        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=True,
                              output_key="properties_summary")

    def __call__(self, properties_available):
        info = self.chain({"properties_available": properties_available})    
        return self.output_parser.parse(info["properties_summary"])
    

class PropertiesSummarizerTool(BaseTool):
    name = "properties_summarizer"
    description = "useful for when you need to summarize the information of a list of properties available for booking."

    summarizer = PropertiesSummarizerChain()

    def _run(
        self, properties_available: dict, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.summarizer(properties_available)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")