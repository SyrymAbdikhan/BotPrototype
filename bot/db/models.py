
import datetime

from bot.db.base import Base

from sqlalchemy import Column, BigInteger, DateTime, Boolean, select


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    reg_time = Column(DateTime, default=datetime.datetime.now())
    subscribed = Column(Boolean, default=True)
    
    @classmethod
    async def find(self, db_session, user_id):
        sql = select(self).where(self.user_id == user_id)
        result = await db_session.execute(sql)
        return result.scalars().first()

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'
