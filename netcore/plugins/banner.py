from core.models import ScanContext, Status
from .support.base_class import BasePlugin
import socket

class Banner(BasePlugin):

    name = "banner"
    dependency = "tcp"

    def execute(self, context: ScanContext):
        sock = context.sock

        sock.settimeout(1)

        try:
            results = sock.recv(512)
            context.result.plg_data["banner"] = results.decode(errors="replace").rstrip("\r\n")

        except socket.timeout as e:
            context.result.error['banner'] = str(e)

        except ConnectionResetError as e:
            context.result.error['banner'] = str(e)

        except OSError as e:
            context.result.error["banner"] = str(e)