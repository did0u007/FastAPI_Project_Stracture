from .users import router as user_router
from .states import router as state_router
from .files import router as file_router
from .cities import router as city_router


def routers_gen():
    yield user_router
    yield state_router
    yield city_router
    yield file_router
