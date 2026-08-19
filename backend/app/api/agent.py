from fastapi import APIRouter,Depends,HTTPException
from app.schemas.agent import AgentCreate,AgentResponse,AgentUpdate,OnboardingChatRequest,OnboardingChatResponse
from sqlalchemy.orm import Session

from sqlalchemy  import select

from app.database.database import get_db
from app.models.agent import Agent
from app.ai.client import onboarding_chat

router = APIRouter(
    prefix='/agents',
    tags=['Agents']
)

@router.get("/",response_model=list[AgentResponse])
def get_agents(db:Session=Depends(get_db)):
    result=db.scalars(select(Agent)).all()

    return result

@router.get("/{agent_id}",response_model=AgentResponse)
def get_agent(agent_id:int,db: Session=Depends(get_db)):
    agent= db.get(Agent,agent_id)

    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent

@router.post('/',response_model=AgentResponse)
def create_agent(agent:AgentCreate,db: Session= Depends(get_db)):

    new_agent= Agent(
        business_name=agent.business_name
    )
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent

@router.put("/{agent_id}",response_model=AgentResponse)
def update_agent(agent_id:int,agent_data:AgentUpdate,db: Session= Depends(get_db)):
    agent= db.get(Agent,agent_id)

    if agent is None:
        raise HTTPException(status_code=404,detail="Agent not Found")

    agent.business_name=agent_data.business_name
    db.commit()
    db.refresh(agent)

    return agent

@router.delete("/{agent_id}")
def delete_agent(agent_id:int,db: Session=Depends(get_db)):
    agent= db.get(Agent,agent_id)

    if agent is None:
            raise HTTPException(status_code=404,detail="Agent not Found")

    db.delete(agent)
    db.commit()

    return {
         "message":"Agent deleted successfully",
         "agent_id":agent_id
    }

@router.post("/{agent_id}/onboarding/chat",response_model=OnboardingChatResponse)
def onboarding_chat_endpoint(agent_id:int,request:OnboardingChatRequest,db: Session=Depends(get_db)):
     agent = db.get(Agent,agent_id)
     if agent is None:
        raise HTTPException(status_code=404,detail="Agent not found")

     reply = onboarding_chat(
         agent_id=agent_id,
         message=request.message
     )

     return{ "reply": reply}