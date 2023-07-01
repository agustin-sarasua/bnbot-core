# from langchain.agents import AgentType
# from langchain.chat_models import ChatOpenAI
# from langchain.llms import OpenAI
# from langchain.agents import initialize_agent
# from ..tools import PropertiesFilterTool, PropertiesSummarizerTool
# from langchain.prompts import MessagesPlaceholder
# from langchain.memory import ConversationBufferMemory

# PREFIX = """You are an assistant that helps customer pick the best accommodation to stay. You have access to the following tools:"""

# # tools = [PropertiesFilterTool(), PropertiesSummarizerTool()]

# llm = ChatOpenAI(temperature=0) # Also works well with Anthropic models

# # def get_house_selection_agent(conversation):
# #     chat_history = MessagesPlaceholder(variable_name="chat_history")
# #     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# #     for msg in conversation:
# #         if msg["role"] == "user":
# #             memory.chat_memory.add_user_message(msg["content"])
# #         elif msg["role"] == "assistant":
# #             memory.chat_memory.add_ai_message(msg["content"])


# #     house_selection_agent = initialize_agent(
# #         tools,
# #         llm, 
# #         agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
# #         verbose=True, 
# #         memory=memory, 
# #         agent_kwargs = { 
# #             "memory_prompts": [chat_history], 
# #             "input_variables": ["input", 
# #                     # "checkin_date", 
# #                     # "checkout_date", 
# #                     # "num_guests", 
# #                     # "num_nights", 
# #                     "agent_scratchpad", 
# #                     "chat_history"],
# #             "prefix": PREFIX
# #         })
    
# #     return house_selection_agent


# llm = ChatOpenAI(temperature=0) # Also works well with Anthropic models

# def get_house_selection_agent(conversation, properties_available):
#     system_message=f"""You are an Assistant that helps users pick a house from the available houses based on its preferences. 
# Your task is only helping them pick a house for booking, any other task must not be handled by you.

# Here is the list of properties available:
# {properties_available}"""
    
#     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

#     for msg in conversation:
#         if msg["role"] == "user":
#             memory.chat_memory.add_user_message(msg["content"])
#         elif msg["role"] == "assistant":
#             memory.chat_memory.add_ai_message(msg["content"])

#     return initialize_agent([], 
#                             llm, 
#                             agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
#                             verbose=True,
#                             memory=memory,
#                             agent_kwargs = {
#                                 "system_message":system_message,
#                             })