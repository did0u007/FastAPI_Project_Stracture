from .users import router as user_router
from .states import router as state_router


def routers_gen():
    yield user_router
    yield state_router
