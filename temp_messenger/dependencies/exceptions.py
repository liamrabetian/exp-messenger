class RedisError(Exception):
    pass


class CreateUserError(Exception):
    pass


class UserAlreadyExists(CreateUserError):
    pass
