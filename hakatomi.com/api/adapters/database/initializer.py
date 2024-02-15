import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../../.."))

import random

from api.drivers.password import generate_password, generate_password_hash
from api.drivers.usernames import generate_username
from orso.tools import random_int, random_string

USER_COUNT: int = 100


def generate_user_record(index):
    username = generate_username()
    salt = random_string(16)
    password = generate_password()
    password_hash = generate_password_hash(password, salt)
    failed_sign_in_attempts = 0
    if random.random() < 0.1:
        failed_sign_in_attempts = 3
    elif random.random() < 0.2:
        failed_sign_in_attempts = 2
    elif random.random() < 0.3:
        failed_sign_in_attempts = 1
    account_balance = random_int() % 100000000 / 100

    if index == 0:
        print("Your test user is")
        print("username:", username)
        print("password:", password)

    return (
        index,
        username,
        password_hash,
        salt,
        failed_sign_in_attempts,
        account_balance,
    )


CREATE_DB = (
    """
CREATE TABLE user_table (
  id INTEGER PRIMARY KEY,
  username VARCHAR(32),
  password VARCHAR(64),
  salt VARCHAR(16),
  failed_sign_in_attempts INTEGER,
  account_balance DECIMAL(14, 2)
);

INSERT INTO user_table (id, username, password, salt, failed_sign_in_attempts, account_balance)
VALUES 
"""
    + ",\n".join(str(generate_user_record(i)) for i in range(USER_COUNT))
    + ";"
)


def create_duck_db():
    """
    blat and rebuild the database.
    """
    import os

    import duckdb

    try:
        os.remove("hakatomi.duckdb")
    except Exception as err:
        # we expect to fail when running in GitHub Actions, but not fail
        # when running locally - just ignore failures here, it's not a
        # meaningful part of the script
        print(err)

    conn = duckdb.connect(database="hakatomi.duckdb")
    cur = conn.cursor()
    res = cur.execute(CREATE_DB)
    print(res.commit().arrow())
    cur.close()


print(CREATE_DB)
create_duck_db()
