from aiogram_dialog import Dialog
from bot.dialogs.history.channel_select import channel_select_window
from bot.dialogs.history.date_select import date_select_window

history_dialog = Dialog(
    channel_select_window,
    date_select_window,
)
