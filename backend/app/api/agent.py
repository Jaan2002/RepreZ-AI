import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.client import onboarding_chat, extract_business_knowledge
from app.database.database import get_db
from app.models.agent import Agent
from app.models.business_profile import BusinessProfile
from app.models.knowledge_entry import KnowledgeEntry
from app.models.knowledge_source import KnowledgeSource
from app.models.onboarding import OnboardingMessage
from app.schemas.agent import (
    AgentCreate,
    AgentResponse,
    AgentUpdate,
    OnboardingChatRequest,
    OnboardingChatResponse,
)

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("/", response_model=list[AgentResponse])
def get_agents(db: Session = Depends(get_db)):
    result = db.scalars(
        select(Agent).order_by(Agent.created_at.desc())
    ).all()

    return result


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    return agent


@router.post("/", response_model=AgentResponse, status_code=201)
def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
):
    business_name = agent_data.business_name.strip()

    if not business_name:
        raise HTTPException(
            status_code=400,
            detail="Business name cannot be empty",
        )

    new_agent = Agent(
        business_name=business_name,
        status="learning",
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent


@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db),
):
    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    business_name = agent_data.business_name.strip()

    if not business_name:
        raise HTTPException(
            status_code=400,
            detail="Business name cannot be empty",
        )

    agent.business_name = business_name

    db.commit()
    db.refresh(agent)

    return agent


@router.delete("/{agent_id}")
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    db.delete(agent)
    db.commit()

    return {
        "message": "Agent deleted successfully",
        "agent_id": agent_id,
    }


@router.get("/{agent_id}/knowledge")
def get_agent_knowledge(
    agent_id: int,
    db: Session = Depends(get_db),
):
    """
    Return the structured knowledge currently stored
    for an AI Representative.
    """

    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    profile = db.scalars(
        select(BusinessProfile).where(
            BusinessProfile.agent_id == agent_id
        )
    ).first()

    entries = db.scalars(
        select(KnowledgeEntry)
        .where(KnowledgeEntry.agent_id == agent_id)
        .order_by(
            KnowledgeEntry.category,
            KnowledgeEntry.created_at,
        )
    ).all()

    return {
        "agent": {
            "id": agent.id,
            "business_name": agent.business_name,
            "status": agent.status,
            "created_at": agent.created_at,
        },
        "profile": (
            {
                "id": profile.id,
                "business_name": profile.business_name,
                "business_type": profile.business_type,
                "description": profile.description,
                "location": profile.location,
                "phone": profile.phone,
                "email": profile.email,
                "website": profile.website,
                "timezone": profile.timezone,
            }
            if profile
            else None
        ),
        "entries": [
            {
                "id": entry.id,
                "category": entry.category,
                "title": entry.title,
                "content": entry.content,
                "metadata": entry.extra_data,
                "source_id": entry.source_id,
                "created_at": entry.created_at,
                "updated_at": entry.updated_at,
            }
            for entry in entries
        ],
        "total_entries": len(entries),
    }


@router.post(
    "/{agent_id}/onboarding/chat",
    response_model=OnboardingChatResponse,
)
def onboarding_chat_endpoint(
    agent_id: int,
    request: OnboardingChatRequest,
    db: Session = Depends(get_db),
):
    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    message_text = request.message.strip()

    if not message_text:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty",
        )

    previous_messages = db.scalars(
        select(OnboardingMessage)
        .where(OnboardingMessage.agent_id == agent_id)
        .order_by(OnboardingMessage.created_at)
    ).all()

    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in previous_messages
    ]

    try:
        reply = onboarding_chat(
            agent_id=agent_id,
            business_name=agent.business_name,
            message=message_text,
            history=history,
        )

    except Exception as exc:
        print("========== ONBOARDING AI ERROR ==========")
        print(exc)
        print("=========================================")

        raise HTTPException(
            status_code=502,
            detail="The AI onboarding service is temporarily unavailable.",
        )

    user_message = OnboardingMessage(
        agent_id=agent_id,
        role="user",
        content=message_text,
    )

    db.add(user_message)
    db.flush()

    assistant_message = OnboardingMessage(
        agent_id=agent_id,
        role="assistant",
        content=reply,
    )

    db.add(assistant_message)

    owner_messages = [
        message.content
        for message in previous_messages
        if message.role == "user"
    ]

    owner_messages.append(message_text)

    conversation = "\n".join(
        f"owner: {message}"
        for message in owner_messages
    )

    try:
        extracted = extract_business_knowledge(
            conversation
        )

    except Exception as exc:
        print("========== KNOWLEDGE EXTRACTION FAILED ==========")
        print(exc)
        print("=================================================")

        db.commit()

        return {
            "reply": reply,
        }

    profile = db.scalars(
        select(BusinessProfile).where(
            BusinessProfile.agent_id == agent_id
        )
    ).first()

    if profile is None:
        profile = BusinessProfile(
            agent_id=agent_id,
            business_name=agent.business_name,
        )

        db.add(profile)

    if extracted.profile.business_type is not None:
        profile.business_type = (
            extracted.profile.business_type
        )

    if extracted.profile.location is not None:
        profile.location = extracted.profile.location

    if extracted.profile.description is not None:
        profile.description = (
            extracted.profile.description
        )

    source = None

    if extracted.knowledge:
        source = KnowledgeSource(
            agent_id=agent_id,
            source_type="onboarding_chat",
            reference=f"onboarding_message:{user_message.id}",
        )

        db.add(source)
        db.flush()

    for extracted_entry in extracted.knowledge:
        normalized_category, normalized_title = (
                normalize_knowledge_key(
                    extracted_entry.category,
                    extracted_entry.title,
                )
            )
        existing_entries = db.scalars(
                select(KnowledgeEntry)
                .where(
                    KnowledgeEntry.agent_id == agent_id,
                    KnowledgeEntry.category == normalized_category,
                )
            ).all()
        existing_entry = None
        for candidate in existing_entries:
                candidate_category, candidate_title = (
                    normalize_knowledge_key(
                        candidate.category,
                        candidate.title,
                    )
                )
        
                if candidate_title == normalized_title:
                    existing_entry = candidate
                    break
        if existing_entry is None:
        
                knowledge_entry = KnowledgeEntry(
                    agent_id=agent_id,
                    source_id=(
                        source.id
                        if source
                        else None
                    ),
                    category=normalized_category,
                    title=(
                        extracted_entry.title.strip()
                        if extracted_entry.title
                        else None
                    ),
                    content=extracted_entry.content.strip(),
                    extra_data=extracted_entry.metadata,
                )
        
                db.add(knowledge_entry)

        else:
        
                existing_entry.category = normalized_category
        
                existing_entry.title = (
                    extracted_entry.title.strip()
                    if extracted_entry.title
                    else existing_entry.title
                )
        
                existing_entry.content = (
                    extracted_entry.content.strip()
                )
        
                existing_entry.extra_data = (
                    extracted_entry.metadata
                )
        
                if source is not None:
                    existing_entry.source_id = source.id   

    agent.status = "learning"

    db.commit()

    return {
        "reply": reply,
    }

def normalize_knowledge_key(category: str, title: str | None) -> tuple[str, str]:
    """
    Convert equivalent knowledge categories/titles into
    one canonical key.
    """

    category = (category or "").strip().lower()
    title = (title or "").strip().lower()

    category_aliases = {
        "hours": "opening_hours",
        "operating_hours": "opening_hours",
        "business_hours": "opening_hours",

        "order": "ordering",
        "order_methods": "ordering",
        "ordering_methods": "ordering",

        "payments": "payment",
        "payment_method": "payment",
        "payment_methods": "payment",

        "deliveries": "delivery",

        "bookings": "reservation",
        "booking": "reservation",
        "reservations": "reservation",

        "prices": "pricing",
        "product_prices": "pricing",
    }

    category = category_aliases.get(category, category)

    title_aliases = {
        "opening hours": "opening hours",
        "operating hours": "opening hours",
        "business hours": "opening hours",

        "order methods": "ordering methods",
        "ordering methods": "ordering methods",
        "ordering": "ordering methods",

        "payment methods": "payment methods",
        "payment method": "payment methods",

        "delivery": "delivery",
        "deliveries": "delivery",

        "reservation": "reservations",
        "reservations": "reservations",

        "prices": "pricing",
        "product prices": "pricing",
        "pricing": "pricing",
    }

    title = title_aliases.get(title, title)

    title = re.sub(r"\s+", " ", title)

    return category, title