from fastapi import APIRouter,Depends,HTTPException
from app.schemas.agent import AgentCreate,AgentResponse,AgentUpdate,OnboardingChatRequest,OnboardingChatResponse
from sqlalchemy.orm import Session

from sqlalchemy  import select

from app.database.database import get_db
from app.models.agent import Agent
from app.ai.client import onboarding_chat, extract_business_knowledge, is_confirmation
from app.models.onboarding import OnboardingMessage
from app.models.business_knowledge import BusinessKnowledge

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

     # Get previous conversation from database
     previous_messages = db.scalars(
         select(OnboardingMessage).where(OnboardingMessage.agent_id == agent_id).order_by(OnboardingMessage.created_at)
     ).all()

    
     # Convert database messages to OpenAI format
     history = [
         {
            "role": message.role,
            "content": message.content 
         }
         for message in previous_messages
     ]

     # Get AI response
     reply = onboarding_chat(
         agent_id=agent_id,
         message=request.message,
         history=history
     )

     # Save user's message
     user_message = OnboardingMessage(
         agent_id= agent_id,
         role="user",
         content=request.message
     )
      # Save AI response
     assistant_message = OnboardingMessage(
         agent_id=agent_id,
         role="assistant",
         content=reply
     )
     db.add(user_message)
     db.add(assistant_message)
     db.commit()

     # Check if business knowledge already exists
     knowledge = db.scalars(
         select(BusinessKnowledge)
         .where(BusinessKnowledge.agent_id == agent_id)
     ).first()

     # Simple confirmation detection
     confirmation_words = {
             "yes",
                 "correct",
                 "looks good",
                 "that's correct",
                 "that is correct",
                 "confirmed",
                 "confirm",
                 "everything is correct",
                 "everything looks correct",
                 "everything is fine",
                 "all correct",
                 "all good"
     }

     user_text = request.message.strip().lower()

     is_confirmation = any(
         phrase in user_text for phrase in confirmation_words
     )

     if knowledge and confirmation_words:
         knowledge.is_confirmed = True

         db.commit()

         return{
             "reply" :" Perfect! Your business information has been confirmed. Your AI Representative is now ready."
         }
     

     # Extract business information from owner's message
     extracted = extract_business_knowledge(request.message)

    #  # Build the complete conversation
    #  conversation = "\n".join(
    #     f"{message.role}: {message.content}"
    #     for message in previous_messages
    #  )

    #  # Include the current user message
    #  conversation += f"\nuser: {request.message}"

    #  # Extract business information from the complete conversation
    #  extracted = extract_business_knowledge(conversation)

    #  # Check if knowledge already exists for this agent
    #  knowledge = db.scalars(
    #      select(BusinessKnowledge)
    #      .where(BusinessKnowledge.agent_id == agent_id)
    #  ).first()

     if knowledge is None:
         # Create first knowledge record
         knowledge = BusinessKnowledge(
             agent_id = agent_id,
             business_name = extracted.business_name,
             business_type = extracted.business_type,
             location = extracted.location,
             description = extracted.description,
             services = extracted.services,
             additional_information = extracted.additional_information,
             is_confirmation=False
         )

         db.add(knowledge)
     else:
         # Update only information that was actually provided
         if extracted.business_name is not None:
             knowledge.business_name =extracted.business_name

         if extracted.business_type is not None:
             knowledge.business_type = extracted.business_type

         if extracted.location is not None:
             knowledge.location = extracted.location
         
         if extracted.description is not None:
             knowledge.description = extracted.description
         
         if extracted.services is not None:
             existing_services= knowledge.services or []

             knowledge.services = list(set(existing_services + extracted.services))
         
         if extracted.additional_information is not None:
             knowledge.additional_information = extracted.additional_information

         # New information means confirmation must be done again
         knowledge.is_confirmed = True
        
    #  if is_confirmation(request.message):
    #      knowledge.is_confirmed = True
    #      agent.status = "ready"

     db.commit()
         
     return{ "reply": reply}


