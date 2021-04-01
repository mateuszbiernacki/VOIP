from random import randrange
import json

try:
    file = open(f"Data/users.json", "r")
    users = json.loads(file.read())
except json.decoder.JSONDecodeError:
    users = {}
else:
    file.close()

try:
    file = open(f"Data/friends.json", "r")
    friends = json.loads(file.read())
except json.decoder.JSONDecodeError:
    friends = {}
else:
    file.close()
logged_users = {}


def add_user(*, login, password, email):
    """Returns 0 when process of adding new users was correct.
    Returns 1 when login is occupied."""
    if login in users:
        return 1
    else:
        try:
            users[login] = (password, email)
            users_file = open(f"Data/users.json", "w")
            users_file.write(json.dumps(users))
            users_file.close()
            friends[login] = []
            friends_file = open(f"Data/friends.json", "w")
            friends_file.write(json.dumps(friends))
            friends_file.close()
        except OSError:
            return 2
        print(users)
        return 0


def logg_in(*, login, password, address):
    """Returns -2 when password is wrong.
    Returns -1 when user is not exist."""
    if login in users:
        if password == users[login][0]:
            key = generate_token()
            logged_users[login] = (key, address)
            return key
        else:
            return -2
    else:
        return -1


def add_friend(*, login, friend_login):
    """Returns 0 when process of adding new friend was correct.
    Returns 1 when there is authorization problem.
    Returns 2 when friend is already in friend list."""
    if login in users:
        if friend_login in users:
            if friend_login in friends[login]:
                return 2
            friends[login].append(friend_login)
            friends_file = open(f"Data/friends.json", "w")
            friends_file.write(json.dumps(friends))
            friends_file.close()
            return 0
        else:
            return 1
    else:
        return 1


def generate_token():
    return randrange(0, 2 ** 64)
