from api.core.middlewares import query_limit
from api.routers.cities import sub_router
from api.schemas.state import StateRequest, StateResponse
from sqlalchemy.orm import Session
from api.crud import state as st
from fastapi import APIRouter, Body, Depends, Path
from typing import Annotated, List
from api.db import getDB

router = APIRouter(prefix="/state", tags=["state"])


######## Get All States ##############
@router.get(
    "/all", response_model=List[StateResponse]
)  # response_model=List[StateResponse]
async def get_all_states(db: Session = Depends(getDB)):
    return await st.db_get_all_states(db)


######## Create States ##############
@router.post(
    path="/create",
    tags=["admin"],
    response_model=List[StateResponse],
    dependencies=[Depends(query_limit)],  # type: ignore
    status_code=201,
)
async def create_state(
    states: Annotated[List[StateRequest], Body],  # type: ignore
    db: Session = Depends(getDB),
):
    return await st.db_create_states(db, states)  # type: ignore


######## Drope States ##############
@router.delete("/delete", tags=["admin"])
async def delete_states(states: List[int], db: Session = Depends(getDB)):
    return await st.db_drop_states(db, states)


######## Get State By ID ##############
@router.get("/{id}", response_model=StateResponse)
async def get_state(
    id: Annotated[int, Path(ge=1, title="State ID", allow_inf_nan=False)],
    db: Session = Depends(getDB),
):
    return await st.db_get_state(db, id)  # type: ignore


######## Update State   ##############
@router.put("/{id}", response_model=StateResponse)
async def update_state(
    id: Annotated[int, Path(ge=1, allow_inf_nan=False)],
    new_name: Annotated[StateRequest, Body],
    db: Session = Depends(getDB),
):
    return await st.db_update_state(db, id, new_name.name)  # type: ignore


router.include_router(sub_router, prefix="/{state_id}/city")
