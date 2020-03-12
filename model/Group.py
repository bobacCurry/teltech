from model.Base import Base

class GroupModel(Base):
	
	def __init__(self):

		Base.__init__(self,'GroupModel')

		self.scheme = {
			'uid':'',
			'phone':'',
			'id':'',
			'is_verified':False,
			'is_restricted':False,
			'is_scam':False,
			'title':'',
			'description':'',
			'username':'',
			'photo':'',
			'invite_link':'',
			'pinned_message':'',
			'members_count':0,
			'restrictions':[],
			'permissions':{},
			'admins':[],
			'bots':[]
		}

		self.timeStamp = False
		