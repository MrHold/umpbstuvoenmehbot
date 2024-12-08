from sqlalchemy import Column, Integer, BigInteger, Boolean
from src.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    # Все новые пользователи по умолчанию подписаны
    is_subscribed_for_events = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
