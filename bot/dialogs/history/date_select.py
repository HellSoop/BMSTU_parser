from asyncio import gather
from datetime import date, timedelta
from pytz import timezone
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Calendar, CalendarUserConfig, CalendarScope
from aiogram_dialog.widgets.kbd.calendar_kbd import (CalendarScopeView, CalendarDaysView,
                                                     CalendarMonthView, CalendarYearsView)

from aiogram.types import CallbackQuery
from bot.dialogs.history.states import HistoryDialogSG
from sqlalchemy import select
from database import async_session, Post
from bot.utils.post_utils import send_post

tz = timezone('Europe/Moscow')
months = {
    'January': 'Январь', 'February': 'Февраль', 'March': 'Март', 'April': 'Апрель',
    'May': 'Май', 'June': 'Июнь', 'July': 'Июль', 'August': 'Август',
    'September': 'Сентябрь', 'October': 'Октябрь', 'November': 'Ноябрь', 'December': 'Декабрь',
}
weekdays = {'Mon': 'Пн', 'Tue': 'Вт', 'Wed': 'Ср', 'Thu': 'Чт', 'Fri': 'Пт', 'Sat': 'Сб', 'Sun': 'Вс'}


class MonthLocalizedFormat(Format):
    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        assert 'date' in data, "Missing 'date' key"
        res = await super()._render_text(data, manager)

        format_month = data['date'].strftime('%B')
        return res.replace(format_month, months[format_month])


class DayLocalizedFormat(Format):
    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        assert 'date' in data, "Missing 'date' key"
        res = await super()._render_text(data, manager)

        format_weekday = data['date'].strftime('%a')
        return res.replace(format_weekday, weekdays[format_weekday])


class LocalizedCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                today_text=Format("🔴 {date:%d}"),
                weekday_text=DayLocalizedFormat("{date:%a}"),
                header_text=MonthLocalizedFormat("🗓 {date:%B %Y}"),
                next_month_text=MonthLocalizedFormat("{date:%B %Y} ⏩"),
                prev_month_text=MonthLocalizedFormat("⏪ {date:%B %Y}"),
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                month_text=MonthLocalizedFormat("{date:%B}"),
                this_month_text=MonthLocalizedFormat('🔴 {date:%B}'),
                header_text=MonthLocalizedFormat("🗓 {date:%Y}"),
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
                this_year_text=Format("🔴 {date:%Y}")
            ),
        }

    async def _get_user_config(self, data: dict, manager: DialogManager) -> CalendarUserConfig:
        return CalendarUserConfig(timezone=tz)


async def on_date_select(cq: CallbackQuery, widget: Calendar, dialog_manager: DialogManager, selected_date: date):
    if 'start_date' not in dialog_manager.dialog_data:  # first click
        dialog_manager.dialog_data.update(start_date=selected_date)
        return

    # second click
    start_date = dialog_manager.dialog_data['start_date']
    end_date = selected_date + timedelta(days=1)  # we will include selected date
    channel_id = dialog_manager.dialog_data['channel_id']
    channel_name = dialog_manager.dialog_data['channel_name']

    if selected_date == start_date:
        posts_header_message_text = f'Посты из канала <u>"{channel_name}"</u> за <b>{start_date:%d.%m.%Y}</b>:'
    else:
        posts_header_message_text = (f'Посты из канала <u>"{channel_name}"</u> '
                                     f'с <b>{start_date:%d.%m.%Y}</b> по <b>{selected_date:%d.%m.%Y}</b>:')

    async with async_session() as session:
        stmt = select(Post.url).order_by(Post.date).filter_by(
            channel_id=channel_id).filter(Post.date.between(start_date, end_date))

        posts_urls = (await session.scalars(stmt)).all()

    await dialog_manager.done()
    await cq.message.answer(posts_header_message_text, parse_mode='HTML')
    await gather(*[send_post(cq.from_user.id, url, channel_id) for url in posts_urls])


date_select_window = Window(
    Const('Пожалуйста, первый и последний дни, посты за которые хотите получить'),
    LocalizedCalendar(id='his_datesel', on_click=on_date_select),
    state=HistoryDialogSG.date_select,
)
