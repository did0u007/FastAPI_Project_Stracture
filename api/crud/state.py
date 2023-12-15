from api.schemas.state import StateRequest
from api.core.helper import raise_error, sublists
from sqlalchemy.orm import Session
from api.models import State
from sqlite3 import DatabaseError
from fastapi import status
from typing import List
from cache import AsyncTTL


######## Get State By ID ##############
@AsyncTTL(time_to_live=120, maxsize=120, skip_args=1)
async def db_get_state(db: Session, id):
    try:
        return db.get_one(State, id)
    except Exception as e:
        raise_error(status.HTTP_404_NOT_FOUND, f"State {id} Not Found")


######## Get All State ##############
@AsyncTTL(time_to_live=120, maxsize=120, skip_args=1)
async def db_get_all_states(db: Session):
    return db.query(State).all()


######## Create State ##############
async def db_create_states(db: Session, states: List[StateRequest]):  # type: ignore
    existing_state = await db_get_all_states(db)
    if existing_state:
        diff = sublists(
            [i.name for i in states], [i.name for i in existing_state]  # type: ignore
        )
        if diff:
            raise_error(
                status.HTTP_406_NOT_ACCEPTABLE,
                f"You Try To Dublicate An Existing Item {diff}",
            )

    try:
        objs = [State(name=state.name) for state in states]  # type: ignore
        db.add_all(objs)
        db.flush(objs)
        db.commit()
        return objs
    except DatabaseError as e:
        db.rollback()
        raise_error(502, str(e))


######## Drop States ##############
async def db_drop_states(db: Session, states: List[int]):
    try:
        dropped = db.query(State).filter(State.id.in_(states)).delete()
        db.commit()
        return dropped
    except Exception as e:
        db.rollback()
        raise_error(502, str(e))


######## Update States ##############
async def db_update_state(db: Session, state_id: int, new_name: str):
    try:
        old_state = await db_get_state(db, state_id)  # type: ignore
        old_state.name = new_name  # type: ignore
        db.commit()
        return old_state
    except Exception as e:
        db.rollback()
        raise_error(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
