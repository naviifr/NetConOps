from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Status(Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    TIMEOUT = "Timeout"
    UNREACHABLE = "Unreachable"
    DNS_ERROR = "DNS Resolution Failed"

@dataclass
class Job:
    target: str
    port: int

@dataclass
class Result:
    port: int
    status: Status
    error: Optional[str] = None