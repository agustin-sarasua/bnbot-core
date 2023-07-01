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

template = """{context}

Respond ONLY with the next message from the Customer.
If the conversation if over you reply with an empty string, i.e: "".
Current conversation:
{chat_history}
Customer:
"""

# template ="""Given a conversation between a user and an assistant.
# What is the next interaction of the user?
# Always respond in spanish.

# These are your requirements for the accommodation: {context}

# Follow these Steps:

# Step 1: Make sure you provide information about check-in, check-out and number of people.

# Step 2: Choose from the available houses one that meets your requirements if there is one.

# Step 3: If you managed to choose a house, provide the information asked by the assistant to book the house.

# Step 4: If you finally booked a house, thank the assistant for its help.

# You respond in a short, very conversational friendly style.

# Here is the conversation:
# {chat_history}"""

chain_of_though_template = """You are customer that wants to book an accommodation for the weekend \
in the city of "Mercedes" at the "Complejo Enrique Joaquin". \
Allways answer in Spanish.
You ask your requirements one at a time.

These are your requirements for the accommodation: {context}

Follow these Steps before responding to the user new message:
{chain_of_though}

Current conversation:
{chat_history}
user:
"""

response_schemas = [
    ResponseSchema(name="text", description="The response to the user"),
]


class FakeCustomerChain:

    chain_of_though_steps: List[str] = None
    context: str =""

    def __init__(self, chain_of_though_steps: List = None, context: str =""):
        llm = ChatOpenAI(temperature=0.)
        
        self.context = context
        used_template = template

        self.chain_of_though_steps = chain_of_though_steps
        input_variables = ["chat_history", "context"]
        if chain_of_though_steps is not None:
            used_template = chain_of_though_template
            input_variables.append("chain_of_though")

        # self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        # format_instructions =self.output_parser.get_format_instructions()

        prompt_template = PromptTemplate(
            input_variables=input_variables, 
            # partial_variables={"format_instructions": format_instructions},
            template=used_template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=True,
                              output_key="output")

    def __call__(self, chat_history):
        if self.chain_of_though_steps is not None:
            chain_of_though_input = ""
            for idx, step in enumerate(self.chain_of_though_steps):
                chain_of_though_input += "Step {idx}: {step} \n"
            info = self.chain({"chat_history": chat_history, "chain_of_though": chain_of_though_input, "context": self.context})
        else:
            info = self.chain({"chat_history": chat_history, "context": self.context})
        # return self.output_parser.parse(info["output"])["text"]
        return info["output"]
    