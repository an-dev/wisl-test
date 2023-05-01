from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException


def raise_exception(status_code: int, detail: str) -> None:
    raise HTTPException(
        status_code=status_code,
        detail=jsonable_encoder(detail),
    )
