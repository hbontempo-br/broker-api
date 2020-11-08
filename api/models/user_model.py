from sqlalchemy import BIGINT, Column, DateTime, String

from .base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "User"
    __table_args__ = {"schema": "broker"}

    user_key = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    document = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    balance = Column(BIGINT, nullable=False)
    deleted_at = Column(DateTime, nullable=False)
