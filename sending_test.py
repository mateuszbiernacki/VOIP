import socket

if __name__ == '__main__':
    pass
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"TEST3", ("127.0.0.1", 2137))