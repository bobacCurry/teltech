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

from controller.admin.order import admin_order

from controller.admin.chat import admin_chat

from controller.admin.proxy import admin_proxy

from controller.data.index import data_index

app = Flask(__name__)

app.register_blueprint(account,url_prefix='/account')

app.register_blueprint(service_push,url_prefix='/service/push')

app.register_blueprint(service_order,url_prefix='/service/order')

app.register_blueprint(service_auth,url_prefix='/service/auth')

app.register_blueprint(service_client,url_prefix='/service/client')

app.register_blueprint(service_chat,url_prefix='/service/chat')

app.register_blueprint(service_vip,url_prefix='/service/vip')

app.register_blueprint(admin_order,url_prefix='/admin/order')

app.register_blueprint(admin_chat,url_prefix='/admin/chat')

app.register_blueprint(admin_proxy,url_prefix='/admin/proxy')

app.register_blueprint(data_index,url_prefix='/data')

if __name__ == '__main__':

	app.debug = True

	handler = logging.FileHandler('log/flask.log')

	handler.setLevel(logging.DEBUG)

	logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

	handler.setFormatter(logging_format)

	app.logger.addHandler(handler)

	app.run()