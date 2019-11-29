# 广告代发服务

from flask import Blueprint, request, current_app

from model.Client import Client

from model.Order import Order

from model.Push import Push

from model.Chat import Chat

import time

from controller.account.auth import token_decode

service_push = Blueprint('service_push',__name__)

@service_push.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@service_push.route('/get',methods=['GET'])
def get():

	push = Push()

	data = push.find({"uid":request.user['_id']},{"created_at":0,"updated_at":0})

	return { "success":True, "msg":data }

@service_push.route('/add',methods=['POST'])
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

@service_push.route('/remove',methods=['POST'])
def remove():

	data = request.form

	try:

		data['_id']

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	push = Push()

	ret = push.remove({"uid":request.user['_id'],"_id":data['_id']})

	return ret


@service_push.route('/update',methods=['POST'])
def update():

	data = request.form

	try:
	
		data['_id'],data['cat'],data['type'],data['chat'],data['text'],data['media'],data['caption']

		if not data['_id']:
			
			return { "success":False, "msg":"数据缺失" }

		if (str(data['type'])=='1' and not data['text']) or (str(data['type'])=='2' and not data['media']):
			
			return { "success":False, "msg":"广告文案不得为空" }

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	push = Push()

	ret = push.update({"_id":data['_id']},{"cat":data['cat'],'type':data['type'],'chat':data['chat'],'text':data['text'],'media':data['media'],'caption':data['caption']})

	return ret


@service_push.route('/addOrder',methods=['POST'])
def addOrder():

	data = request.form

	try:

		data['type'],data['cid'],data['days'],data['memo']

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	# 判断购买的服务是否存在

	push = Push()

	service = push.findOne({"_id":data['cid']},{"_id"})

	if not service:
		
		return { "success":False, "msg":"购买的服务不存在" }

	order = Order()

	exist = order.findOne({"cid":data['cid'],"status":0},{"_id"})

	if exist:
		
		return { "success":False, "msg":"订单已经存在，请不要重复提交" }

	ret = order.insert({"type":data['type'],"cid":data['cid'],"uid":request.user['_id'],"days":data['days'],"memo":data['memo']})

	return ret

@service_push.route('/getOrder',methods=['GET'])
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
		
@service_push.route('/delOrder',methods=['POST'])
def delOrder():

	data = request.form

	try:

		data['_id']

		order = Order()

		ret = order.remove({"_id":data['_id']})

		return ret

	except Exception as e:
		
		return { "success":False, "msg":"删除失败" }

@service_push.route('/addChat/<chatid>/<chatType>',methods=['POST'])
def addChat(chatid,chatType):

	chat = Chat()

	exist = chat.findOne({"chatid":chatid,"type":chatType})

	if exist:
		
		return { "success":False, "msg":"群名称已存在" }

	ret = chat.insert({"chatid":chatid,"type":chatType})

	return ret

@service_push.route('/getChat/<chatType>',methods=['GET'])
def getChat(chatType):

	chat = Chat()

	ret = chat.find({"type":chatType,"status":1})

	return { "success":True,"msg":ret }




