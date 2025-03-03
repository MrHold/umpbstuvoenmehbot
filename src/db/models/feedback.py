from sqlalchemy import Column, Integer, BigInteger, Boolean, String, Text
from src.db.base import Base

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=False)
    username = Column(String(255))
    message = Column(Text, nullable=False)
    type = Column(String(255), nullable=False)
    contact = Column(String(255))