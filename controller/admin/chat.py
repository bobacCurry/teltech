from flask import Blueprint, request, current_app

from controller.account.auth import token_decode

from model.Chat import Chat

admin_chat = Blueprint('admin_chat',__name__)

@admin_chat.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		if "admin" not in user['msg']['access']:
			
			return { "success":False, "msg":"用户权限不足" }

		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@admin_chat.route('/add_chat/<_id>/<auth>',methods=['POST'])
def addChat(_id,auth):

	chat = Chat()

	ret = chat.update({"_id":_id},{"status":1,"auth":int(auth)})

	return ret

@admin_chat.route('/del_chat/<_id>',methods=['POST'])
def delChat(_id):

	chat = Chat()

	ret = chat.remove({"_id":_id})

	return ret

@admin_chat.route('/get_chat/<page>/<limit>',methods=['GET'])
def getChat(page,limit):

	page = int(page)

	limit = int(limit)

	status = request.args.get("status")

	_type = request.args.get("type")

	skip = (page-1)*limit

	query = {}

	if status:
		
		query['status'] = int(status)

	if _type:
		
		query['type'] = int(_type)

	print(query)

	chat = Chat()

	ret = chat.find(query,skip=skip,limit=limit)

	return { "success":True,"msg":ret }
