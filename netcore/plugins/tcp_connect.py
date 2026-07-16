import socket
from core.models import Job, Result, Status, ScanContext
import core.config as config

class TCP_Connect:

    def __init__(self, context: ScanContext, config: config.ScanConfig):
        self.job = context.job
        self.context = context
        self.config = config

    def execute(self):

        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.context.sock = temp_sock
        temp_sock.settimeout(self.config.timeout)

        try:
            temp_sock.connect((self.job.target, self.job.port,))
            self.context.result = Result(port=self.job.port, status=Status.OPEN, error=None)
        
        except TimeoutError:
            self.context.result = Result(port=self.job.port, status=Status.TIMEOUT)
        
        except ConnectionRefusedError as e:
            self.context.result = Result(port=self.job.port, status=Status.CLOSED, error=str(e))
        
        except socket.gaierror as e:
            self.context.result = Result(port=self.job.port, status=Status.DNS_ERROR, error=str(e))

        except OSError as e:
            self.context.result = Result(port=self.job.port, status=Status.UNREACHABLE, error=str(e))
