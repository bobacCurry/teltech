from model.AddMember import AddMember

from model.User import User

import sys

from client.group import Group

import time

import timeout_decorator

def adduser(phone,target,addids):

	group_obj = Group(phone,True)

	success = []

	fail = []

	i = 0

	for uid in addids:
		
		addinfo = group_obj.add_chat_members(target,uid)

		print(phone,addinfo['msg'])

		if addinfo['success']:
			
			success.append(uid)

		else:

			if '[420 FLOOD_WAIT_X]' in addinfo['msg']:
				
				break

			elif '[400 PEER_FLOOD' in addinfo['msg']:

				break

			elif '[400 CHAT_ID_INVALID' in addinfo['msg']:

				break

			elif '[400 CHAT_ADMIN_REQUIRED' in addinfo['msg']:

				break

			elif '[400 CHAT_ADMIN_REQUIRED' in addinfo['msg']:

				break

			else:

				fail.append(uid)

		i = i + 1

	return {'success':success,'fail':fail,'last':addids[i:]}

def run():

	add_member_obj = AddMember()

	user_obj = User()

	add_item = add_member_obj.findOne({'count':{'$lt':4},'nexttime':{'$lt':time.time()},'status':1,'$where':"this.uids.length>0"})

	if not add_item:
		
		return {'success':False,'msg':'暂无拉人服务'}

	user = user_obj.findOne({'_id':add_item['uid']})

	if user['money']<1000:
		
		add_member_obj.update({'_id':add_item['_id']},{'status':0})
		
		return {'success':False,'msg':user['account']+' 金额不足'}

	phones = add_item['phone']

	uids = add_item['uids']

	success = add_item['success']

	fail = add_item['fail']

	cost = 0

	for phone in phones:

		if len(uids) == 0:
			
			break

		addids = uids[0:15]
		
		uids = uids[15:]

		ret = {}

		try:
			
			ret = adduser(phone,add_item['target'],addids)

		except Exception as e:
			
			print(e)

			ret = {'success':[],'fail':[],'last':addids}

		success = success + ret['success']

		fail = fail + ret['fail']

		uids = uids + ret['last']
		# 发广告花费
		cost = cost + len(ret['success'])

	count = add_item['count'] + 1

	nexttime = 0

	if count==4:
		
		nexttime = int(time.time()) + 24*3600 + 600

	status = 1

	if len(uids) == 0:
		
		status = 0

	money = user['money'] - cost*3

	user_obj.update({'_id':add_item['uid']},{'money':money})

	ret = add_member_obj.update({'_id':add_item['_id']},{ 'uids': uids,'success':success,'fail':fail,'count':count,'nexttime':nexttime,'status':status})

	return ret

ret = run()

sys.exit()