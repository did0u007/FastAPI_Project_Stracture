from enum import Enum


class userType(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SELLEER = "seller"
