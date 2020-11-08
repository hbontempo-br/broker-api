from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


class _Base(object):
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)


BaseModel = declarative_base(cls=_Base)
