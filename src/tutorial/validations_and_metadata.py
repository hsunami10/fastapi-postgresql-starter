from typing import Annotated

from fastapi import APIRouter, Body, Path, Query
from pydantic import BaseModel, Field, HttpUrl

router = APIRouter(
    prefix="/validations_and_metadata", tags=["Additional Validations and Metadata"]
)


"""
Additional validations and metadata

FastAPI functions (not comprehensive):
- Path()
- Query()
- Header()
- Cookie()
- Body()
- Form()
- File()

Pydantic functions (not comprehensive):
- Field()

Metadata for OpenAPI docs
• title (str)
• description (str)
• deprecated (bool) - show if deprecated or not
• include_in_schema (bool) - show/hide in OpenAPI docs
• examples (list[var_type]) - a list of examples (use examples over example)

General validations
• default (var_type) - the default value if None is provided (only use for Pydantic)
• for FastAPI functions, use var_name Annotated[...] = default_value
• https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#alternative-old-query-as-the-default-value

String validations
• alias (str) - an alias for the parameter / body
• min_length (int) - minimum length of string
• max_length (int) - maximum length of string
• pattern (str) - validates if there's a regex pattern match

Integer validations
• ge (>=) - greater than or equal to
• le (<=) - less than or equal to
• gt (>) - greater than
• lt (<) - less than
"""


class MetaItem(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])
    url: HttpUrl | None = Field(default=None)

    # Add additional data to OpenAPI's generated JSON schema
    # https://docs.pydantic.dev/latest/api/config/
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@router.get("/{item_id}")
async def read_item(
    item_id: Annotated[
        int,
        Path(
            title="Path int param",
            description="Path param to search with item id",
            ge=1,
        ),
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
            include_in_schema=True,
        ),
    ] = None,
):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    return item


# Examples in the JSON schema
@router.post("/extra_json_schema_data")
async def create_item(item: MetaItem):
    return item.model_dump()


# Examples in the path operation
@router.put("/open_api_examples/{item_id}")
async def update_item(
    # *,
    item_id: int,
    item: Annotated[
        MetaItem,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
