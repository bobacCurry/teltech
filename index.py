from flask import Flask,request,Blueprint

from cache.index import Cache

import logging

from controller.account.account import account

from controller.account.auth import token_encode,token_decode

from controller.service.push import service_push

from controller.service.auth import service_auth

from controller.admin.order import admin_order

app = Flask(__name__)

app.register_blueprint(account,url_prefix='/account')

app.register_blueprint(service_push,url_prefix='/service/push')

app.register_blueprint(service_auth,url_prefix='/service/auth')

app.register_blueprint(admin_order,url_prefix='/admin/order')

if __name__ == '__main__':

	app.debug = True

	handler = logging.FileHandler('flask.log')

	handler.setLevel(logging.DEBUG)

	logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

	handler.setFormatter(logging_format)

	app.logger.addHandler(handler)

	app.run()