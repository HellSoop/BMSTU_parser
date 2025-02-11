from bot.bot import bot
from aiogram.exceptions import AiogramError
from parsers.channels import channels_names
from bot.logger import logger

NOTIFICATION_TEMPLATE = 'В канале <u><b>{0}</b></u> появилась важная информация:\n{1}'


async def send_post(user_id: int, url: str, channel_id: int,  notification: bool = False) -> None:
    """
    Sends a post message to user specified by user_id. Can send a notification.
    :param user_id: id of the user
    :param url: post url
    :param channel_id: post channel id
    :param notification: whether send a notification message
    :return: None
    """

    if notification:
        text = NOTIFICATION_TEMPLATE.format(channels_names[channel_id], url)
    else:
        text = url

    try:
        await bot.send_message(
            user_id,
            text,
            parse_mode='HTML',
        )
    except AiogramError:
        logger.warning('Caught AiogramError while sending post message to user(id=%s)', user_id, exc_info=True)
