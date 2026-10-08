from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_NAME, APP_VERSION
from app.api.health import router as health_router
from app.api.agent import router as agent_router
from app.api.customer import router as customer_router

from app.database.database import engine
from app.database.base import Base

# Import models so SQLAlchemy knows about all tables
from app.models.agent import Agent
from app.models.business_profile import BusinessProfile
from app.models.business_knowledge import BusinessKnowledge
from app.models.knowledge_entry import KnowledgeEntry
from app.models.knowledge_source import KnowledgeSource
from app.models.onboarding import OnboardingMessage
from app.models.customer_session import CustomerSession
from app.models.customer_message import CustomerMessage


# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

app.include_router(health_router)
app.include_router(agent_router)
app.include_router(customer_router)


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Reprez AI backend is running...",
        "version": APP_VERSION,
    }