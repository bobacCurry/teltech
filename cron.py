# coding:utf-8

# nohup python3 cron.py>>cron.log 2>&1 &

from apscheduler.schedulers.blocking import BlockingScheduler

import datetime

from client.message import Message

from client.chat import Chat

from client.user import User

from model.Push import Push

from model.Queue import Queue

import sys

now = datetime.datetime.now()

clearing = False

def forward(phone,chatid,message_id):
	
	message = Message(phone)
	
	ret = message.forward_message(chatid,'me',message_id)

	print(ret)

# 在队列中添加任务
def add_job():

	now = datetime.datetime.now()

	minute = now.minute

	push = Push()

	queue = Queue()

	pushs = push.find({"minute":minute,"message_id":{"$ne":0},"status":1})

	for push in pushs:

		queue.insert({"phone":push["phone"],"chat":push["chat"],"message_id":push["message_id"]})

# 执行并且消除队列中的任务
def clear_job():

	global clearing

	if not clearing:

		clearing = True
		
		queue_obj = Queue()

		queue = queue_obj.findOne({})

		if queue:

			for chatid in queue["chat"]:
				
				forward(queue["phone"],chatid,queue["message_id"])

			queue_obj.remove({"_id":queue["_id"]})

		clearing = False

# 自动加群 
def add_chat():
	
	print(1111)

scheduler = BlockingScheduler()

scheduler.add_job(func=add_job, trigger='cron', minute='*')

scheduler.add_job(func=clear_job, trigger='cron', second='*/2')

scheduler.add_job(func=add_chat, trigger='cron', minute='*/15')

scheduler.start()