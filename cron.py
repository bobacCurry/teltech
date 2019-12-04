# coding:utf-8

# nohup python3 cron.py>>cron.log 2>&1 &

from apscheduler.schedulers.blocking import BlockingScheduler

import datetime

from client.message import Message

from client.chat import Chat

from model.Push import Push

from model.Queue import Queue

import sys

now = datetime.datetime.now()

def forward(phone,chatid,message_id):
	# 886985027138
	message = Message(phone)
	# CBobac 5218
	ret = message.forward_message(chatid,'me',message_id)

	print(ret)

# 在队列中添加任务
def add_job():

	now = datetime.datetime.now()

	minute = now.minute

	print(minute)

# 执行并且消除队列中的任务
def clear_job():
	
	print(22222)

scheduler = BlockingScheduler()

scheduler.add_job(func=add_job, trigger='cron', minute='*')

scheduler.add_job(func=clear_job, trigger='cron', second='*/5')

scheduler.start()