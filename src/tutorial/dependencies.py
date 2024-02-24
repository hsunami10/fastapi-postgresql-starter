"""
Dependencies + Dependency Injection
https://fastapi.tiangolo.com/tutorial/dependencies/

Dependencies should be callable - function, class, etc.
Use keyword: Depends()

FastAPI under the hood:
- calls your dependency in Depends() with the correct params
- gets the result from your function/class
- assigns that result to the parameter in your path operation function

Annotated[type1, Depends(callable)]
type1 should match the return type/output of calling callable()
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, HTTPException

router = APIRouter(prefix="/dependencies", tags=["Dependencies"])


# Using Classes as dependencies
# (better than functions for typing + auto-completion)
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


# Type Aliasing
CommonQueryDep = Annotated[CommonQueryParams, Depends(CommonQueryParams)]
# can omit the 2nd reference if it's a CLASS: Annotated[CommonQueryParams, Depends()]


@router.get("/users/")
async def read_users(commons: CommonQueryDep) -> dict[str, Any]:
    return commons.__dict__


@router.get("/items/")
async def read_items(commons: CommonQueryDep) -> dict[str, Any]:
    return commons.__dict__


async def verify_token(x_token: Annotated[str, Header()]) -> None:
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]) -> str:
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# Use dependencies= in path operation decorators
# if you don't want a return value
@router.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items2() -> list[dict[str, str]]:
    return [{"item": "Foo"}, {"item": "Bar"}]


# Global dependencies

# everywhere
# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

# per-path
# router = APIRouter(prefix="/dependencies", dependencies=[Depends(verify_token)])
