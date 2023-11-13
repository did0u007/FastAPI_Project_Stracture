from fastapi import Depends, HTTPException


def raise_error(statu_code: int, detail: str):
    raise HTTPException(status_code=statu_code, detail=detail)


def sublists(j, k):
    return list(set(j) & set(k))


def limit_args_dependency(max_args: int = 3):
    def inner(request):
        query_params = request.query_params
        if len(query_params) > max_args:
            raise HTTPException(status_code=422, detail="Too many query params")

        return query_params

    return inner
