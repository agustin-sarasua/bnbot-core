# from langchain.agents import AgentType
# from langchain.chat_models import ChatOpenAI
# from langchain.llms import OpenAI
# from langchain.prompts import MessagesPlaceholder
# from langchain.memory import ConversationBufferMemory
# from langchain.agents import initialize_agent
# from ..tools import InfoExtractorTool, CreateBookingTool, LocationInformationTool, PropertiesFilterTool, PropertiesSummarizerTool, UserInfoExtractorTool

# tools = [
#     InfoExtractorTool(), 
#     PropertiesFilterTool(), 
#     PropertiesSummarizerTool(), 
#     UserInfoExtractorTool(),
#     CreateBookingTool(return_direct=True)
# ]

# llm = ChatOpenAI(temperature=0) # Also works well with Anthropic models

# # "Respond to the human as helpfully and accurately as possible. You have access to the following tools:"

# PREFIX = """You are an assistant to help the user book houses for short-term stay.
# All the information for the booking should be gathered from the conversation.
# You have access to the following tools:"""

# PREFIX =f"""
# You are an Assistant that helps users book a house to stay at "Complejo Enrique Joaquin" located in Mercedes, Uruguay.
# Users can only reserve one house at a time.
# You have access to the following tools:"""

# def get_create_booking_agent(conversation):
#     chat_history = MessagesPlaceholder(variable_name="chat_history")
#     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

#     for msg in conversation:
#         if msg["role"] == "user":
#             memory.chat_memory.add_user_message(msg["content"])
#         elif msg["role"] == "assistant":
#             memory.chat_memory.add_ai_message(msg["content"])

#     return initialize_agent(tools, 
#                             llm, 
#                             agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
#                             verbose=True,
#                             memory=memory,
#                             agent_kwargs = {
#                                     "memory_prompts": [chat_history],
#                                     "input_variables": ["input", "agent_scratchpad", "chat_history"],
#                                     # "prefix": PREFIX
#                                 })