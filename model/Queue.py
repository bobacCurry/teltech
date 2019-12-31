# push队列
from model.Base import Base

class Queue(Base):
	
	def __init__(self):

		Base.__init__(self,'Queue')

		self.scheme = {
			# 手机号
			"phone":"",
			# chatid
			"chat":[],
			# 需要forward的message
			"message_id":0,

			"text_type":0,

			"text":'',

			"media":'',

			"caption":''
		}

		self.timeStamp = False


		