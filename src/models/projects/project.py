
from sqlalchemy import Column, Boolean, Text
from sqlalchemy.exc import InternalError

from src.common.database import Database
from src.common.utils import Utils


class Project(Database.Base):
    __tablename__ = "projects"

    title = Column(Text(), nullable=False)
    description = Column(Text(), nullable=False)
    completed = Column(Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", None)
        self.description = kwargs.get("description", None)
        self.completed = kwargs.get("completed", None)

    def save(self):
        Database.session.add(self)
        try:
            Database.session.commit()
        except Exception as error:
            print(error.__str__())
            Database.session.rollback()
            return InternalError(
                error="Error while creating the Project", message=str(error)
            )
        return True


    @staticmethod
    def find_project_by_id(id):
        projectDB = Database.session.query(Project).filter_by(id = id).first()
        return projectDB


    @staticmethod
    def delete_project_by_id(id):
        Database.session.query(Project).filter(
            Project.id == id
        ).delete()
        Database.session.commit()
