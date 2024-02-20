import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../../.."))

import duckdb
from drivers.creds import generate_password_hash
from exceptions import AccountLockedError
from exceptions import InvalidAuthenticationError
from exceptions import UserDoesntExistError




DATABASE: str = "hakatomi.duckdb"


def _get_user(username: str) -> dict:

    sql = f"""
SELECT *
  FROM user_table 
 WHERE username LIKE '{username}';
"""
    conn = duckdb.connect(database=DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql)

    match = cursor.fetchone()
    if match is None:
        return None

    # Fetch column names
    columns = [description[0] for description in cursor.description]

    # Convert tuple to dictionary using column names
    user_dict = dict(zip(columns, match))

    return user_dict


def _update_user(user):

    # Create the SET part of the SQL statement, excluding 'username'
    set_part = ", ".join(
        [
            f"{key} = '{value}'" if isinstance(value, str) else f"{key} = {value}"
            for key, value in user.items()
            if key not in ("username", "id")
        ]
    )

    sql = f"""
UPDATE user_table 
   SET {set_part}
 WHERE username LIKE '{user['username']}';
"""

    conn = duckdb.connect(database=DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.commit()


def authenticate_user(username: str, password: str) -> bool:
    user = _get_user(username)
    if user is None:
        raise UserDoesntExistError(username)

    if user["failed_sign_in_attempts"] >= 3:
        raise AccountLockedError(username)

    # sign-in test
    password_hash = generate_password_hash(password, user["salt"])
    if password_hash != user["password"]:
        user["failed_sign_in_attempts"] += 1
        _update_user(user)
        raise InvalidAuthenticationError(username)

    user["failed_sign_in_attempts"] = 0
    _update_user(user)


def get_signin_stats():
    sql = f"""
SELECT COUNT(*), failed_sign_in_attempts
  FROM user_table 
 GROUP BY failed_sign_in_attempts
"""
    conn = duckdb.connect(database="hakatomi.duckdb")
    cursor = conn.cursor()
    cursor.execute(sql)

    match = cursor.arrow()
    return match.to_pydict()
