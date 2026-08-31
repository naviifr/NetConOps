from dataclasses import dataclass

WORKERS = 7
TIMEOUT = 2
MAX_HEADER_SIZE = 4096

@dataclass
class ScanConfig:
    timeout: int = TIMEOUT
    worker: int = WORKERS
    header_size: int = MAX_HEADER_SIZE
    syn_timeout: int = TIMEOUT
    udp_timeout: int = TIMEOUT