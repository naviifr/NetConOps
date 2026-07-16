import socket

sock = socket.socket()
try:
    sock.connect(("github.com", 22,))
    a= sock.recv(1024)
    print(a)
except Exception as e:
    print(e)
