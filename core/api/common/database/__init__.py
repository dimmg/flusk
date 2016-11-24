import os

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database


engine = create_engine(os.environ.get(
    'SQLALCHEMY_DATABASE_URI'), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


class CustomBase(object):
    def __init__(self, **kwargs):
        cls_ = type(self)
        for k in kwargs:
            if hasattr(cls_, k):
                setattr(self, k, kwargs[k])
            else:
                continue

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def save(self):
        db_session.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        return self.save()

    def delete(self):
        db_session.delete(self)
        self._flush()

    def _flush(self):
        try:
            db_session.flush()
        except DatabaseError:
            db_session.rollback()
            raise


BaseModel = declarative_base(cls=CustomBase, constructor=None)
BaseModel.query = db_session.query_property()


def init_db():
    if not database_exists(engine.url):
        create_database(engine.url)
    BaseModel.metadata.create_all(bind=engine)


def drop_db():
    BaseModel.metadata.drop_all(bind=engine)
    drop_database(engine.url)
