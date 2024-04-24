from fastapi import APIRouter

router = APIRouter(prefix="/")


@router.get("/")
async def index():
    return {"hello": "world"}
