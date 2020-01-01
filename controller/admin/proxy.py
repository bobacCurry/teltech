from flask import Blueprint, request, current_app

from model.Proxy import Proxy

from controller.account.auth import token_decode

admin_proxy = Blueprint('admin_proxy',__name__)

@admin_proxy.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		if "admin" not in user['msg']['access']:
			
			return { "success":False, "msg":"用户权限不足" }

		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@admin_proxy.route('/add_proxy',methods=['POST'])
def add_proxy():

	data = request.form or request.get_json()

	try:
	
		data['hostname'],data['port'],data['username'],data['password'],data['minute']
	
	except Exception as e:
		
		return { "success":False, "msg":"注册数据缺失" }

	proxy_obj = Proxy()

	exist = proxy_obj.findOne({'hostname':data['hostname']})

	if exist:
		
		return {'success':False,'msg':'已存在相同代理'}

	ret = proxy_obj.insert({'hostname':data['hostname'],'port':int(data['port']),'username':data['username'],'password':data['password'],'minute':int(data['minute']),'status':0})

	return ret

@admin_proxy.route('/get_proxy',methods=['GET'])
def get_proxy():

	proxy_obj = Proxy()

	data = proxy_obj.find({},sort='minute')

	return {'success':True,'msg':data}

@admin_proxy.route('/del_proxy/<_id>',methods=['POST'])
def del_proxy(_id):

	proxy_obj = Proxy()	

	ret = proxy_obj.remove({'_id':_id})

	return ret

@admin_proxy.route('/change_status/<_id>/<status>',methods=['POST'])
def change_status(_id,status):

	proxy_obj = Proxy()	

	ret = proxy_obj.update({'_id':_id},{'status':int(status)})

	return ret
