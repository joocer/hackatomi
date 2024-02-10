from dataclasses import dataclass
import decimal


@dataclass
class UserAuthenticationModel:
    username: str
    password: str


@dataclass
class UserModel:
    username: str
    failed_sign_in_attempts: int = 0
    account_balance: decimal.Decimal = decimal.Decimal("0.0")
