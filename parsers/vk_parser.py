import os
import datetime
import requests
from dotenv import load_dotenv
from base_classes import AbstractParser

load_dotenv('../.env')
TOKEN = os.getenv('VK_API_TOKEN')


# TODO: Create in VKParser method that extracts all valuable data from output posts for the final response
class VKParser(AbstractParser):
    """Parses content from the VK group specified at creation"""
    MAX_POSTS = 100  # maximum number of posts in one response provided by VK API
    NEW_POSTS_TIME = datetime.timedelta(hours=1)

    def __init__(self, owner_id=None, domain=None) -> None:
        super().__init__()

        if not bool(owner_id) ^ bool(domain):
            if owner_id is None:  # in this case domain will be None too
                raise ValueError('owner_id or domain must be specified')
            else:
                raise ValueError('owner_id and domain are mutually exclusive')

        if owner_id:
            self.url = (f"https://api.vk.com/method/wall.get?owner_id={owner_id}"
                        f"&count={self.MAX_POSTS}&lang=ru&v=5.199")
        else:
            self.url = (f"https://api.vk.com/method/wall.get?domain={domain}"
                        f"&count={self.MAX_POSTS}&lang=ru&v=5.199")

    def parse(self) -> list[dict]:
        """
        Parse posts from the page determined by `self.url`. self.MAX_POSTS posts will be returned.
        :return: List of posts parsed from the page.
        """
        response = requests.post(self.url, headers={'Authorization': 'Bearer ' + TOKEN}).json()
        posts = [post for post in response['response']['items']]

        return posts

    def parse_new(self) -> list[dict]:
        """
        Parse posts as well as self.parse().
        Only posts that appeared within self.NEW_POSTS_TIME before the method call will be returned.
        :return: Filtered list of posts parsed from the page.
        """
        posts = self.parse()
        since_datetime = datetime.datetime.now() - self.NEW_POSTS_TIME
        new_posts = [p for p in posts if p['date'] >= since_datetime.timestamp()]

        return new_posts


if __name__ == '__main__':  # DEBUG! Don't forget to remove!
    parser = VKParser(domain='bmstu_snto')
    print(parser.parse()[0])
