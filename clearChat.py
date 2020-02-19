from model.AddChat import AddChat

from model.AddQueue import AddQueue

from model.Client import Client

from client.chat import Chat

import datetime

import time

import logging

import sys

add_obj = AddChat()

clear_obj = AddQueue()

def logger(info):
	
	today=datetime.date.today()

	filename = 'log/'+'cron'+'-'+str(today)+'.log'

	logging.basicConfig(level=logging.INFO,filename=filename,format='%(asctime)s - %(message)s')
	
	logging.info(info)


def add_runner(add_item,clear):

	success = add_item['success']

	fail = add_item['fail']

	# removeids = []

	chat = Chat(add_item['phone'])

	auth = chat.authCheck()

	if not auth['success']:
		
		msg = '客户端验证失败'

		add_obj.update({'_id':add_item['_id']},{'status':-1,'msg':msg})

		clear_obj.remove({"_id":clear['_id']})

		return {'success':False,'msg':msg}


	chatid = add_item['chatids'][0]

	ret = chat.join_chat(chatid)

	if '[420 FLOOD_WAIT_X]' in ret['msg']:

		nexttime = int(time.time())+300

		clear_obj.update({'_id':clear['_id']},{'nexttime':nexttime})

		break

	else:

		if ret['success']:
			
			success.append(chatid)

		else:

			fail.append(chatid)
	
	chatids = add_item['chatids'][1:]

	# count = 0

	# for chatid in add_item['chatids']:

	# 	if count>=5:
			
	# 		break

	# 	ret = chat.join_chat(chatid)

	# 	if '[420 FLOOD_WAIT_X]' in ret['msg']:

	# 		nexttime = int(time.time())+300

	# 		clear_obj.update({'_id':clear['_id']},{'nexttime':nexttime})

	# 		break

	# 	else:

	# 		if ret['success']:
				
	# 			success.append(chatid)

	# 			count=count+1

	# 			time.sleep(5)

	# 		else:

	# 			fail.append(chatid)

	# 		removeids.append(chatid)

	# 		clear_obj.remove({"_id":clear['_id']})

	# chatids = [x for x in add_item['chatids'] if x not in removeids]



	if len(chatids):
		
		add_obj.update({'_id':add_item['_id']},{'chatids':chatids,'success':success,'fail':fail})

	else:

		add_obj.update({'_id':add_item['_id']},{'chatids':chatids,'success':success,'fail':fail,'msg':'执行完毕','status':1})

		clear_obj.remove({"_id":clear['_id']})

	return {'success':True,'msg':add_item['phone']+'加群执行完毕'}

def clearQueue():
	
	clear = clear_obj.findOne({'nexttime':{'$lt':time.time()}})
	
	if clear:

		add_item = add_obj.findOne({'_id':clear['aid']})

		if add_item:
			
			ret = add_runner(add_item,clear)

			logger(ret['msg'])

	return 

clearQueue()

del add_obj

del clear_obj

logger('添加群任务完成')

sys.exit()