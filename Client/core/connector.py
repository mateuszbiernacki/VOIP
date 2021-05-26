import json
import socket


class Connector:
    def __init__(self):
        self.server_ip = 'localhost'
        self.port = 2137
        self.token = -1

    def set_token(self, _token):
        self.token = _token

    def send_message_to_server(self, data_to_send):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(data_to_send).encode(), (self.server_ip, self.port))
        data, address = sock.recvfrom(1024)
        return json.loads(data.decode('utf-8'))

    def log_in(self, login, password):
        return self.send_message_to_server({
            "command": "login",
            "login": login,
            "password": password
        })