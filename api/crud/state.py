from sqlite3 import DatabaseError
from api.core.helper import raise_error, sublists
from api.models import State
from sqlalchemy.orm import Session
from typing import List
from api.schemas.state import StateRequest
from cache import AsyncTTL


######## Get State By ID ##############
@AsyncTTL(time_to_live=120, maxsize=120, skip_args=1)
async def db_get_state(db: Session, id):
    try:
        print("###########################")
        return db.get_one(State, id)
    except Exception as e:
        raise_error(404, f"State {id} Not Found")


######## Get All State ##############
@AsyncTTL(time_to_live=120, maxsize=120, skip_args=1)
async def db_get_all_states(db: Session):
    print("###########################")
    return db.query(State).all()


# TODO: check if is there a states in the db
######## Create State ##############
async def db_create_states(db: Session, states: List[StateRequest]):  # type: ignore
    existing_state = await db_get_all_states(db)
    diff = sublists(
        [i.capitalize() for i in states], [i.name for i in existing_state]  # type: ignore
    )
    if len(diff):
        raise_error(409, f"You Try To Dublicate An Existing Item {diff}")

    try:
        objs = [State(name=state.capitalize()) for state in states]  # type: ignore
        # db.bulk_save_objects(objs)
        db.add_all(objs)
        db.flush(objs)
        # print([obj.id for obj in objs])
        db.commit()
        return objs
    except DatabaseError as e:
        db.rollback()
        raise_error(502, str(e))
