# push队列
from model.Base import Base

from datetime import datetime

class Queue(Base):
	
	def __init__(self):

		Base.__init__(self,'Queue')

		self.scheme = {
			# 手机号
			"phone":"",
			# chatid
			"chat":[],
			# 需要forward的message
			"message_id":0
		}

		self.timeStamp = False


		