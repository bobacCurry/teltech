from model.Base import Base

# 手机客户端
class Client(Base):
	
	def __init__(self):

		Base.__init__(self,'Client')

		self.scheme = {
			# 手机号
			"phone":0,
			# 用户id
			"uid":"",
			# tg的用户名
			"name":"",
			# 状态 1 开启正常 2 spam 3 banned
			"status":1,
			#是否被服务占用
			"used":0
		}

		self.timeStamp = False