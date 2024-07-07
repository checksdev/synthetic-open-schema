# type: ignore
from synthetic_open_schema_model.v1beta1.dns import DnsCheck

full_dns_check = {
    "apiVersion": "checks.dev/v1beta1",
    "kind": "DnsCheck",
    "metadata": {"name": "dns-resolution-test"},
    "spec": {
        "hostname": "example.com",
        "recordType": "A",
        "checks": [
            {"type": "recordValue", "operator": "equals", "value": "93.184.216.34"}
        ],
        "interval": "5m",
        "locations": ["us-west-1", "us-east-1"],
    },
}


def test_dns_check() -> None:
    check = DnsCheck(**full_dns_check)

    assert check.spec.hostname == "example.com"
    assert check.spec.recordType == "A"
    assert check.spec.interval == "5m"
    assert check.spec.locations == ["us-west-1", "us-east-1"]
