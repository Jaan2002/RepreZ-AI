from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_NAME, APP_VERSION
from app.api.health import router as health_router
from app.api.agent import router as agent_router
from app.api.customer import router as customer_router

from app.database.database import engine
from app.database.base import Base
from app.models.agent import Agent


# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

#CORS
app = FastAPI()
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


app.include_router(health_router)
app.include_router(agent_router)
app.include_router(customer_router)

@app.get("/")
def home():
    return {
        "message": "Reprez AI backend is running..."
    }


