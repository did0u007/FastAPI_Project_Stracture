from fastapi import HTTPException


def raise_error(statu_code: int, detail: str):
    raise HTTPException(status_code=statu_code, detail=detail)


def sublists(j, k):
    return list(set(j) & set(k))


def integrety_error_hundler(error) -> str:
    return eval(str(error))[1]
