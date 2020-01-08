from model.Base import Base

# 代理
class Proxy(Base):
	
	def __init__(self):

		Base.__init__(self,'Proxy')

		self.scheme = {
			
			"hostname":"",
			
			"port":0,

			"username":"",

			"password":"",

			"minute":0,
			
			"status":0
		}

		self.timeStamp = False