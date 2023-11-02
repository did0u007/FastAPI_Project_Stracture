from functools import lru_cache
from fastapi import APIRouter
from api.schemas import UserResponse, UserRequest


router = APIRouter(prefix="/user", tags=["user"])


############ GET user #####################
# TODO: return Auth user details.
@router.get("/")
@lru_cache()
def get_user():
    return {"test": "passed"}


############## Create User #####################
@router.post("/", response_model=UserResponse)
def create_user(
    user: UserRequest,
):
    return user


####################### ADMIN PRIVLEGE ONLY #################
# TODO: Add check for admin only middleware here.
@router.get("/{id}", tags=["admin"])
@lru_cache()
def get_user_by_id(id: int):
    print("on")
    return {"test": f"passed {id}"}
