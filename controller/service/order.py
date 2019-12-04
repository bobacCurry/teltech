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

@service_order.route('/addOrder',methods=['POST'])
def addOrder():

	data = request.form

	try:

		data['type'],data['cid'],data['days'],data['memo']

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	# 判断购买的服务是否存在

	push = Push()

	service = push.findOne({"_id":data['cid'],"uid":request.user['_id']},{"_id"})

	if not service:
		
		return { "success":False, "msg":"购买的服务不存在" }

	order = Order()

	exist = order.findOne({"cid":data['cid'],"status":0},{"_id"})

	if exist:
		
		return { "success":False, "msg":"订单已经存在，请不要重复提交" }

	ret = order.insert({"type":data['type'],"cid":data['cid'],"days":data['days'],"uid":request.user['_id'],"memo":data['memo']})

	return ret

@service_order.route('/getOrder',methods=['GET'])
def getOrder():

	page = None

	limit = None

	try:

		page = request.args.get("page")

		limit = request.args.get("limit")

		page = int(page)

		limit = int(limit)

		skip = (page-1)*limit

		order = Order()

		data = order.find({"uid":request.user['_id']},{"updated_at":0},skip=skip,limit=limit)

		return { "success":True, "msg":data }

	except Exception as e:
		
		return { "success":False, "msg":[] }
		
@service_order.route('/delOrder',methods=['POST'])
def delOrder():

	data = request.form

	try:

		data['_id']

		order = Order()

		ret = order.remove({"_id":data['_id']})

		return ret

	except Exception as e:
		
		return { "success":False, "msg":"删除失败" }
