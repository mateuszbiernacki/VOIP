from random import randrange
import json
from _smtp import send_email
from database_connector import DBConnector


PATH_TO_USERS_DATABASE = 'TestData/users.db'

db = DBConnector()
logged_users = {}
current_invites = {}
forgot_password_codes = {}
connections = {}


def add_user(*, login, password, email):
    """Returns 0 when process of adding new users was correct.
    Returns 1 when login is occupied."""
    if db.check_user_exits(login):
        return 1
    else:
        db.add_user(login, password, email)
        return 0


def logg_in(*, login, password, address):
    """Returns -2 when password is wrong.
    Returns -1 when user is not exist.
    Returns token when user was successfully logged."""
    if db.check_user_exits(login):
        if db.check_user_password(login, password):
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
    """Returns 0 when invite was saved.
        Returns 1 when token is incorrect.
        Returns 2 when user with that login is not logged.
        Returns 3 when user with that login is not exist.
        Returns 4 when friend is not existed.
        Returns 5 when friend is not logged."""

    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        if db.check_user_exits(friend_login):
            if friend_login in logged_users:
                if friend_login in current_invites:
                    current_invites[friend_login].append(login)
                else:
                    current_invites[friend_login] = [login]
                return 0
            else:
                return 5
        else:
            return 4
    else:
        return result


def check_friendship(*, login, friend_login, token):
    """Returns 0 when it's a friend.
        Returns 1 when token is incorrect.
        Returns 2 when user with that login is not logged.
        Returns 3 when user with that login is not exist.
        Returns 4 when friend is not existed.
        Returns 5 when friend is not logged."""

    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        if db.check_user_exits(friend_login):
            if friend_login in logged_users:

                return 0
            else:
                return 5
        else:
            return 4
    else:
        return result


def get_address_by_login(*, login):
    return logged_users[login][1]


def is_invited(*, login, friend_login):
    """Returns 0 when user was invited by friend.
        Returns 1 when he was not."""
    if login in current_invites:
        if friend_login in current_invites[login]:
            return 0
    return 1


def add_friend(*, login, friend_login):
    """Returns 0 when process of adding new friend was correct.
    Returns 1 when there is authorization problem.
    Returns 2 when friend is already in friend list."""
    if db.check_user_exits(login):
        if db.check_user_exits(friend_login):
            if db.check_friendship(login, friend_login):
                return 2
            db.set_new_friend(login, friend_login)
            return 0
        else:
            return 1
    else:
        return 1


def reject_invite_to_friends_list(*, login, friend_login, token):
    """Returns 0 when invite was rejected.
        Returns 1 when token is incorrect.
        Returns 2 when user with that login is not logged.
        Returns 3 when user with that login is not exist.
        Returns 4 when friend login is not existed.
        Returns 5 when there is not any invite."""
    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        if db.check_user_exits(friend_login):
            if login in current_invites:
                current_invites[login].remove(friend_login)
                return 0
            else:
                return 5
        else:
            return 4
    else:
        return result


def delete_friend(*, login, friend_login, token):
    """Returns 0 when process of deleting new friend was correct.
        Returns 1 when token is incorrect.
        Returns 2 when user with that login is not logged.
        Returns 3 when user with that login is not exist.
        Returns 4 when friend login is not existed.
        Returns 5 when that is not your current friend."""
    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        if db.check_user_exits(friend_login):
            if db.check_friendship(login, friend_login):
                db.delete_friendship(login, friend_login)
                return 0
            else:
                return 5
        else:
            return 4
    else:
        return result


def get_list_of_friend(*, login, token):
    """Returns 0 and friends list when everything is correct.
        Returns 1 when token is incorrect.
        Returns 2 when user with that login is not logged.
        Returns 3 when user with that login is not exist."""
    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        return 0, db.get_list_of_friend(login)
    else:
        return result, []


def forgot_password__send_code(*, login):
    """Return 0 when code was send.
    Return 1 when it was not."""
    if db.check_user_exits(login):
        code = generate_token()
        send_email(to=db.get_user_email(login), subject='Authentication Code', message=f'Your code: {code}')
        forgot_password_codes[login] = code
        return 0
    else:
        return 1


def change_password(*, login, code, new_password):
    """Return 0 when password was successfully changed.
    Return 1 when that login is not existed.
    Return 2 when there is not generated code yet.
    Return 3 when code is wrong."""
    if db.check_user_exits(login):
        if login in forgot_password_codes:
            if code == forgot_password_codes[login]:
                db.change_password(login, new_password)
                return 0
            else:
                return 3
        else:
            return 2
    else:
        return 1


def invite_to_connection(*, login, token, friend_login):
    # TODO test it
    """Returns 0 when it is everything okey.
    Returns 1 when token is incorrect.
    Returns 2 when user with that login is not logged.
    Returns 3 when user with that login is not exist.
    Returns 4 when friend is not existed.
    Returns 5 when it is not your friend."""
    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        if friend_login in logged_users:
            if db.check_friendship(login, friend_login):
                connections[friend_login] = (login, 1)
                return 0
            else:
                return 5
        else:
            return 4
    elif result in {1, 2, 3}:
        return result
    else:
        return -1


def accept_connection(*, login, token, friend_login):
    # TODO test it
    """Returns 0 when it is everything okey.
    Returns 1 when token is incorrect.
    Returns 2 when user with that login is not logged.
    Returns 3 when user with that login is not exist.
    Returns 4 when friend is not existed.
    Returns 5 when it is not your friend.
    Returns 6 when login is not in connections dictionary.
    Returns 7 when you are not invited."""
    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        if friend_login in logged_users:
            if db.check_friendship(login, friend_login):
                if login in connections:
                    if connections[login][0] == friend_login:
                        connections[login] = (friend_login, 0)
                        return 0
                    else:
                        return 7
                else:
                    return 6
            else:
                return 5
        else:
            return 4
    elif result in {1, 2, 3}:
        return result
    else:
        return -1


def reject_connection(*, login, token, friend_login):
    # TODO test it
    """Returns 0 when it is everything okey.
    Returns 1 when token is incorrect.
    Returns 2 when user with that login is not logged.
    Returns 3 when user with that login is not exist.
    Returns 4 when friend is not existed.
    Returns 5 when it is not your friend.
    Returns 6 when login is not in connections dictionary.
    Returns 7 when you are not invited."""
    result = is_it_correct_user_token(login=login, token=token)
    if result == 0:
        if friend_login in logged_users:
            if db.check_friendship(login, friend_login):
                if login in connections:
                    if connections[login][0] == friend_login:
                        connections[login] = None
                        return 0
                    else:
                        return 7
                else:
                    return 6
            else:
                return 5
        else:
            return 4
    elif result in {1, 2, 3}:
        return result
    else:
        return -1


def generate_token():
    return randrange(0, 2 ** 64)


def is_it_correct_user_token(*, login, token):
    """Returns 0 when token is correct.
    Returns 1 when token is incorrect.
    Returns 2 when user with that login is not logged.
    Returns 3 when user with that login is not exist."""
    if db.check_user_exits(login):
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
