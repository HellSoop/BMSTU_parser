import os
import datetime
import asyncio
from pyrogram import Client
from pyrogram.types import Message, Photo, Video, Voice
from dotenv import load_dotenv
from base_classes import AsyncAbstractParser, ParserPost, PostAttachment
from database.models import posts

load_dotenv('../.env')
TG_USER_USERNAME = os.getenv('TG_USER_USERNAME')


# TODO: Create in TGParser method that extracts all valuable data from output posts for the final response
# TODO: Make TGParser return all photo/video appeared at the same time as single post
class TGParser(AsyncAbstractParser):
    """Parses content from the Telegram channel specified in the channel parameter"""
    MAX_POSTS = 60  # I suppose that fewer than 60 posts appear in the channel per hour
    NEW_POSTS_TIME = datetime.timedelta(hours=24)
    CONTENT_TYPES = ('photo', 'video', 'audio', 'animation')

    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    async def parse(self) -> list[ParserPost]:
        """
        Parse posts from the channel determined by `self.channel`. self.MAX_POSTS posts will be returned.
        :return: List of posts parsed from the channel.
        """
        async with Client("user_account") as user_client:
            posts = [post async for post in user_client.get_chat_history(self.channel, limit=self.MAX_POSTS)]

            return await self.process_posts(posts, user_client=user_client)

    async def parse_new(self) -> list[ParserPost]:
        """
        Parse posts from the channel determined by `self.channel`. self.MAX_POSTS posts will be returned.
        Only posts that appeared within self.NEW_POSTS_TIME before the method call will be returned.
        :return: Filtered list of posts parsed from the channel.
        """
        since_datetime = datetime.datetime.now() - self.NEW_POSTS_TIME

        async with Client("user_account") as user_client:
            posts = [post async for post in user_client.get_chat_history(self.channel, limit=self.MAX_POSTS)
                     if post.date >= since_datetime]

            # return await self.process_posts(posts, user_client=user_client)
            return [p.link for p in posts]

    async def process_posts(self, posts: list[Message], user_client=None, bot_client=None) -> list[ParserPost]:
        # TODO: add process_post docstring

        separated_posts, posts_mask = self._separate_posts(posts)

        user_client_passed = user_client is not None
        bot_client_passed = bot_client is not None
        if not user_client_passed:
            user_client = Client('user_account')
            await user_client.start()
        if not bot_client_passed:
            bot_client = Client('bot')
            await bot_client.start()

        tasks = [self.get_bot_file_id(p, bot_client=bot_client, user_client=user_client) for p in posts]
        attachments = await asyncio.gather(*tasks)

        if not user_client_passed:
            await user_client.stop()
        if not bot_client_passed:
            await bot_client.stop()

        separated_attachments = []  # TODO: check if we must to reverse every attachments list
        current_post_index = None
        for attach, index in zip(attachments, posts_mask):
            if current_post_index != index:
                separated_attachments.append([])
                current_post_index = index

            if attach is not None:
                separated_attachments[index].append(attach)

        posts_instances = [self._gather_post_instance(p, a) for p, a in zip(separated_posts, separated_attachments)]

        return posts_instances

    async def get_bot_file_id(self, message: Message, user_client=None, bot_client=None) -> PostAttachment | None:
        # TODO: add get_bot_file_id docstring

        user_client_passed = user_client is not None
        bot_client_passed = bot_client is not None
        if not user_client_passed:
            user_client = Client('user_account')
            await user_client.start()

        if message.media is not None:
            content_type = message.media.value
        else:
            content_type = None

        if content_type not in self.CONTENT_TYPES:
            return None

        file = await user_client.download_media(message, in_memory=True)

        if not user_client_passed:
            await user_client.stop()

        if not bot_client_passed:
            bot_client = Client('bot')
            await bot_client.start()

        bot_msg = await getattr(bot_client, 'send_' + content_type)(TG_USER_USERNAME, file)
        await bot_client.delete_messages(TG_USER_USERNAME, bot_msg.id)
        file_id = getattr(bot_msg, bot_msg.media.value).file_id  # it's absurd, but in some cases the new file type
        # may be different from the old one
        # , 'document'

        if not bot_client_passed:
            await bot_client.stop()

        return PostAttachment(content_type=content_type, content=file_id)

    def _separate_posts(self, posts: list[Message]) -> tuple[list[list[Message]], list[int]]:
        # TODO: add _separate_posts docstring

        separated_posts = []
        current_post = []
        current_date = posts[0].date
        current_post_index = 0
        posts_mask = []

        for p in posts:
            if current_date == p.date:
                current_post.append(p)
            else:
                separated_posts.append(current_post)
                current_date = p.date
                current_post = [p]
                current_post_index += 1

            posts_mask.append(current_post_index)

        separated_posts.append(current_post)

        return separated_posts, posts_mask

    def _gather_post_instance(self, messages: list[Message], attachments: list[PostAttachment]) -> ParserPost:
        text = ''
        for m in messages:
            if m.caption is not None:
                text = m.caption
                break
            if m.text is not None:
                text = m.text
                break

        post = ParserPost(text=text, channel=self.channel, date=messages[0].date, attachments=attachments)
        return post


if __name__ == '__main__':  # DEBUG! Don't forget to remove!
    async def main():
        post = await parser.parse_new()
        print(post)


    parser = TGParser(channel='python2day')  # 'b2b_bmstu'
    asyncio.run(main())
