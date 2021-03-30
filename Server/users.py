users = []
occupied_logins = []
logged_users = []

def add_user(*, login, password, email):
    """Returns 0 when process of adding new users was correct.
    Returns 1 when login is occupied."""
    if login in occupied_logins:
        return 1
    else:
        users.append({login: (password, email)})
        occupied_logins.append(login)
        print(users)
        return 0


