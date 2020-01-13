from client.group import Group

def get_chat(chatid):
	
	group = Group('639776884112')

	return group.get_chat(chatid)

ret = get_chat('MeiShiShuo')

print(ret['msg']['members_count'],ret['msg']['permissions'])