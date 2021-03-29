import socket
import json

JSON_DATA = {
    "command": "registration",
    "login": "testowy_login",
    "password": "testowe_haslo",
}

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(JSON_DATA).encode(), ("185.66.213.128", 2137))
