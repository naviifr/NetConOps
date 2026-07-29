import socket
from core.models import Result, Status, ScanContext
from .base_plugin import BasePlugin

class TCP_Connect(BasePlugin):

    name = "tcp"
    dependency = None

    def execute(self, context: ScanContext):

        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context.sock = temp_sock
        temp_sock.settimeout(context.config.timeout)

        try:
            temp_sock.connect((context.job.target, context.job.port,))
            context.result = Result(port=context.job.port, status=Status.OPEN)
        
        except TimeoutError as e:
            context.result = Result(port=context.job.port, status=Status.TIMEOUT)
        
        except ConnectionRefusedError as e:
            context.result = Result(port=context.job.port, status=Status.CLOSED)
            context.result.error["tcp"]  = str(e)
        
        except socket.gaierror as e:
            context.result = Result(port=context.job.port, status=Status.DNS_ERROR)
            context.result.error["tcp"]  = str(e)

        except OSError as e:
            context.result = Result(port=context.job.port, status=Status.UNREACHABLE)
            context.result.error["tcp"]  = str(e)
