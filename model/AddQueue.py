from model.Base import Base

class AddQueue(Base):
	
	def __init__(self):

		Base.__init__(self,'AddQueue')

		self.scheme = {

			'aid':'',
			# 下一次执行时间
			'nexttime':0
		
		}

		self.timeStamp = False