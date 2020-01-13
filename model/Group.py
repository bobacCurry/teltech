from model.Base import Base

class Group(Base):
	
	def __init__(self):

		Base.__init__(self,'Group')

		self.scheme = {
			'uid':'',
			'phone':'',
			'id':'',
			'type':'supergroup',
			'is_verified':False,
			'is_restricted':False,
			'is_scam':False,
			'title':'',
			'username':'',
			'photo':'',
			'description':'',
			'invite_link':'',
			'pinned_message':'',
			'members_count':0,
			'restrictions':[],
			'permissions':[],
		}

		self.timeStamp = False