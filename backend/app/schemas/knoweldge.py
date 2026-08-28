from pydantic import BaseModel, Field
from typing import Optional


class BusinessKnowledge(BaseModel):
    business_name: Optional[str] = Field(default=None)
    business_type: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    services: Optional[list[str]] = Field(default=None)
    additional_information: Optional[str] = Field(default=None)
    is_confirmed: bool = False

class BusinessKnowledgeUpdate(BaseModel):
    business_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    business_type: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    services: Optional[list[str]] = None
    additional_information: Optional[str] = None