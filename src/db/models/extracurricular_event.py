from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from src.db.base import Base

class ExtracurricularEvent(Base):
    __tablename__ = "extracurricular_events"
    id = Column(Integer, primary_key=True)
    message = Column(Text, nullable=False)
