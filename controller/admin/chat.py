from flask import Blueprint, request, current_app

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

	if user['success']:
		
		request.user = user['msg']


@admin_chat.route('/addChat/<_id>/<auth>',methods=['POST'])
def addChat(_id,auth):

	chat = Chat()

	ret = chat.update({"_id":_id},{"status":1,"auth":int(auth)})

	return ret

@admin_chat.route('/delChat/<_id>',methods=['POST'])
def delChat(_id):

	chat = Chat()

	ret = chat.remove({"_id":_id})

	return ret

@admin_chat.route('/getChat/<chatType>/<status>',methods=['GET'])
def getChat(chatType,status):

	chat = Chat()

	ret = chat.find({"status":int(status),"type":int(chatType)})

	return { "success":True,"msg":ret }
