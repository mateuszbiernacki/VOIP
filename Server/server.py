import socket
import json
import users

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 2137))

while True:
    data, address = sock.recvfrom(1024)
    print(data)
    JSON_DATA = json.loads(data.decode('utf-8'))
    if JSON_DATA["command"] == "login":
        pass
    elif JSON_DATA["command"] == "logout":
        # TODO removing token
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
    elif JSON_DATA["command"] == "registration":
        result = users.add_user(login=JSON_DATA["login"], password=JSON_DATA["password"], email=JSON_DATA["email"])
        if result == 0:
            json_response = {
                "short": "OK",
                "long": "Successfully added new user."
            }
            sock.sendto(json.dumps(json_response).encode(), address)
        elif result == 1:
            json_response = {
                "short": "Error",
                "long": "Login is occupied."
            }
            sock.sendto(json.dumps(json_response).encode(), address)
    elif JSON_DATA["command"] == "invite_friend":
        # TODO sending invite to friend by login
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
        print("friend login :", JSON_DATA["friend_login"])
    elif JSON_DATA["command"] == "remove_friend":
        # TODO removing friend by login
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
        print("friend login :", JSON_DATA["friend_login"])
    elif JSON_DATA["command"] == "remind_password":
        # TODO
        print("login: ", JSON_DATA["login"])
        print("email: ", JSON_DATA["email"])
    elif JSON_DATA["command"] == "accept_invite":
        # TODO
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
        print("friend login: ", JSON_DATA["friend_login"])
    elif JSON_DATA["command"] == "reject_invite":
        # TODO
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
        print("friend login: ", JSON_DATA["friend_login"])
    elif JSON_DATA["command"] == "get_list_of_friends":
        # TODO
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
    elif JSON_DATA["command"] == "connect":
        # TODO
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
        print("friend login: ", JSON_DATA["friend_login"])
    elif JSON_DATA["command"] == "accept_connection":
        # TODO
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
        print("friend login: ", JSON_DATA["friend_login"])
    elif JSON_DATA["command"] == "reject_connection":
        # TODO
        print("login: ", JSON_DATA["login"])
        print("token: ", JSON_DATA["token"])
        print("friend login: ", JSON_DATA["friend_login"])