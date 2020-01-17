from client.index import Index

from pyrogram import ChatPermissions

class Group(Index):

	def __init__(self,phone):

		super().__init__(phone)

	def create_supergroup(self,title,description=''):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not title or title.strip():
			
			return { "success":True,"msg":"请设置标题" }

		try:
			
			ret = self.app.create_supergroup(title,description)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }


	def delete_supergroup(self,chatid):


		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"请设置标题" }


		try:
			
			ret = self.app.delete_supergroup(chatid)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }


	def get_chat(self,chatid):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"请选择群" }

		try:
			
			ret = self.app.get_chat(chatid)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }

	def update_chat_username(self,chatid,username=None):
		
		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"请选择群" }

		try:
			
			ret = self.app.update_chat_username(chatid,username)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }		


	def export_chat_invite_link(self,chatid):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"设置群名称" }

		try:
			
			ret = self.app.export_chat_invite_link(chatid)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }


	def set_chat_photo(self,chatid,photo):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"设置群名称" }

		if not photo or photo.strip():
			
			return { "success":True,"msg":"设置群头像" }

		try:
			
			ret = self.app.set_chat_photo(chatid,photo)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }


	def set_chat_title(self,chatid,title):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"设置群名称" }

		if not title or title.strip():
			
			return { "success":True,"msg":"设置群名称" }

		try:
			
			ret = self.app.set_chat_title(chatid,title)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }


	def set_chat_description(self,chatid,description):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"设置群名称" }
		
		if not description or description.strip():
			
			return { "success":True,"msg":"设置群描述" }

		try:
			
			ret = self.app.set_chat_description(chatid)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }


	def set_chat_permissions(self,chatid,can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"设置群名称" }
		
		try:
			
			ret = self.app.set_chat_permissions(chatid,ChatPermissions(can_send_messages,can_send_media_messages,can_send_other_messages))

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }


	def get_chat_members(self,chatid,offset=0,limit=100,filter=None):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"设置群名称" }
		
		try:
			
			ret = self.app.get_chat_members(chatid,offset=offset,limit=limit,filter=filter)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }

	def get_chat_members_count(self,chatid):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"设置群名称" }
		
		try:
			
			ret = self.app.get_chat_members_count(chatid)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }

	def add_chat_members(self,chatid,users = []):

		if not self.is_authorized:
			
			return { "success":False,"msg":"客户端:"+self.phone+"未验证" }

		if not chatid or not chatid.strip():
			
			return { "success":True,"msg":"设置群名称" }

		try:
			
			ret = self.app.add_chat_members(chatid,users)

			return { "success":True,"msg":ret }

		except Exception as e:
			
			return { "success":False,"msg":str(e) }			

	def __del__(self):

		self.app.stop()