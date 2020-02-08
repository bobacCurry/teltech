from model.AddMember import AddMember

import multiprocessing

import sys

from client.group import Group

def adduser(phone,addids):
	
	group_obj = Group(phone)

	success = []

	fail = []

	i = 0

	for uid in addids:
		
		addinfo = group_obj.add_chat_members(add_item['target'],uid)

		print(addinfo)

		if addinfo['success']:
			
			success.append(uid)

		else:

			if '[420 FLOOD_WAIT_X]' in addinfo['msg']:
				
				break

			elif '[400 PEER_FLOOD]' in addinfo['msg']:

				break

			elif '[400 USER_KICKED]' in addinfo['msg'] or '[403 USER_PRIVACY_RESTRICTED]' in addinfo['msg'] or '[403 USER_CHANNELS_TOO_MUCH]' in addinfo['msg'] or '[400 USER_NOT_MUTUAL_CONTACT]' in addinfo['msg']:

				fail.append(uid)

			else:

				break

		i = i + 1

	print({'success':success,'fail':fail,'last':addids[i:]})

	return {'success':success,'fail':fail,'last':addids[i:]}

add_member_obj = AddMember()

add_item = add_member_obj.findOne({'status':0})

status = 0

phones = add_item['phone']

uids = add_item['uids']

success = add_item['success']

fail = add_item['fail']

for phone in phones:

	uids = uids[20:]

	addids = uids[0:20]

	ret = adduser(phone,addids)

	success = success + ret['success']

	fail = fail + ret['fail']

	uids = uids + ret['last']

add_member_obj = AddMember()

ret = add_member_obj.update({'_id':add_item['_id']},{ 'uids': uids,'success':success,'fail':fail,'status':status })

print(ret)

sys.exit()