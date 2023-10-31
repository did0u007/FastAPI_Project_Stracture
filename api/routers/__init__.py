from .users import router as user_router


def routers_gen():
    yield user_router
