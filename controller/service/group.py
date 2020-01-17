# 群组管理服务

from flask import Blueprint, request, current_app

from time import time

from client.group import Group

from controller.account.auth import token_decode

service_group = Blueprint('service_group',__name__)

def get_chat(chatid):
	
	pass

@service_group.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@service_group.route('/create_group',methods=['POST'])
def create_group():

	group = Group()

	return '111111'

@service_group.route('/get_chat_info/<chatid>',methods=['GET'])
def get_chat_info(chatid):
	
	pass

@service_group.route('/update_chat_username/<chatid>/<username>',methods=['POST'])
def update_chat_username(chatid,username):

	pass

@service_group.route('/export_chat_invite_link/<chatid>',methods=['POST'])
def export_chat_invite_link(chatid):

	pass

@service_group.route('/set_chat_photo/<chatid>',methods=['POST'])
def set_chat_photo(chatid):

	pass

@service_group.route('/set_chat_title/<chatid>',methods=['POST'])
def set_chat_title(chatid):

	pass

@service_group.route('/set_chat_description/<chatid>',methods=['POST'])
def set_chat_description(chatid):

	pass

@service_group.route('/set_chat_permissions/<chatid>',methods=['POST'])
def set_chat_permissions(chatid):

	pass

@service_group.route('/get_chat_members/<chatid>/<offset>/<limit>/<filter>',methods=['GET'])
def get_chat_members(chatid,offset,limit,filter):

	pass

@service_group.route('/get_chat_members_count/<chatid>',methods=['GET'])
def get_chat_members_count(chatid):

	pass

@service_group.route('/add_chat_members/<chatid>',methods=['GET'])
def add_chat_members(chatid):

	pass
