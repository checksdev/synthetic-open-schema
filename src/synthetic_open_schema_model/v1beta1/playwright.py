from enum import Enum
from typing import Any, Optional

from pydantic import ConfigDict, model_validator

from synthetic_open_schema_model.base import Check, CheckSpec


class PlaywrightLanguage(str, Enum):
    python = "python"
    javascript = "javascript"
    typescript = "typescript"
    java = "java"
    dotnet = "dotnet"


class PlaywrightCheckSpec(CheckSpec):
    script: Optional[str] = None
    script_file: Optional[str] = None
    language: PlaywrightLanguage

    @model_validator(mode="before")
    def check_either_script_or_script_file(
        cls, values: dict[str, str]
    ) -> dict[str, Any]:
        script = values.get("script")
        script_file = values.get("script_file")

        print(script, script_file)
        if script and script_file:
            raise ValueError("Only one of script or script_file can be provided.")
        if not script and not script_file:
            raise ValueError("One of script or script_file must be provided.")

        return values


class PlaywrightCheck(Check):
    model_config = ConfigDict(extra="forbid")

    spec: PlaywrightCheckSpec
