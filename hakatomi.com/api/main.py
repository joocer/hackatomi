from argparse import ArgumentParser
from fastapi import FastAPI
import database_adapter
import uvicorn
import os
import models

application = FastAPI()


@application.post("/v1/authenticate")
async def authenticate_user(user_auth: models.UserAuthenticationModel):
    user = database_adapter.get_user(user_auth.username)
    if user is None:
        return "failed"
    if user.failed_sign_in_attempts > 2:
        return "failed"

    try_authenticate = database_adapter.authenticate_user(
        user_auth.username, user_auth.password
    )
    if not try_authenticate:
        return "failed"

    return "okay"


@application.get("/v1/measure/signin/success")
async def get_measure_signin_success():
    return {}


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="reset the database")
    args = parser.parse_args()

    if args.reset:
        database_adapter.reset_database()

    uvicorn.run(
        "main:application", host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
    )
