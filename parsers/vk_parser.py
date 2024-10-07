import os
import datetime
import requests
from dotenv import load_dotenv
from base_classes import AbstractParser, IDsManagerMixin

load_dotenv('../.env')
token = os.getenv('VK_API_TOKEN')


class VKParser(AbstractParser, IDsManagerMixin):
    # MAX_POSTS = 100
    # NEW_POSTS_TIME = datetime.timedelta(hours=1)

    def __init__(self, owner_id=None, domain=None) -> None:
        super().__init__()

        if not bool(owner_id) ^ bool(domain):
            if owner_id is None:  # in this case domain will be None too
                raise ValueError('owner_id or domain must be specified')
            else:
                raise ValueError('owner_id and domain are mutually exclusive')

        if owner_id:
            self.url = (f"https://api.vk.com/method/wall.get?owner_id={owner_id}"
                        f"&count={self.MAX_IDS_COUNT}&lang=ru&v=5.199")
        else:
            self.url = (f"https://api.vk.com/method/wall.get?domain={domain}"
                        f"&count={self.MAX_IDS_COUNT}&lang=ru&v=5.199")

    def parse(self) -> list[dict]:
        response = requests.post(self.url, headers={'Authorization': 'Bearer ' + token}).json()
        posts_ids = (post['id'] for post in response['response']['items'])

        self.update_ids(*posts_ids)
        return [post for post in response['response']['items']]

    def parse_new(self) -> list[dict]:
        previous_ids = self.previous_ids.copy()

        posts = self.parse()
        posts_ids = [p['id'] for p in posts]
        new_posts_ids = self.get_new_ids(*posts_ids, previous_ids=previous_ids)

        posts = [p for p in posts if p['id'] in new_posts_ids]
        return posts


if __name__ == '__main__':  # DEBUG! Don't forget to remove!
    parser = VKParser(domain='bmstu_snto')
    print(len(parser.parse_new()))
