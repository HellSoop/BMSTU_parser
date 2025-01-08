from dotenv import load_dotenv
load_dotenv('.env')

import asyncio
from bot.bot import bot
from database import session, User, Post
from parsers import FullParserList

# temporary
import pickle as pkl

get_important_posts = lambda x: x  # mock function, it will be implemented in model package


async def notify_user(user_id: int, post: Post):
    await bot.send_message(user_id, post.url)


def do_periodic_parsing():
    # posts = FullParserList.parse_new()
    with open('posts.pkl', 'rb') as f:  # There is some test posts
        posts = pkl.load(f)
    important_posts = get_important_posts(posts)

    post_model_instances = [p.get_model_instance() for p in important_posts]
    s = session()
    s.add_all(post_model_instances)
    s.commit()

    user_ids = [u[0] for u in s.query(User.telegram_id).all()]
    s.close()

    tasks = [notify_user(uid, p) for p in post_model_instances for uid in user_ids]
    asyncio.run(asyncio.gather(*tasks))


if __name__ == '__main__':
    do_periodic_parsing()
