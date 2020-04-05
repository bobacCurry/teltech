from pyrogram import Client

from config.client import APIID,APIHASH

from datetime import timedelta, datetime

from model.Proxy import Proxy

from client.proxyTest import ProxyTest

import random

class Index:

	def __init__(self,phone,proxy_enable=None):

		proxy = None

		if proxy_enable:

			proxy_obj = Proxy()
			
			proxy_list = proxy_obj.find({},limit=1,sort='ping')

			if len(proxy_list):
				
				test_obj = ProxyTest(proxy_list[0]['ip'],proxy_list[0]['port'])

				test_ret = test_obj.Check()

				if test_ret['success']:
					
					proxy = dict(hostname=proxy_list[0]['ip'],port=proxy_list[0]['port'])

				else:

					proxy_obj.remove({'_id':proxy_list[0]['_id']})

		print(proxy)

		self.app = Client(phone,APIID,APIHASH,workdir='./session/',phone_number=phone,proxy=proxy)

		self.is_authorized = True

		self.phone = phone

		try:

			is_authorized = self.app.connect()

			if not is_authorized:

				self.is_authorized = False

				self.app.disconnect()

			else:

				self.app.disconnect()

				self.app.start()

		except BaseException as e:

			self.is_authorized = False

	def authCheck(self):
		
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		return { "success":True,"msg":"已经登陆" }