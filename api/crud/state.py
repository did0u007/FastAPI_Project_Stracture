from sqlite3 import DatabaseError
from api.models import State
from sqlalchemy.orm import Session

from api.schemas.state import StateRequest


class StateDublicationException(Exception):
    def __init__(self, *args: object, state: State) -> None:
        super().__init__(*args)
        self.items = {"id": state.id, "name": state.name}
        self.msg = "The state you are trying to create is already taken"
        self.type = "DublicationException"

    def __repr__(self) -> str:
        return f"'items': {self.items}, 'msg': {self.msg}, 'type': {self.type}"  # type: ignore


######## Create State ##############
async def create_state(db: Session, state: StateRequest):
    existing_state = db.query(State).filter(State.name == state.name).first()
    if existing_state:
        raise StateDublicationException(state)  # type: ignore

    try:
        db.add(state)
        db.commit()
        db.refresh(state)
        return {"status": "OK"}
    except DatabaseError as e:
        db.rollback()
        return {"msg": str(e)}
