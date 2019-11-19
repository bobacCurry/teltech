from model.Base import Base

from datetime import datetime

import time

class Push(Base):
	
	def __init__(self):

		Base.__init__(self,'Push')

		self.scheme = {
			# 用户id
			"uid":"",
			# 服务类型
			"cat":0,
			# 文本类型
			"type":0,
			# chatid
			"chat":[],
			# 文案
			"text":"",
			# 图片
			"media":"",
			# 介绍
			"caption":"",
			# 发送时间
			"minute":[],
			# 服务状态
			"status":0,
			# 到期时间
			"deadline":0
		}

		self.timeStamp = True

	def insert_one(self,document):

		doc = dict(self.scheme, **document)

		if self.timeStamp :
				
			timeStamp  = { "created_at":datetime.now(),"updated_at":datetime.now() }

			doc = dict(doc, **timeStamp)

		try:
			
			self.db.insert_one(doc)

			return {"success":True, "msg":"创建实例成功"}

		except Exception as e:
			
			return { "success":False, "msg":str(e) }

	def get_one(self,query):

		return '11111'

	def get(self,query):

		return '11111'

	def remove(self,query):

		try:
		
			self.db.remove(query)

			return { "success":True, "msg":"删除成功" }

		except Exception as e:
			
			return { "success":False, "msg":str(e) }

	def update(self,query,update):
		
		return '11111'