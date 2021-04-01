import socket
import json
import users

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 2137))

while True:
    data, address = sock.recvfrom(1024)
    print(data)
    JSON_DATA = json.loads(data.decode('utf-8'))
    json_response = {
        "short": "Error",
        "long": "Undefined operation."
    }
    if JSON_DATA["command"] == "login":
        result = users.logg_in(login=JSON_DATA["login"], password=JSON_DATA["password"], address=address)
        if result == -1:
            json_response = {
                "short": "Error",
                "long": "User is not existed."
            }
        elif result == -2:
            json_response = {
                "short": "Error",
                "long": "Bad password."
            }
        else:
            json_response = {
                "short": "OK",
                "long": "Successfully logged.",
                "token": result
            }
    elif JSON_DATA["command"] == "logout":
        result = users.log_out(login=JSON_DATA["login"], token=JSON_DATA["token"])
        json_response = users.prepare_standard_response(result)
    elif JSON_DATA["command"] == "registration":
        result = users.add_user(login=JSON_DATA["login"], password=JSON_DATA["password"], email=JSON_DATA["email"])
        if result == 0:
            json_response = {
                "short": "OK",
                "long": "Successfully added new user."
            }
        elif result == 1:
            json_response = {
                "short": "Error",
                "long": "Login is occupied."
            }
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
    elif JSON_DATA["command"] == "forgot_password":
        # TODO
        print("login: ", JSON_DATA["login"])
        print("email: ", JSON_DATA["email"])
    elif JSON_DATA["command"] == "accept_invite":
        result = users.is_it_correct_user_token(login=JSON_DATA['login'], token=JSON_DATA['token'])
        if result == 0:
            result_0 = users.add_friend(login=JSON_DATA["login"], friend_login=JSON_DATA["friend_login"])
            result_1 = users.add_friend(login=JSON_DATA["friend_login"], friend_login=JSON_DATA["login"])
            if result_0 != result_1:
                json_response = {
                    "short": "BigError",
                    "long": "Problem with consistence of data. Please contact with system administrator."
                }
            elif result_1 == 2 or result_0 == 2:
                json_response = {
                    "short": "Error",
                    "long": "Friend is already in friend list."
                }
            elif result_1 == 1 or result_0 == 1:
                json_response = {
                    "short": "Error",
                    "long": "There is not user with that login."
                }
            elif result_1 == 0 and result_0 == 0:
                json_response = {
                    "short": "OK",
                    "long": "Friend was added."
                }
        else:
            json_response = users.prepare_standard_response(result)
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
    sock.sendto(json.dumps(json_response).encode(), address)

