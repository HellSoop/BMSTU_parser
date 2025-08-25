from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Channel, Post, User, Base, UserChannelAssociation

# it will only work if you use it from main or another root package
async_database_url = 'sqlite+aiosqlite:///expose/bot.db'
async_engine = create_async_engine(async_database_url)
async_session = async_sessionmaker(async_engine)
sync_database_url = 'sqlite:///expose/bot.db'
sync_engine = create_engine(sync_database_url)
sync_session = sessionmaker(sync_engine)


def async_connection(func):

    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper
