"""
HTTP Responses with Pydantic Models
https://fastapi.tiangolo.com/tutorial/response-model/
"""
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/response_pydantic_models", tags=["HTTP Responses with Pydantic Models"])


class ResponseItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


# Level 0: returning the same input model
@router.post("/same_input_output/single/")
async def create_item(item: ResponseItem) -> ResponseItem:
    return item


@router.get("/same_input_output/multiple/")
async def read_items() -> list[ResponseItem]:
    return [
        ResponseItem(name="Portal Gun", price=42.0),
        ResponseItem(name="Plumbus", price=32.0),
    ]


# Level 1 - returning a dict with "any" return type
# response_model - automatically converts the returned value to a Pydantic model
@router.get("/any_with_response_model/", response_model=list[ResponseItem])
async def read_items() -> any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


# Another example of response_model, with 2 Pydantic models
class UserIn(BaseModel):
    username: str
    password: str # do NOT do this in production!
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


# Level 2 - input + output Pydantic models
# returning a Pydantic model, with "any" return type
@router.post("/in_out_models/", response_model=UserOut)
async def create_user(user: UserIn) -> any:
    # Having a function return type as UserOut would cause typing complaints
    # because those are different classes - this is why response_model is needed
    return user


# Level 3 - using class inheritance
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    # Includes all of BaseUser's fields
    password: str


@router.post("/inheritance/")
async def create_user(user: UserIn) -> BaseUser:
    return user
