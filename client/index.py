from pyrogram import Client

from config.client import APIID,APIHASH

class Index:

	def __init__(self, phone):

		self.app = Client(phone,APIID,APIHASH,workdir='./session/',phone_number=phone)
	
		self.is_authorized = True

		self.phone = phone

		try:
			
			is_authorized = self.app.connect()

			if not is_authorized:

				self.is_authorized = False

		except Exception as e:

			self.is_authorized = False



	def authCheck(self):
		
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		return { "success":True,"msg":"已经登陆" }