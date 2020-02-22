# vip服务

from flask import Blueprint, request, current_app

from model.Client import Client

from client.check import Check

from model.AddChat import AddChat

from controller.account.auth import token_decode

service_vip = Blueprint('service_vip',__name__)

@service_vip.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success'] and user['msg']['vip']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"此功能为vip用户专属" },401


@service_vip.route('/add_chat',methods=['POST'])
def addChat():

	data = request.form or request.get_json()

	try:

		data['phone'],data['chatids']
	
	except Exception as e:
	
		return { "success":False, "msg":"请求数据缺失" }

	client_obj = Client()

	client = client_obj.findOne({'phone':data['phone'],'uid':request.user['user_id'],'status':{'$in':[1,2]}})

	if not client:
		
		return { "success":False, "msg":"TG账号未绑定" }

	check_obj = Check(data['phone'])

	check_ret = check_obj.authCheck()

	if not check_ret['success']:
		
		return check_ret


	add_obj = AddChat()

	exist = add_obj.findOne({'phone':data['phone'],'status':0})

	if exist:
		
		return { "success":False, "msg":"目前存在正在执行的订单" }


	ret = add_obj.insert({'phone':data['phone'],'uid':request.user['user_id'],'chatids':data['chatids'],'status':0})

	return ret


@service_vip.route('/get_add_chat/<page>',methods=['GET'])
def getAddChat(page):

	limit = 50

	skip = (int(page)-1)*limit

	add_obj = AddChat()

	data = add_obj.find({'uid':request.user['user_id']},skip=skip,limit=limit,sort="_id")

	return {'success':True,'msg':data}
