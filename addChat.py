from model.AddChat import AddChat

from model.Client import Client

from client.chat import Chat

import datetime

import time

import logging

import sys

add_obj = AddChat()

def logger(info):
	
	today=datetime.date.today()

	filename = 'log/'+'cron'+'-'+str(today)+'.log'

	logging.basicConfig(level=logging.INFO,filename=filename,format='%(asctime)s - %(message)s')
	
	logging.info(info)


def add_runner(add_item):

	success = add_item['success']

	fail = add_item['fail']

	removeids = []

	chat = Chat(add_item['phone'])

	auth = chat.authCheck()

	if not auth['success']:
		
		msg = '客户端验证失败'

		add_obj.update({'_id':add_item['_id']},{'status':-1,'msg':msg})

		return {'success':False,'msg':msg}
	
	count = 0

	for chatid in add_item['chatids']:

		if count>=5:
			
			break

		ret = chat.join_chat(chatid)

		if '[420 FLOOD_WAIT_X]' in ret['msg']:

			break

		if ret['success']:
			
			success.append(chatid)

			count=count+1

			time.sleep(5)

		else:

			fail.append(chatid)

		removeids.append(chatid)

	chatids = [x for x in add_item['chatids'] if x not in removeids]

	if len(chatids):
		
		add_obj.update({'_id':add_item['_id']},{'chatids':chatids,'success':success,'fail':fail})

	else:

		add_obj.update({'_id':add_item['_id']},{'chatids':chatids,'success':success,'fail':fail,'msg':'执行完毕','status':1})

	return {'success':True,'msg':add_item['phone']+'加群执行完毕'}

add_list = add_obj.find({'status':0})

if len(add_list):

	for add_item in add_list:
		
		ret = add_runner(add_item)

		logger(ret['msg'])

logger('添加群任务完成')

sys.exit()