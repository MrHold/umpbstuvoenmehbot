from sqlalchemy import Column, Integer, BigInteger, Boolean, String
from src.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255))
    is_admin = Column(Boolean, default=False)
