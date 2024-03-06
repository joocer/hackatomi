import os
import sys
from argparse import ArgumentParser

sys.path.insert(1, os.path.join(sys.path[0], "./api/"))

import models
import uvicorn
from adapters import database
from adapters import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from exceptions import AccountLockedError
from exceptions import InvalidAuthenticationError
from exceptions import UserDoesntExistError


application = FastAPI()
application.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8085", "http://admin.hakatomi.com:8085"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@application.post("/v1/authenticate")
async def authenticate_user(user_auth: models.UserAuthenticationModel):

    try:
        database.authenticate_user(user_auth.username, user_auth.password)
    except AccountLockedError:
        logging.log("auth", user_auth.username, "denied", cause="Account Locked")
        return "locked"
    except InvalidAuthenticationError:
        logging.log(
            "auth", user_auth.username, "denied", cause="Password Incorrect"
        )
        return "password"
    except UserDoesntExistError:
        logging.log("auth", user_auth.username, "denied", cause="Unknown User")
        return "user"
    logging.log("auth", user_auth.username, "pass")
    return "okay"


@application.get("/v1/measure/signin/success")
async def get_measure_signin_success():
    return database.get_signin_stats()

@application.get("/v1/logs/tail")
async def get_log_tail(size:int = 10):
    return logging.logfile.tail(size)

@application.post("/v1/user/reset")
async def post_reset_user(user_auth: models.UserAuthenticationModel):
    try:
        database.reset_user(user_auth.username, user_auth.password)
    except UserDoesntExistError:
        logging.log("reset", user_auth.username, "denied", cause="Unknown User")
        return "user"
    logging.log("reset", user_auth.username, "done")
    return "okay"

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="reset the database")
    args = parser.parse_args()

    if args.reset:
        database.reset_database()

    uvicorn.run("main:application", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
