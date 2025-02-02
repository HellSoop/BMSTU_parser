from sqlalchemy import select
from database import async_connection, User
from sqlalchemy.ext.asyncio import AsyncSession


# TODO: optimize registration check
@async_connection
async def is_registered(session: AsyncSession, telegram_id: int) -> bool:
    u = await session.scalar(select(User).filter_by(telegram_id=telegram_id))
    return u is not None


@async_connection
async def register_user(session: AsyncSession, telegram_id: int) -> None:
    session.add(User(telegram_id=telegram_id))
    await session.commit()


@async_connection
async def unregister_user(session: AsyncSession, telegram_id: int) -> None:
    u = await session.scalar(select(User).filter_by(telegram_id=telegram_id))

    if u is not None:
        await session.delete(u)
        await session.commit()
