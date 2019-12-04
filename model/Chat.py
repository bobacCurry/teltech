from model.Base import Base

from datetime import datetime
# 群组
class Chat(Base):
	
	def __init__(self):

		Base.__init__(self,'Chat')

		self.scheme = {
			# 群类型
			"type":'',
			# 群名称
			"chatid":'',
			# 需要进群验证
			"auth":0,
			# 状态
			"status":0
		}

		self.timeStamp = False