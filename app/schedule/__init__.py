from apscheduler.schedulers.background import BackgroundScheduler as _BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .roll_call_absent import roll_call_absent


_scheduler = _BackgroundScheduler()


def start():
    _scheduler.start()
    _scheduler.add_job(roll_call_absent, trigger=CronTrigger(
        minute='55',
        hour='23',
        day='*',
        month='*',
        year='*',
        timezone='Asia/Tashkent'
    ))


def stop():
    _scheduler.shutdown()
