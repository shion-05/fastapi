# item.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/item")
def get_item():
    return {"item": "Book"}
