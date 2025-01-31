import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv('.env')
TG_API_ID = os.getenv('TG_USER_API_ID')
TG_API_HASH = os.getenv('TG_USER_API_HASH')

user_client = Client("user_account", api_id=TG_API_ID, api_hash=TG_API_HASH)
user_client.start()
user_client.stop()
print('User client available')
