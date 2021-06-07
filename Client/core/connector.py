import json
import socket


class Connector:
    def __init__(self):
        self.server_ip = 'localhost'
        self.port = 2137
        self.login = ''
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

    def registration(self, login, password, email):
        return self.send_message_to_server({
            "command": "registration",
            "login": login,
            "password": password,
            "email": email
        })

    def log_out(self):
        return self.send_message_to_server({
            "command": "logout",
            "login": self.login,
            "token": self.token
        })

    def get_list_of_friends(self):
        return self.send_message_to_server({
            "command": "get_list_of_friends",
            "login": self.login,
            "token": self.token
        })

    def forgot_password(self, login):
        return self.send_message_to_server({
            "command": "forgot_password",
            "login": login
        })

    def change_password(self, login, code, new_password):
        return self.send_message_to_server({
            "command": "change_password",
            "login": login,
            "code": code,
            "new_password": new_password
        })

    def delete_friend(self, friend_login):
        return self.send_message_to_server({
            "command": "remove_friend",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login
        })

    def invite_friend(self, friend_login):
        return self.send_message_to_server({
            "command": "invite_friend",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login
        })

    def get_message(self):
        return self.send_message_to_server({
            "command": "get_message",
            "login": self.login,
            "token": self.token
        })

    def accept_invite(self, friend_login):
        return self.send_message_to_server({
            "command": "accept_invite",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login
        })

    def send_message_to_friend(self, friend_login, message):
        return self.send_message_to_server({
            "command": "send_message_to_friend",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login,
            'message': message
        })

    def invite_to_connect(self, friend_login):
        return self.send_message_to_server({
            "command": "invite_to_connect",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login
        })

    def accept_connection(self, friend_login):
        return self.send_message_to_server({
            "command": "accept_connection",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login
        })

    def reject_connection(self, friend_login):
        return self.send_message_to_server({
            "command": "reject_connection",
            "login": self.login,
            "token": self.token,
            "friend_login": friend_login
        })
