import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import sync_session, Post, Channel
from periodic_parsing.logger import logger
from bot.utils.post_utils import send_post

NOTIFICATION_TEMPLATE = 'В канале <u><b>{0}</b></u> появилась важная информация:\n{1}'


async def run_tasks(tasks):
    return await asyncio.gather(*tasks)


def do_periodic_parsing():
    """
    Performs the periodic parsing task, saves the results to database and sends notifications.
    :return: None
    """
    # these imports should be there  to avoid loading useless data into the main process
    from parsers import full_parser_list
    from parsers.channels import channels_names
    from model import get_important_posts

    logger.info('Periodic parsing has been started')

    # the interval is set to two hours to be completely sure that all duplicate posts will be in the set
    stmt = select(Post).filter(Post.date >= datetime.now() - timedelta(hours=2))
    with sync_session() as session:
        previous_post_urls = {p.url for p in session.scalars(stmt).all()}

    posts = full_parser_list.parse_new()

    # overlap check. I will be useful in case of a scheduler misfire
    posts = [p for p in posts if p.url not in previous_post_urls]
    logger.info('%d new posts was parsed', len(posts))

    important_posts = get_important_posts(posts)

    post_model_instances = [p.get_model_instance() for p in important_posts]

    # So, this will not work asynchronously, but it doesn't matter since it will run in parallel process
    with sync_session() as session:
        session.add_all(post_model_instances)
        session.commit()

        channel_posts = {cid: tuple(p for p in important_posts if p.channel_id == cid) for cid in channels_names}
        tasks = []
        for cid, channel_posts in channel_posts.items():
            c = session.scalar(select(Channel).filter_by(id=cid).options(selectinload(Channel.subscribers)))
            user_ids = [u.telegram_id for u in c.subscribers]

            tasks.append(run_tasks([
                send_post(uid, p.url, p.channel_id, notification=True) for p in channel_posts for uid in user_ids
            ]))

    asyncio.run(run_tasks(tasks))
