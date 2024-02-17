from typing import Annotated
from enum import Enum
from fastapi import APIRouter, Query, Path
from pydantic import BaseModel


router = APIRouter()

"""
Path Parameters Tutorial
https://fastapi.tiangolo.com/tutorial/path-params/
"""


# With similar paths, such as /users/me and /users/{user_id},
# order matters - whatever endpoint is declared first is prioritized.
# https://fastapi.tiangolo.com/tutorial/path-params/#order-matters
@router.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


# Path parameters with types example
@router.get("/users/{user_id}")
async def read_user(user_id: str) -> dict[str, str]:
    return {"user_id": user_id}


# Predefined path param values
# https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values

# Enum definition
class CompanyName(str, Enum):
    apple = "apple"
    microsoft = "microsoft"
    google = "google"


@router.get("/company/{company_name}")
async def get_model(company_name: CompanyName):
    if company_name is CompanyName.apple:
        return {"model_name": company_name, "message": "apple vision pro?"}

    if company_name.value == CompanyName.microsoft.value:
        return {"model_name": company_name, "message": "hi this is microsoft"}

    return {"model_name": company_name, "message": "\"hey google\""}


# Path params that are paths themselves
# https://fastapi.tiangolo.com/tutorial/path-params/#path-parameters-containing-paths
@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}




"""
Query Parameters Tutorial
https://fastapi.tiangolo.com/tutorial/query-params/
Don't include them in routing string
"""


# Query params with default values
@router.get("/items/default_values/")
async def read_item(offset: int = 0, limit: int = 10):
    items = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    return items[offset : offset + limit]


# Optional query params
@router.get("/items/optional/{item_id}")
async def read_item_short(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "this item has a long description!"})
    return item


# Required query params
@router.get("/items/required/{item_id}")
async def read_user_item(item_id: str, required_q_param: str):
    item = {"item_id": item_id, "required_q_param": required_q_param}
    return item


# Ellipses (...) are used to declare that a value is required
# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#required-with-ellipsis
@router.get("/items/ellipse/")
async def read_items(q: Annotated[str, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Allow multiple query params
@router.get("/items/multiple_q_params/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items


"""
Additional validations and metadata for Query and Path functions

Generic validations and metadata
    • alias (str) - an alias for the query parameter
    • title (str) - title metadata for OpenAPI docs
    • description (str) - description metadata for OpenAPI docs
    • deprecated (bool) - show if deprecated or not (for OpenAPI docs)
    • include_in_schema (bool) - show/hide query param in OpenAPI docs

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


@router.get("/items/metadata_and_more_validations/{item-id}")
async def read_items(
    item_id: Annotated[
        int,
        Path(
            alias="item-id",
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


"""
Request Body (Pydantic)
https://fastapi.tiangolo.com/tutorial/body/
"""


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


fake_items_db: list[dict] = []


@router.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    fake_items_db.append(item_dict)
    return item_dict


@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    # ** is like a spread operator in JavaScript
    return {"item_id": item_id, **item.dict()}
