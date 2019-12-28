# nohup python3 index.py>>flask_run.log 2>&1 &
from apscheduler.schedulers.blocking import BlockingScheduler

from cronrunner.group import Group

group = Group()

scheduler = BlockingScheduler()

scheduler.add_job(func=group.add_job, trigger='cron', minute='*')

scheduler.add_job(func=group.clear_job, trigger='cron', second='*/2')

scheduler.add_job(func=group.join_chat, trigger='cron', minute='*/5')

scheduler.start()