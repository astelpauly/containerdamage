from fastapi import APIRouter
from app.services import say_hi

router = APIRouter()

@router.get("/hello")
def hello():
    return {"message":say_hi()}