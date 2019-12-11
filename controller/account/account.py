from flask import Blueprint, request, current_app

from model.User import User

from hashlib import md5

from controller.account.auth import token_encode,token_decode

account = Blueprint('account',__name__)

@account.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

@account.route('/register',methods=['POST'])
def register():

	data = request.form

	try:
	
		data['account'],data['password'],data['name']
	
	except Exception as e:
		
		return { "success":False, "msg":"注册数据缺失" }

	if not data['account'] or not data['password'] or not data['name'] :
		
		return { "success":False, "msg":"注册数据缺失" }

	user = User()

	ret = user.insert({"account":data['account'],"password":md5(data['password'].encode(encoding='utf-8')).hexdigest(),"name":data['name']})

	if not ret['success'] :

		current_app.logger.info(ret['msg'])
		
		return {'success':False,'msg':ret['msg']}

	return {'success':True,'msg':'注册成功'}

@account.route('/login',methods=['POST'])
def login():
	
	data = request.get_json()
	print(data)
	try:
	
		data['account'],data['password']

		if not data['account'] or not data['password']:
			
			return { "success":False, "msg":"登陆数据缺失" },500
	
	except Exception as e:
		
		return { "success":False, "msg":"登陆数据缺失" },500

	user = User()

	ret = user.findOne({"account":data['account'],"password":md5(data['password'].encode(encoding='utf-8')).hexdigest(),"status":1},{ "password":0, "status":0, "created_at":0, "updated_at":0 })

	if not ret:
		
		return { "success":False, "msg":"用户信息不存在" },500

	token_ret = token_encode({"user_id":ret["_id"],"name":ret["name"],"avatar":ret["avatar"],"access":ret["access"]})

	return token_ret

@account.route('/get_info',methods=['GET'])
def get_info():

	if not request.user:
		
		return { "success":False, "msg":"token缺失" },500

	# user = User()

	# ret = user.findOne({"_id":request.user["_id"]},{ "password":0, "status":0, "created_at":0, "updated_at":0 })

	# if not ret:
		
	# 	return { "success":False, "msg":"用户不存在" }

	return { "success":True, "msg":request.user }

# @account.before_request

# def before_request():

# 	return '22222222'





