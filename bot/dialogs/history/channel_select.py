import operator
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Select, Cancel, ScrollingGroup
from aiogram.types import CallbackQuery
from bot.dialogs.history.states import HistoryDialogSG
from parsers.channels import channels_names

channels = tuple((cid, channel) for cid, channel in channels_names.items())


async def getter(**_):
    return {'channels': channels}


async def on_select(cq: CallbackQuery, widget: Select, dialog_manager: DialogManager, channel_id: str) -> None:
    channel_id = int(channel_id)

    dialog_manager.dialog_data.update(channel_id=channel_id, channel_name=channels_names[channel_id])
    await dialog_manager.switch_to(HistoryDialogSG.date_select)


channel_select_window = Window(
    Const('Пожалуйста, выберете канал для получения записей'),
    ScrollingGroup(
        Select(
            Format('{item[1]}'),
            id='his_c_select',
            items='channels',
            item_id_getter=operator.itemgetter(0),
            on_click=on_select,
        ),
        id='his_channels',
        width=1,
        height=7,
    ),
    Cancel(Const('❌ Назад'), 'his_channel_cancel'),
    state=HistoryDialogSG.channel_select,
    getter=getter,
)
