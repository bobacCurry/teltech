# 下订单

from flask import Blueprint, request, current_app

from model.Client import Client

from model.Order import Order

from model.Push import Push

from model.Chat import Chat

from client.message import Message

import time

from controller.account.auth import token_decode

service_order = Blueprint('service_order',__name__)

@service_order.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }


@service_order.route('/add_group_order',methods=['POST'])
def add_group_order():

	data = request.form or request.get_json()

	try:

		data['sid'],data['days'],data['memo']

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	# 判断购买的服务是否存在

	if not data['sid'].strip():
		
		return { "success":False, "msg":"购买的服务不存在" }

	if data['days'] not in [30,60,90,120]:
		
		return { "success":False, "msg":"购买的天数不合法" }

	push = Push()

	service = push.findOne({"_id":data['sid'],"uid":request.user['user_id']},{"user_id"})

	if not service:
		
		return { "success":False, "msg":"购买的服务不存在" }

	order = Order()

	exist = order.findOne({"sid":data['sid'],"status":0})

	if exist:
		
		return { "success":False, "msg":"存在未处理的订单，请不要重复提交" }

	ret = order.insert({"type":0,"sid":data['sid'],"days":data['days'],"uid":request.user['user_id'],"memo":data['memo']})

	return ret


@service_order.route('/add_personal_order',methods=['POST'])
def add_personal_order():

	return '22222222'


@service_order.route('/get_order',methods=['GET'])
def get_order():

	try:

		page = request.args.get("page")

		limit = 50

		status = request.args.get("status")

		if not page:
			
			page = 1

		skip = (int(page)-1)*limit

		query = {"uid":request.user['user_id']}

		if status:
			
			query = {"uid":request.user['user_id'],"status":int(status)}

		order = Order()

		data = order.find(query,{"updated_at":0},skip=skip,limit=limit)

		return { "success":True, "msg":data }

	except Exception as e:
		
		return { "success":False, "msg":[] }
		

@service_order.route('/del_order',methods=['POST'])
def del_order():

	data = request.form

	try:

		data['_id']

		order = Order()

		ret = order.remove({"_id":data['_id']})

		return ret

	except Exception as e:
		
		return { "success":False, "msg":"删除失败" }
