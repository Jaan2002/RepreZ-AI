from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import APP_NAME, APP_VERSION
from app.api.agent import router as agent_router

from app.database.database import engine
from app.database.base import Base
from app.models.agent import Agent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.include_router(health_router)
app.include_router(agent_router)

@app.get("/")
def home():
    return {
        "message": "Reprez AI backend is running..."
    }


