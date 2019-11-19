from model.Base import Base

from datetime import datetime
# 订单
class Order(Base):
	
	def __init__(self):

		Base.__init__(self,'Order')

		self.scheme = {
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

	def insert_one(self,document):

		return '11111'