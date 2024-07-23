from enum import Enum
from typing import List, Optional

from pydantic import ConfigDict, HttpUrl, field_serializer

from ..base import BaseAssertion, Check, CheckSpec

Headers = dict[str, str]


class HttpAssertionType(str, Enum):
    duration = "duration"
    size = "size"
    statusCode = "statusCode"
    body = "body"
    header = "header"


class HttpAssertion(BaseAssertion):
    type: HttpAssertionType


HttpAssertionList = List[HttpAssertion]


class HttpCheckSpec(CheckSpec):
    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    method: Optional[str] = "GET"
    headers: Optional[Headers] = {}
    checks: HttpAssertionList

    @field_serializer("url")
    def serialize_url(self, url: HttpUrl) -> str:
        return str(url)


class HttpCheck(Check):
    model_config = ConfigDict(extra="forbid")

    spec: HttpCheckSpec
