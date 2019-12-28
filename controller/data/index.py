from flask import Blueprint, request, current_app

data_index = Blueprint('data_index',__name__)

@data_index.route('/save_error_logger',methods=['POST'])
def save_error_logger():

	return { "success":True, "msg":"ok" }