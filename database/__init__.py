from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Channel, Post, User, Base

database_url = 'sqlite+aiosqlite:///database/bot.db'
engine = create_async_engine(database_url)  # it will only work if you use it from main or another root package
async_session = async_sessionmaker(engine)


def connection(func):

    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper
