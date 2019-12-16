from model.Base import Base

from datetime import datetime
# 手机客户端
class Client(Base):
	
	def __init__(self):

		Base.__init__(self,'Client')

		self.scheme = {
			# 手机号
			"phone":0,
			# 用户id
			"uid":"",
			# 群类型
			"type":0,
			# tg的用户名
			"name":"",
			# 状态 0 未开启 1 开启正常 2 spam 3 banned
			"status":0,
			#是否被服务占用
			"used":0
		}

		self.timeStamp = False