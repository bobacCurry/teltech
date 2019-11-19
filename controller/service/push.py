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

	return '1111111'

@push.route('/add',methods=['POST'])
def add():

	data = request.form

	try:
	
		data['cat'],data['type'],data['chat'],data['text'],data['media'],data['caption']

		if (str(data['type'])=='0' and not data['text']) or (str(data['type'])=='1' and not data['media']):
			
			return { "success":False, "msg":"广告文案不得为空" }

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	token = request.headers.get("token")

	push = Push()

	ret = push.insert_one({'uid':request.user['_id'],"cat":data['cat'],'type':data['type'],'chat':data['chat'],'text':data['text'],'media':data['media'],'caption':data['caption']})

	return ret

@push.route('/remove',methods=['POST'])
def remove():

	data = request.form

	try:

		data['id']

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	push = Push()

	ret = push.remove({"_id":ObjectId(data['id'])})

	return ret

@push.route('/edit',methods=['POST'])
def edit():

	print(111111)

	return '1111111'

@push.route('/order',methods=['POST'])
def order():

	print(111111)

	return '1111111'