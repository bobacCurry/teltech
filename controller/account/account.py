from flask import Blueprint, request, current_app

account = Blueprint('account',__name__)

@account.before_request

def before_request():

	return '22222222'

@account.route('/login',methods=['POST'])

def login():

	return '111111'

# @account.route('/test/<test>',methods=['POST','GET'])

# def test(test):

# 	method = request.method

# 	path = request.path

# 	what = request.args.get('what')

# 	current_app.logger.info('info log')

# 	return {"path":path,"method":method,"test":test,"what":what}