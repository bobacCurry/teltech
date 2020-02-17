from model.AddChat import AddChat

from model.AddQueue import AddQueue

import time

import logging

import sys

def CreateQueue():
	
	add_obj = AddChat()

	queue = add_obj.find({'status':0})

	if len(queue):
		
		clear_obj = AddQueue()

		for item in queue:

			exist = clear_obj.findOne({'aid':item['_id']})
			
			if not exist:
				
				clear_obj.insert({'aid':item['_id']})

CreateQueue()

sys.exit()