from random import randrange
import json
from _smtp import send_email

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
current_invites = {}
forgot_password_codes = {}


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
    Returns -1 when user is not exist.
    Returns token when user was successfully logged."""
    if login in users:
        if password == users[login][0]:
            token = generate_token()
            logged_users[login] = (token, address)
            return token
        else:
            return -2
    else:
        return -1


def log_out(*, login, token):
    """Returns 0 when user was successfully logged out.
    Returns 1 when token is incorrect.
    Returns 2 when user with that login is not logged.
    Returns 3 when user with that login is not exist."""
    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        print('Logged out: ', login, logged_users.pop(login))
        return 0
    return result


def save_invite_if_is_possible(*, login, friend_login, token):
    # TODO test it
    """Returns 0 when invite was saved.
        Returns 1 when token is incorrect.
        Returns 2 when user with that login is not logged.
        Returns 3 when user with that login is not exist.
        Returns 4 when friend is not existed.
        Returns 5 when friend is not logged."""

    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        if friend_login in users:
            if friend_login in logged_users:
                current_invites[friend_login] = login
                return 0
            else:
                return 5
        else:
            return 4
    else:
        return result


def give_address_by_login(*, login):
    # TODO test it
    return logged_users[login][1]


def is_invited(*, login, friend_login):
    """Returns 0 when user was invited by friend.
        Returns 1 when he was not."""
    if login in current_invites:
        if current_invites[login] == friend_login:
            return 0
    return 1


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


def delete_friend(*, login, friend_login, token):
    """Returns 0 when process of deleting new friend was correct.
        Returns 1 when token is incorrect.
        Returns 2 when user with that login is not logged.
        Returns 3 when user with that login is not exist.
        Returns 4 when friend login is not existed.
        Returns 5 when that is not your current friend."""
    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        if friend_login in users:
            if friend_login in friends[login]:
                friends[login].remove(friend_login)
                friends[friend_login].remove(login)
                friends_file = open(f"Data/friends.json", "w")
                friends_file.write(json.dumps(friends))
                friends_file.close()
                return 0
            else:
                return 5
        else:
            return 4
    else:
        return result


def get_list_of_friend(*, login, token):
    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        return 0, friends[login]
    else:
        return result, []


def forgot_password__send_code(*, login):
    """Return 0 when code was send.
    Return 1 when it was not."""
    if login in users:
        code = generate_token()
        send_email(to=users[login][1], subject='Authentication Code', message=f'Your code: {code}')
        forgot_password_codes[login] = code
        return 0
    else:
        return 1


def change_password(*, login, code, new_password):
    """Return 0 when password was successfully changed.
    Return 1 when that login is not existed.
    Return 2 when there is not generated code yet.
    Return 3 when code is wrong."""
    if login in users:
        if login in forgot_password_codes:
            if code == forgot_password_codes[login]:
                users[login][0] = new_password
                users_file = open(f"Data/users.json", "w")
                users_file.write(json.dumps(users))
                users_file.close()
                return 0
            else:
                return 3
        else:
            return 2
    else:
        return 1


def generate_token():
    return randrange(0, 2 ** 64)


def is_it_correct_user_token(*, login, token):
    """Returns 0 when token is correct.
    Returns 1 when token is incorrect.
    Returns 2 when user with that login is not logged.
    Returns 3 when user with that login is not exist."""
    if login in users:
        if login in logged_users:
            if token == logged_users[login][0]:
                return 0
            else:
                return 1
        else:
            return 2
    else:
        return 3


def prepare_standard_response(int_result):
    if int_result == 0:
        json_response = {
            "short": "OK",
            "long": "Successfully logged out.",
        }
    elif int_result == 1:
        json_response = {
            "short": "Error",
            "long": "Wrong token."
        }
    elif int_result == 2:
        json_response = {
            "short": "Error",
            "long": "Users is not logged."
        }
    elif int_result == 3:
        json_response = {
            "short": "Error",
            "long": "Users is not existed."
        }
    else:
        json_response = {
            "short": "BigError",
            "long": "Wrong argument in prepare_standard_response(int_result). Please contact with administrator."
        }
    return json_response
