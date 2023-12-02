from api.db import getDB
from api.models import State, City


# TODO cache it ..
async def valid_state(id) -> bool | State:
    if id is None:
        return False
    db = getDB().__next__()
    state = db.query(State).filter(State.id == id).first()
    return False if state is None else state


# TODO cache it ..
async def valid_city(id) -> bool | City:
    if id is None:
        return False
    db = getDB().__next__()
    city = state = db.query(City).filter(City.id == id).first()
    return False if city is None else city


async def valid_state_city(state_id, city_id) -> bool:
    if (state := valid_state(state_id)) and (city := valid_city(city_id)):
        return city in state.cities  # type: ignore
    return False
