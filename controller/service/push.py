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

	data = push.find({"uid":request.user['user_id']},{"chat":0,"text":0,"media":0,"caption":0,"created_at":0,"updated_at":0,"message_id":0})

	return { "success":True, "msg":data }

@service_push.route('/add',methods=['POST'])
def add():

	data = request.form or request.get_json()

	client = Client()

	try:
	
		data['phone'],data['chat_type'],data['text_type'],data['chat'],data['text'],data['media'],data['caption'],data['minute']

		exist = client.findOne({"phone":data['phone'],"used":0})

		if not exist:
			
			return { "success":False, "msg":"TG实例不存在" },500

		if not str(data['text_type'])=='0' and not str(data['text_type'])=='1':
			
			return { "success":False, "msg":"文案类型有误" },500

		if (str(data['text_type'])=='0' and not data['text']) or (str(data['text_type'])=='1' and not data['media']):
			
			return { "success":False, "msg":"广告文案不得为空" },500

		if not data['minute']:
			
			return { "success":False, "msg":"请选择发送的时间" },500

		if int(data['minute']) >= 20:
		
			return { "success":False, "msg":"发送的时间有误" },500

		if len(data['chat']) == 0 :
			
			return { "success":False, "msg":"请选择发送的群组" },500

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" },500

	message = Message(data['phone'])

	message_ret = None

	if str(data['text_type'])=='1':

		message_ret = message.send_photo("me",data["media"],data["caption"])

	else:

		message_ret = message.send_message("me",data["text"])
		
	if not message_ret["success"]:
		
		return message_ret,500

	message_id = message_ret["msg"]["message_id"]

	minute = [int(data['minute']),int(data['minute'])+20,int(data['minute'])+40]

	push = Push()

	ret = push.insert({'phone':data['phone'],'uid':request.user['user_id'],'message_id':message_id,"minute":minute,"chat_type":int(data['chat_type']),'text_type':int(data['text_type']),'chat':data['chat'],'text':data['text'],'media':data['media'],'caption':data['caption']})

	if ret['success']:
		
		client.update({"phone":data['phone']},{"used":1})

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

	push = Push()

	ret = push.remove({"uid":request.user['_id'],"_id":data['_id']})

	return ret

@service_push.route('/update',methods=['POST'])
def update():

	data = request.form

	try:
	
		data['_id'],data['phone'],data['cat'],data['type'],data['chat'],data['text'],data['media'],data['caption']

		if not data['_id']:
			
			return { "success":False, "msg":"数据缺失" }

		if (str(data['type'])=='1' and not data['text']) or (str(data['type'])=='2' and not data['media']):
			
			return { "success":False, "msg":"广告文案不得为空" }

	except Exception as e:
		
		return { "success":False, "msg":"请求数据缺失" }

	message = Message(data["phone"])

	message_ret = message.send_message("me",data["text"])

	if not message_ret["success"]:
		
		return message_ret

	message_id = message_ret["msg"]["message_id"]

	push = Push()

	ret = push.update({"_id":data['_id']},{"cat":data['cat'],'type':data['type'],'chat':data['chat'],'text':data['text'],'media':data['media'],'caption':data['caption']})

	return ret

@service_push.route('/start/<_id>',methods=['POST'])
def start(_id):

	push_obj = Push()

	push = push_obj.findOne({"_id":_id})

	ret = push_obj.update({"_id":_id},{"status":1})

	if not ret["success"]:
		
		return ret

	return { "success":True, "msg":"开启成功" }

