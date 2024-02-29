from datetime import datetime, timezone
from typing import Annotated, Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, PlainSerializer


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


# Replaces Pydantic v1 json_encoders
# https://github.com/pydantic/pydantic/discussions/7199#discussioncomment-7798544
JSONDateTime = Annotated[
    datetime, PlainSerializer(func=convert_datetime_to_gmt, return_type=str)
]


class CoreModel(BaseModel):
    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()

    def to_json_string(self) -> str:
        return self.model_dump_json()

    def to_json(self) -> Any:
        """Return a dict which contains only JSON-serializable fields."""
        return jsonable_encoder(self.model_dump())
