from cronrunner.index import Index

from model.Push import Push

from model.Queue import Queue

from model.AddChat import AddChat

from model.Client import Client

import datetime

import time

class Group(Index):

	def __init__(self):

		super().__init__()

		self.clearing = False

		self.client_obj = Client()

		self.push_obj = Push()

		self.queue_obj = Queue()

		self.add_obj = AddChat()

	def forward(self,phone,chatids,message_id):
		
		message = self.message(phone)

		log = str(phone)

		for chatid in chatids:
			
			ret = message.forward_message(chatid,'me',message_id)

			if ret['success']:
				
				log = log + '-' + chatid + '（success）'

			else:

				log = log + '-' + chatid + '（' + ret['msg'] + '）'

				if 'check @SpamBot' in ret['msg']:
					
					self.client_obj.update({'phone':phone},{'status':2})

					self.push_obj.update({'phone':phone},{'status':0})

					break

		self.logger(log)

	def send_text(self,phone,chatids,text):
		
		message = self.message(phone)

		log = str(phone)

		for chatid in chatids:
			
			ret = message.send_message(chatid,text)

			if ret['success']:
				
				log = log + '-' + chatid + '（success）'

			else:

				log = log + '-' + chatid + '（' + ret['msg'] + '）'

				if 'check @SpamBot' in ret['msg']:
					
					self.client_obj.update({'phone':phone},{'status':2})

					self.push_obj.update({'phone':phone},{'status':0})

					break

		self.logger(log)

	def send_media(self,phone,chatids,media,caption):
		
		message = self.message(phone)

		log = str(phone)

		for chatid in chatids:
			
			ret = message.send_photo(chatid,media,caption)

			if ret['success']:
				
				log = log + '-' + chatid + '（success）'

			else:

				log = log + '-' + chatid + '（' + ret['msg'] + '）'

				if 'check @SpamBot' in ret['msg']:
					
					self.client_obj.update({'phone':phone},{'status':2})

					self.push_obj.update({'phone':phone},{'status':0})

					break

		self.logger(log)

	# 在队列中添加任务
	def add_job(self):

		now = datetime.datetime.now()

		minute = now.minute

		# minute1 = minute + 1

		# minute2 = minute + 2
			
		# if minute==58:
			
		# 	minute2 = 0

		# if minute==59:
			
		# 	minute1 = 0

		# 	minute2 = 1

		# # 将群分割
		# slice_num = 30

		# pushs1 = self.push_obj.find({"minute":minute,"message_id":{"$ne":0},"status":1},{"phone":1,"chat":{"$slice":slice_num},"message_id":1,"text_type":1,"text":1,"media":1,"caption":1})

		# pushs2 = self.push_obj.find({"minute":minute1,"message_id":{"$ne":0},"count":{"$gt":slice_num*1},"status":1},{"phone":1,"chat":{"$slice":[slice_num*1,slice_num]},"message_id":1,"text_type":1,"text":1,"media":1,"caption":1})

		# pushs3 = self.push_obj.find({"minute":minute2,"message_id":{"$ne":0},"count":{"$gt":slice_num*2},"status":1},{"phone":1,"chat":{"$slice":[slice_num*2,slice_num]},"message_id":1,"text_type":1,"text":1,"media":1,"caption":1})

		# pushs = pushs1 + pushs2 + pushs3

		pushs = self.push_obj.find({"minute":minute,"message_id":{"$ne":0},"status":1},{"phone":1,"chat":1,"message_id":1,"text_type":1,"text":1,"media":1,"caption":1})

		for push in pushs:

			self.queue_obj.insert({"phone":push["phone"],"chat":push["chat"],"message_id":push["message_id"],"text_type":push["text_type"],"text":push["text"],"media":push["media"],"caption":push["caption"]})

		self.logger(str(minute) + '分任务添加')

	# 执行并且消除队列中的任务
	def clear_job(self):

		if not self.clearing:

			self.clearing = True

			queue = self.queue_obj.findOne({})

			if queue:
				
				if queue["text_type"]==1 and queue["media"]!='':
					
					self.send_media(queue["phone"],queue["chat"],queue["media"],queue["caption"])

				else :

					if queue["text_type"]==0 and queue["text"]!='':

						self.send_text(queue["phone"],queue["chat"],queue["text"])

				# self.forward(queue["phone"],queue["chat"],queue["message_id"])

				self.queue_obj.remove({"_id":queue["_id"]})

			self.clearing = False

	def join_chat(self):

		add_list = self.add_obj.find({'status':0})

		if len(add_list):

			for add_item in add_list:
				
				ret = self.add_runner(add_item)

				self.logger(ret['msg'])

		self.logger('添加群任务完成')

	def add_runner(self,add_item):

		success = add_item['success']

		fail = add_item['fail']

		removeids = []

		chat = self.chat(add_item['phone'])

		auth = chat.authCheck()

		if not auth['success']:
			
			msg = '客户端验证失败'

			self.add_obj.update({'_id':add_item['_id']},{'status':-1,'msg':msg})

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
			
			self.add_obj.update({'_id':add_item['_id']},{'chatids':chatids,'success':success,'fail':fail})

		else:

			self.add_obj.update({'_id':add_item['_id']},{'chatids':chatids,'success':success,'fail':fail,'msg':'执行完毕','status':1})

		return {'success':True,'msg':add_item['phone']+'加群执行完毕'}