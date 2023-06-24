from app.task_resolver.task_model import StepResolver
from typing import List, Any
from datetime import datetime, timedelta


from typing import List, Any
from datetime import datetime, timedelta
from app.task_resolver.task_model import StepResolver
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

Here is the conversation: 
{chat_history}

{format_instructions}"""

response_schemas = [
    ResponseSchema(name="conversation_finished", type="bool", description="Wether the conversation between the user and the assistant came to an end."),
    ResponseSchema(name="text", description="Response to the user."),
]


class ExitTaskChain:

    def __init__(self):

        llm = OpenAI(temperature=0.)
        
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=["chat_history"], 
            partial_variables={"format_instructions": format_instructions},
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=chain_verbose,
                              output_key="result")

    def __call__(self, chat_history, current_task):

        info = self.chain({"chat_history": chat_history})
        return self.output_parser.parse(info["result"])


class ExitTaskResolver(StepResolver):

    exit_task_chain: ExitTaskChain = ExitTaskChain()

    def run(self, step_data: dict, messages: List[Any], previous_steps_data: List[Any]):
        chat_history = self.build_chat_history(messages)

        # current_task = step_data["current_task_name"]
        exit_result = self.exit_task_chain(chat_history, "")

        step_data["result"] = exit_result
        if ("conversation_finished" in exit_result and  
            exit_result["conversation_finished"] != "" and 
            exit_result["conversation_finished"] == True):
            # TODO what to respond
            return None
        
    def is_done(self, step_data: dict):
        # Force to execute this step every time.
        return (
            "result" in step_data and  
            
            "conversation_finished" in step_data["result"] != "" and 
            step_data["result"]["conversation_finished"] is not None
        )
            