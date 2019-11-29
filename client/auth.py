from pyrogram import Client

from config.client import APIID,APIHASH

from cache.index import Cache

from time import sleep

class Auth:

	def __init__(self, phone):

		self.app = Client(phone,APIID,APIHASH,workdir='./session/',phone_number=phone)

		self.phone_code_hash = None

		self.phone_number = phone

	def auth(self):

		is_authorized = self.app.connect()

		if not is_authorized:
			
			ret = self.send_code()

			if not ret["success"]:
				
				return ret

			num = 0

			while num < 60:

				key = "auth-code-"+str(self.phone_number)

				if Cache.get(key):

					ret = self.sign_in(Cache.get(key).decode())				

					if ret["success"]:
						
						return {"success":True,"msg":"验证成功"}

					else:

						return ret

				num+=1

				sleep(1)

			return {"success":False,"msg":"验证失败"}

		return {"success":False,"msg":"已经通过认证"}
	
	def send_code(self):

		try:

			ret = self.app.send_code(self.phone_number)

			self.phone_code_hash = ret["phone_code_hash"]

			return {"success":True,"msg":"验证码发送成功"}
		
		except Exception as e:

			print(e,111111)
			
			return {"success":False,"msg":str(e)}

	def sign_in(self,phone_code):
		
		try:

			ret = self.app.sign_in(self.phone_number,self.phone_code_hash,phone_code)

			print(ret,2222)

			return {"success":True,"msg":ret}

		except Exception as e:

			print(e,33333)

			return {"success":False,"msg":str(e)}
			
	def __del__(self):

		self.app.disconnect()