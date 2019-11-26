# 广告代发服务

from flask import Blueprint, request, current_app

from model.Client import Client

from model.Order import Order

from model.Push import Push

import time

from bson import ObjectId

from controller.account.auth import token_decode

push = Blueprint('push',__name__)

@push.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@push.route('/get',methods=['GET'])
def get():

	push = Push()

	data = push.find({"uid":request.user['_id']})

	return data

@push.route('/add',methods=['POST'])
def add():

	data = request.form

	try:
	
		data['cat'],data['type'],data['chat'],data['text'],data['media'],data['caption']

		if not str(data['type'])=='1' and not str(data['type'])=='2':
			
			return { "success":False, "msg":"文案类型有误" } 

		if (str(data['type'])=='1' and not data['text']) or (str(data['type'])=='2' and not data['media']):
			
			return { "success":False, "msg":"广告文案不得为空" }

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	push = Push()

	ret = push.insert({'uid':request.user['_id'],"cat":data['cat'],'type':data['type'],'chat':data['chat'],'text':data['text'],'media':data['media'],'caption':data['caption']})

	return ret

@push.route('/remove',methods=['POST'])
def remove():

	data = request.form

	try:

		data['id']

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	push = Push()

	ret = push.remove({"uid":request.user['_id'],"_id":ObjectId(data['id'])})

	return ret

@push.route('/update',methods=['POST'])
def update():

	data = request.form

	try:
	
		data['_id'],data['cat'],data['type'],data['chat'],data['text'],data['media'],data['caption']

		if (str(data['type'])=='1' and not data['text']) or (str(data['type'])=='2' and not data['media']):
			
			return { "success":False, "msg":"广告文案不得为空" }

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	push = Push()

	ret = push.update({"_id":ObjectId(data['_id'])},{"cat":data['cat'],'type':data['type'],'chat':data['chat'],'text':data['text'],'media':data['media'],'caption':data['caption']})

	return ret

@push.route('/order',methods=['POST'])
def order():

	data = request.form

	return '1111111'






