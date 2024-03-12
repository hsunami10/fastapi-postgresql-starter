from enum import Enum
from typing import Literal, final


@final
class Environment(str, Enum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self) -> bool:
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self) -> bool:
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)


@final
class ApiVersionPrefixes:
    AUTH_API_V1_PREFIX: Literal["/api/v1/users"] = "/api/v1/users"
