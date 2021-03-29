import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 2137))

users = []  # LIST OF USERS, IN FUTURE DATABASE

while True:
    data, address = sock.recvfrom(1024)
    print(data)
    JSON_DATA = json.loads(data.decode('utf-8'))
    if JSON_DATA["command"] == "login":
        # TODO service of login and password, saving address to database, generating, assigning and send token to client
        print("login: ", JSON_DATA["login"])
        print("password: ", JSON_DATA["password"])
    elif "logout":
        # TODO removing token
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
    elif "registration":
        # TODO adding user to db
        print("login: ", JSON_DATA["login"])
        print("password: ", JSON_DATA["password"])
    elif "add_friend":
        # TODO sending invite to friend by login
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
        print("friend login :", JSON_DATA["friend_login"])
