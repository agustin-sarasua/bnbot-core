from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from ..tools.conversation import InfoExtractorTool, LocationInformationTool, PropertiesFilterTool, PropertiesSummarizerTool, UserInfoExtractorTool

tools = [
    InfoExtractorTool(), 
    # PropertiesFilterTool(), 
    # PropertiesSummarizerTool(), 
    # UserInfoExtractorTool(),
    # CreateBookingTool(return_direct=True)
]

system_message="""You are an Assistant that helps users book a house to stay at "Complejo Enrique Joaquin" located in Mercedes, Uruguay.
Users can only reserve one house at a time."""

llm = ChatOpenAI(temperature=0) # Also works well with Anthropic models

def get_booking_conversation_agent(conversation):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    for msg in conversation:
        if msg["role"] == "user":
            memory.chat_memory.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            memory.chat_memory.add_ai_message(msg["content"])

    return initialize_agent(tools, 
                            llm, 
                            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
                            verbose=True,
                            memory=memory,
                            agent_kwargs = {
                                "system_message":system_message,
                            })