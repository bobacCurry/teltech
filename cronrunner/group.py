from cronrunner.index import Index

from model.Push import Push

from model.Queue import Queue

from model.AddChat import AddChat

import datetime

class Group(Index):

	def __init__(self):

		super().__init__()

		self.clearing = False

	def forward(self,phone,chatids,message_id):
		
		message = self.message(phone)

		log = str(phone)

		for chatid in chatids:
			
			ret = message.forward_message(chatid,'me',message_id)

			if ret['success']:
				
				log = log + '-' + chatid + '（success）'

			else:

				log = log + '-' + chatid + '（' + str(ret['msg']) + '）'

		self.logger(log)

	# 在队列中添加任务
	def add_job(self):

		now = datetime.datetime.now()

		minute = now.minute

		push = Push()

		queue = Queue()

		pushs = push.find({"minute":minute,"message_id":{"$ne":0},"status":1})

		for push in pushs:

			queue.insert({"phone":push["phone"],"chat":push["chat"],"message_id":push["message_id"]})

		self.logger(str(minute) + '分任务添加')

	# 执行并且消除队列中的任务
	def clear_job(self):

		if not self.clearing:

			self.clearing = True

			queue_obj = Queue()

			queue = queue_obj.findOne({})

			if queue:
					
				self.forward(queue["phone"],queue["chat"],queue["message_id"])

				queue_obj.remove({"_id":queue["_id"]})

			self.clearing = False

	def add_chat(self):
		
		add_obj = AddChat()

		add_list = add_obj.find({status:0})

		if len(add_list):

			for add_item in add_list:
				
				ret = self.add_runner(add_obj,add_item)

				self.logger(ret['msg'])

		self.logger('添加群任务完成')

	def add_runner(self,add_obj,add_item):

		success = add_item['success']

		fail = add_item['fail']

		chatids = add_item['chatids']

		chat = self.chat(add_item['phone'])

		auth = chat.authCheck()

		if not auth['success']:
			
			msg = '客户端验证失败'

			add_obj.update({'_id':add_item['_id']},{'status':-1,'msg':msg})

			return {'success':False,'msg':msg}
		
		count = 0

		for chatid in add_item['chatids']:

			if count>=5:
				
				break

			chatids.remove(chatid)

			try:

				app.join_chat(chatid)

				success.append(chatid)

				count=count+1

			except Exception as e:

				print(e)
				
				fail.append(chatid)

				continue

			time.sleep(5)

		if len(chatids):
			
			add_obj.update({'_id':add_item['_id']},{'chatids':chatids,'success':success,'fail':fail})

		else:

			add_obj.update({'_id':add_item['_id']},{'chatids':chatids,'success':success,'fail':fail,'status':1})

		return {'success':True,'msg':add_item['phone']+'加群执行完毕'}