from functools import cache
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from api.crud import state as st
from api.db.database import get_db

from api.schemas.state import StateRequest, StateResponse


router = APIRouter(prefix="/state", tags=["state"])


@router.get("/all")  # response_model=List[StateResponse]
@cache
async def get_all_states():
    pass


@router.post("/create", tags=["admin"])
async def create_state(state: StateRequest, db: Session = Depends(get_db)):
    return state  # type: ignore
