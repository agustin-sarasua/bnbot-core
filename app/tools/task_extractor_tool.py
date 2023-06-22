from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from langchain.chat_models import ChatOpenAI
from utils import chain_verbose
#from langchain.llms import OpenAI

template="""You are an Assistant that helps users.
Your task is to identify which action does the user want to do. You allways answer in Spanish.

Here is the list of possible actions:

MAKE_RESERVATION_TASK: the user wants to book an accomodation.
PROPERTIES_INFORMATION_TASK: the user needs information about the properties available.
RESERVATION_INFORMATION_TASK: the user wants information about an accomodation booked before.
OTHER: when None of the actions described above fits.

Here is the conversation: 
{chat_history}

{format_instructions}"""

response_schemas = [
    ResponseSchema(name="task_id", description="The task_id of the Task that the user wants to perform."),
    ResponseSchema(name="text", description="The response to the user."),
]


class TaskExtractorChain:

    def __init__(self):

        llm = ChatOpenAI(temperature=0.)
        
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions =self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=["chat_history"], 
            partial_variables={"format_instructions": format_instructions},
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=chain_verbose,
                              output_key="task_info")

    def __call__(self, chat_history):

        info = self.chain({"chat_history": chat_history})
        return self.output_parser.parse(info["task_info"])
    