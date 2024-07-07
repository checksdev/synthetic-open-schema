from enum import Enum
from typing import List, Optional, Union

from pydantic import ConfigDict, Field, IPvAnyAddress

from ..base import BaseAssertion, Check, CheckSpec, DNSHostname

Headers = dict[str, str]


class TcpAssertionType(str, Enum):
    reachable = "reachable"
    latency = "latency"
    sslHandshake = "sslHandshake"


class TcpAssertion(BaseAssertion):
    type: TcpAssertionType


TcpAssertionList = List[TcpAssertion]


class TcpCheckSpec(CheckSpec):
    """
    Specification for a TCP Check.
    """

    model_config = ConfigDict(extra="forbid")

    host: Union[DNSHostname, IPvAnyAddress] = Field(
        ..., description="The hostname or IP address of the TCP service to check."
    )
    port: int

    checks: Optional[TcpAssertionList] = []


class TcpCheck(Check):
    """
    Model representing a TCP Check resource.

    A TcpCheck is a resource used to define and manage the monitoring of a TCP service. It provides the necessary
    configuration to perform periodic checks on a TCP endpoint, ensuring that the service is reachable and meets
    specified expectations.

    The TcpCheck resource is particularly useful for developers and operations teams who need to ensure the reliability
    and performance of their TCP services. It allows for detailed specification of the target host and port, as well as
    any expectations that the service must meet. These checks can be integrated into CI/CD pipelines, monitoring systems,
    or other automated workflows.

    Example:
        .. code-block:: python

            from my_monitoring_library import TcpCheck, TcpCheckSpec, TcpAssertion, TcpAssertionType

            # Define the specification for the TCP check
            tcp_check_spec = TcpCheckSpec(
                host="example.com",
                port=443,
                expect=[
                    TcpAssertion(type=TcpAssertionType.SOME_EXPECTATION_TYPE)
                ]
            )

            # Create the TCP check resource
            tcp_check = TcpCheck(spec=tcp_check_spec)

            # Use the tcp_check instance in your monitoring setup
            print(tcp_check)

    The above example demonstrates how to define a TCP check with a specific host and port, along with optional expectations.
    The `TcpCheck` instance can then be used in various monitoring or automation setups to ensure the service is operating correctly.
    """

    model_config = ConfigDict(extra="forbid")

    spec: TcpCheckSpec
