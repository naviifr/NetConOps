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
    error: dict[str, str] = field(default_factory=dict)
    plg_data: dict[str, Any] = field(default_factory=dict)
    status: Optional[Status] = None
    
@dataclass
class ScanContext:
    config: ScanConfig
    job: Job
    result: Result
    sock: Optional[socket.socket] = None
