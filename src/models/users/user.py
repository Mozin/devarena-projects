
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.exc import InternalError

from src.common.database import Database
from src.common.utils import Utils


class User(Database.Base):
    __tablename__ = "users"

    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get("email", None)
        self.password = kwargs.get("password", None)
        self.name = kwargs.get("name", None)

    def save(self):
        self.password = Utils.hash_password(self.password)
        Database.session.add(self)
        try:
            Database.session.commit()
        except Exception as error:
            print(error.__str__())
            Database.session.rollback()
            return InternalError(
                error="Error while creating the User", message=str(error)
            )
        return True


    @staticmethod
    def find_user_by_email(email):
        userDB = Database.session.query(User).filter_by(email = email).first()
        return userDB


    @staticmethod
    def find_user_by_id(id):
        userDB = Database.session.query(User).filter_by(id = id).first()
        return userDB

