import socket
import json

JSON_DATA = {
    "command": "invite_friend",
    "login": "wiki",
    "token": 16197327193853488976,
    "friend_login": "mateusz"
}

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(JSON_DATA).encode(), ("192.168.2.62", 2137))
    data, address = sock.recvfrom(1024)
    print(data)