"""
Request Body (Pydantic Models)
https://fastapi.tiangolo.com/tutorial/body/
"""
from typing import Annotated
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field, HttpUrl


router = APIRouter(prefix="/request_body", tags=["Request Body"])


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, title="Item Description", max_length=300)
    price: float = Field(gt=0, description="The price of an item, must be greater than zero.")
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class SalesPost(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class User(BaseModel):
    username: str
    full_name: str | None = None


fake_items_db: list[dict] = []


@router.post("/single")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    fake_items_db.append(item_dict)
    return item_dict


@router.put("/multiple_keys/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


@router.post("/list/")
async def create_multiple_images(images: list[Image]):
    return images


@router.put("/spread/{item_id}")
async def update_item(item_id: int, item: Item):
    # ** is like a spread operator in JavaScript
    return {"item_id": item_id, **item.model_dump()}


# Using singular values (not dicts) in request body
@router.put("/scalar_value/{item_id}")
async def update_item(
    item_id: int, item: Item, importance: Annotated[int, Body(gt=0)]
):
    results = {"item_id": item_id, "item": item, "importance": importance}
    return results


# Instead of {name: ..., description: ...}, embed would make it
# {item: {name: ..., description: ...}}
@router.put("/embed/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


# Allow JSON with any key-value pairs
@router.post("/arbitrary_dicts/")
async def create_index_weights(weights: dict[int, float]):
    return weights
