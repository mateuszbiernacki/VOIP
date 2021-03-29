import socket

"""Port have to be open.
   Linux example: sudo ufw allow 2137/udp"""

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 2137))
    while True:
        data, address = sock.recvfrom(1024)
        print(f"Received from {address[0]}: {data}")
        sock.sendto(b"Hej", address)
