from api.core.middlewares import query, query_limit
from api.schemas.city import CityRequest, CityResponse
from sqlalchemy.orm import Session
from api.crud import city as ct
from fastapi import APIRouter, Body, Depends
from api.db import getDB
from typing import Annotated, List
from anyio import Path

router = APIRouter(prefix="/city", tags=["city"], dependencies=[Depends(query_limit)])


######## Get All Cities ##############
@router.get("/all", response_model=List[CityResponse])
async def get_all_cities(
    db: Annotated[Session, Depends(getDB)],
    q=Depends(query),
):
    return await ct.db_get_all_cities(db, q)  # type: ignore


######## Get All Cities ##############
@router.get("/{city_id}", response_model=CityResponse)
async def get_city(
    db: Annotated[Session, Depends(getDB)],
    city_id: Annotated[int, Path],
):
    return await ct.db_get_city(db, city_id)


######## Drope Cities ##############
@router.delete("/delete", tags=["admin"])
async def delete_cities(cities: List[int], db: Session = Depends(getDB)):
    return await ct.db_drop_cities(db, cities)


######## Update City ##############
@router.put("/{city_id}/update", tags=["admin"])
async def update_city(
    city_id: Annotated[int, Path],
    city: Annotated[CityRequest, Body],
    db: Session = Depends(getDB),
):
    return await ct.db_update_city(db, city_id, city)


##############################################################################
#                                                                            #
##################### Sub Router For State-City Relationship #################
sub_router = APIRouter(tags=["city"])  # ../state/{id}/city/...


################### Add cities to state ################
@sub_router.post(path="/add", response_model=List[CityResponse])
async def add_sities_to_state(
    cities: Annotated[List[CityRequest], Body],
    state_id: Annotated[int, Path()],
    db: Session = Depends(getDB),
):
    return await ct.db_create_city(db, state_id, cities)


################### Get All State's Cities ################
@sub_router.get("/all", response_model=List[CityResponse])
async def get_all_cities_of_state(
    db: Annotated[Session, Depends(getDB)],
    state_id: Annotated[int, Path],
):
    return await ct.db_get_all_cities_of_state(db, state_id)
