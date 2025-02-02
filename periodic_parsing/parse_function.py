import asyncio
from sqlalchemy import select
from bot.bot import bot
from database import sync_session, User, Post
from parsers import full_parser_list
from parsers.base_classes import ParserPost
from parsers.channels import channels_names
from model import get_important_posts
from periodic_parsing.logger import logger

NOTIFICATION_TEMPLATE = 'В канале <u><b>{0}</b></u> появилась важная информация:\n{1}'

stmt = select(Post).order_by(Post.date.desc()).limit(300)
with sync_session() as session:
    previous_post_urls = {p.url for p in session.scalars(stmt).all()}  # I suppose it will be enough


async def notify_user(user_id: int, post: ParserPost):
    await bot.send_message(
        user_id,
        NOTIFICATION_TEMPLATE.format(channels_names[post.channel_id], post.url),
        parse_mode='HTML',
    )


async def run_tasks(tasks):
    return await asyncio.gather(*tasks)


def do_periodic_parsing():
    global previous_post_urls

    logger.info('Periodic parsing has been started')

    posts = full_parser_list.parse_new()

    # overlap check. I will be useful in case of a scheduler misfire
    posts = [p for p in posts if p.url not in previous_post_urls]
    previous_post_urls = {p.url for p in posts}

    important_posts = get_important_posts(posts)

    post_model_instances = [p.get_model_instance() for p in important_posts]

    # So, this will not work asynchronously, but it doesn't matter since it will run in parallel process
    with sync_session() as session:
        session.add_all(post_model_instances)
        session.commit()
        user_ids = session.scalars(select(User.id)).all()
        user_ids = [u[0] for u in user_ids]

    tasks = [notify_user(uid, p) for p in important_posts for uid in user_ids]
    asyncio.run(run_tasks(tasks))
