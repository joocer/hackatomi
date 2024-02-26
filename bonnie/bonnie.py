import os
import random
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../hakatomi.com"))


import requests
import time
import orjson
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
import random
from orso.tools import random_string


@dataclass
class User():
    username:str
    password:str

users = List[User]

HAKATOMI_URL:str = "http://localhost:8080/v1/authenticate"
DWELL: int = 0.25

def load_users():
    list_of_users = []
    with open("assets/users.txt", "r") as uf:
        for line in uf.readlines():
            username, password = line.split("\t")
            user = User(username, password[:-1])
            list_of_users.append(user)
    return list_of_users

def randomly_select_user() -> User:
    return random.choice(users)
    
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

    users = load_users()
    print(users)

    while True:
        time.sleep(random.random())
        user = random.choice(users)
        username = user.username
        password = user.password
        if random.random() < 0.1:
            # 10% of the time get the username wrong
            username = random_string(8)
        if random.random() < 0.15:
            # 15% of the time, get the password wrong
            password = random_string(8)
        
        # attempt
        print(username, password, user)

        if False:


            # 50% of the time, attempt a new password user
            user = randomly_select_user([UserStatus.unknown, UserStatus.active, UserStatus.new])
            if user:
                print(f"[{len(users)}] Trying {user.username}, who last time I checked was {user.status}.")
                issue_request(user)

            # 10% of the time, attempt new password for a already locked account
            user = randomly_select_user([UserStatus.locked])
            if user:
                print(f"[{len(users)}] Trying {user.username}, who last time I checked was {user.status}.")
                issue_request(user)

            # 10% of the time, attempt a SQL injection
            payload = randomly_select_sql_injection()
            print("Trying SQL injection - ", payload)
            user = User(username=payload)
            status, message = issue_request(user)
            if status != 500:
                print("WORKED", status, message)
            pass
