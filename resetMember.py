from model.AddMember import AddMember

import sys

add_member_obj = AddMember()

add_member_obj.update({'count':{ '$ne' : 0 }},{ 'count':0 })

sys.exit()