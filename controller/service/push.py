# 广告代发服务

from flask import Blueprint, request, current_app

from model.Client import Client

from model.Order import Order

from model.Push import Push

from model.Chat import Chat

from client.message import Message

from time import time

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

	data = push.find({"uid":request.user['user_id']},{"chat":0,"text":0,"media":0,"caption":0,"created_at":0,"updated_at":0,"message_id":0})

	return { "success":True, "msg":data }

@service_push.route('/get_one/<_id>',methods=['GET'])
def getOne(_id):
	
	push = Push()

	data = push.findOne({"_id":_id,"uid":request.user['user_id']},{"created_at":0,"updated_at":0,"message_id":0})

	if not data:
		
		return { "success":False, "msg":data } 

	return { "success":True, "msg":data }


@service_push.route('/add',methods=['POST'])
def add():

	data = request.form or request.get_json()

	client_obj = Client()

	try:
	
		data['phone'],data['chat_type'],data['text_type'],data['chat'],data['text'],data['media'],data['caption'],data['minute'],data['title']

		exist = client_obj.findOne({"phone":data['phone'],'uid':request.user['user_id'],"used":0})

		if not exist:
			
			return { "success":False, "msg":"TG实例不存在或已被占用" },500

		if not str(data['text_type'])=='0' and not str(data['text_type'])=='1':
			
			return { "success":False, "msg":"文案类型有误" },500

		if (str(data['text_type'])=='0' and not data['text']) or (str(data['text_type'])=='1' and not data['media']):
			
			return { "success":False, "msg":"广告文案不得为空" },500

		if not str(data['minute']):
			
			return { "success":False, "msg":"请选择发送的时间" },500

		if int(data['minute']) >= 30:
		
			return { "success":False, "msg":"发送的时间有误" },500

		if len(data['chat']) == 0 :
			
			return { "success":False, "msg":"请选择发送的群组" },500

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" },500

	message = Message(data['phone'])

	push = Push()

	message_ret = None

	if str(data['text_type'])=='1':

		message_ret = message.send_photo("me",data["media"],data["caption"])

	else:

		message_ret = message.send_message("me",data["text"])
		
	if not message_ret["success"]:
		
		if '[401 USER_DEACTIVATED_BAN]' in  message_ret["msg"]:
			
			client_obj.update({'phone':data['phone'],'uid':request.user['user_id']},{'status':3})

		return message_ret,500

	message_id = message_ret["msg"]["message_id"]

	minute = [int(data['minute']),int(data['minute'])+20,int(data['minute'])+40]

	ret = push.insert({'title':data['title'],'phone':data['phone'],'uid':request.user['user_id'],'message_id':message_id,"minute":minute,"chat_type":int(data['chat_type']),'text_type':int(data['text_type']),'chat':data['chat'],'count':len(data['chat']),'text':data['text'],'media':data['media'],'caption':data['caption']})

	if ret['success']:
		
		client_obj.update({"phone":data['phone']},{"used":1})

	else:

		return ret,500

	return ret

@service_push.route('/remove',methods=['POST'])
def remove():

	data = request.form

	try:

		data['_id']

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	push_obj = Push()

	ret = push_obj.remove({"uid":request.user['_id'],"_id":data['_id']})

	return ret

@service_push.route('/update/<_id>',methods=['POST'])
def update(_id):

	data = request.form or request.get_json()

	try:
	
		data['phone'],data['text_type'],data['chat'],data['text'],data['media'],data['caption'],data['title']

		if not str(data['text_type'])=='0' and not str(data['text_type'])=='1':
			
			return { "success":False, "msg":"文案类型有误" },500

		if (str(data['text_type'])=='0' and not data['text']) or (str(data['text_type'])=='1' and not data['media']):
			
			return { "success":False, "msg":"广告文案不得为空" },500

		if not str(data['minute']):
			
			return { "success":False, "msg":"请选择发送的时间" },500

		if int(data['minute']) >= 30:
		
			return { "success":False, "msg":"发送的时间有误" },500

		if len(data['chat']) == 0 :
			
			return { "success":False, "msg":"请选择发送的群组" },500

	except Exception as e:

		return { "success":False, "msg":"请求数据缺失" }

	push_obj = Push()

	client_obj = Client()

	push = push_obj.findOne({"_id":_id,'uid':request.user['user_id']})

	if not push:
		
		return { "success":False, "msg":"服务实例不存在" }

	client = client_obj.findOne({"phone":data['phone'],'uid':request.user['user_id']})

	if not client or (client["used"] and (client["phone"] != push["phone"])):
		
		return { "success":False, "msg":"TG实例不合法" }

	message = Message(data["phone"])

	
	message_ret = None

	if str(data['text_type'])=='1':

		message_ret = message.send_photo("me",data["media"],data["caption"])

	else:

		message_ret = message.send_message("me",data["text"])

	if not message_ret["success"]:
		
		if '[401 USER_DEACTIVATED_BAN]' in  message_ret["msg"]:
			
			client_obj.update({'phone':data['phone'],'uid':request.user['user_id']},{'status':3})

		return message_ret

	message_id = message_ret["msg"]["message_id"]

	minute = [int(data['minute']),int(data['minute'])+20,int(data['minute'])+40]

	ret = push_obj.update({"_id":_id,'uid':request.user['user_id']},{"phone":data["phone"],'text_type':int(data['text_type']),'message_id':message_id,"minute":minute,'chat':data['chat'],'count':len(data['chat']),'text':data['text'],'media':data['media'],'caption':data['caption'],"title":data['title']})

	if ret["success"]:
		
		if client["phone"] != push['phone']:
			
			client_obj.update({"phone":push["phone"]},{"used":0})

			client_obj.update({"phone":client["phone"]},{"used":1})

	return ret

@service_push.route('/change_status/<_id>',methods=['POST'])
def changeStatus(_id):

	push_obj = Push()

	push = push_obj.findOne({"_id":_id,'uid':request.user['user_id']})

	client_obj = Client()

	client = client_obj.findOne({'uid':request.user['user_id'],'phone':push['phone']})

	if not client:
		
		return { "success":False, "msg":"该服务的TG账号不存在" }

	if not push:
		
		return { "success":False, "msg":"服务实例不存在" }

	if push["expire"]<int(time()):

		return { "success":False, "msg":"服务未购买或已过期" }

	status = 0

	if push["status"] == 0:
		
		status = 1

		if client['status']==2:
			
			return { "success":False, "msg":"TG账号已被禁言，请确认账号已解除禁言" }

		if client['status']==3:
			
			return { "success":False, "msg":"TG账号已被ban，请确认账号是正常的" }

	ret = push_obj.update({"_id":_id,'uid':request.user['user_id']},{"status":status})

	if ret["success"]:
		
		ret["status"] = status

	return ret