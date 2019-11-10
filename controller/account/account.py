from flask import Blueprint, request, current_app

from model import User

account = Blueprint('account',__name__)

@account.before_request

# def before_request():

# 	return '22222222'

@account.route('/register',methods=['POST'])

def register():

	data = request.form

	try:
	
		data['name'],data['password'],data['username']
	
	except Exception as e:
		
		return { "code":0, "msg":"注册数据缺失" }

	if not data['name'] or not data['password'] or not data['username'] :
		
		return { "code":0, "msg":"注册数据缺失" }

	user = User.User()

	user.insert_one({})

	return '注册成功'



# @account.route('/test/<test>',methods=['POST','GET'])

# def test(test):

# 	method = request.method

# 	path = request.path

# 	what = request.args.get('what')

# 	current_app.logger.info('info log')

# 	return {"path":path,"method":method,"test":test,"what":what}