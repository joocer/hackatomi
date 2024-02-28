import decimal
from dataclasses import dataclass


@dataclass
class UserAuthenticationModel:
    username: str
    password: str


@dataclass
class UserModel:
    username: str
    account_balance: decimal.Decimal = decimal.Decimal("0.0")
