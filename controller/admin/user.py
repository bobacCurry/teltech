from flask import Blueprint, request, current_app

from controller.account.auth import token_decode

from model.User import User

from hashlib import md5

admin_user = Blueprint('admin_user',__name__)

@admin_user.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		if "admin" not in user['msg']['access']:
			
			return { "success":False, "msg":"用户权限不足" }

		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@admin_user.route('/get_users/<page>',methods=['GET'])
def get_users(page):

	limit = 50

	skip = limit*(int(page)-1)

	user_obj = User()

	ret = user_obj.find({},{'account':1,'name':1,'vip':1},limit=limit,skip=skip)

	return {'success':True,'msg':ret}

@admin_user.route('/reset_pwd/<uid>',methods=['POST'])
def reset_pwd(uid):

	user_obj = User()

	password = '123qwe'

	ret = user_obj.update({'_id':uid},{"password":md5(password.encode(encoding='utf-8')).hexdigest()})

	return ret

@admin_user.route('/set_vip/<uid>',methods=['POST'])
def set_vip(uid):

	user_obj = User()

	ret = user_obj.update({'_id':uid},{'vip':1})

	return ret