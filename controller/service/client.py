# 下订单

from flask import Blueprint, request, current_app

from controller.account.auth import token_decode

from model.Client import Client

from model.Push import Push

from model.AddChat import AddChat

from client.user import User

import os

service_client = Blueprint('service_client',__name__)

@service_client.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }


@service_client.route('/get_user_client',methods=['GET'])
def getUserClient():

	client = Client()

	data = client.find({"uid":request.user["user_id"]})

	return { "success":True, "msg":data }

@service_client.route('/del_user_client/<phone>',methods=['POST'])
def delUserClient(phone):

	client_obj = Client()

	client_exist = client_obj.findOne({'phone':phone,"uid":request.user["user_id"]})

	if not client_exist:
		
		return { "success":False, "msg":"TG账号不存在" }

	push_obj = Push()

	push_exist = push_obj.findOne({'phone':phone,"uid":request.user["user_id"],'status':1})

	if push_exist:
		
		return { "success":False, "msg":"TG账号目前有绑定正在运行的服务，请先停止的服务" }

	ret = client_obj.remove({'phone':phone,"uid":request.user["user_id"]})

	if not ret['success']:
		
		return { "success":False, "msg":ret['msg'] }

	session = './session/'+phone+'.session'

	if os.path.exists(session):

		os.remove(session)

	return { "success":True, "msg":"TG账号已经解除绑定" }

@service_client.route('/get_notused_client',methods=['GET'])
def getNotUsed():
	
	client = Client()

	data = client.find({"uid":request.user["user_id"],"used":0,"status":1})

	return { "success":True, "msg":data }

@service_client.route('/restore/<phone>',methods=['POST'])
def restore(phone):
	
	client = Client()

	data = client.update({'uid':request.user['user_id'],'phone':phone},{'status':1})

	return { "success":True, "msg":data }

@service_client.route('/get_add_chat/<page>',methods=['GET'])
def getAddChat(page):

	limit = 50

	skip = (int(page)-1)*limit

	add_obj = AddChat()

	data = add_obj.find({'uid':request.user['user_id']},skip=skip,limit=limit)

	return {'success':True,'msg':data}

@service_client.route('/get_client/<phone>',methods=['GET'])
def getClient(phone):

	user_obj = User(phone)

	ret = user_obj.getMe()

	if ret['success']:
		
		info = {'id':ret['msg']['id'],'username':ret['msg']['username'],'first_name':ret['msg']['first_name'],'is_deleted':ret['msg']['is_deleted']}

		client = Client()

		client.update({'uid':request.user['user_id'],'phone':phone},{'info':info})

		return { 'success':True,'msg':info }

	else:

		return { 'success':False,'msg':ret['msg'] }

