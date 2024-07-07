# type: ignore
from typing import Union

import pytest
from pydantic_core import ValidationError

from synthetic_open_schema_model.v1beta1.playwright import (
    PlaywrightCheck,
    PlaywrightLanguage,
)

full_playwright_check = {
    "apiVersion": "checks.dev/v1beta1",
    "kind": "PlaywrightCheck",
    "metadata": {"name": "playwright-browser-test"},
    "spec": {
        "script": "...",
        "script_file": None,
        "interval": "10m",
        "locations": ["us-west-1", "eu-central-1"],
    },
}


@pytest.mark.parametrize("language", PlaywrightLanguage)
def test_playwright_check(language):
    check_definition = full_playwright_check.copy()
    check_definition["spec"]["language"] = language.value

    check = PlaywrightCheck(**check_definition)

    assert check.spec.script == "..."
    assert check.spec.script_file is None
    assert check.spec.language == language
    assert check.spec.interval == "10m"
    assert check.spec.locations == ["us-west-1", "eu-central-1"]


@pytest.mark.parametrize(
    "script, script_file, error",
    [
        ["foo", None, None],
        [None, "foo/bar.js", None],
        [None, None, "One of script or script_file must be provided."],
        ["foo", "foo/bar.js", "Only one of script or script_file can be provided."],
    ],
)
def test_playwright_script_mutually_exclusive(
    script: Union[str, None], script_file: Union[str, None], error: Union[str, None]
) -> None:
    check_definition = full_playwright_check.copy()
    check_definition["spec"]["language"] = "python"
    check_definition["spec"]["script"] = script
    check_definition["spec"]["script_file"] = script_file

    if error is not None:
        with pytest.raises(ValidationError):
            PlaywrightCheck(**check_definition)
    else:
        PlaywrightCheck(**check_definition)
