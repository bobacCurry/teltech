# 群组管理服务

from flask import Blueprint, request, current_app

from time import time

from client.group import Group

from model.Group import GroupModel

from model.Client import Client

from controller.account.auth import token_decode

service_group = Blueprint('service_group',__name__)

def get_chat(chatid):
	
	group = Group()

	ret = group.get_chat(chatid)

	return ret

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

	data = request.form or request.get_json()

	try:

		data['title'],data['description'],data['phone']

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	client_obj = Client()

	exist = client_obj.findOne({'uid':request.user['user_id'],'phone':data['phone']})

	if not exist:
		
		return { "success":False, "msg":"tg号不存在" } 

	group = Group(data['phone'])

	ret = group.create_supergroup(data['title'],data['description'])

	if not ret["success"]:

		return ret

	group_obj = GroupModel()

	permissions = {

		'can_send_messages':ret['msg']['permissions']['can_send_messages'],

		'can_send_media_messages':ret['msg']['permissions']['can_send_media_messages'],

		'can_send_other_messages':ret['msg']['permissions']['can_send_other_messages'],

		'can_add_web_page_previews':ret['msg']['permissions']['can_add_web_page_previews'],

		'can_send_polls':ret['msg']['permissions']['can_send_polls'],

		'can_change_info':ret['msg']['permissions']['can_change_info'],

		'can_invite_users':ret['msg']['permissions']['can_invite_users'],

		'can_pin_messages':ret['msg']['permissions']['can_pin_messages'],

	}

	ret1 = group_obj.insert({'uid':request.user['user_id'],'phone':data['phone'],'id':ret['msg']['id'],'title':data['title'],'description':data['description'],'permissions':permissions})

	if not ret1["success"]:
		
		return ret1

	return { "success":True, "msg":"创建成功" } 

@service_group.route('/get_chat_info/<chatid>',methods=['GET'])
def get_chat_info(chatid):
	
	ret = get_chat(chatid)

	return ret

@service_group.route('/update_chat_username/<chatid>/<username>',methods=['POST'])
def update_chat_username(chatid,username):

	group = Group()

	ret = group.update_chat_username(chatid,username)

	return ret

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
