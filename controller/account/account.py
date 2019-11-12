from flask import Blueprint, request, current_app

from model import User

from hashlib import md5

account = Blueprint('account',__name__)

@account.before_request

# def before_request():

# 	return '22222222'

@account.route('/register',methods=['POST'])
def register():

	data = request.form

	try:
	
		data['account'],data['password'],data['username']
	
	except Exception as e:
		
		return { "code":0, "msg":"注册数据缺失" }

	if not data['account'] or not data['password'] or not data['username'] :
		
		return { "code":0, "msg":"注册数据缺失" }

	user = User.User()

	ret = user.insert_one({"account":data['account'],"password":md5(data['password'].encode(encoding='utf-8')).hexdigest(),"username":data['username']})

	if not ret:
		
		return '注册失败'

	return '注册成功'


@account.route('/login',methods=['POST'])
def login():
	
	data = request.form

	try:
	
		data['account'],data['password']
	
	except Exception as e:
		
		return { "code":0, "msg":"登陆数据缺失" }

	user = User.User()



# @account.route('/test/<test>',methods=['POST','GET'])

# def test(test):

# 	method = request.method

# 	path = request.path

# 	what = request.args.get('what')

# 	current_app.logger.info('info log')

# 	return {"path":path,"method":method,"test":test,"what":what}