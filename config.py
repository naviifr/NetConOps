from dataclasses import dataclass

WORKERS = 7
TIMEOUT = 2

@dataclass
class ScanConfig:
    timeout: int = TIMEOUT
    worker: int = WORKERS