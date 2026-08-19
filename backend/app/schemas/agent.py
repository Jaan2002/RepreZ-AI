from pydantic import BaseModel,Field
from typing import Annotated
class AgentCreate(BaseModel):
    business_name: Annotated[str,Field(...,description="Mention your Business name",min_length=2,max_length=100)]

class AgentUpdate(BaseModel):
    business_name: Annotated[str,Field(...,description="Update Business name",min_length=2,max_length=100)]

class AgentResponse(BaseModel):
    id: int
    business_name:str
    status:str

class OnboardingChatRequest(BaseModel):
    message: str = Field(...,min_length=1,description="Message from the business owner")


class OnboardingChatResponse(BaseModel):
    reply: str