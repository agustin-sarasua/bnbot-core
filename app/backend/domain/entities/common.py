from typing import List, Dict, Optional
from pydantic import BaseModel

class TokenData(BaseModel):
    sub: Optional[str] = None