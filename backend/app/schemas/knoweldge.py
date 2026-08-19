from pydantic import BaseModel, Field
from typing import Optional


class BusinessKnowledge(BaseModel):
    business_name: Optional[str] = Field(default=None)
    business_type: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    services: Optional[list[str]] = Field(default=None)
    additional_information: Optional[str] = Field(default=None)