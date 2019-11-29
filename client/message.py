from client.index import Index

class Message:

	def __init__(self,phone):

		Index.__init__(self,phone)

	def send_message(self,chat_id,text,parse_mode="html"):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端未验证" }

		if not chat_id or not text:
			
			return { "success":True,"msg":ret }

		try:
			
			ret = self.app.send_message(chat_id,text,parse_mode)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }

	def __del__(self):

		self.app.disconnect()