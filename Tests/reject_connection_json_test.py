import socket
import json

JSON_DATA = {
    "command": "reject_connection",
    "login": "wiki",
    "token": 13019580135609300876,
    "friend_login": "pat"
}

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(JSON_DATA).encode(), ("localhost", 2137))
    data, address = sock.recvfrom(1024)
    print(data)

