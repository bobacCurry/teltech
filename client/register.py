from pyrogram import Client

from config.client import APIID,APIHASH,APIKEY

from time import sleep

import requests

import json

import random

import re

class Register:

	def __init__(self,phone,orderId):

		self.app = Client(phone,APIID,APIHASH,workdir='./session/',phone_number=phone)

		self.phone_code_hash = None

		self.phone_number = phone

		self.orderId = orderId

	def auth(self):

		is_authorized = self.app.connect()

		if not is_authorized:
			
			ret = self.send_code()

			if not ret["success"]:
				
				return ret

			num = 0

			while num < 25:

				get_code_url = 'http://www.jindousms.com/public/sms/getCode?orderId='+self.orderId+'&apikey='+APIKEY

				code_ret = requests.get(get_code_url,timeout=10)

				if code_ret.status_code != 200:

					return {"success":False,"msg":"获取验证码失败"}

				text = json.loads(code_ret.text)

				print(text)

				if text["code"] == 1:
			
					code = None

					if text["data"]["code"]:
				
						code = text["data"]["code"]

						if not code:

							content = re.findall(r'\d{5}', text["data"]["content"])

							code = content[0]						

					print(code)

					if code:

						ret = self.sign_in(code)

						return ret

					else:

						return {"success":False,"msg":"获取验证码失败"}

				num+=1

				sleep(3)

			return {"success":False,"msg":"时间超时，注册失败"}

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

			if type(ret).__name__=='TermsOfService':

				_ret = self.sign_up()

				return _ret

			return ret

		except Exception as e:

			if str(phone_code)=='1111':
				
				return {"success":False,"msg":"取消验证"}

			return {"success":False,"msg":str(e)}
	
	def sign_up(self):

		try:

			sleep(10)

			name = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5))

			ret = self.app.sign_up(self.phone_number,self.phone_code_hash,name,'')

			return {"success":True,"msg":ret}

		except Exception as e:

			return {"success":False,"msg":str(e)}		

	def __del__(self):

		self.app.disconnect()