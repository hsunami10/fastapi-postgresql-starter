from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class CoreModel(BaseModel):
    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()

    def to_json_string(self) -> str:
        return self.model_dump_json()

    def to_json(self) -> Any:
        """Return a dict which contains only JSON-serializable fields."""
        return jsonable_encoder(self.model_dump())
