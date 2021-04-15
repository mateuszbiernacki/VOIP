import socket
import json

JSON_DATA = {
    "command": "invite_to_connect",
    "login": "pat",
    "token": 320821389009989877,
    "friend_login": "wiki"
}

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(JSON_DATA).encode(), ("localhost", 2137))
    data, address = sock.recvfrom(1024)
    print(data)