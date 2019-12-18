from flask import Blueprint, request, current_app

from controller.account.auth import token_decode

from model.Chat import Chat

service_chat = Blueprint('service_chat',__name__)

@service_chat.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@service_chat.route('/add_chat/<chatid>/<chatType>/<auth>',methods=['POST'])
def addChat(chatid,chatType,auth):

	chat = Chat()

	exist = chat.findOne({"chatid":chatid,"type":int(chatType)})

	if exist:
		
		return { "success":False, "msg":"群名称已存在" },500

	ret = chat.insert({"chatid":chatid,"type":int(chatType),"uid":request.user["user_id"],"auth":int(auth)})

	return ret

@service_chat.route('/get_user_chat/<page>/<limit>',methods=['GET'])
def getUserChat(page,limit):

	chat = Chat()

	page = int(page)

	limit = int(limit)

	skip = (page-1)*limit

	ret = chat.find({"uid":request.user["user_id"]},skip=skip,limit=limit)

	return { "success":True,"msg":ret }


@service_chat.route('/get_chat/<chatType>',methods=['GET'])
def getChat(chatType):

	chat = Chat()

	ret = chat.find({"type":int(chatType),"status":1})

	return { "success":True,"msg":ret }