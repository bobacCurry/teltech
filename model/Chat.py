from model.Base import Base

from datetime import datetime
# 群组
class Chat(Base):
	
	def __init__(self):

		Base.__init__(self,'Chat')

		self.scheme = {
			# 群类型
			"type":0,
			# 群名称
			"chatid":0,
			# 服务状态
			"status":0
		}

		self.timeStamp = True

	def insert_one(self,document):

		