from model.AddMember import AddMember

import multiprocessing

import sys

from client.group import Group

import time

def adduser(phone,target,addids):
	
	group_obj = Group(phone)

	success = []

	fail = []

	i = 0

	for uid in addids:
		
		addinfo = group_obj.add_chat_members(target,uid)

		print(addinfo)

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

	print({'success':success,'fail':fail,'last':addids[i:]})

	return {'success':success,'fail':fail,'last':addids[i:]}

def run():

	add_member_obj = AddMember()

	add_item = add_member_obj.findOne({'count':{'$lt':3},'nexttime':{'$gt':time.time()},'uids': {'$size': {'$gt':0}},'status':1})

	if not add_item:
		
		return {'success':False,'msg':'暂无拉人服务'}

	phones = add_item['phone']

	uids = add_item['uids']

	success = add_item['success']

	fail = add_item['fail']

	for phone in phones:

		uids = uids[20:]

		addids = uids[0:20]

		ret = adduser(phone,add_item['target'],addids)

		success = success + ret['success']

		fail = fail + ret['fail']

		uids = uids + ret['last']

	add_member_obj = AddMember()

	count = add_item['count'] + 1

	if count==3:
		
		nexttime = time.time() + 24*3600 + 600

	ret = add_member_obj.update({'_id':add_item['_id']},{ 'uids': uids,'success':success,'fail':fail,'count':count,'nexttime':nexttime})

	return ret

ret = run()

print(ret)

sys.exit()