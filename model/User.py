from model.Base import Base

from datetime import datetime

class User(Base):
	
	def __init__(self):

		Base.__init__(self,'User')

		self.scheme = {

			"account":"",

			"password":"",

			"username":"",

			"job":"",

			"role":1,

			"money":0,

			"status":1
		}

		self.timeStamp = True