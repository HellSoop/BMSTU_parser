import operator
from asyncio import gather
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Multiselect, Button, Cancel, ScrollingGroup
from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_connection, User, UserChannelAssociation
from parsers.channels import channels_names


channels = tuple((cid, cname) for cid, cname in channels_names.items())


class SubscriptionsDialogSG(StatesGroup):
    main = State()


async def getter(**_):
    return {'channels': channels}


@async_connection
async def on_start(session: AsyncSession, _, dialog_manager: DialogManager, **kwargs):
    subs_widget: Multiselect = dialog_manager.dialog().find('subscriptions')

    stmt = select(User).filter_by(
        telegram_id=dialog_manager.event.from_user.id
    ).options(selectinload(User.channels))
    u = await session.scalar(stmt)
    current_channels = [c.id for c in u.channels]

    dialog_manager.dialog_data.update(current_channels=current_channels, user_id=u.id)

    await gather(*[subs_widget.set_checked(
        event=dialog_manager.event, item_id=cid, checked=True, manager=dialog_manager
    ) for cid in current_channels])


@async_connection
async def on_click(session: AsyncSession, cq: CallbackQuery, button: Button, dialog_manager: DialogManager):
    current_channels = set(dialog_manager.dialog_data['current_channels'])
    user_id = dialog_manager.dialog_data['user_id']
    subs_widget: Multiselect = dialog_manager.dialog().find('subscriptions')
    new_channels = set(map(int, subs_widget.get_checked(dialog_manager)))

    channels_to_remove = current_channels - new_channels
    channels_to_add = new_channels - current_channels

    session.add_all([UserChannelAssociation(user_id=user_id, channel_id=cid) for cid in channels_to_add])
    remove_stmt = delete(UserChannelAssociation).filter_by(
        user_id=user_id).filter(UserChannelAssociation.channel_id.in_(channels_to_remove))
    await session.execute(remove_stmt)
    await session.commit()
    await dialog_manager.done()


main_window = Window(
    Const('Пожалуйста, выберите каналы, уведомления о важных новостях в которых Вы хотели бы получать'),
    ScrollingGroup(
        Multiselect(
            Format('✅ {item[1]}'),
            Format('❌ {item[1]}'),
            id='subscriptions',
            items='channels',
            item_id_getter=operator.itemgetter(0),
        ),
        id='subs_channels',
        width=1,
        height=7,
    ),
    Button(Const('✅ Подтвердить'), id='subs_confirm', on_click=on_click),
    Cancel(Const('❌ Назад'), id='subs_cancel'),
    state=SubscriptionsDialogSG.main,
    getter=getter,
)

subscriptions_dialog = Dialog(main_window, on_start=on_start)
