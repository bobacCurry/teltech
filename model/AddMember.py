from model.Base import Base

class AddMember(Base):
	
	def __init__(self):

		Base.__init__(self,'AddMember')

		self.scheme = { 
			'uid':'',
			# 目标群
			'target':'',
			# 用哪些客户端去拉
			'phone':[],
			# 需要拉取的群
			'chatids':[],
			# 要拉的人
			'uids':[],
			# 拉成功的人
			'success':[],
			# 拉失败的人
			'fail':[],
			# 本日第几次执行
			'count':0,
			# 下次执行时间
			'nexttime':0,
			# 开启拉人服务
			'status':0
		}

		self.timeStamp = False