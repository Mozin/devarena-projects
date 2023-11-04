import uuid

from sqlalchemy import create_engine, String, Column, DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base


def generate_uuid():
    return str(uuid.uuid4())




class Database:
    RootBase = declarative_base()
    session = None

    class BaseAssign(RootBase):
        __abstract__ = True

        id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
        created_at = Column(DateTime)
        # updated_at = Column(DateTime)
    Base = BaseAssign

    @staticmethod
    def initialize(app):
        Database.db = SQLAlchemy(app)
        Database.session = Database.db.session


        class Base(Database.RootBase):
            __abstract__ = True

            id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
            created_at = Column(Database.db.DateTime, default=Database.db.func.now())
            # updated_at = Column(Database.db.DateTime, default=Database.db.func.now(), onupdate=Database.db.func.now())

        Database.Base = Base
