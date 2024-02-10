from api.models import UserModel
from api.adapters import database
from api.adapters import logging

def reset_database():
    pass


def get_user(username: str) -> UserModel:
    pass


def update_user(user):
    pass


def authenticate_user(username: str, password: str) -> bool:
    user = get_user(username)

    # sign-in test
    successful = True

    if successful:
        user.failed_sign_in_attempts = 0
    else:
        user.failed_sign_in_attempts += 1
    database_adapter.update_user(user)


def get_signin_stats():
    pass
