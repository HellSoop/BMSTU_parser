import asyncio
from bot.bot import bot
from database import session, User, Channel, Post
from parsers import full_parser_list
from parsers.base_classes import ParserPost

# temporary
get_important_posts = lambda x: x  # mock function, it will be implemented in model package


NOTIFICATION_TEMPLATE = 'В канале <u><b>{0}</b></u> появилась важная информация:\n{1}'

s = session()

channels = s.query(Channel).all()
channels_names = {c.id: c.name for c in channels}
previous_posts = s.query(Post).order_by(Post.date.desc()).limit(300).all()  # I suppose it will be enough
previous_post_urls = {p.url for p in previous_posts}

s.close()


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

    posts = full_parser_list.parse_new()

    # overlap check. I will be useful in case of a scheduler misfire
    posts = [p for p in posts if p.url not in previous_post_urls]
    previous_post_urls = {p.url for p in posts}

    important_posts = get_important_posts(posts)

    post_model_instances = [p.get_model_instance() for p in important_posts]
    s = session()
    s.add_all(post_model_instances)
    s.commit()

    user_ids = [u[0] for u in s.query(User.telegram_id).all()]
    s.close()

    tasks = [notify_user(uid, p) for p in important_posts for uid in user_ids]
    asyncio.run(run_tasks(tasks))
