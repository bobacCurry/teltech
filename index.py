from flask import Flask,request,Blueprint

import logging

from controller.account.account import account

from controller.service.push import push

from controller.account.auth import token_encode,token_decode

app = Flask(__name__)

app.register_blueprint(account,url_prefix='/account')

app.register_blueprint(push,url_prefix='/service/push')

if __name__ == '__main__':

	app.debug = True

	handler = logging.FileHandler('flask.log')

	handler.setLevel(logging.DEBUG)

	logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

	handler.setFormatter(logging_format)

	app.logger.addHandler(handler)

	app.run()