from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AgentCreate(BaseModel):
    business_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the business",
    )


class AgentUpdate(BaseModel):
    business_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Updated business name",
    )


class AgentResponse(BaseModel):
    id: int
    business_name: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OnboardingChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class OnboardingChatResponse(BaseModel):
    reply: str