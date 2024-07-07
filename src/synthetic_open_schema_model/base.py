import re
from enum import Enum
from typing import Annotated, Any, Dict, List, Optional, Union

from croniter import croniter
from pydantic import BaseModel, ConfigDict, StringConstraints, model_validator

"""
CaseInsensitiveKey: A string that is case-insensitive and only contains alphanumeric characters and hyphens.
"""
CaseInsensitiveKey = Annotated[
    str,
    StringConstraints(
        pattern=re.compile(r"^[A-Za-z0-9\-]+$"), to_lower=True, min_length=1
    ),
]

Time = Annotated[
    str,
    StringConstraints(
        pattern=r"^[0-9]+(ns|ms|s|m|h|d|w|M|y)?$", to_lower=True, min_length=1
    ),
]


DNSHostname = Annotated[
    str,
    StringConstraints(
        pattern=re.compile(
            r"^(([a-zA-Z0-9]+|([a-zA-Z0-9]+-*[a-zA-Z0-9]+))\.)*[a-zA-Z0-9]+$"
        ),
        to_lower=True,
        min_length=1,
        max_length=253,
    ),
]


class Operator(str, Enum):
    contains = "contains"
    equals = "equals"
    greater_than = "greaterThan"
    less_than = "lessThan"
    not_contains = "notContains"
    not_equals = "notEquals"


class BaseAssertion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    # Make operator an enum of valid operators
    operator: Operator
    value: Union[int, str]


class Metadata(BaseModel):
    """Metadata for a resource."""

    name: CaseInsensitiveKey
    title: Optional[str] = None
    labels: Optional[Dict[str, str]] = {}


class Resource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    apiVersion: str
    kind: str
    metadata: Metadata


class Frequency(BaseModel):
    class errors:
        invalid_unit = "unit must be one of s, m, h, d, w, M, y"

    interval: int
    unit: str

    @model_validator(mode="before")
    def validate_values(cls, values: dict[str, Any]) -> dict[str, int]:

        interval: int = int(values["value"][:-1])
        unit = values["value"][-1]
        assert unit in [
            "s",
            "m",
            "h",
            "d",
            "w",
            "M",
            "y",
        ], cls.errors.invalid_unit

        return {"interval": interval, "unit": unit}


class Crontab(BaseModel):
    class errors:
        invalid_cron = "Invalid cron expression"

    cron: object

    @model_validator(mode="before")
    def validate_values(cls, values: dict[str, str]) -> dict[str, Any]:
        if isinstance(values, str):
            values = {"value": values}

        assert croniter.is_valid(values["value"]), cls.errors.invalid_cron

        return {"cron": croniter(values["value"])}


class CheckSpec(BaseModel):
    class errors:
        either_interval_or_cron = "Either interval or cron must be configured."
        only_one_interval_or_cron = "Only one of interval or cron can be configured."

    interval: Optional[Time] = None
    cron: Optional[Crontab] = None
    locations: Optional[List[str]] = []

    channels: Optional[List[dict[str, Any]]] = []

    timeout: Optional[Time] = "1s"
    retries: Optional[int] = 1

    @model_validator(mode="before")
    def check_either_interval_or_cron(cls, values: dict[str, str]) -> dict[str, Any]:
        interval = values.get("interval", None)

        cron = values.get("cron", None)

        assert not all([interval, cron]), cls.errors.only_one_interval_or_cron
        assert any([interval, cron]), cls.errors.either_interval_or_cron

        return values


class Check(Resource):
    pass
