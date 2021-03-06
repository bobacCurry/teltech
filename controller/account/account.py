from flask import Blueprint, request, current_app

from model.User import User

from hashlib import md5

from controller.account.auth import token_encode,token_decode

account = Blueprint('account',__name__)

@account.before_request
def before_request():

	request.user = None

	token = request.headers.get("token")

	user = token_decode(token)

	if user['success']:
		
		request.user = user['msg']

@account.route('/register',methods=['POST'])
def register():

	data = request.form or request.get_json()

	try:
	
		data['account'],data['password'],data['name'],data['job'],data['vip']
	
	except Exception as e:
		
		return { "success":False, "msg":"注册数据缺失" }

	if not data['account'] or not data['password'] or not data['name'] :
		
		return { "success":False, "msg":"注册数据缺失" }

	user = User()

	exist = user.findOne({"account":data['account']})

	if exist:
		
		return {'success':False,'msg':"已存在相同的账号名称"} 

	ret = user.insert({"account":data['account'],"password":md5(data['password'].encode(encoding='utf-8')).hexdigest(),"name":data['name'],"job":int(data['job']),"vip":int(data['vip'])})

	if not ret['success'] :

		current_app.logger.info(ret['msg'])
		
		return {'success':False,'msg':ret['msg']}

	return {'success':True,'msg':'注册成功'}

@account.route('/login',methods=['POST'])
def login():
	
	data = request.get_json()
	
	try:
	
		data['account'],data['password']

		if not data['account'] or not data['password']:
			
			return { "success":False, "msg":"登陆数据缺失" },500
	
	except Exception as e:
		
		return { "success":False, "msg":"登陆数据缺失" },500

	user = User()

	ret = user.findOne({"account":data['account'],"password":md5(data['password'].encode(encoding='utf-8')).hexdigest(),"status":1},{ "password":0, "status":0, "created_at":0, "updated_at":0 })

	if not ret:
		
		return { "success":False, "msg":"密码输入错误" },500

	token_ret = token_encode({"user_id":ret["_id"],"name":ret["name"],"avatar":ret["avatar"],"access":ret["access"],"vip":ret["vip"],"vip_expire":ret["vip_expire"],"money":ret["money"]})

	return token_ret

@account.route('/get_info',methods=['GET'])
def get_info():

	if not request.user:
		
		return { "success":False, "msg":"token缺失" },500

	user_obj = User()

	user = user_obj.findOne({'_id':request.user['user_id']},{'password':0,'created_at':0,'updated_at':0,'status':0})

	return user

@account.route('/reset_password',methods=['POST'])
def reset_password():

	data = request.form or request.get_json()

	if not request.user:
		
		return { "success":False, "msg":"用户数据有误" },500

	user = User()

	exist = user.findOne({'_id':request.user['user_id'],"password":md5(data['old_password'].encode(encoding='utf-8')).hexdigest(),"status":1})

	if not exist:
		
		return { "success":False, "msg":"账号与密码不符" },500

	ret = user.update({'_id':request.user['user_id']},{"password":md5(data['new_password'].encode(encoding='utf-8')).hexdigest()})

	if not ret["success"]:

		return ret,500

	return ret

@account.route('/logout',methods=['POST'])
def logout():
	
	return { "success":True, "msg":"退出账号" }





