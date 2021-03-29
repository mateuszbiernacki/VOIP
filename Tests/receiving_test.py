import socket

"""UDP Example"""

"""Port have to be opened.
   Linux example: sudo ufw allow 2137/udp"""

if __name__ == '__main__':
    """This script receive data from other client and send back a response.
    It's work in loop, so that can receive and resend several times."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 2137))
    while True:
        data, address = sock.recvfrom(1024)
        print(f"Received from {address[0]}: {data}")
        sock.sendto(b"Hej", address)
