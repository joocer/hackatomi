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

URL:str = "http://hakatomi.com/v1/authenticate:8080"
DWELL: int = 0.5

users = {}

def randomly_select_user(statuses: List[UserStatus]) -> User:
    return random.choice([v for k, v in users.items() if v.status in statuses] + [None])


if __name__ == "__main__":

    while True:
        time.sleep(DWELL)
        if random.random() < 0.5:
            # 50% of the time, guess a new username
            username = random_string(4)
            while username in users:
                username = random_string(4)
            user = User(username=username)
            users[username] = user
            print(f"I'm fishing for a new user - {user}")
        
        if random.random() < 0.50:
            # 50% of the time, attempt a new password user
            user = randomly_select_user([UserStatus.unknown, UserStatus.active, UserStatus.new])
            if user:
                print(f"Trying {user.username}, who last time I checked was {user.status}.")
            else:
                print("No good users to try password for")

        if random.random() < 0.10:
            # 10% of the time, attempt new password for a already locked account
            user = randomly_select_user([UserStatus.locked])
            if user:
                print(f"Trying {user.username}, who last time I checked was locked.")
            else:
                print("No locked users to retry")

        if random.random() < 0.10:
            # 10% of the time, attempt a SQL injection
            print("Trying SQL injection")
            pass

        print(f"I am tracking {len(users)} users")