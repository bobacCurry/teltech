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

import signal

import time

client_obj = Client()

queue_obj = Queue()

push_obj = Push()

def logger(info):
	
	today=datetime.date.today()

	filename = 'log/'+'cron'+'-'+str(today)+'.log'

	logging.basicConfig(level=logging.INFO,filename=filename,format='%(asctime)s - %(message)s')
	
	logging.info(info)

	return

def set_timeout(num, callback):

    def wrap(func):
    
        def handle(signum, frame):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
    
            raise RuntimeError
    
        def to_do(*args, **kwargs):
    
            try:
    
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
    
                signal.alarm(num)  # 设置 num 秒的闹钟
    
                print('start alarm signal.')
    
                r = func(*args, **kwargs)
    
                print('close alarm signal.')
    
                signal.alarm(0)  # 关闭闹钟
    
                return r
    
            except RuntimeError as e:
    
                callback()
    
        return to_do
    
    return wrap

def after_timeout():  # 超时后的处理函数
    
	log('--------超时退出--------')

	sys.exit()

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


# @set_timeout(60, after_timeout)  # 限时 60 秒超时
def clear():
	
	queue = queue_obj.findOne({})

	if queue:

		queue_obj.remove({"_id":queue["_id"]})

		try:

			forward(queue["phone"],queue["chat"],queue["message_id"])
		
		except Exception as e:
			
			log(str(e))
	return

clear()

sys.exit()