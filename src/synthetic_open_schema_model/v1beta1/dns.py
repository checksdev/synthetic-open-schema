from enum import Enum
from typing import List, Optional

from pydantic import ConfigDict, IPvAnyAddress

from ..base import BaseAssertion, Check, CheckSpec, DNSHostname

Headers = dict[str, str]


class DnsRecordType(str, Enum):
    A = "A"  # Host address (IPv4)
    AAAA = "AAAA"  # IPv6 address

    # Alias records
    CNAME = "CNAME"  # Canonical name (alias for another hostname)
    ALIAS = "ALIAS"  # Alias (similar to CNAME, less common)

    # Mail exchange records
    MX = "MX"  # Mail exchange server

    # Resource records
    NS = "NS"  # Nameserver
    PTR = "PTR"  # Pointer record
    SOA = "SOA"  # Start of authority

    # Service location records (SRV, NAPTR)
    SRV = "SRV"  # Service record
    NAPTR = "NAPTR"  # Naming authority pointer record

    # Text records
    TXT = "TXT"  # Text record
    SPF = "SPF"  # Sender Policy Framework record

    # Other common types
    HINFO = "HINFO"  # Host information
    CAA = "CAA"  # Certificate authority authorization
    AAAAAAA = "AAAAAAA"  # Experimental IPv6 address record (not widely used)


class DnsAssertionType(str, Enum):
    recordExists = "recordExists"
    recordValue = "recordValue"


class DnsAssertion(BaseAssertion):
    type: DnsAssertionType


DnsAssertionList = List[DnsAssertion]


class DnsCheckSpec(CheckSpec):
    model_config = ConfigDict(extra="forbid")

    hostname: DNSHostname
    resolver: Optional[list[IPvAnyAddress]] = None
    recordType: DnsRecordType

    checks: Optional[DnsAssertionList] = []


class DnsCheck(Check):
    model_config = ConfigDict(extra="forbid")

    spec: DnsCheckSpec
