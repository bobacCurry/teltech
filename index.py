# nohup python3 index.py>>flask_run.log 2>&1 &
from flask import Flask,request,Blueprint

from cache.index import Cache

import logging

from controller.account.account import account

from controller.account.auth import token_encode,token_decode

from controller.service.push import service_push

from controller.service.order import service_order

from controller.service.auth import service_auth

from controller.service.client import service_client

from controller.service.chat import service_chat

from controller.service.vip import service_vip

from controller.service.group import service_group

from controller.admin.order import admin_order

from controller.admin.chat import admin_chat

# from controller.admin.proxy import admin_proxy

from controller.admin.user import admin_user

from controller.data.index import data_index

from controller.group.addMember import group_add_member

app = Flask(__name__)

app.register_blueprint(account,url_prefix='/account')

app.register_blueprint(service_push,url_prefix='/service/push')

app.register_blueprint(service_order,url_prefix='/service/order')

app.register_blueprint(service_auth,url_prefix='/service/auth')

app.register_blueprint(service_client,url_prefix='/service/client')

app.register_blueprint(service_chat,url_prefix='/service/chat')

app.register_blueprint(service_vip,url_prefix='/service/vip')

app.register_blueprint(service_group,url_prefix='/service/group')

app.register_blueprint(admin_order,url_prefix='/admin/order')

app.register_blueprint(admin_chat,url_prefix='/admin/chat')

# app.register_blueprint(admin_proxy,url_prefix='/admin/proxy')

app.register_blueprint(admin_user,url_prefix='/admin/user')

app.register_blueprint(data_index,url_prefix='/data')

app.register_blueprint(group_add_member,url_prefix='/group/add_member')

if __name__ == '__main__':

	app.debug = True

	app.run()