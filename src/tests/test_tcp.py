# type: ignore
from synthetic_open_schema_model.v1beta1.tcp import TcpCheck

full_tcp_check = {
    "apiVersion": "checks.dev/v1beta1",
    "kind": "TcpCheck",
    "metadata": {"name": "ssh-port-test"},
    "spec": {
        "host": "ssh.example.com",
        "port": 22,
        "interval": "1m",
        "locations": ["us-west-1", "us-east-1"],
    },
}


def test_tcp_check():
    check = TcpCheck(**full_tcp_check)

    assert check.spec.host == "ssh.example.com"
    assert check.spec.port == 22
    assert check.spec.interval == "1m"
    assert check.spec.locations == ["us-west-1", "us-east-1"]
