from model.AddMember import AddMember

import sys

add_member_obj = AddMember()

add_member_obj.updateSelf({'count':10},{'$set':{ 'count':0 }})

sys.exit()