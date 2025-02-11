import datetime
import asyncio
from typing import Union, Literal
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError
from parsers.base_classes import AsyncAbstractParser, ParserPost, ParserList, AbstractParser
from parsers.logger import logger


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

    async def parse(self, user_client: Client) -> list[ParserPost]:
        """
        Parse posts from the channel determined by `self.channel`. self.MAX_POSTS posts will be returned.
        :return: List of posts parsed from the channel.
        """
        logger.info("Parsing posts from Telegram channel %s", self.channel)

        try:
            posts = [post async for post in user_client.get_chat_history(self.channel, limit=self.MAX_POSTS)]
        except RPCError:
            logger.error('Got a telegram error during parsing posts from channel %s', self.channel, exc_info=True)
            return []

        return self.process_posts(posts)

    async def parse_new(self, user_client: Client) -> list[ParserPost]:
        """
        Parse posts from the channel determined by `self.channel`. self.MAX_POSTS posts will be returned.
        Only posts that appeared within self.NEW_POSTS_TIME before the method call will be returned.
        :return: Filtered list of posts parsed from the channel.
        """
        since_datetime = datetime.datetime.now() - self.NEW_POSTS_TIME

        logger.info("Parsing new posts from Telegram channel %s", self.channel)

        try:
            posts = [post async for post in user_client.get_chat_history(self.channel, limit=self.MAX_POSTS)
                     if post.date >= since_datetime]
        except RPCError:
            logger.error('Got a telegram error during parsing posts from channel %s', self.channel, exc_info=True)
            return []

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


class TelegramParserList(ParserList):
    """
    Special ParserList for TelegramParser's. It creates a pyrogram client and pass it to the TelegramParser.parse() and
    TelegramParser.parse_new() methods.
    """
    def __init__(self, *items: Union[AbstractParser, AsyncAbstractParser, ParserList]):
        super().__init__(*items)

        self.telegram_parsers = []

        for i in range(len(self.async_parsers) - 1, -1, -1):
            if isinstance(self.async_parsers[i], TelegramParser):
                self.telegram_parsers.insert(0, self.async_parsers.pop(i))

    def parse(self) -> list[ParserPost]:
        res = super().parse()

        telegram_posts = asyncio.run(self._parse_telegram(method='parse'))
        res.extend(telegram_posts)

        return res

    def parse_new(self) -> list[ParserPost]:
        res = super().parse()

        telegram_posts = asyncio.run(self._parse_telegram(method='parse_new'))
        res.extend(telegram_posts)

        return res

    async def _parse_telegram(self, method: Union[Literal["parse"], Literal['parse_new']]) -> list[ParserPost]:
        """
        Use self.telegram_parsers: list[TelegramParser] to perform parsing
        :param method: method to call from TelegramParser's
        :return: parsed posts
        """
        assert method in ("parse", "parse_new"), 'method must be "parse" or "parse_new"'

        async with Client('user_account') as user_client:
            tasks = [getattr(p, method)(user_client=user_client) for p in self.telegram_parsers]
            posts_lists = await asyncio.gather(*tasks)

        res = []
        for plist in posts_lists:
            res.extend(plist)

        return res
