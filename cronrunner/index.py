import logging

import datetime

from client.message import Message

from client.chat import Chat

class Index:

	def __init__(self):

		self.message = Message

		self.chat = Chat

	def logger(self,info):
		
		today=datetime.date.today()

		filename = 'log/'+'cron'+'-'+str(today)+'.log'

		logging.basicConfig(level=logging.INFO,filename=filename,format='%(asctime)s - %(message)s')
		
		logging.info(info)