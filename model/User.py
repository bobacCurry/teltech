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

		if self.timeStamp :
			
			timeStamp  = { "created_at":datetime.now(),"updated_at":datetime.now() }

			doc = dict(doc, **timeStamp)

		try:
			
			exist = self.db.find_one({"account": document['account']})

			if exist :

				return { "success":False, "msg":'账号已尽注册过' }				

			self.db.insert_one(doc)

			return {"success":True}

		except Exception as e:
			
			return { "success":False, "msg":str(e) }

	def find_one(self,query):
			
		try:
			
			msg = self.db.find_one(query,{ "password":0, "status":0, "created_at":0, "updated_at":0 })
			
			if not msg:
				
				return { "success":False, "msg":"用户信息不存在" }

			msg['_id'] = str(msg['_id'])

			return { "success":True, "msg":msg }

		except Exception as e:

			return { "success":False, "msg":str(e) }


