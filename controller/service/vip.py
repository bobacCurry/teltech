# vip服务

from flask import Blueprint, request, current_app

from model.Client import Client

from model.Order import Order

from client.check import Check

from controller.account.auth import token_decode

service_vip = Blueprint('service_vip',__name__)

@service_push.before_request
def before_request():

	request.user = None

	user = token_decode(request.headers.get("token"))

	if user['success'] and user['vip']:
		
		request.user = user['msg']

	else:
		
		return { "success":False, "msg":"用户数据缺失或权限不足" },401


