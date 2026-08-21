from fastapi import FastAPI,APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.database import get_db
from app.models.agent import Agent
from app.models.business_knowledge import BusinessKnowledge
from app.models.customer_message import CustomerMessage
from app.models.customer_session import CustomerSession
from app.schemas.customer_session import CustomerSessionResponse

from app.ai.client import customer_chat


router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)

@router.post("/{agent_id}/chat")
def customer_chat_endpoint(agent_id: int,message: str,session_id: int,db: Session = Depends(get_db)):

    #Find agent
    agent = db.get(Agent,agent_id)

    if agent is None:
        raise HTTPException(status_code=404,detail="Agent not found")
    # Find session
    session = db.get(CustomerSession, session_id)

    if session is None:
        raise HTTPException(status_code=404,detail="Session not found")

    # Make sure session belongs to this agent
    if session.agent_id != agent_id:
        raise HTTPException(status_code=400,detail="Session does not belong to this agent")

     # Get business knowledge
    knowledge = db.scalars(
        select(BusinessKnowledge)
        .where(BusinessKnowledge.agent_id == agent_id)
    ).first()

    if knowledge is None:
        raise HTTPException(status_code=404,detail="Business Knowledge not found")

    #Make sure onboarding is confirmed
    if not knowledge.is_confirmed:
        raise HTTPException(status_code=400,detail="Business onboarding is not confirmed yet")

    # Get previous customer conversation
    previous_messages = db.scalars(
            select(CustomerMessage)
            .where(CustomerMessage.session_id == session_id)
            .order_by(CustomerMessage.created_at)
    ).all()

    print("========== SESSION DEBUG ==========")
    print("Agent ID:", agent_id)
    print("Session ID:", session_id)
    print("Messages found:", len(previous_messages))

    for msg in previous_messages:
        print(msg.id, msg.session_id, msg.role, msg.content)

    print("===================================")

    history = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in previous_messages
    ]

    # Get AI response
    reply = customer_chat(
            knowledge=knowledge,
            message=message,
            history=history
    )

    # Save customer message
    user_message = CustomerMessage(
            agent_id=agent_id,
            session_id=session_id,
            role="user",
            content=message
    )
    
    # Save AI response
    assistant_message = CustomerMessage(
            agent_id=agent_id,
            session_id=session_id,
            role="assistant",
            content=reply
    )

    db.add(user_message)
    db.add(assistant_message)
    db.commit()

    return {"reply": reply}

@router.post("/agents/{agent_id}/session",response_model=CustomerSessionResponse)
def create_customer_session(agent_id:int,db: Session = Depends(get_db)):
    agent = db.get(Agent,agent_id)

    if agent is None:
        raise HTTPException(status_code=404,detail="Agent not found")

    #Create new customer session
    session = CustomerSession(agent_id=agent_id)

    db.add(session)
    db.commit()
    db.refresh(session)

    return session

@router.get("/agents/{agent_id}/session/{session_id}/messages")
def get_session_messages(
    agent_id: int,
    session_id: int,
    db: Session = Depends(get_db)
):
    # Find agent
    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    # Find session
    session = db.get(CustomerSession, session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # Make sure session belongs to this agent
    if session.agent_id != agent_id:
        raise HTTPException(
            status_code=400,
            detail="Session does not belong to this agent"
        )

    # Get messages for this session
    messages = db.scalars(
        select(CustomerMessage)
        .where(CustomerMessage.session_id == session_id)
        .order_by(CustomerMessage.created_at)
    ).all()

    return {
        "session_id": session_id,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }

@router.get("/agents/{agent_id}/sessions")
def get_customer_sessions(
    agent_id: int,
    db: Session = Depends(get_db)
):
    # Find agent
    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    sessions = db.scalars(
        select(CustomerSession)
        .where(CustomerSession.agent_id == agent_id)
        .order_by(CustomerSession.updated_at.desc())
    ).all()

    result = []

    for session in sessions:

        messages = db.scalars(
            select(CustomerMessage)
            .where(CustomerMessage.session_id == session.id)
            .order_by(CustomerMessage.created_at.desc())
        ).all()

        last_message = messages[0] if messages else None

        result.append({
            "id": session.id,
            "agent_id": session.agent_id,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "message_count": len(messages),
            "last_message": last_message.content if last_message else None,
            "last_message_at": (
                last_message.created_at
                if last_message else None
            )
        })

    return {
        "agent_id": agent_id,
        "sessions": result
    }