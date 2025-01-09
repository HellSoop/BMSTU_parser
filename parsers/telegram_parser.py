import datetime
from pyrogram import Client
from pyrogram.types import Message
from parsers.base_classes import AsyncAbstractParser, ParserPost


class TelegramParser(AsyncAbstractParser):
    """Parses content from the Telegram channel specified in the channel parameter"""
    MAX_POSTS = 60  # I suppose that fewer than 60 posts appear in the channel per hour
    # There is a planned overlap in case of a scheduler misfire
    NEW_POSTS_TIME = datetime.timedelta(hours=1, seconds=15)

    def __init__(self, channel_id: int, channel: str):
        """
        :param channel_id: channel ID in database
        :param channel: username or identifier of target chat
        """
        super().__init__(channel_id)
        self.channel = channel

    async def parse(self) -> list[ParserPost]:
        """
        Parse posts from the channel determined by `self.channel`. self.MAX_POSTS posts will be returned.
        :return: List of posts parsed from the channel.
        """
        async with Client("user_account") as user_client:
            posts = [post async for post in user_client.get_chat_history(self.channel, limit=self.MAX_POSTS)]

        return self.process_posts(posts)

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

        return self.process_posts(posts)

    def process_posts(self, posts: list[Message]) -> list[ParserPost]:
        """
        Converts Pyrogram messages into ParserPost objects.
        :param posts: list of Pyrogram messages
        :return: list of ParserPost objects
        """
        res = []
        for p in posts:
            if p.text or p.caption:
                text = p.text if p.text else p.caption

                res.append(ParserPost(
                    text=text,
                    url=p.link,
                    channel_id=self.channel_id,
                    date=p.date
                ))

        return res
