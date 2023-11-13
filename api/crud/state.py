from os import name
from sqlite3 import DatabaseError
from api.core.helper import raise_error, sublists
from api.models import State
from sqlalchemy.orm import Session
from typing import List
from api.schemas.state import StateRequest


######## Create State ##############
async def create_state(db: Session, states: List[StateRequest]):  # type: ignore
    existing_state = db.query(State).all()
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
