# 下订单

from flask import Blueprint, request, current_app

from controller.account.auth import token_decode

from model.Client import Client

service_client = Blueprint('service_client',__name__)

@service_client.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }


@service_client.route('/get_user_client',methods=['GET'])
def getUserClient():

	client = Client()

	data = client.find({"uid":request.user["user_id"]})

	return { "success":True, "msg":data }

@service_client.route('/get_notused_client',methods=['GET'])
def getNotUsed():
	
	client = Client()

	data = client.find({"uid":request.user["user_id"],"used":0})

	return { "success":True, "msg":data }

@service_client.route('/restore/<phone>',methods=['POST'])
def restore(phone):
	
	client = Client()

	data = client.update({'uid':request.user['user_id'],'phone':phone},{'status':1})

	return { "success":True, "msg":data }
