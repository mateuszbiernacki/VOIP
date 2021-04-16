import socket
import json
import time

address_config = ("localhost", 2137)

if __name__ == '__main__':
    JSON_DATA = {
        "command": "login",
        "login": "pat",
        "password": "2137"
    }
    friend_login = 'wiki'
    login = JSON_DATA["login"]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(JSON_DATA).encode(), address_config)
    data, address = sock.recvfrom(1024)
    JSON_DATA = json.loads(data.decode('utf-8'))
    token = JSON_DATA['token']
    time.sleep(10)
    # it is time to run part2
    JSON_DATA = {
        "command": "invite_to_connect",
        "login": login,
        "token": token,
        "friend_login": friend_login
    }
    sock.sendto(json.dumps(JSON_DATA).encode(), address_config)
    data, address = sock.recvfrom(1024)
    print(data)
    data, address = sock.recvfrom(1024)
    print(data)
