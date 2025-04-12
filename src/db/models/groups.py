from sqlalchemy import Column, Integer, BigInteger, Boolean, String, Text
from src.db.base import Base

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)