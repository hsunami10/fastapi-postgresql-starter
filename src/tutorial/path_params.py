"""
Path Parameters Tutorial
https://fastapi.tiangolo.com/tutorial/path-params/
"""
from enum import Enum
from fastapi import APIRouter


router = APIRouter(prefix="/path_params", tags=["Path Parameters"])


# With similar paths, such as /users/me and /users/{user_id},
# order matters - whatever endpoint is declared first is prioritized.
# https://fastapi.tiangolo.com/tutorial/path-params/#order-matters
@router.get("/similar_paths/me")
async def read_user_me():
    return {"user_id": "the current user"}


# Path parameters with types example
@router.get("/similar_paths/{user_id}")
async def read_user(user_id: str) -> dict[str, str]:
    return {"user_id": user_id}


# Predefined path param values
# https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values

# Enum definition
class CompanyName(str, Enum):
    apple = "apple"
    microsoft = "microsoft"
    google = "google"


@router.get("/enums/{company_name}")
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