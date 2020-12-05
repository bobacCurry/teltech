from flask import Blueprint, request, current_app

from model.Client import Client

from cache.index import Cache

from client.auth import Auth

from client.register import Register

from controller.account.auth import token_decode

import requests

from config.client import APIKEY

import json

service_auth = Blueprint('service_auth',__name__)

@service_auth.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@service_auth.route('/send_code/<phone>',methods=['POST'])
def send_code(phone):

	if not phone:
		
		return { "success":False,"msg":"请输入手机号" },500

	key = "auth-code-"+str(phone)

	Cache.delete(key)

	auth_obj = Auth(phone,True)

	ret = auth_obj.auth()

	if ret["success"]:

		client_obj = Client()

		exist = client_obj.findOne({"phone":phone})

		if not exist:
			
			info = {'username':ret['msg']['username'],'first_name':ret['msg']['first_name'],'is_deleted':ret['msg']['is_deleted']}

			client_obj.insert({"phone":phone,"uid":request.user["user_id"],"status":1,"info":info})

		return { "success":True,"msg":"验证成功" }

	return ret

@service_auth.route('/confirm_code/<phone>/<code>',methods=['POST'])
def confirm_code(phone,code):
	
	if not phone or not code:
		
		return { "success":False,"msg":"参数缺失" },500

	key = "auth-code-"+str(phone)

	Cache.set(key,code,120)

	return { "success":True,"msg":"发送完成" }

@service_auth.route('/get_project',methods=['POST'])
def get_project():

	try:

		get_project_url = 'http://www.jindousms.com/public/project/list?page=1&limit=10&keyword=电报&apikey='+APIKEY

		ret = requests.get(get_project_url,timeout=10)

		if ret.status_code == 200:

			return ret.text

		return {"success":False,"msg":"获取失败"}

	except Exception as e:

		print(e)

		return {"success":False,"msg":str(e)}

@service_auth.route('/register',methods=['POST'])
def register():

	myPid = request.args.get("myPid")

	locale = request.args.get("locale")

	try:

		get_number_url = 'http://www.jindousms.com/public/sms/getNumber?myPid='+myPid+'&locale='+locale+'&apikey='+APIKEY

		ret = requests.get(get_number_url,timeout=10)

		text = json.loads(ret.text)

		if ret.status_code != 200:

			return {"success":False,"msg":"获取手机号失败"}

		if text["code"] != 1:
			
			return {"success":False,"msg":text}

		phone = text["data"]["number"]

		orderId = text["data"]["orderId"]

		register_obj = Register(phone,orderId)

		ret = register_obj.auth()

		release_number_url = 'http://www.jindousms.com/public/sms/releaseNumber?orderId='+orderId+'&apikey='+APIKEY

		ret2 = requests.get(release_number_url,timeout=10)

		print(ret2.text)

		if ret["success"]:

			client_obj = Client()

			exist = client_obj.findOne({"phone":phone})

			if not exist:
				
				info = {'username':ret['msg']['username'],'first_name':ret['msg']['first_name'],'is_deleted':ret['msg']['is_deleted']}

				client_obj.insert({"phone":phone,"uid":request.user["user_id"],"status":1,"info":info})

			return { "success":True,"msg":"注册成功" }

		return ret		

	except Exception as e:

		print(e)

		return {"success":False,"msg":str(e)}

@service_auth.route('/logout/<phone>',methods=['POST'])
def logout(phone):

	auth_obj = Auth(phone)

	ret = auth_obj.logout()

	if ret["success"]:

		client_obj = Client()

		client_obj.remove({"phone":phone})

	return ret

