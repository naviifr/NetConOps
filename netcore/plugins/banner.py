from core.models import ScanContext
import socket

class Banner:

    def execute(self, context: ScanContext):
        sock = context.sock

        if sock is None or context.result is None:
            return

        sock.settimeout(1)

        try:
            results = sock.recv(512)
            context.result.banner = results.decode(errors="replace").rstrip("\r\n")

        except socket.timeout as e:
            pass
    