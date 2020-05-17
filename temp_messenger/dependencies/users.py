from nameko_sqlalchemy import DatabaseSession

from .users_model import Base, User
from temp_messenger.helpers import hash_password


class UserWrapper:
    def __init__(self, session):
        self.session = session


def create(self, **kwargs):
    plain_text_password = kwargs["password"]
    hashed_password = hash_password(plain_text_password)
    kwargs.update(password=hashed_password)

    user = User(**kwargs)
    self.session.add(user)
    self.session.commit()


class UserStore(DatabaseSession):
    def __init__(self):
        super().__init__(Base)

    def get_dependency(self, worker_ctx):
        database_session = super().get_dependency(worker_ctx)
        return UserWrapper(session=database_session)
