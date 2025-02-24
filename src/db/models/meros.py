from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from src.db.base import Base

class Mero(Base):
    __tablename__ = "meros"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)
    location = Column(String(255))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    category = Column(String(255), nullable=False)
