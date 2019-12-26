from model.Base import Base

class AddChat(Base):
	
	def __init__(self):

		Base.__init__(self,'Chat')

		self.scheme = {
			# 实例
			phone:'',
			# 准备加入
			chatids:[],
			# 加入成功
			success:[],
			# 加入失败
			fail:[],
			# 0需要加入 1已经加完
			status:0
		}

		self.timeStamp = False