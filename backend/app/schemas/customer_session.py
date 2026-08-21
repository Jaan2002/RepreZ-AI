from datetime import datetime

from pydantic import BaseModel


class CustomerSessionResponse(BaseModel):
    id: int
    agent_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True