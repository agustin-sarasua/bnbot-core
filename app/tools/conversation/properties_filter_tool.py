from typing import Optional
from langchain.tools import BaseTool
from datetime import datetime

from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

import requests
from langchain.tools import StructuredTool


from typing import Optional, Type

import aiohttp
import requests

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, BaseSettings, Field

from datetime import datetime, timedelta
# from app.utils import Cache, read_json_from_s3
from ...utils import Cache, read_json_from_s3


class PropertiesFilterTool(BaseTool, BaseSettings):
    """My custom Properties filter tool."""

    name = "properties_filter"
    description = "useful for when you need to filter the properties based on the check-in date, check-out date and number of guests. Do not use this tool if any of this information is missing."

    def _run(
        self, 
        query: str, 
        # available_properties: dict,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        
        pass

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
