# push队列
from model.Base import Base

from datetime import datetime

class Queue(Base):
	
	def __init__(self):

		Base.__init__(self,'User')

		self.scheme = {
			# 文本类型
			"type":0,
			# 手机号
			"phone":"",
			# chatid
			"chat":[],
			# 需要forward的message
			"message_id":0,
			# 文案
			"text":"",
			# 图片
			"media":"",
			# 介绍
			"caption":""
		}

		self.timeStamp = False


		