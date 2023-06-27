from app.task_resolver.engine import StepResolver, Message

from typing import List, Any
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

# from langchain.chat_models import ChatOpenAI
from app.utils import chain_verbose
from langchain.llms import OpenAI

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

template="""Given a conversation between a user and an assistant about booking a house for short-term stay. \
Your job is to decide which is the next step to take.

Here are the steps for you to choose from:
{steps}

Current conversation: 
{chat_history}

{format_instructions}"""

response_schemas = [
    ResponseSchema(name="step", description="The name of the next step to take.")
]

class PostProcessRouterChain:

    def __init__(self):

        llm = OpenAI(temperature=0.)
        
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions =self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=["chat_history", "steps"], 
            partial_variables={"format_instructions": format_instructions},
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=chain_verbose,
                              output_key="result")

    def run(self, chat_history: str, steps: str):
        info = self.chain({"chat_history": chat_history, "steps": steps})
        return self.output_parser.parse(info["result"])
    


class PostProcessRouterResolver(StepResolver):

    router_chain: PostProcessRouterChain

    def __init__(self, steps):
        self.steps_str = self._build_steps_str(steps)
        self.router_chain = PostProcessRouterChain()

    def _build_steps_str(self, steps):
        result = ""
        for step in steps:
            result += f"{step['name']}: {step['description']}\n"
        return result[:-1]
    
    def run(self, messages: List[Message], previous_steps_data: dict=None):
        chat_history = self.build_chat_history(messages)
        return self.router_chain.run(chat_history, self.steps_str)
        
    def is_done(self):
        return True
            