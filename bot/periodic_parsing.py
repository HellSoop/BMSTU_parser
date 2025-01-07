from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

tz = timezone('Europe/Moscow')

executors = {
    'default': ProcessPoolExecutor()
}
periodic_parsing_scheduler = AsyncIOScheduler(executors=executors, timezone=tz)


def foobar():
    print(foobar.counter)
    foobar.counter += 1


foobar.counter = 0

periodic_parsing_scheduler.add_job(foobar, trigger='cron', second='*/5')
