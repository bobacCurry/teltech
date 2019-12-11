from model.Base import Base

from datetime import datetime

class User(Base):
	
	def __init__(self):

		Base.__init__(self,'User')

		self.scheme = {

			"account":"",

			"password":"",

			"avatar":"http://m.imeitou.com/uploads/allimg/2019031709/eoyjh4zwlxd.jpg",

			"name":"",

			"job":"",
			# client admin
			"access":["client"],

			"money":0,

			"status":1
		}

		self.timeStamp = True