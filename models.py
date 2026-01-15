from typing import List, Dict, Any

from pydantic import BaseModel

class ThreatOut(BaseModel):
    name: str
    location: str
    danger_rate: int
