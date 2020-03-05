from cronrunner.index import Index

from model.Queue import Queue

from model.Client import Client

from model.Queue import Queue

from model.Push import Push

import datetime

import time

import logging

from client.message import Message

import sys

client_obj = Client()

queue_obj = Queue()

push_obj = Push()

def logger(info):
	
	today=datetime.date.today()

	filename = 'log/'+'cron'+'-'+str(today)+'.log'

	logging.basicConfig(level=logging.INFO,filename=filename,format='%(asctime)s - %(message)s')
	
	logging.info(info)

	return

def forward(phone,chatids,message_id):
	
	message = Message(phone)

	log = str(phone)

	for chatid in chatids:

		ret = message.forward_message(chatid,'me',message_id)

		if ret['success']:
			
			log = log + '-' + chatid + '（success）'

		else:

			log = log + '-' + chatid + '（' + ret['msg'] + '）'

			if 'check @SpamBot' in ret['msg']:
				
				client_obj.update({'phone':phone},{'status':2})

				push_obj.update({'phone':phone},{'status':0})

				break

			elif '未验证' in ret["msg"]:

				client_obj.update({'phone':phone},{'status':4,"used":0})

				push_obj.update({'phone':phone},{'status':0})

				break

	logger(log)

	return

def clear():
	
	queue = queue_obj.findOne({})

	if queue:

		queue_obj.remove({"_id":queue["_id"]})

		forward(queue["phone"],queue["chat"],queue["message_id"])

	return

clear()

sys.exit()