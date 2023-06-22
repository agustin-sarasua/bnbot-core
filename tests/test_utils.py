from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chat_models import ChatOpenAI
from typing import List

# Follow these Steps before responding to the user new message:

# Step 1: Make sure the user provided user name and email.

# Step 2: If the user provided with this information, you thank him.

template ="""You are customer that wants to book an accomodation for the weekend \
in the city of "Mercedes" at the "Complejo Enrique Joaquin". \
Allways answer in Spanish.
You ask your requirements one at a time.

These are your requirements for the accomodation: {context}

Current conversation:
{chat_history}

You respond in a short, very conversational friendly style."""

chain_of_though_template = """You are customer that wants to book an accomodation for the weekend \
in the city of "Mercedes" at the "Complejo Enrique Joaquin". \
Allways answer in Spanish.
You ask your requirements one at a time.

These are your requirements for the accomodation: {context}

Follow these Steps before responding to the user new message:
{chain_of_though}

Current conversation:
{chat_history}

You respond in a short, very conversational friendly style.
"""

response_schemas = [
    ResponseSchema(name="text", description="The response to the user"),
]


class FakeCustomerChain:

    chain_of_though_steps: List[str] = None

    def __init__(self, chain_of_though_steps: List = None):
        llm = ChatOpenAI(temperature=0.)
        
        self.chain_of_though_steps = chain_of_though_steps
        input_variables = ["chat_history", "context"]
        if chain_of_though_steps is not None:
            template = chain_of_though_template
            input_variables.append("chain_of_though")

        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions =self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=input_variables, 
            partial_variables={"format_instructions": format_instructions},
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=True,
                              output_key="output")

    def __call__(self, chat_history, context: str =""):
        if self.chain_of_though_steps is not None:
            chain_of_though_input = ""
            for idx, step in enumerate(self.chain_of_though_steps):
                chain_of_though_input += "Step {idx}: {step} \n"
            info = self.chain({"chat_history": chat_history, "chain_of_though": chain_of_though_input, "context": context})
        else:
            info = self.chain({"chat_history": chat_history, "context": context})
        return self.output_parser.parse(info["user_info"])
    