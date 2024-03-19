"""
Error Handling
https://fastapi.tiangolo.com/tutorial/handling-errors/

NOTE: If you want to override the HTTPException handler,
use the starlette.exceptions one. Explained here:
https://fastapi.tiangolo.com/tutorial/handling-errors/#fastapis-httpexception-vs-starlettes-httpexception
"""

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/error_handling", tags=["Error Handling"])


@router.get("/items/{item_id}")
async def read_item(item_id: str) -> dict[str, str]:
    items = {"foo": "The Foo Wrestlers"}
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


# More examples in main.py
