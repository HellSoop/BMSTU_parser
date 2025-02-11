from sqlalchemy import select
from database import async_connection, User, UserChannelAssociation
from sqlalchemy.ext.asyncio import AsyncSession
from bot.logger import logger
from parsers.channels import channels_names


# TODO: optimize registration check
@async_connection
async def is_registered(session: AsyncSession, telegram_id: int) -> bool:
    u = await session.scalar(select(User).filter_by(telegram_id=telegram_id))
    res = u is not None

    logger.info('Called is_registered for [telegram id]=%s. Result: %s', telegram_id, res)

    return res


@async_connection
async def register_user(session: AsyncSession, telegram_id: int) -> None:
    u = User(telegram_id=telegram_id)
    session.add(u)
    await session.flush()
    session.add_all([UserChannelAssociation(user_id=u.id, channel_id=cid) for cid in channels_names])
    await session.commit()

    logger.info('User [telegram id]=%s is successfully registered', telegram_id)


@async_connection
async def unregister_user(session: AsyncSession, telegram_id: int) -> None:
    u = await session.scalar(select(User).filter_by(telegram_id=telegram_id))

    if u is not None:
        await session.delete(u)
        await session.commit()

    logger.info('User [telegram id]=%s is deleted from database', telegram_id)
