from sqlalchemy import Column, Integer, String, Time
from src.db.base import Base

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False)
    parity = Column(String(15), nullable=False)
    day_of_week = Column(String(15), nullable=False)
    start_time = Column(Time, nullable=False)
    room = Column(String(20), nullable=False)
    subject = Column(String(255), nullable=False)
    teacher = Column(String(100), nullable=False)