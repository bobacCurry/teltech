from flask import Blueprint, request, current_app

from model.Client import Client

from cache.index import Cache

from client.auth import Auth

service_auth = Blueprint('service_auth',__name__)

@service_auth.route('/send_code/<phone>',methods=['POST'])
def send_code(phone):

	if not phone:
		
		return { "success":False,"msg":"请输入手机号" }

	auth_obj = Auth(phone)

	ret = auth_obj.auth()

	return ret

@service_auth.route('/confirm_code/<phone>/<code>',methods=['POST'])
def confirm_code(phone,code):
	
	if not phone or not code:
		
		return { "success":False,"msg":"参数缺失" }

	key = "auth-code-"+str(phone)

	Cache.set(key,code,90)

	return { "success":True,"msg":"发送完成" }