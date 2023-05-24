
async def get_db(db_session):
    async with db_session() as session:
        return await session
