from datetime import datetime, timezone
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, field_serializer, model_validator


class CoreModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # dt: datetime

    @field_serializer("dt")
    def convert_datetime_to_gmt(cls, dt: datetime) -> str:
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt.strftime("%Y-%m-%dT%H:%M:%S%z")

    @model_validator(mode="before")
    @classmethod
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(v, datetime)
        }

        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs: dict[str, Any]) -> Any:
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)
