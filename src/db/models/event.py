from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from src.db.base import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)
    location = Column(String(255))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
