from typing import Union

from pydantic import TypeAdapter

from .dns import DnsCheck
from .http import HttpCheck
from .playwright import PlaywrightCheck
from .ssl import SslCheck
from .tcp import TcpCheck

CheckUnion = Union[DnsCheck, HttpCheck, TcpCheck, PlaywrightCheck, SslCheck]


ALL_TYPES: TypeAdapter[CheckUnion] = TypeAdapter(CheckUnion)
