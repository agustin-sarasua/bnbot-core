from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


# template = """Given a conversation between a User and Assistant about booking a house to stay \
# You have to decide which ACTION to take next.
# The possible actions for you to choose from are:

# load_properties_information: Respond with this ACTION when: \
# The user has provided all the information needed to load the properties:
# - checkin date
# - checkout date or number of nights
# - number of guests.
# IMPORTANT: You should NOT return this ACTION if this information hasn't been provided by the user.

# pre_booking: Respond with this ACTION when: \
# The user was shown by the Assistant with the Summary of the Booking that the user is about to make \
# and the user has agreed to book the house.

# other: Respond with this ACTION when: \
# None of the above actions are suitable.

# Here is the conversation: 
# {conversation}

# {format_instructions}"""

template = """Given a input message from an assistant to a user and a set of actions, \
your job is to decide what is the assistant next action.

Here are the available actions:

load_properties_information: Respond with this action when \
the assistant is going to load information about available properties.

pre_booking: Respond with this action when \
the assistant is going to book the reservation for the user.

wait_response: Respond with this action when \
te assistant asks the user to provide more information about the booking \
including: check-in date, check-out date, number of guests, number of nights, name, email or house to book.

other: Respond with this action when \
none of the above actions are suitable.

Here is the message: 
{message}

{format_instructions}"""

response_schemas = [
    ResponseSchema(name="action", description="Name of the next action to take.")
]


# class AssistantResponseRouter:

#     def __init__(self):

#         llm = OpenAI(temperature=0.)
        
#         self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
#         format_instructions =self.output_parser.get_format_instructions()


#         prompt_template = PromptTemplate(
#             input_variables=["conversation"], 
#             partial_variables={"format_instructions": format_instructions},
#             template=template
#         )

#         self.chain = LLMChain(llm=llm, 
#                               prompt=prompt_template, 
#                               verbose=True,
#                               output_key="router_output")

#     def __call__(self, conversation: str) -> str:
#         info = self.chain({"conversation": conversation})
#         return self.output_parser.parse(info["router_output"])

class AssistantResponseRouter:

    def __init__(self):

        llm = OpenAI(temperature=0.)
        
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions =self.output_parser.get_format_instructions()


        prompt_template = PromptTemplate(
            input_variables=["message"], 
            partial_variables={"format_instructions": format_instructions},
            template=template
        )

        self.chain = LLMChain(llm=llm, 
                              prompt=prompt_template, 
                              verbose=True,
                              output_key="router_output")

    def __call__(self, message: str) -> str:
        info = self.chain({"message": message})
        return self.output_parser.parse(info["router_output"])