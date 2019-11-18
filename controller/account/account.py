from flask import Blueprint, request, current_app

from model.User import User

from hashlib import md5

from controller.account.auth import token_encode,token_decode

# import time

# pyjwt

# import jwt

# import json

account = Blueprint('account',__name__)

# token_dict = { 'time':time.time(), 'info':'' }

# headers = { 'alg': "HS256", 'kid': "TelTech" }

# jwt_ket = 'TelTech'



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
	
	except Exception as e:
		
		return { "success":False, "msg":"登陆数据缺失" }

	user = User()

	ret = user.find_one({"account":data['account'],"password":md5(data['password'].encode(encoding='utf-8')).hexdigest()})

	# if not ret['success'] or not ret['msg']:

	# 	current_app.logger.info(ret['msg'])
		
	# 	return {'success':False,'msg':'登录失败'}

	# token_dict['info'] = json.dumps(ret['msg'])

	token = token_encode(ret['msg'])

	# jwt.encode(token_dict, jwt_ket, algorithm="HS256", headers=headers).decode('ascii') 

	return token

@account.route('/get_info',methods=['GET'])
def get_info():

	token = None

	try:
	
		token = request.args.get('token')

	except Exception as e:
		
		return { "success":False, "msg":"token数据缺失" }

	data = token_decode(token)

	if not data['success'] :
		
		current_app.logger.info(str(data['msg']))

	return data
	# try:

	    # data = jwt.decode(token, jwt_ket, algorithms=['HS256'])

	    # now = time.time()

	    # if (now - data['time'])/1000 > 3600*24*7 :

	    # 	return {'success':False,'msg':'token过期'}

	    # return json.loads(data['info'])



	# except Exception as e:

	#     current_app.logger.info(e)

	#     return {'success':False,'msg':'获取信息失败'}




# @account.before_request

# def before_request():

# 	return '22222222'

# @account.route('/test/<test>',methods=['POST','GET'])

# def test(test):

# 	method = request.method

# 	path = request.path

# 	what = request.args.get('what')

# 	current_app.logger.info('info log')

# 	return {"path":path,"method":method,"test":test,"what":what}