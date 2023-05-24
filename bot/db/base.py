
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    async def save(self, db_session: AsyncSession):
        db_session.add(self)
        return await db_session.commit()

    async def delete(self, db_session: AsyncSession):
        await db_session.delete(self)
        await db_session.commit()

    async def update(self, db_session: AsyncSession, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        await self.save(db_session)
