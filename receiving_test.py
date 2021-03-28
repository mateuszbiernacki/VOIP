import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 2137))
    while True:
        data, address = sock.recvfrom(1024)
        print(f"Received from {address[0]}: {data}")

