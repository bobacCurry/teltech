from client.index import Index

class Chat(Index):

	def __init__(self,phone):

		super().__init__(phone)

	def get_chat(self,chat_id):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chat_id:
			
			return { "success":True,"msg":"chatid不存在" }

		try:
			
			ret = self.app.get_chat(chat_id)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }

	def get_chat_members(self,chat_id,filter1='all'):
		
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chat_id:
			
			return { "success":True,"msg":"chatid不存在" }

		try:
			
			ret = self.app.get_chat_members(chat_id,filter=filter1)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }

	def get_dialogs(self):
			
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		try:
			
			ret = self.app.get_dialogs()

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }

	def join_chat(self,chatid):
		
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		try:
			
			ret = self.app.join_chat(chatid)

			return {'success':True,'msg':chatid}

		except Exception as e:
			
			return {'success':False,'msg':str(e)}

	def __del__(self):

		self.app.disconnect()