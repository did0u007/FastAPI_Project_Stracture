from typing import Annotated, List
from unittest import skip
from urllib import request
from fastapi import Path, Query, Request
from api.core import Settings

from api.core.helper import raise_error


async def query_limit(request: Request):
    max_args = int(Settings().STATE_QUERY_LIMIT) | 0  # type: ignore # 25
    query = request.query_params.multi_items()
    print(query)
    if len(query) > max_args:
        raise_error(422, "Too many query params")


async def query(
    skip: Annotated[int, Query(ge=0, allow_inf_nan=False)] = 0,  # type: ignore
    limit: Annotated[int, Query(ge=0, le=50)] = 50,
):
    return {"skip": skip, "limit": limit}
