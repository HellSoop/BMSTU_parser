from os import getenv
from dotenv import load_dotenv, set_key
from setup import main as setup

load_dotenv('.env')

setup_completed = getenv('SETUP_COMPLETED')
if setup_completed != 'true':
    # setup app
    while True:
        try:
            setup()
            break
        except RuntimeError:
            print('\n\nAn error occurred. Please try again.')

    set_key('.env', 'SETUP_COMPLETED', 'true')

# run bot
import asyncio  # these imports must be there because there is logging config loading in main.py
from main import main as run_bot

asyncio.run(run_bot())
