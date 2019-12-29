from flask import Blueprint, request, current_app

from controller.account.auth import token_decode

import os,base64,datetime

from hashlib import md5

from env import static_url

data_index = Blueprint('data_index',__name__)

@data_index.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失" }

@data_index.route('/save_error_logger',methods=['POST'])
def save_error_logger():

	return { "success":True, "msg":"ok" }


@data_index.route('/upload_image',methods=['POST'])
def upload_image():
	
	data = request.form or request.get_json()

	try:

		data['image']

		if not data['image']:
			
			return { "success":False, "msg":"数据缺失" }
	
	except Exception as e:
	
		return { "success":False, "msg":"数据缺失" }

	image = data['image']

	if len(image) % 4:
	    
	    image += '=' * (4 - len(image) % 4)
	
	image = image.split(',')

	image = image[len(image)-1]

	userid = request.user['user_id']

	time = datetime.datetime.now()

	filename = md5((userid+str(time)).encode(encoding='utf-8')).hexdigest()+'.jpeg'

	path = static_url+'/static/'+filename

	try:

		imgdata = base64.b64decode(image)

		file = open('static/'+filename,'wb')

		file.write(imgdata)

		file.close()

	except Exception as e:
		
		return { "success":False, "msg":str(e) }

	return { "success":True, "msg":"保存成功","path":path }