import os
import datetime
import requests
from base_classes import AbstractParser, ParserPost

TOKEN = os.getenv('VK_API_TOKEN')


class VKParser(AbstractParser):
    """Parses content from the VK group specified at creation"""
    MAX_POSTS = 100  # maximum number of posts in one response provided by VK API
    NEW_POSTS_TIME = datetime.timedelta(hours=1)

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
        response = requests.post(self.parse_url, headers={'Authorization': 'Bearer ' + TOKEN}).json()
        posts = [post for post in response['response']['items']]

        return self.process_posts(posts)

    def parse_new(self) -> list[ParserPost]:
        """
        Parse posts as well as self.parse().
        Only posts that appeared within self.NEW_POSTS_TIME before the method call will be returned.
        :return: Filtered list of posts parsed from the page.
        """
        since_datetime = (datetime.datetime.now() - self.NEW_POSTS_TIME).timestamp()
        response = requests.post(self.parse_url, headers={'Authorization': 'Bearer ' + TOKEN}).json()
        posts = [post for post in response['response']['items'] if post['date'] >= since_datetime]

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


if __name__ == '__main__':  # DEBUG! Don't forget to remove!
    from dotenv import load_dotenv
    load_dotenv('../.env')
    TOKEN = os.getenv('VK_API_TOKEN')

    parser = VKParser(1, domain='bmstu_snto')
    print([p.get_model_instance() for p in parser.parse_new()])
