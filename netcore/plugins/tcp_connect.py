import socket
from core.models import Status, ScanContext
from .base_class import BasePlugin

class TCP_Connect(BasePlugin):

    name = "tcp"
    dependency = None

    def execute(self, context: ScanContext):

        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_sock.settimeout(context.config.timeout)
        context.sock = temp_sock

        try:
            temp_sock.connect((context.job.target, context.job.port,))
            context.result.status = Status.OPEN
        
        except TimeoutError as e:
            context.result.status = Status.TIMEOUT
        
        except ConnectionRefusedError as e:
            context.result.status = Status.CLOSED
            context.result.error["tcp"]  = str(e)
        
        except socket.gaierror as e:
            context.result.status = Status.DNS_ERROR
            context.result.error["tcp"]  = str(e)

        except OSError as e:
            context.result.status = Status.UNREACHABLE
            context.result.error["tcp"]  = str(e)
