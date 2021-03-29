import socket
import json

JSON_DATA = {
    "command": "logout",
    "login": "testowy_login",
    "token": "testowy_token",
}

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(JSON_DATA).encode(), ("185.66.213.128", 2137))
