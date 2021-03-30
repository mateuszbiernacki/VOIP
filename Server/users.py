from random import randrange

users = {}
logged_users = {}


def add_user(*, login, password, email):
    """Returns 0 when process of adding new users was correct.
    Returns 1 when login is occupied."""
    if login in users:
        return 1
    else:
        users[login] = (password, email)
        print(users)
        return 0


def logg_in(*, login, password):
    if login in users:
        if password == users[login][0]:
            key = randrange(0, 2**64)
            logged_users[login] = key
            return key
        else:
            return -2
    else:
        return -1

