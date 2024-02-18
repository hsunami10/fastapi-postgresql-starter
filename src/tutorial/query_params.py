"""
Query Parameters Tutorial
https://fastapi.tiangolo.com/tutorial/query-params/
"""
from typing import Annotated
from fastapi import APIRouter, Query, Path


router = APIRouter(prefix="/query_params", tags=["Query Parameters"])


# Query params with default values
@router.get("/default_values/")
async def read_item(offset: int = 0, limit: int = 10):
    items = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    return items[offset : offset + limit]


# Optional query params
@router.get("/optional_values/{item_id}")
async def read_item_short(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "this item has a long description!"})
    return item


# Required query params
@router.get("/required/")
async def read_user_item(required_q_param: str):
    item = {"item_id": 10, "required_q_param": required_q_param}
    return item


# Ellipses (...) are used to declare that a value is required
# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#required-with-ellipsis
@router.get("/ellipses/")
async def read_items(q: Annotated[str, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Allow multiple query params
@router.get("/multiple_params/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items
