from pymongo import MongoClient

from datetime import datetime

from bson import ObjectId

name = ""

password=""

url="localhost"

port="27017"

dbname="teltech"

print("mongodb://"+url+":"+port+"/"+dbname)

client = MongoClient("mongodb://"+url+":"+port+"/")[dbname]

class Base:
	
	def __init__(self, collection):
		
		self.collection = collection
	
		self.db = client[collection]

	# 将_id字符串化
	def id_to_str(self, data):
		
		data_filter = []

		for x in data:

			x["_id"] = str(x["_id"])
			
			data_filter.append(x)

		return data_filter

	def  id_to_obj(self, data):
		
		for key in data:
			
			if key=='_id':
				
				data[key] = ObjectId(data[key])

		return data

	def insert(self,document):

		doc = dict(self.scheme, **document)

		if self.timeStamp :
				
			timeStamp  = { "created_at":datetime.now(),"updated_at":datetime.now() }

			doc = dict(doc, **timeStamp)

		try:
			
			self.db.insert(doc)

			return {"success":True, "msg":"创建成功"}

		except Exception as e:
			
			return { "success":False, "msg":str(e) }

	def find(self,query):

		data = self.db.find(query,{"created_at":0,"updated_at":0})

		data_filter = self.id_to_str(data)

		return {"success":True,"msg":data_filter}

	def remove(self,query):

		try:
		
			self.db.remove(query)

			return { "success":True, "msg":"删除成功" }

		except Exception as e:
			
			return { "success":False, "msg":str(e) }

	def update(self,query,document):

		try:

			self.db.update(query,{"$set":update})

			return { "success":True, "msg":"更新成功" }

		except Exception as e:

			return { "success":False, "msg":str(e) }