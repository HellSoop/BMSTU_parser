import os
import subprocess
from getpass import getpass
from dotenv import set_key
from authorize_user_account import main as authorize_user_account


def main():
    # check if the current working directory matches the file directory
    # otherwise Pyrogram will not ba able connect to Telegram
    path = os.path.dirname(os.path.realpath(__file__))
    if os.getcwd() != path:
        print(f'Your current working directory interferes with the execution. Please run "cd {path}" '
              f'and try again.')
        exit(1)

    # fill .env file
    with open('.env.tmp', 'w', encoding='utf-8'):
        pass

    vk_api_token = getpass('Please enter your VK API token. You can obtain it from https://id.vk.com/business/go\n'
                           'Please note that you should use the service key, not the secure key.\n>')
    tg_user_api_id = getpass('Please enter Telegram user API ID. You can obtain it from '
                             'https://core.telegram.org/api/obtaining_api_id\n>')
    tg_user_api_hash = getpass('Please enter Telegram user API hash. You can obtain it from '
                               'https://core.telegram.org/api/obtaining_api_id\n>')
    bot_token = getpass('Please enter Telegram bot API token. You can obtain it from https://t.me/BotFather\n>')

    set_key('.env', 'VK_API_TOKEN', vk_api_token)
    set_key('.env', 'TG_USER_API_ID', tg_user_api_id)
    set_key('.env', 'TG_USER_API_HASH', tg_user_api_hash)
    set_key('.env', 'BOT_TOKEN', bot_token)

    # log into Telegram account
    print('Trying to log into Telegram. Please note that you may need to enter your phone number and confirmation code.')

    authorize_user_account()

    print('Telegram login successful')

    # make migrations
    print('Applying database migrations...')

    result = subprocess.run(['alembic', 'upgrade', 'head'], stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f'Unable to apply database migrations.\nThere is an exception:\n{result.stderr}')
        exit(1)

    print('Database migrations was applied successfully')

    # create logs directory
    print('Creating "logs" directory...')

    try:
        os.mkdir('pog')
    except FileExistsError:  # if logs directory is already created for some reason we will use it
        pass
    except OSError:
        print('Failed to create "logs" directory. Make sure you have permission to create "logs" directory '
              'or create it manually')
        exit(1)

    print('"logs" directory was created')


if __name__ == '__main__':
    main()
