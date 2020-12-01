from flask import jsonify
from flask import request
from config import app
from config import mysql


@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/user_table')
def user_table():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("Select * from user_table")
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))
		#return json.dumps(json_data)
		respone = jsonify(json_data)
		respone.status_code = 200
		return respone
	except cursor.Error as err:
		print(err)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/user_check')
def user_check():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.json
		_usrName = json['usrName']
		cursor.execute("SELECT Exists(SELECT * FROM user_table WHERE login_username = %s);",_usrName)
		empRows = cursor.fetchall()

		respone = jsonify(empRows)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

		
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