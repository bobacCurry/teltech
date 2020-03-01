from client.index import Index

class User(Index):

	def __init__(self,phone):

		super().__init__(phone)

	def getMe(self):
		
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		try:
			
			ret = self.app.get_me()

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }

	def __del__(self):

		try:
			
			self.app.stop()
		
		except Exception as e:
			
			print(e)