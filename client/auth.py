from pyrogram import Client

from config.client import APIID,APIHASH

from cache.index import Cache

from time import sleep

from model.Proxy import Proxy

from client.proxyTest import ProxyTest

import random

class Auth:

	def __init__(self,phone,proxy_enable=None):

		proxy = None

		if proxy_enable:

			proxy_obj = Proxy()
			
			count = proxy_obj.count()

			if count:

				skip = random.randint(0,count-1)

				print(skip)

				proxy_list = proxy_obj.find({},skip=skip,limit=1,sort='ping')

				if len(proxy_list):
					
					test_obj = ProxyTest(proxy_list[0]['ip'],proxy_list[0]['port'])

					test_ret = test_obj.Check()

					if test_ret['success']:
						
						proxy = dict(hostname=proxy_list[0]['ip'],port=proxy_list[0]['port'])

					else:

						proxy_obj.remove({'_id':proxy_list[0]['_id']})

		print(proxy)

		self.app = Client(phone,APIID,APIHASH,workdir='./session/',phone_number=phone,proxy=proxy)

		self.phone_code_hash = None

		self.phone_number = phone

	def auth(self):

		is_authorized = self.app.connect()

		if not is_authorized:
			
			ret = self.send_code()

			if not ret["success"]:
				
				return ret

			num = 0

			while num < 120:

				key = "auth-code-"+str(self.phone_number)

				if Cache.get(key):

					ret = self.sign_in(Cache.get(key).decode())				

					return ret

				num+=1

				sleep(1)

			return {"success":False,"msg":"时间超时，验证失败"}

		return {"success":True,"msg":"已经通过认证"}
	
	def send_code(self):

		try:

			ret = self.app.send_code(self.phone_number)

			self.phone_code_hash = ret["phone_code_hash"]

			return {"success":True,"msg":"验证码发送成功"}
		
		except Exception as e:
			
			return {"success":False,"msg":str(e)}

	def sign_in(self,phone_code):
		
		try:

			ret = self.app.sign_in(self.phone_number,self.phone_code_hash,phone_code)

			return {"success":True,"msg":ret}

		except Exception as e:

			if str(phone_code)=='1111':
				
				return {"success":False,"msg":"取消验证"}

			return {"success":False,"msg":str(e)}
	
	def logout(self):
		
		try:

			ret = self.app.log_out()

			return {"success":True,"msg":"实例已退出"}
		
		except Exception as e:
			
			return {"success":False,"msg":str(e)}		

	def __del__(self):

		self.app.disconnect()