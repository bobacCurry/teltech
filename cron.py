# coding:utf-8

# nohup python3 cron.py>>cron.log 2>&1 &

from apscheduler.schedulers.blocking import BlockingScheduler

import datetime

from client.message import Message

from client.chat import Chat

import sys

now = datetime.datetime.now()

def forward():
	
	message = Message('886985027138')

	ret = message.forward_message('CBobac','me',5218)

	print(ret)

def add_job():

	print(11111)

def clear_job():
	
	print(22222)

scheduler = BlockingScheduler()

scheduler.add_job(func=add_job, trigger='cron', minute='*')

scheduler.add_job(func=clear_job, trigger='cron', second='*/5')

scheduler.start()