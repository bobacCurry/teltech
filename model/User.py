from model.Base import Base

class User(Base):
	
	def __init__(self):

		Base.__init__(self,'User')

		self.scheme = {

			"account":"",

			"password":"",

			"avatar":"http://m.imeitou.com/uploads/allimg/2019031709/eoyjh4zwlxd.jpg",

			"name":"",

			"job":0,
			# client admin
			"access":[],
			# vip
			"vip":0,
			# vip到期时间 
			"vip_expire":0,

			"money":0,

			"status":1
		}

		self.timeStamp = True