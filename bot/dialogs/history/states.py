from aiogram.fsm.state import StatesGroup, State


class HistoryDialogSG(StatesGroup):
    channel_select = State()
    date_select = State()
