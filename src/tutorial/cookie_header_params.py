from typing import Annotated

from fastapi import APIRouter, Cookie, Header

router = APIRouter(
    prefix="/cookie_header_params", tags=["Cookie and Header Parameters"]
)


@router.get("/items/")
async def read_items(
    ads_id: Annotated[str | None, Cookie()] = None
) -> dict[str, str | None]:
    return {"ads_id": ads_id}


# NOTE: FastAPI automatically converts underscores to proper header format (with dashes)
# https://fastapi.tiangolo.com/tutorial/header-params/#automatic-conversion
@router.get("/items/")
async def read_items2(
    user_agent: Annotated[str | None, Header()] = None
) -> dict[str, str | None]:
    return {"User-Agent": user_agent}


@router.get("/items/")
async def read_items3(
    x_token: Annotated[list[str] | None, Header()] = None
) -> dict[str, list[str] | None]:
    return {"X-Token values": x_token}
