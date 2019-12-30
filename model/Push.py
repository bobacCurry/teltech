from model.Base import Base

class Push(Base):
	
	def __init__(self):

		Base.__init__(self,'Push')

		self.scheme = {
			# title
			"title":"",
			# 用户id
			"uid":"",
			# 服务类型
			"chat_type":0,
			# 文本类型
			"text_type":0,
			# 手机号
			"phone":"",
			# chatid
			"chat":[],
			# chatid的数量
			"count":0,
			# 需要forward的message
			"message_id":0,
			# 文案
			"text":"",
			# 图片
			"media":"",
			# 介绍
			"caption":"",
			# 发送时间
			"minute":[],
			# 服务状态
			"status":0,
			# 到期时间
			"expire":0
		}

		self.timeStamp = True