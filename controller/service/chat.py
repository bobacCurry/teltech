from flask import Blueprint, request, current_app

service_chat = Blueprint('service_chat',__name__)

@service_chat.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@service_chat.route('/addChat/<chatid>/<chatType>',methods=['POST'])
def addChat(chatid,chatType):

	chat = Chat()

	exist = chat.findOne({"chatid":chatid,"uid":request.user["user_id"],"type":int(chatType)})

	if exist:
		
		return { "success":False, "msg":"群名称已存在" }

	ret = chat.insert({"chatid":chatid,"type":int(chatType)})

	return ret

@service_chat.route('/addChat/<chatid>/<chatType>',methods=['POST'])
def getUserChat():

	chat = Chat()

	ret = chat.find({"uid":request.user["user_id"]})

	return { "success":True,"msg":ret }


@service_chat.route('/getChat/<chatType>',methods=['GET'])
def getChat(chatType):

	chat = Chat()

	ret = chat.find({"type":int(chatType),"status":1})

	return { "success":True,"msg":ret }