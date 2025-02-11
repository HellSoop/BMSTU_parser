import os
import datetime
import requests
from parsers.base_classes import AbstractParser, ParserPost
from parsers.logger import logger

TOKEN = os.getenv('VK_API_TOKEN')


class VKParser(AbstractParser):
    """Parses content from the VK group specified at creation"""
    MAX_POSTS = 60  # optimal number of posts in one response
    # There is a planned overlap in case of a scheduler misfire
    NEW_POSTS_TIME = datetime.timedelta(hours=1, seconds=15)

    def __init__(self, channel_id: int, owner_id: str | int | None = None, domain: str | None = None) -> None:
        """
        :param channel_id: channel ID in database
        :param owner_id: wall owner id. Excludes domain argument
        :param domain: domain of the group. Excludes owner_id argument
        """
        super().__init__(channel_id)

        if not bool(owner_id) ^ bool(domain):
            if owner_id is None:  # in this case domain will be None too
                raise ValueError('owner_id or domain must be specified')
            else:
                raise ValueError('owner_id and domain are mutually exclusive')

        if owner_id:
            self.parse_url = (f"https://api.vk.com/method/wall.get?owner_id={owner_id}"
                              f"&count={self.MAX_POSTS}&lang=ru&v=5.199")
        else:
            self.parse_url = (f"https://api.vk.com/method/wall.get?domain={domain}"
                              f"&count={self.MAX_POSTS}&lang=ru&v=5.199")

    def parse(self) -> list[ParserPost]:
        """
        Parse posts from the page determined by `self.url`. self.MAX_POSTS posts will be returned.
        :return: List of posts parsed from the page.
        """
        logger.info("Parsing VK posts in url %s", self.parse_url)

        response = requests.post(self.parse_url, headers={'Authorization': 'Bearer ' + TOKEN}).json()
        try:
            posts = [post for post in response['response']['items']]
        except KeyError:
            logger.error("VK parsing filed for url=%s, got an error: %s", self.parse_url,
                           response.get('error').get('error_msg'))
            return []

        return self.process_posts(posts)

    def parse_new(self) -> list[ParserPost]:
        """
        Parse posts as well as self.parse().
        Only posts that appeared within self.NEW_POSTS_TIME before the method call will be returned.
        :return: Filtered list of posts parsed from the page.
        """
        since_datetime = (datetime.datetime.now() - self.NEW_POSTS_TIME).timestamp()

        logger.info("Parsing new VK posts in url %s", self.parse_url)

        response = requests.post(self.parse_url, headers={'Authorization': 'Bearer ' + TOKEN}).json()
        try:
            posts = [post for post in response['response']['items'] if post['date'] >= since_datetime]
        except KeyError:
            logger.error("VK parsing filed for url: %s, got an error: %s", self.parse_url,
                           response.get('error').get('error_msg'))
            return []

        return self.process_posts(posts)

    def process_posts(self, posts: list[dict]) -> list[ParserPost]:
        """
        Converts response items in JSON format into ParserPost objects.
        :param posts: list of items
        :return: list of ParserPost objects
        """
        return [ParserPost(
            text=p['text'],
            url=f'https://vk.com/wall{p["owner_id"]}_{p["id"]}',
            channel_id=self.channel_id,
            date=datetime.datetime.fromtimestamp(p['date'])
        ) for p in posts if p['text']]
