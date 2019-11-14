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

	def insert_one(self,document):
		
		doc = dict(self.scheme, **document)

		print(doc)

		if self.timeStamp :
			
			timeStamp  = { "created_at":datetime.now(),"updated_at":datetime.now() }

			doc = dict(doc, **timeStamp)

		try:
			
			exist = self.client.find_one({"account": document['account']})

			if exist :

				return { "success":False, "msg":'账号已尽注册过' }				

			self.client.insert_one(doc)

			return {"success":True}

		except Exception as e:
			
			return { "success":False, "msg":str(e) }

	def find_one(self,document):
			
		if not document['account'] or not document['password']:
			
			return False

		try:
			
			msg = self.client.find_one({"account": document['account'],"password": document['password'],"status":1},{"password":0,"status":0,"created_at":0,"updated_at":0})
			
			msg['_id'] = str(msg['_id'])

			return { "success":True, "msg":msg }

		except Exception as e:

			return { "success":False, "msg":e }