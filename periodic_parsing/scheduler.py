from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from .parse_function import do_periodic_parsing

tz = timezone('Europe/Moscow')

executors = {
    'default': ProcessPoolExecutor()
}
periodic_parsing_scheduler = AsyncIOScheduler(executors=executors, timezone=tz)

periodic_parsing_scheduler.add_job(do_periodic_parsing, trigger='cron', second='*/5')
