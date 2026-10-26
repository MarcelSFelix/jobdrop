from typing import Literal
from pydantic import BaseModel, ConfigDict


class JobAd(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    title: str
    languages: list[str]
    frameworks: list[str]
    remote: Literal["onsite", "hybrid", "remote", "unknown"]
    seniority: Literal["junior", "mid", "senior", "unknown"]
    
