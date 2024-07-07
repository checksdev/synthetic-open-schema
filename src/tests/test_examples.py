# type: ignore

import os
from typing import Any, Iterator

import pytest
import yaml  # type: ignore

from synthetic_open_schema_model import v1beta1
from synthetic_open_schema_model.base import Resource


def load_dir_recursively(directory: str) -> Iterator[str]:
    """
    Recursively yield relative paths of all files in a directory.

    Args:
        directory (str): Directory path to recursively search for files.

    Yields:
        str: Relative path of each file found within the directory and its subdirectories.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            yield os.path.relpath(os.path.join(root, file), directory)


EXAMPLES_DIR = "examples" if "CI" not in os.environ else "../examples"
files = list(load_dir_recursively(EXAMPLES_DIR))


def resource_loader(resource_dict: dict[str, Any]) -> Any:
    """
    Load and instantiate a class based on the provided resource dictionary.

    Args:
        resource_dict (dict): Dictionary containing resource data.

    Returns:
        object: Instance of the class specified by the 'kind' field in resource_dict.

    Raises:
        AssertionError: If 'apiVersion' is not 'checks.dev/v1beta1'.
        AssertionError: If 'kind' field is missing or invalid.
    """

    api_version = resource_dict.get("apiVersion")
    assert api_version == "checks.dev/v1beta1", "Invalid apiVersion"

    kind = resource_dict.get("kind")
    assert kind, "kind is required"

    kind_class = getattr(v1beta1, kind, None)
    assert kind_class, f"Invalid kind: {kind} for apiVersion: {api_version}"

    return kind_class(**resource_dict)


def test_example_files_count() -> None:
    # Ensure there's actual test files loaded
    files = list(load_dir_recursively(EXAMPLES_DIR))
    assert "http-check.yaml" in files


@pytest.mark.parametrize("file", files)  # type: ignore
def test_example(file: str) -> None:
    """Ensures example files contain valid resource definitions."""

    with open(os.path.join(EXAMPLES_DIR, file)) as f:
        defns = list(yaml.safe_load_all(f))
        assert len(defns) > 0
        resources = list(map(resource_loader, defns))
        assert len(resources) == len(defns)
        assert all(isinstance(resource, Resource) for resource in resources)
