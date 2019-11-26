from model.Base import Base

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
			"type":1,
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