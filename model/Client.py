from model.Base import Base

from datetime import datetime
# 手机客户端
class Client(Base):
	
	def __init__(self):

		Base.__init__(self,'Chat')

		self.scheme = {
			# 手机号
			"phone":0,
			# 群类型
			"type":0,
			# 状态
			"status":0
		}

		self.timeStamp = True

	def insert_one(self,document):

		