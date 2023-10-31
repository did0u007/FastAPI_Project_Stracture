from functools import lru_cache
from fastapi import APIRouter


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
@lru_cache()
def get_user():
    return {"test": "passed"}


@router.get("/{id}")
@lru_cache()
def get_user_by_id(id: int):
    print("on")
    return {"test": f"passed {id}"}
