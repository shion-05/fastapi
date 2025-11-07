# user.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/user")
def get_users():
    return {"name": "yamada"}
