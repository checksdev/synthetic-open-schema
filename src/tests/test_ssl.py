# type: ignore
from synthetic_open_schema_model.v1beta1.ssl import SslCheck

full_ssl_check = {
    "apiVersion": "checks.dev/v1beta1",
    "kind": "SslCheck",
    "metadata": {"name": "ssl-cert-test", "title": "SSL Cert Test"},
    "spec": {
        "hostname": "example.com",
        "interval": "1h",
        "locations": ["us-west-1", "us-east-1"],
        "checks": [
            {"type": "expirationTime", "operator": "greaterThan", "value": "30d"}
        ],
    },
}


def test_ssl_check() -> None:
    check = SslCheck(**full_ssl_check)

    assert check.spec.hostname == "example.com"
    assert check.spec.port == 443
    assert check.spec.interval == "1h"
    assert check.spec.locations == ["us-west-1", "us-east-1"]
    assert check.spec.checks[0].type == "expirationTime"
    assert check.spec.checks[0].operator == "greaterThan"
    assert check.spec.checks[0].value == "30d"
