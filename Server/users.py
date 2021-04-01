from random import randrange
import json

try:
    file = open(f"Data/users.json", "r")
    users = json.loads(file.read())
except json.decoder.JSONDecodeError:
    users = {}
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
        except OSError:
            return 2
        users[login] = (password, email)
        print(users)
        return 0


def logg_in(*, login, password):
    """Returns -2 when password is wrong.
    Returns -1 when user is not exist."""
    if login in users:
        if password == users[login][0]:
            key = generate_token()
            logged_users[login] = key
            return key
        else:
            return -2
    else:
        return -1


def generate_token():
    return randrange(0, 2 ** 64)
