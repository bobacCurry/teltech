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

@service_push.route('/create_group',methods=['POST'])
def create_group():

	group = Group()

	return '111111'

@service_push.route('/get_chat/<chatid>',methods=['GET'])
def get_chat(chatid):
	
	pass

