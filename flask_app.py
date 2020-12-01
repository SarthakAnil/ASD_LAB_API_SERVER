from flask import jsonify
from flask import request
from config import app
from config import mysql


@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message': 'Record not found: ' + request.url,
	}
	respone = jsonify(message)
	respone.status_code = 404
	return respone
		
if __name__ == "__main__":
	app.run()