from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum
import socket 
from core.config import ScanConfig

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
    error: dict[str, str] = field(default_factory=dict)
    plg_data: dict[str, Any] = field(default_factory=dict)
    
@dataclass
class ScanContext:
    config: ScanConfig
    job: Job
    sock: Optional[socket.socket] = None
    result: Optional[Result] = None
