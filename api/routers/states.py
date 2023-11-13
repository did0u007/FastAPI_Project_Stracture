from functools import cache
from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from api.core.helper import limit_args_dependency
from api.crud import state as st
from api.db.database import get_db

from api.schemas.state import StateRequest, StateResponse


router = APIRouter(prefix="/state", tags=["state"])


@router.get("/all")  # response_model=List[StateResponse]
@cache
async def get_all_states():
    pass


@router.get(
    "/create", tags=["admin"], response_model=List[StateResponse], dependencies=[limit_args_dependency()]  # type: ignore
)
async def create_state(
    state: Annotated[List[str], Query(max_length=20)],
    db: Session = Depends(get_db),
):
    return await st.create_state(db, state)  # type: ignore
