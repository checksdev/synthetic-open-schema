# type: ignore
from typing import Union

import pytest
from pydantic import BaseModel
from pydantic_core import ValidationError

from synthetic_open_schema_model.base import (
    CaseInsensitiveKey,
    CheckSpec,
    Crontab,
    DNSHostname,
    Frequency,
    Metadata,
    Resource,
    Time,
)


def test_no_api_version_fails() -> None:
    with pytest.raises(ValidationError):
        Resource(kind="test", metadata=Metadata(name="test", labels={}))


def test_no_kind_fails() -> None:
    with pytest.raises(ValidationError):
        Resource(
            apiVersion="checks.dev/v1beta1", metadata=Metadata(name="test", labels={})
        )


def test_no_metadata_fails() -> None:
    with pytest.raises(ValidationError):
        Resource(apiVersion="checks.dev/v1beta1", kind="test")


def test_valid_resource() -> None:
    resource = Resource(
        apiVersion="checks.dev/v1beta1",
        kind="test",
        metadata=Metadata(name="test", labels={}),
    )
    assert resource.apiVersion == "checks.dev/v1beta1"
    assert resource.kind == "test"
    assert resource.metadata.name == "test"
    assert resource.metadata.labels == {}


def test_metadata_labels_must_be_dict() -> None:
    with pytest.raises(ValidationError):
        Resource(
            apiVersion="checks.dev/v1beta1",
            kind="test",
            metadata=Metadata(name="test", labels="not a dict"),
        )


def test_metadata_name_must_be_str() -> None:
    with pytest.raises(ValidationError):
        Resource(
            apiVersion="checks.dev/v1beta1",
            kind="test",
            metadata=Metadata(name=1, labels={}),
        )


def test_interval_unit_must_be_valid() -> None:
    with pytest.raises(ValidationError):
        Frequency(value="1x")


@pytest.mark.parametrize(
    "unit",
    [
        "ns",
        "ms",
        "s",
        "m",
        "h",
        "d",
        "w",
        "M",
        "y",
    ],
)
def test_time_valid(unit: str) -> None:
    class MyModel(BaseModel):
        interval: Time

    MyModel(interval=f"1{unit}")
    MyModel(interval=f"10{unit}")


@pytest.mark.parametrize(
    "value, valid",
    [
        ("valid-key", True),
        ("ANOTHER-KEY", True),
        ("123-key", True),
        ("valid-key-with-hyphens", True),
        ("", False),  # Empty string, violates min_length
        ("with space", False),  # Contains space, not allowed
        ("with unserscore", False),  # Contains underscore, not allowed
        ("special-char!", False),  # Contains special character, not allowed
        ("UPPERCASE", True),  # Converted to lowercase
        ("lowercase", True),
        ("MiXeD-CaSe", True),  # Converted to lowercase
    ],
)
def test_case_insensitive_key(value: str, valid: bool) -> None:
    class MyModel(BaseModel):
        key: CaseInsensitiveKey

    if valid:
        MyModel(key=value)
    else:
        with pytest.raises(ValidationError):
            MyModel(key=value)


@pytest.mark.parametrize(
    "interval, cron, error",
    [
        (None, None, CheckSpec.errors.either_interval_or_cron),
        ("1s", "* * * * *", CheckSpec.errors.only_one_interval_or_cron),
        # ("1x", None, Frequency.errors.invalid_unit),
        (None, "* * *", Crontab.errors.invalid_cron),
    ],
)
def test_resource_spec_interval_cron_fails(
    interval: Union[str, None], cron: Union[Crontab, None], error: str
) -> None:
    with pytest.raises(ValidationError) as err:
        CheckSpec(interval=interval, cron=cron)

    assert error in str(err)


@pytest.mark.parametrize(
    "interval,cron",
    [
        ("1h", None),
        (None, "* * * * *"),
    ],
)
def test_resource_spec_interval_cron_ok(
    interval: Union[str, None], cron: Union[Crontab, None]
) -> None:
    # No exception should be raised
    CheckSpec(interval=interval, cron=cron)


@pytest.mark.parametrize(
    "hostname, valid",
    [
        ("example.com", True),
        ("sub.example.com", True),
        ("example-123.com", True),
        ("123-example.com", True),
        ("EXAMPLE.COM", True),
        ("ex-ample.com", True),
        ("localhost", True),
        ("-example.com", False),
        ("example-.com", False),
        ("example..com", False),
        ("example.com-", False),
        ("example.com.", False),
        ("a.com", True),
        ("123.com", True),
        ("-abc.com", False),
        ("abc-.com", False),
        ("abc.-com", False),
        ("abc..com", False),
        ("abc.def.ghi.jkl.mno.pqr.stu.vwx.yz", True),
        ("abc_def.com", False),
        ("123.-abc.com", False),
        ("abc.def-.com", False),
        ("example-.123.com", False),
    ],
)
def test_dns_hostname(hostname: str, valid: bool) -> None:
    class MyModel(BaseModel):
        hostname: DNSHostname

    if valid:
        MyModel(hostname=hostname)
    else:
        with pytest.raises(ValidationError):
            MyModel(hostname=hostname)
