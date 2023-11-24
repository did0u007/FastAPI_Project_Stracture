from api.schemas.city import CityRequest, CityResponse
from api.core.helper import raise_error, sublists
from sqlalchemy.orm import Session
from api.models import City, State
from fastapi import status
from typing import List
from cache import AsyncTTL


######## Get City By ID ##############
@AsyncTTL(time_to_live=120, maxsize=120, skip_args=1)
async def db_get_state(db: Session, id):
    try:
        return db.get_one(City, id)
    except Exception as e:
        raise_error(status.HTTP_404_NOT_FOUND, f"State {id} Not Found")


########## Get All Cities ##########
@AsyncTTL(time_to_live=30, skip_args=1)
async def db_get_all_cities(db: Session, q: dict[str, int]):
    try:
        cities = (
            db.query(City).order_by(City.name).offset(q["skip"]).limit(q["limit"]).all()
        )
        return cities
    except Exception as e:
        db.rollback()
        raise_error(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


########## Get All Cities Of As State ##########
@AsyncTTL(time_to_live=30, skip_args=1)
async def db_get_all_cities_of_state(
    db: Session,
    state_id: int,
) -> List[CityResponse] | None:
    try:
        state = db.get(State, state_id)
        return state.cities  # type:ignore
    except Exception as e:
        db.rollback()
        raise_error(status.HTTP_400_BAD_REQUEST, f"Invalid state with ID {state_id}")


########## Create City ##########
async def db_create_city(
    db: Session,
    state_id: int,
    cities_list: list[CityRequest],
):
    db_cities = await db_get_all_cities_of_state(db, state_id)
    if db_cities:
        exists_cities = sublists(
            [c.name for c in db_cities],
            [c.name.capitalize() for c in cities_list],
        )
        if exists_cities:
            raise_error(
                status.HTTP_406_NOT_ACCEPTABLE,
                f"You Try To Dublicate An Existing Item {exists_cities}",
            )
    try:
        cities_objs = [
            City(name=i.name.capitalize(), state_id=state_id) for i in cities_list
        ]
        db.add_all(cities_objs)
        db.flush(cities_objs)
        db.commit()
        return cities_objs
    except Exception as e:
        raise_error(status.HTTP_501_NOT_IMPLEMENTED, str(e))


async def db_drop_cities(db: Session, cities: List[int]):
    try:
        dropped = db.query(City).filter(State.id.in_(cities)).delete()
        db.commit()
        return dropped
    except Exception as e:
        db.rollback()
        raise_error(502, str(e))


@AsyncTTL(time_to_live=20, skip_args=1)
async def db_get_city(db, city_id):
    try:
        return db.get_one(City, city_id)
    except:
        raise_error(status.HTTP_404_NOT_FOUND, f"City ID {city_id} not found")


async def db_update_city(db: Session, city_id: int, new_city: CityRequest):
    city = await db_get_city(db, city_id)

    if city.name == new_city.name.capitalize() and city.state_id == new_city.state_id:
        raise_error(
            status.HTTP_304_NOT_MODIFIED,
            f"Same data entred to update city ID {city_id}",
        )

    city.name = new_city.name.capitalize() if new_city.name else city.name
    city.state_id = new_city.state_id if new_city.state_id else city.state_id
    db.flush([city])
    db.commit()
    return city
