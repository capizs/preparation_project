import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy.ext.declarative as dec

from .db_session import SqlAlchemyBase
   

class Answer(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'answers'

    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('tasks.id'))
