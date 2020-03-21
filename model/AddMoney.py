from model.Base import Base

# 订单
class AddMoney(Base):
	
	def __init__(self):

		Base.__init__(self,'AddMoney')

		self.scheme = {
			# userid
			"uid":"",
			# 数量
			"money":0,
			# 备注
			"memo":"",
			# 状态
			"status":0
		}

		self.timeStamp = True