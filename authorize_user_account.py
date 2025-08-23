import os
from pyrogram import Client
from dotenv import load_dotenv


def main():
    load_dotenv('.env')
    tg_api_id = os.getenv('TG_USER_API_ID')
    tg_api_hash = os.getenv('TG_USER_API_HASH')

    user_client = Client("user_account", api_id=tg_api_id, api_hash=tg_api_hash)
    user_client.start()
    user_client.stop()


if __name__ == '__main__':
    main()
    print('User client available')
