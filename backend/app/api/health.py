from fastapi import APIRouter

router = APIRouter(
    prefix="/health",  #all routes start with /health
    tags=["Health"]
)


@router.get("/")
def health_check():
    return {
        "status": "ok"
    }