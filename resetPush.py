import time

import sys

from model.Push import Push

def reset():

	push_obj = Push()

	ret = push_obj.updateSelf({'expire':{'$lt':time.time()}},{'$set':{'status':0}})

	print(ret)

reset()

sys.exit()