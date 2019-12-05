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
	# 886985027138
	message = Message(phone)
	# CBobac 5218
	ret = message.forward_message(chatid,'me',message_id)

	print(ret)

# 在队列中添加任务
def add_job():

	now = datetime.datetime.now()

	minute = now.minute

	push = Push()

	queue = Queue()

	pushs = push.find({"minute":minute,"status":1})

	for push in pushs:

		if (str(push['type'])=='1' and push['text']) or (str(push['type'])=='2' and push['media']):

			queue.insert({"type":push["type"],"phone":push["phone"],"chat":push["chat"],"message_id":push["message_id"],"text":push["text"],"media":push["media"],"caption":push["caption"]})

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

scheduler = BlockingScheduler()

scheduler.add_job(func=add_job, trigger='cron', minute='*')

scheduler.add_job(func=clear_job, trigger='cron', second='*/2')

scheduler.start()