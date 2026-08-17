from .base_class import BasePlugin
from core.models import ScanContext
import socket

class HTTP(BasePlugin):
    name = "http"
    dependency = "tcp"

    def execute(self, context: ScanContext):

        if context.sock is None:
            return

        if context.result is None:
            return
        try:
            sock = context.sock
            self.send_request(context.job.target, sock)

            data = self.receive_response(sock, context.config.header_size)

            results = self.parse_response(data)
            context.result.plg_data['http'] = results

        except Exception as e:
            context.result.error['http'] = str(e)


    def send_request(self, host, sock: socket.socket, protocol = "HTTP/1.1"):

        request = (
                        f"GET / {protocol}\r\n"
                        f"Host: {host}\r\n"
                        f"Connection: close\r\n"
                        f"\r\n"
                    )
        
        sock.sendall(request.encode())

    def receive_response(self, sock:socket.socket, header_size):

        data = b""

        while b"\r\n\r\n" not in data:
        
            chunk = sock.recv(header_size)
            data += chunk

            if len(data) > header_size:
                raise ValueError("header exceeds configured max size")

            if chunk == b"":
                raise ConnectionError

        return data
        

    def parse_response(self, data: bytes):

        if b'HTTP/1.' not in data[:10]:
            raise TypeError("The port does not support HTTP")    
        
        clean_data = data.decode('iso-8859-1')
        header, body = clean_data.split("\r\n\r\n", 1)

        header = header.split("\r\n")
        version, code, reason = header[0].split(' ', 2)

        result = {'version':version,
                  'code': int(code),
                  'reason': reason,
                  }

        for i in header[1:]:

            key , value = i.split(':',1)

            key = key.strip().lower()
            value = value.strip()

            result[key] = value

        return result