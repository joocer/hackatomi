import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "./hackatomi.com/"))

from argparse import ArgumentParser

from adapters import database
from adapters import logging
import models
import uvicorn
from fastapi import FastAPI

application = FastAPI()


@application.post("/v1/authenticate")
async def authenticate_user(user_auth: models.UserAuthenticationModel):

    from exceptions import AccountLockedError
    from exceptions import InvalidAuthenticationError
    from exceptions import UserDoesntExistError

    try:
        database.authenticate_user(user_auth.username, user_auth.password)
    except AccountLockedError:
        logging.log("auth", user_auth.username, "hakatomi.com", "denied", cause="Account Locked")
        return "locked"
    except InvalidAuthenticationError:
        logging.log("auth", user_auth.username, "hakatomi.com", "denied", cause="Password Incorrect")
        return "password"
    except UserDoesntExistError:
        logging.log("auth", user_auth.username, "hakatomi.com", "denied", cause="Unknown User")
        return "user"
    logging.log("auth", user_auth.username, "hakatomi.com", "pass")
    return "okay"


@application.get("/v1/measure/signin/success")
async def get_measure_signin_success():
    return database.get_signin_stats()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="reset the database")
    args = parser.parse_args()

    if args.reset:
        database.reset_database()

    uvicorn.run("main:application", host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
