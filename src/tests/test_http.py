# type: ignore
import json

from synthetic_open_schema_model.v1beta1.http import HttpCheck

full_http_check = {
    "apiVersion": "checks.dev/v1beta1",
    "kind": "HttpCheck",
    "metadata": {"name": "test"},
    "spec": {
        "url": "https://example.com/foo?bar=baz#qux",
        "cron": "* * * * *",
        "headers": {
            "User-Agent": "testsuite/0.1.0",
        },
        "checks": [
            {
                "type": "statusCode",
                "operator": "equals",
                "value": 200,
            }
        ],
    },
}


def test_http_check():
    check = HttpCheck(**full_http_check)

    assert check.spec.url.scheme == "https"
    assert check.spec.url.host == "example.com"
    assert check.spec.url.path == "/foo"
    assert check.spec.url.query == "bar=baz"
    assert check.spec.url.fragment == "qux"

    assert check.spec.cron.cron.get_next() is not None


def test_http_check_serializes():
    check = HttpCheck(**full_http_check)
    json.dumps(list(check.model_dump()))
