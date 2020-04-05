import requests

class ProxyTest:
	
	def __init__(self,ip,port):
		
		self.ip = ip

		self.port = port

	def Check(self):
		
		try:

		    ret = requests.get('http://www.baidu.com',proxies={'http':'socks5://'+self.ip+':'+str(self.port)},timeout=5)

		except Exception as e:

		    print(e)

		    return {'success':False,'msg':str(e)}

		return {'success':True,'msg':'proxy ok'}