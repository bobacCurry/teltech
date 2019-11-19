from flask import Blueprint, request, current_app

from model.User import User

from hashlib import md5

from bson import ObjectId

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
	
		data['account'],data['password'],data['username']
	
	except Exception as e:
		
		return { "success":False, "msg":"注册数据缺失" }

	if not data['account'] or not data['password'] or not data['username'] :
		
		return { "success":False, "msg":"注册数据缺失" }

	user = User()

	ret = user.insert_one({"account":data['account'],"password":md5(data['password'].encode(encoding='utf-8')).hexdigest(),"username":data['username']})

	if not ret['success'] :

		current_app.logger.info(ret['msg'])
		
		return {'success':False,'msg':ret['msg']}

	return {'success':True,'msg':'注册成功'}

@account.route('/login',methods=['POST'])
def login():
	
	data = request.form

	try:
	
		data['account'],data['password']

		if not data['account'] or not data['password']:
			
			return { "success":False, "msg":"登陆数据缺失" }
	
	except Exception as e:
		
		return { "success":False, "msg":"登陆数据缺失" }

	user = User()

	ret = user.find_one({"account":data['account'],"password":md5(data['password'].encode(encoding='utf-8')).hexdigest(),"status":1})

	if not ret['success']:
		
		return { "success":False, "msg":"用户信息不存在" }

	token_ret = token_encode({"_id":ret["msg"]["_id"]})

	return token_ret

@account.route('/get_info',methods=['GET'])
def get_info():

	print(request.user)


	if not request.user:
		
		return { "success":False, "msg":"token缺失" }

	user = User()

	ret = user.find_one({"_id":ObjectId(request.user["_id"])})

	return ret

# @account.before_request

# def before_request():

# 	return '22222222'

