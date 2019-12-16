from flask import Blueprint, request, current_app

from model.Client import Client

from cache.index import Cache

from client.auth import Auth

from controller.account.auth import token_decode

service_auth = Blueprint('service_auth',__name__)

@service_auth.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@service_auth.route('/send_code/<phone>/<_type>',methods=['POST'])
def send_code(phone,_type):

	if not phone:
		
		return { "success":False,"msg":"请输入手机号" }

	if not _type:
		
		return { "success":False,"msg":"请输入客户端类型" }

	key = "auth-code-"+str(phone)

	Cache.delete(key)

	auth_obj = Auth(phone)

	ret = auth_obj.auth()

	if ret["success"]:

		client_obj = Client()

		client_obj.insert({"phone":phone,"uid":request.user["_id"],"type":_type})

		print(phone,_type)

	return ret

@service_auth.route('/confirm_code/<phone>/<code>',methods=['POST'])
def confirm_code(phone,code):
	
	if not phone or not code:
		
		return { "success":False,"msg":"参数缺失" }

	key = "auth-code-"+str(phone)

	Cache.set(key,code,120)

	return { "success":True,"msg":"发送完成" }