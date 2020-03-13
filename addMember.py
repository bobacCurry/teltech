from model.AddMember import AddMember

import multiprocessing

import sys

from client.group import Group

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

def run(_id):

	add_member_obj = AddMember()

	add_item = add_member_obj.findOne({"_id":_id})

	if not add_item:
		
		return {'success':False,'msg':'拉人服务不存在'}

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

	ret = add_member_obj.update({'_id':add_item['_id']},{ 'uids': uids,'success':success,'fail':fail})

	return ret

_id = sys.argv[1]

print(_id)

ret = run(_id)

print(ret)

sys.exit()