from flask import Blueprint, request, current_app

from hashlib import md5

from time import time

from controller.account.auth import token_decode

from model.Order import Order

from model.Push import Push

from model.Chat import Chat

from client.check import Check

import random

admin_order = Blueprint('admin_order',__name__)

@admin_order.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		if "admin" not in user['msg']['access']:
			
			return { "success":False, "msg":"用户权限不足" }

		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

	if user['success']:
		
		request.user = user['msg']

@admin_order.route('/get_order',methods=['GET'])
def get_order():

	try:

		page = request.args.get("page")

		limit = 50

		query = {}

		if request.args.get("status"):
			
			query = { "status":int(request.args.get("status")) }

		if not page:
			
			page = 1

		page = int(page)

		skip = (page-1)*limit

		order = Order()

		data = order.find(query,{"updated_at":0},skip=skip,limit=limit)

		return { "success":True, "msg":data }

	except Exception as e:

		return { "success":False, "msg":[] }


@admin_order.route('/start_order/<_id>',methods=['POST'])
def start_order(_id):

	order_obj = Order()

	order = order_obj.findOne({"_id":_id,"status":0})

	if not order:
		
		return  { "success":False, "msg":"暂无该待审核订单" }

	push_obj = Push()

	push = push_obj.findOne({"_id":order["sid"]})

	if not push:
		
		return  { "success":False, "msg":"服务不存在" }

	expire = int(time()) + int(order['days'])*24*3600

	if int(time()) < push["expire"]:
		
		expire = int(push["expire"]) + int(order['days'])*24*3600

	ret1 = push_obj.update({"_id":order['sid']},{"expire":expire,"status":1})

	if not ret1["success"]:
		
		return  { "success":False, "msg":"订单更新失败1" }

	ret2 = order_obj.update({"_id":_id},{"status":1})

	if not ret2["success"]:
		
		return  { "success":False, "msg":"订单更新失败2" }

	return { "success":True, "msg":"订单开启成功" }

















