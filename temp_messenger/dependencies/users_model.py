from sqlalchemy import Column, Integer, Unicode, LargeBinary
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(length=128))
    last_name = Column(Unicode(length=128))
    email = Column(Unicode(length=256), unique=True)
    password = Column(LargeBinary())
