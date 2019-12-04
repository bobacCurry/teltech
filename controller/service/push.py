# 广告代发服务

from flask import Blueprint, request, current_app

from model.Client import Client

from model.Order import Order

from model.Push import Push

from model.Chat import Chat

from client.message import Message

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

@service_push.route('/start/<_id>',methods=['POST'])
def start(_id):

	push_obj = Push()

	push = push_obj.findOne({"_id":_id})

	if not push:
		
		return { "success":False, "msg":"实例不存在" }

	if not push["phone"]:
		
		return { "success":False, "msg":"实力客户端未分配" }

	if (str(push['type'])=='1' and not push['text']) or (str(push['type'])=='2' and not push['media']):
			
		return { "success":False, "msg":"广告文案不得为空" }

	message = Message(push["phone"])

	ret = message.send_message("me",push["text"])

	if not ret["success"]:
		
		return ret

	message_id = ret["msg"]["message_id"]

	ret = push_obj.update({"_id":_id},{"message_id":message_id,"status":1})

	if not ret["success"]:
		
		return ret

	return { "success":True, "msg":"开启成功" }

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