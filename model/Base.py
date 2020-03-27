from pymongo import MongoClient

from datetime import datetime

from bson import ObjectId

from env import dbuser,dbpassword,dburl,dbport,dbname

if dbuser:
	
	url = "mongodb://"+dbuser+':'+dbpassword+'@'+dburl+":"+dbport+"/"

else:

	url = "mongodb://"+dburl+":"+dbport+"/"

client = MongoClient(url)[dbname]

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

		data_filter = data
			
		for key in data:
			
			if key=='_id':
				
				data_filter[key] = ObjectId(data_filter[key])

		return data_filter

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

	def find(self,query,projection=None,skip=None,limit=None,sort=None):

		try:
			
			query = self.id_to_obj(query)

			data = self.db.find(query,projection)

			if skip:
				
				data.skip(skip)

			if limit:
				
				data.limit(limit)

			if sort:

				print(sort)

				data.sort(sort)

			data_filter = self.id_to_str(data)

			return data_filter
		
		except Exception as e:
			
			return []

	def findOne(self,query,projection=None):

		try:
			
			query = self.id_to_obj(query)

			data = self.db.find_one(query,projection)

			data["_id"] = str(data["_id"])

			return data

		except Exception as e:
			
			return ''

	def remove(self,query):

		query = self.id_to_obj(query)

		try:

			self.db.remove(query)

			return { "success":True, "msg":"删除成功" }

		except Exception as e:
			
			return { "success":False, "msg":str(e) }

	def update(self,query,document):

		query = self.id_to_obj(query)

		try:

			self.db.update(query,{"$set":document},False,True)

			return { "success":True, "msg":"更新成功" }

		except Exception as e:

			return { "success":False, "msg":str(e) }

	def updatePush(self,query,document):

		query = self.id_to_obj(query)

		try:

			self.db.update(query,{"$push":document},False,True)

			return { "success":True, "msg":"更新成功" }

		except Exception as e:

			return { "success":False, "msg":str(e) }

	def updateSelf(self,query,document):

		query = self.id_to_obj(query)

		try:

			self.db.update(query,document,False,True)

			return { "success":True, "msg":"更新成功" }

		except Exception as e:

			return { "success":False, "msg":str(e) }