from hashlib import md5

import time

# pyjwt

import jwt

import json

token_dict = { 'time':time.time(), 'info':'' }

headers = { 'alg': "HS256", 'kid': "TelTech" }

jwt_ket = 'TelTech'

def token_encode(info):

	token_dict['info'] = json.dumps(info)

	token = jwt.encode(token_dict, jwt_ket, algorithm="HS256", headers=headers).decode('ascii')

	return token

def token_decode(token):
	
	now = time.time()

	try :

		data = jwt.decode(token, jwt_ket, algorithms=['HS256'])

		if (now - data['time'])/1000 > 3600*24*7 :

			return {'success':False,'msg':'token过期'}

		return {'success':True,'msg':json.loads(data['info'])}

	except Exception as e:

		return {'success':False,'msg':e}