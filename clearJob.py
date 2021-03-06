from cronrunner.index import Index

from model.Queue import Queue

from model.Client import Client

from model.Queue import Queue

from model.Push import Push

import datetime

import logging

from client.message import Message

import sys

import signal

import time

import timeout_decorator

client_obj = Client()

queue_obj = Queue()

push_obj = Push()

def logger(info):
	
	today=datetime.date.today()

	filename = 'log/'+'cron'+'-'+str(today)+'.log'

	logging.basicConfig(level=logging.INFO,filename=filename,format='%(asctime)s - %(message)s')
	
	logging.info(info)

	return

@timeout_decorator.timeout(60, use_signals=False)
def forward(phone,chatids,message_id):
	
	message = Message(phone)

	log = str(phone)

	notin = []

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

				client_obj.update({'phone':phone},{'status':4})

				push_obj.update({'phone':phone},{'status':0})

				break

			elif ('[403 CHAT_WRITE_FORBIDDEN]' in ret["msg"]) or ('Username not found' in ret["msg"]):

				notin.append(chatid)

	if len(notin):
		
		push_obj.updateSelf({'phone':phone},{'$pull':{'chat':{'$in':notin}}})

	logger(log)

	return

def clear():
	
	queue = queue_obj.findOne({})

	if queue:

		queue_obj.remove({"_id":queue["_id"]})

		try:

			forward(queue["phone"],queue["chat"],queue["message_id"])
		
		except Exception as e:
			
			logger(str(e)+'---'+queue["phone"])
	return

clear()

sys.exit()