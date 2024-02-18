from typing import Annotated
from enum import Enum
from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel, Field, HttpUrl


router = APIRouter(prefix="/validations_and_metadata", tags=["Additional Validations and Metadata"])


"""
Additional validations and metadata for Query, Path, Body, Field functions

Generic validations and metadata
    • alias (str) - an alias for the parameter / body
    • title (str) - title metadata for OpenAPI docs
    • description (str) - description metadata for OpenAPI docs
    • deprecated (bool) - show if deprecated or not (for OpenAPI docs)
    • include_in_schema (bool) - show/hide in OpenAPI docs

String validations
    • min_length (int) - minimum length of string
    • max_length (int) - maximum length of string
    • pattern (str) - validates if there's a regex pattern match

Integer validations
    • ge (>=) - greater than or equal to
    • le (<=) - less than or equal to
    • gt (>) - greater than
    • lt (<) - less than
"""


@router.get("/{item_id}")
async def read_item(
    item_id: Annotated[
        int,
        Path(
            title="Path int param",
            description="Path param to search with item id",
            ge=1
        )
    ],
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="fixedquery",
            deprecated=True,
            include_in_schema=True
        ),
    ] = None,
):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    return item
