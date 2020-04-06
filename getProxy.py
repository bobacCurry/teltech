from model.Proxy import Proxy

from bs4 import BeautifulSoup

import requests

import time

import sys

try:
	
	ret = requests.get('https://www.firexproxy.com/en',timeout=10)

	status_code = ret.status_code

	if status_code !=200 :

		sys.exit()

except Exception as e:
	
	print(e)

	sys.exit()

text = ret.text

bs = BeautifulSoup(text,"html.parser") # 缩进格式

rowgroup = bs.find_all(role="rowgroup")[1]


rows = rowgroup.find_all(role="row")

proxys = []

addTime = int(time.time())

for row in rows:
	
	cell = row.find_all(role="cell")

	ip = cell[1].get_text()

	port = int(cell[2].get_text())

	protocol = cell[3].get_text()

	ping = int(cell[4].get_text())

	if protocol !='SOCKS5':
		
		break

	if ping > 1000:
		
		continue

	proxys.append({"ip":ip,"port":port,"ping":ping,"time":addTime})

proxy_obj = Proxy()

if len(proxys):
	
	proxy_obj.insertMany(proxys)

clearTime = addTime - 160

proxy_obj.remove({"time":{"$lt":clearTime}})

sys.exit()