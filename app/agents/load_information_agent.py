# from langchain.agents import AgentType
# from langchain.chat_models import ChatOpenAI
# from langchain.llms import OpenAI
# from langchain.agents import initialize_agent
# from ..tools import InfoExtractorTool, PropertiesFilterTool, PropertiesSummarizerTool

# tools = [InfoExtractorTool(), PropertiesFilterTool(), PropertiesSummarizerTool(return_direct=True)]

# llm = ChatOpenAI(temperature=0) # Also works well with Anthropic models
# load_information_agent = initialize_agent(tools, 
#                                llm, 
#                                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
#                                verbose=True)