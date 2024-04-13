import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy.ext.declarative as dec

from .db_session import SqlAlchemyBase


class Answer(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "answers"

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = relationship("User", back_populates="answers")
