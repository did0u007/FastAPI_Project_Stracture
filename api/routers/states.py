from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, Query
from api.core.middlewares import query_limit

from api.crud import state as st
from api.db.database import get_db
from api.schemas.state import StateRequest, StateResponse

router = APIRouter(prefix="/state", tags=["state"])


######## Get All States ##############
@router.get(
    "/all", response_model=List[StateResponse]
)  # response_model=List[StateResponse]
async def get_all_states(db: Session = Depends(get_db)):
    return await st.db_get_all_states(db)


######## Create State ##############
@router.get(
    "/create", tags=["admin"], response_model=List[StateResponse], dependencies=[Depends(query_limit)]  # type: ignore
)
async def create_state(
    state: Annotated[List[str], Query(max_length=20)],  # type: ignore
    db: Session = Depends(get_db),
):
    return await st.db_create_states(db, state)  # type: ignore


######## Get State By ID ##############
@router.get("/{id}", response_model=StateResponse)  # , response_model=StateResponse
async def get_state(
    id: Annotated[int, Path(ge=1, title="State ID", allow_inf_nan=False)],
    db: Session = Depends(get_db),
):
    return await st.db_get_state(db, id)
