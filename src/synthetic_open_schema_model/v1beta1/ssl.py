from enum import Enum
from typing import List, Optional

from pydantic import ConfigDict

from synthetic_open_schema_model.base import (
    BaseAssertion,
    Check,
    CheckSpec,
    DNSHostname,
)


class SslAssertionType(str, Enum):
    expirationTime = "expirationTime"
    certificateIssuer = "certificateIssuer"
    certificateSubject = "certificateSubject"


class SslAssertion(BaseAssertion):
    type: SslAssertionType


SslAssertionList = List[SslAssertion]


class SslCheckSpec(CheckSpec):
    model_config = ConfigDict(extra="forbid")
    hostname: DNSHostname
    port: Optional[int] = 443
    checks: SslAssertionList


class SslCheck(Check):
    model_config = ConfigDict(extra="forbid")

    spec: SslCheckSpec
