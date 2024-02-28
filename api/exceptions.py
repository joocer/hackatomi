class UserDoesntExistError(Exception):
    pass


class InvalidAuthenticationError(Exception):
    pass


class AccountLockedError(Exception):
    pass
