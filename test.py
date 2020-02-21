from client.chat import Chat

import sys

def get_info():
	
	phone = sys.argv[1]

	chatid = sys.argv[2]

	chat = Chat(phone)

	info = chat.send_message(chatid,'.')

	print(info['msg'])

get_info()

sys.exit()