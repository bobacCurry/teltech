from pymongo import MongoClient

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