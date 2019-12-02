from flask import Blueprint, request, current_app

from hashlib import md5

from time import time

from controller.account.auth import token_decode

from model.Order import Order

from model.Push import Push

from model.Chat import Chat

import random

admin_order = Blueprint('admin_order',__name__)

@admin_order.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		if user['msg']['role']<100:
			
			return { "success":False, "msg":"用户权限不足" }

		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

	if user['success']:
		
		request.user = user['msg']

@admin_order.route('/get_order',methods=['GET'])
def get_order():

	page = None

	limit = None

	query = {}

	try:

		page = request.args.get("page")

		limit = request.args.get("limit")

		if request.args.get("status"):
			
			query = { "status":int(request.args.get("status")) }

		page = int(page)

		limit = int(limit)

		skip = (page-1)*limit

		order = Order()

		data = order.find(query,{"updated_at":0},skip=skip,limit=limit)

		return { "success":True, "msg":data }

	except Exception as e:
		
		return { "success":False, "msg":[] }


@admin_order.route('/start_order/<_id>/<phone>',methods=['POST'])
def start_order(_id,phone):

	order_obj = Order()

	order = order_obj.findOne({"_id":_id,"status":0})

	if not order:
		
		return  { "success":False, "msg":"暂无该待审核订单" }

	deadline = int(time()) + int(order['days'])*24*3600

	push_obj = Push()

	minute = random.randint(0, 19)

	ret1 = push_obj.update({"_id":order['cid']},{"deadline":deadline,"status":1,"minute":minute,"phone":phone})

	if not ret1["success"]:
		
		return  { "success":False, "msg":"订单更新失败1" }

	ret2 = order_obj.update({"_id":_id},{"status":1})

	if not ret2["success"]:
		
		return  { "success":False, "msg":"订单更新失败2" }

	return { "success":False, "msg":"订单开启成功" }

@admin_order.route('/addChat/<_id>',methods=['POST'])
def addChat(_id):

	chat = Chat()

	ret = chat.update({"_id":_id},{"status":1})

	return ret

@admin_order.route('/delChat/<_id>',methods=['POST'])
def delChat(_id):

	chat = Chat()

	ret = chat.remove({"_id":_id})

	return ret

@admin_order.route('/getChat/<status>',methods=['GET'])
def getChat(status):

	print(status)

	chat = Chat()

	ret = chat.find({"status":int(status)})

	return { "success":True,"msg":ret }

















