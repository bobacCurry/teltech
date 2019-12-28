from client.index import Index

class Check:

	def __init__(self,phone):

		Index.__init__(self,phone)

	def authCheck(self):
		
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		return { "success":True,"msg":"已经登陆" }


	def __del__(self):

		self.app.disconnect()