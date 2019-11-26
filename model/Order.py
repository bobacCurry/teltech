from model.Base import Base

# 订单
class Order(Base):
	
	def __init__(self):

		Base.__init__(self,'Order')

		self.scheme = {
			# 服务类型
			"type":"",
			# clientid
			"cid":"",
			# 时长（天）
			"days":0,
			# 备注
			"memo":"",
			# 状态
			"status":0
		}

		self.timeStamp = True