from client.index import Index

class User:

	def __init__(self,phone):

		Index.__init__(self,phone)

	def getMe(self):
		
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		try:
			
			ret = self.app.get_me()

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }