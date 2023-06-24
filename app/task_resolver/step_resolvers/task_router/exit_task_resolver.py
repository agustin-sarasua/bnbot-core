from app.task_resolver.model import StepResolver
from typing import List, Any
from datetime import datetime, timedelta


from typing import List, Any
from datetime import datetime, timedelta
from app.task_resolver.model import StepResolver
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from langchain.chat_models import ChatOpenAI
from app.utils import chain_verbose
from langchain.llms import OpenAI

template="""Given a conversation between a user and an assistant about booking a house for short-term stay. \
Your job is to infer if the conversation if finished and if the user wants to end the current task he is doing.
The current task that the user wants to perform is: {current_task}

Here is the conversation: 
{chat_history}

{format_instructions}"""

response_schemas = [
    ResponseSchema(name="conversation_finished", description="Set True if the conversation between the user and the assistant came to an end. Otherwise set False."),
    ResponseSchema(name="leave_current_task", description="Set True if the user does not want to perform the current task he is performing. Otherwise set False."),
]


class ExitTaskChain:

    def __init__(self):

        llm = OpenAI(temperature=0.)
        
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=["chat_history", "current_task"], 
            partial_variables={"format_instructions": format_instructions},
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=chain_verbose,
                              output_key="result")

    def __call__(self, chat_history, current_task):

        info = self.chain({"chat_history": chat_history, "current_task": current_task})
        return self.output_parser.parse(info["result"])

class ExitTaskResolver(StepResolver):

    def __init__(self):
        pass

    def run(self, step_data: dict, messages: List[Any], previous_steps_data: List[Any]) -> str:
        pass
        
    def is_done(self, step_data: dict):
        return True