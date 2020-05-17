from nameko_sqlalchemy import DatabaseSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from .users_model import Base, User
from temp_messenger.helpers import hash_password
from .exceptions import UserAlreadyExists, CreateUserError, UserNotFound


class UserWrapper:
    def __init__(self, session):
        self.session = session

    def create(self, **kwargs):
        plain_text_password = kwargs["password"]
        hashed_password = hash_password(plain_text_password)
        kwargs.update(password=hashed_password)

        user = User(**kwargs)
        self.session.add(user)

        try:
            self.session.commit()
        except IntegrityError as err:
            self.session.rollback()
            error_message = err.args[0]

            if "already exists" in error_message:
                email = kwargs["email"]
                message = f"User already exists - {email}"
                raise UserAlreadyExists(message)
            else:
                raise CreateUserError(error_message)

    def get(self, email):
        query = self.session.query(User)

        try:
            user = query.filter_by(email=email).one()
        except NoResultFound:
            message = "User not found - {email}"
            raise UserNotFound(message)

        return user


class UserStore(DatabaseSession):
    def __init__(self):
        super().__init__(Base)

    def get_dependency(self, worker_ctx):
        database_session = super().get_dependency(worker_ctx)
        return UserWrapper(session=database_session)
