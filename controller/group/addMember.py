from flask import Blueprint, request, current_app

from controller.account.auth import token_decode

from model.AddMember import AddMember

from model.Client import Client

from model.User import User

from client.group import Group

from client.message import Message

from client.group import Group

group_add_member = Blueprint('group_add_member',__name__)

def addUser(phone,target,addids):
	
	group_obj = Group(phone)

	success = []

	fail = []

	i = 0

	for uid in addids:
		
		addinfo = group_obj.add_chat_members(target,uid)

		print(addinfo,uid,phone)

		if addinfo['success']:
			
			success.append(uid)

		else:

			if '[420 FLOOD_WAIT_X]' in addinfo['msg']:
				
				break

			elif '[400 PEER_FLOOD]' in addinfo['msg']:

				break

			else:

				fail.append(uid)

		i = i + 1

	return {'success':success,'fail':fail,'last':addids[i:]}

@group_add_member.before_request
def before_request():
	
	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@group_add_member.route('/get_chat_user',methods=['GET'])
def getChatUser():

	add_member_obj = AddMember()

	data = add_member_obj.find({'uid':request.user['user_id']})

	for key,item in enumerate(data):
		
		data[key]['uids'] = len(item['uids'])

		data[key]['success'] = len(item['success'])

		data[key]['fail'] = len(item['fail'])

	return { "success":True, "msg":data }

@group_add_member.route('/new_chat_user/<phone>/<target>',methods=['POST'])
def NewChatUser(phone,target):

	client_obj = Client()

	client = client_obj.findOne({'uid':request.user['user_id'],'phone':phone})

	if not client:
		
		return { "success":False, "msg":"用户客户端不存在" }

	# 客户端是否在群里

	message_obj = Message(phone)

	send_ret = message_obj.send_message(target,'.')

	if not send_ret['success']:

		if '[400 USERNAME_NOT_OCCUPIED]' in send_ret['msg']:
			
			return { "success":False, "msg":"该群不存在" }

		if '[403 CHAT_WRITE_FORBIDDEN]' in send_ret['msg']:
			
			return { "success":False, "msg":"暂未加入该群" }

		return send_ret

	del message_obj

	# 群是否存在同时获取群信息

	target_chatids = []

	group_obj = Group(phone)

	chatinfo = group_obj.get_chat_members(target)

	if not chatinfo['success']:
		
		return chatinfo

	for chat in chatinfo['msg']:
		
		if chat['status'] == 'member' and not chat['user']['is_bot'] and not chat['user']['is_deleted'] and chat['user']['username']:

			target_chatids.append(chat['user']['username'])

	del group_obj

	add_member_obj = AddMember()

	exist = add_member_obj.findOne({'uid':request.user['user_id'],'target':target})

	if exist:
		
		return { "success":False, "msg":"已经创建过该群的拉群服务" }

	ret = add_member_obj.insert({'uid':request.user['user_id'],'target':target,'phone':[phone],'success':target_chatids})

	return ret

@group_add_member.route('/del_chat_user/<_id>',methods=['POST'])
def DelChatUser(_id):

	add_member_obj = AddMember()

	ret = add_member_obj.remove({'_id':_id,'uid':request.user['user_id']})

	return ret

@group_add_member.route('/add_chat_phone/<phone>/<_id>',methods=['POST'])
def AddChatPhone(phone,_id):

		# 客户端是否在群里

	add_member_obj = AddMember()

	client_obj = Client()

	add_member = add_member_obj.findOne({'uid':request.user['user_id'],'_id':_id})

	if phone in add_member['phone']:
		
		return { "success":False, "msg":"已经存在该手机号" }

	if not add_member:
		
		return { "success":False, "msg":"拉人服务不存在" }

	message_obj = Message(phone)

	send_ret = message_obj.send_message(add_member['target'],'.')

	if not send_ret['success']:

		if '[400 USERNAME_NOT_OCCUPIED]' in send_ret['msg']:
			
			return { "success":False, "msg":"该群不存在" }

		if '[403 CHAT_WRITE_FORBIDDEN]' in send_ret['msg']:
			
			return { "success":False, "msg":"暂未加入该群，请先加入" }

		if 'check @SpamBot' in send_ret['msg']:

			client_obj.update({'phone':phone},{'status':2})

			return { "success":False, "msg":"TG号被spam" }

		if '[401 USER_DEACTIVATED_BAN]' in send_ret['msg']:

			client_obj.update({'phone':phone},{'status':3})

			return { "success":False, "msg":"TG账号已被ban，请确认账号是正常的" }			

		if '未验证' in send_ret["msg"]:

			client_obj.update({'phone':phone},{'status':4})

			return { "success":False, "msg":"TG号验证失效" }

		return send_ret

	del message_obj

	ret = add_member_obj.updatePush({'uid':request.user['user_id'],'_id':_id},{ 'phone': phone })

	return ret

@group_add_member.route('/del_chat_phone/<_id>/<phone>',methods=['POST'])
def DelChatPhone(_id,phone):

	add_member_obj = AddMember()

	ret = add_member_obj.updateSelf({'_id':_id,'uid':request.user['user_id']},{'$pull':{'phone':phone}})

	return ret

@group_add_member.route('/add_chat_user/<chatid>/<_id>',methods=['POST'])
def AddChatUser(chatid,_id):

	add_member_obj = AddMember()

	add_member = add_member_obj.findOne({'uid':request.user['user_id'],'_id':_id})

	chatids = add_member['chatids']

	uids = add_member['uids']

	success = add_member['success']

	fail = add_member['fail']

	phone  = add_member['phone'][0]

	if not phone:
		
		return { "success":False, "msg":"tg号不得为空" }

	if chatid in chatids:
		
		return { "success":False, "msg":"已经添加过该群" }

	chatids.append(chatid)

	group_obj = Group(phone)

	chatinfo = []

	count = group_obj.get_chat_members_count(chatid)

	if not count['success']:

		return count

	time = int(count['msg']/200) + 1

	for x in range(0,time):
		
		offset = x*200

		info = group_obj.get_chat_members(chatid,offset)

		if info['success']:

			for i in info['msg']:
				
				chatinfo.append(i)


	for chat in chatinfo:
		
		if  chat['user']['username'] and chat['status'] == 'member' and not chat['user']['is_self'] and not chat['user']['is_bot'] and not chat['user']['is_deleted'] and chat['user']['username'] not in uids and chat['user']['username'] not in success and chat['user']['username'] not in fail:

			uids.append(chat['user']['username'])

	del group_obj

	ret = add_member_obj.update({'uid':request.user['user_id'],'_id':_id},{ 'chatids': chatids,'uids': uids })

	return ret


@group_add_member.route('/add_run/<_id>/<status>',methods=['POST'])
def AddRun(_id,status):

	add_member_obj = AddMember()

	user_obj = User()

	user = user_obj.findOne({'_id':request.user['user_id']})

	if user['money']<1000 and int(status):
		
		return {'success':False,'msg':'金额不足，服务保底金额1000金币'}

	add_item = add_member_obj.findOne({"_id":_id,'uid':request.user['user_id']})

	if not add_item:
		
		return {'success':False,'msg':'拉人服务不存在'}

	ret = add_member_obj.update({'_id':add_item['_id']},{'status':int(status)})

	return ret

