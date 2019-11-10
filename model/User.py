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
		}

		self.timeStamp = True

	def insert_one(self,document):
		
		doc = dict(self.scheme, **document)

		if self.timeStamp :
			
			timeStamp  = { "created_at":datetime.now(),"updated_at":datetime.now() }

			doc = dict(doc, **timeStamp)

		try:
			
			self.client.insert_one(doc)

		except Exception as e:
			
			return False

		return True