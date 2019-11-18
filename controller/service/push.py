# 广告代发服务

from flask import Blueprint, request, current_app

from model.Client import Client

from model.Order import Order

from model.Push import Push

import time

push = Blueprint('push',__name__)

@push.before_request
def before_request():

	return '22222222'

@push.route('/get_push',methods=['POST'])
def get_push():

	print(111111)

@push.route('/add_push',methods=['POST'])
def add_push():
	print(111111)

@push.route('/del_push',methods=['POST'])
def add_push():
	print(111111)

@push.route('/edit_push',methods=['POST'])
def add_push():
	print(111111)

@push.route('/order_push',methods=['POST'])
def order_push():
	print(111111)