from model.Push import Push

from model.Queue import Queue

from model.AddChat import AddChat

from model.Client import Client

import logging

import datetime

import time

import sys

def logger(info):
	
	today=datetime.date.today()

	filename = 'log/'+'cron'+'-'+str(today)+'.log'

	logging.basicConfig(level=logging.INFO,filename=filename,format='%(asctime)s - %(message)s')
	
	logging.info(info)

push_obj = Push()

queue_obj = Queue()

now = datetime.datetime.now()

minute = now.minute

# minute1 = minute + 2
	
# if minute==58:
	
# 	minute1 = 0

# if minute==59:
	
# 	minute1 = 1

# 将群分割
# slice_num = 30

# pushs1 = push_obj.find({"minute":minute,"message_id":{"$ne":0},"status":1},{"phone":1,"chat":{"$slice":slice_num},"message_id":1,"text_type":1,"text":1,"media":1,"caption":1})

# pushs2 = push_obj.find({"minute":minute1,"message_id":{"$ne":0},"count":{"$gt":slice_num*1},"status":1},{"phone":1,"chat":{"$slice":[slice_num*1,slice_num]},"message_id":1,"text_type":1,"text":1,"media":1,"caption":1})

# pushs = pushs1 + pushs2

pushs = push_obj.find({"minute":minute,"message_id":{"$ne":0},"status":1},{"phone":1,"chat":1,"message_id":1})

for push in pushs:

	queue_obj.insert({"phone":push["phone"],"chat":push["chat"],"message_id":push["message_id"]})

logger(str(minute) + '分任务添加')

sys.exit()