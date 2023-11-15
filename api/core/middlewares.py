from typing import Annotated, List
from fastapi import Query, Request
from api.core import Settings

from api.core.helper import raise_error


async def query_limit(state: Annotated[List[str], Query(max_length=20)]):
    max_args = int(Settings().STATE_QUERY_LIMIT) | 0  # type: ignore
    if not max_args:
        return
    if len(state) > max_args:
        raise_error(422, "Too many query params")
    return
