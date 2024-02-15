from api.models import UserModel
from api.adapters import database
from api.adapters import logging
import duckdb

def _get_connection():
    conn = duckdb.connect(database="hakatomi.duckdb")
    cur = conn.cursor()
    res = cur.execute(CREATE_DB)
    res.commit()
    cur.close()

def reset_database():
    pass


def get_user(username: str) -> UserModel:

    username: str
    failed_sign_in_attempts: int = 0
    account_balance: decimal.Decimal = decimal.Decimal("0.0")

    SQL = "SELECT username, failed_sign_in_attempts FROM user_table WHERE username LIKE "


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
