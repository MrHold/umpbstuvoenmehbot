from sqlalchemy import Column, Integer, String, Text
from src.db.base import Base

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    contacts = Column(Text)
    direction = Column(String(255))
