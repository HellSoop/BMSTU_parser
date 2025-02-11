from aiogram import Router
from bot.dialogs.history.dialog import history_dialog
from bot.dialogs.history.states import HistoryDialogSG
from bot.dialogs.subscriptions.dialog import subscriptions_dialog
from bot.dialogs.subscriptions.dialog import SubscriptionsDialogSG

dialogs_router = Router(name='dialogs')
dialogs_router.include_routers(
    history_dialog,
    subscriptions_dialog,
)
