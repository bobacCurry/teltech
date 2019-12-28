from client.index import Index

class Message:

	def __init__(self,phone):

		Index.__init__(self,phone)

	def send_message(self,chat_id,text,parse_mode="html"):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chat_id or not text:
			
			return { "success":True,"msg":"群组id或文本不存在" }

		try:
			
			ret = self.app.send_message(chat_id,text,parse_mode)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }


	def send_photo(self,chat_id,photo,caption):
		
		try:

			ret = self.app.send_photo(chat_id, photo, caption=caption)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }


	def forward_message(self,chat_id,from_chat_id,message_ids):
		
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chat_id or not from_chat_id or not message_ids:
			
			return { "success":True,"msg":"转发信息缺失" }

		try:
			
			ret = self.app.forward_messages(chat_id,from_chat_id,message_ids)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }
		


	def __del__(self):

		self.app.disconnect()