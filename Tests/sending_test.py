import socket

"""UDP Example"""

if __name__ == '__main__':
    """There are send one message and then receive one message."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"Hej", ("185.66.213.128", 2137))
    data, address = sock.recvfrom(1024)
    print(f"Received from {address[0]}: {data}")
