import socket
import json
import time

address_config = ("localhost", 2137)

if __name__ == '__main__':
    login = "wiki"
    friend_login = "pat"
    JSON_DATA = {
        "command": "login",
        "login": login,
        "password": "2137"
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(JSON_DATA).encode(), address_config)
    data, address = sock.recvfrom(1024)
    JSON_DATA = json.loads(data.decode('utf-8'))
    token = JSON_DATA['token']
    print(data)
    data, address = sock.recvfrom(1024)
    JSON_DATA = json.loads(data.decode('utf-8'))
    print(data)
    JSON_DATA = {
        "command": "accept_connection",
        "login": login,
        "token": token,
        "friend_login": friend_login
    }
    sock.sendto(json.dumps(JSON_DATA).encode(), address_config)
