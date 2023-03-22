
import datetime

from bot.db.base import Base

from sqlalchemy import Column, BigInteger, DateTime, Boolean


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    reg_time = Column(DateTime, default=datetime.datetime.now())
    subscribed = Column(Boolean, default=True)

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'
