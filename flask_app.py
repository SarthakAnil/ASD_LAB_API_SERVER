from flask import jsonify
from flask import request
from config import app
from config import mysql


@app.route('/')
def hello_world():
    return 'Hello from Flask!'
######################################################################
@app.route('/change_pass',methods=['POST'])
def change_pass():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		usrName = json['usrName']
		password = json['pass']
		cursor.execute("UPDATE user_table SET pass =%s where login_username =%s;",(password,usrName))
		conn.commit()
		message = {
		'status': 200,
		'message': 'updated ',
		}
		respone = jsonify(message)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
		message = {
		'status': 500,
		'message': 'error in method ',
		#'ERROR': e,
		}
		respone = jsonify(message)
		respone.status_code = 500
		return respone
	finally:
		cursor.close()
		conn.close()
		######################################################################
@app.route('/put_events',methods=['POST'])
def put_events():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		batch_id = json['batch_id']
		event_desc = json['event_desc']
		event_id = json['event_id']
		event_name = json['event_name']
		userid = json['userid']


		cursor.execute('''insert into 
								events (
									event_id, 
									userid, 
									batch_id, 
									event_name, 
									event_desc
								)
								values
								(%s,%s,%s,%s,%s);
  								''',(event_id, 
									userid, 
									batch_id, 
									event_name, 
									event_desc))
		conn.commit()
		message = {
		'status': 200,
		'message': 'updated ',
		}
		respone = jsonify(message)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
		message = {
		'status': 500,
		'message': 'error in method ',
		#'ERROR': e,
		}
		respone = jsonify(message)
		respone.status_code = 500
		return respone
	finally:
		cursor.close()
		conn.close()
##///////////////////////////////////////////////////////////////////////////////////////////////////////
##########################################################################################
@app.route('/get_events',methods=['POST'])
def user_table():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		usrID = json['usrID']
		cursor.callproc('retEvent', [usrID, ])
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))
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
##//////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/eventid_check',methods=['POST'])
def eventid_check():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		evendID = json['eventID']
		cursor.execute("SELECT Exists(SELECT * FROM events WHERE event_id = %s) AS exist;",evendID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))
		#return json.dumps(json_data)
		respone = jsonify(json_data)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
		message = {
		'status': 500,
		'message': 'error in method ',
		#'ERROR': e,
		}
		respone = jsonify(message)
		respone.status_code = 500
		return respone
	finally:
		cursor.close()
		conn.close()

##//////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/batchid_check',methods=['POST'])
def batchid_check():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		batchID = json['batchID']
		cursor.execute("SELECT Exists(SELECT * FROM batch WHERE batch_id = %s) AS exist;",batchID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))
		#return json.dumps(json_data)
		respone = jsonify(json_data)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
		message = {
		'status': 500,
		'message': 'error in method ',
		#'ERROR': e,
		}
		respone = jsonify(message)
		respone.status_code = 500
		return respone
	finally:
		cursor.close()
		conn.close()

##//////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/user_check',methods=['POST'])
def user_check():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		usrName = json['usrName']
		cursor.execute("SELECT Exists(SELECT * FROM user_table WHERE login_username = %s) AS exist;",usrName)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))
		#return json.dumps(json_data)
		respone = jsonify(json_data)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
		message = {
		'status': 500,
		'message': 'error in method ',
		#'ERROR': e,
		}
		respone = jsonify(message)
		respone.status_code = 500
		return respone
	finally:
		cursor.close()
		conn.close()
##///////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/pass_check',methods=['POST'])
def pass_check():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		usrName = json['usrName']
		cursor.execute("SELECT pass FROM user_table where login_username = %s",usrName)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))
		respone = jsonify(json_data)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
		message = {
		'status': 500,
		'message': 'error in method ',
		}
		respone = jsonify(message)
		respone.status_code = 500
		return respone
	finally:
		cursor.close()
		conn.close()

##///////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/get_time_Table',methods=['POST'])
def get_time_Table():
	try:
		message = {}
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		batchID = json['batchID']
		cursor.execute('''
		SELECT * FROM hour  
		LEFT  JOIN  ((teach
		RIGHT JOIN teacher USING (userid))
		RIGHT JOIN  course USING (course_id)
		) 
		USING (course_id)
		WHERE table_id =(
							SELECT table_id 
							FROM batch
							WHERE batch_id =%s
						)
		AND day ='MONDAY'
		ORDER BY hour_id ; 
		''',batchID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["MONDAY"]=json_data
		##EXECUTING FOR TUESDAY
		cursor.execute('''
		SELECT * FROM hour  
		LEFT  JOIN  ((teach
		RIGHT JOIN teacher USING (userid))
		RIGHT JOIN  course USING (course_id)
		) 
		USING (course_id)
		WHERE table_id =(
							SELECT table_id 
							FROM batch
							WHERE batch_id =%s
						)
		AND day ='TUESDAY'
		ORDER BY hour_id ; 
		''',batchID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["TUESDAY"]=json_data
		##EXECUTING FOR WEDNESDAY
		cursor.execute('''
		SELECT * FROM hour  
		LEFT  JOIN  ((teach
		RIGHT JOIN teacher USING (userid))
		RIGHT JOIN  course USING (course_id)
		) 
		USING (course_id)
		WHERE table_id =(
							SELECT table_id 
							FROM batch
							WHERE batch_id =%s
						)
		AND day ='WEDNESDAY'
		ORDER BY hour_id ; 
		''',batchID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["WEDNESDAY"]=json_data
		##EXECUTING FOR THURSDAY
		cursor.execute('''
		SELECT * FROM hour  
		LEFT  JOIN  ((teach
		RIGHT JOIN teacher USING (userid))
		RIGHT JOIN  course USING (course_id)
		) 
		USING (course_id)
		WHERE table_id =(
							SELECT table_id 
							FROM batch
							WHERE batch_id =%s
						)
		AND day ='THURSDAY'
		ORDER BY hour_id ; 
		''',batchID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["THURSDAY"]=json_data
		##EXECUTING FOR FRIDAY
		cursor.execute('''
		SELECT * FROM hour  
		LEFT  JOIN  ((teach
		RIGHT JOIN teacher USING (userid))
		RIGHT JOIN  course USING (course_id)
		) 
		USING (course_id)
		WHERE table_id =(
							SELECT table_id 
							FROM batch
							WHERE batch_id =%s
						)
		AND day ='FRIDAY'
		ORDER BY hour_id ; 
		''',batchID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["FRIDAY"]=json_data
		respone = jsonify(message)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
		message = {
		'status': 500,
		'message': 'error in method ',
		}
		respone = jsonify(message)
		respone.status_code = 500
		return respone
	finally:
		cursor.close()
		conn.close()
###########################################################################################################
##///////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/get_teacher_TT',methods=['POST'])
def get_teacher_TT():
	try:
		message = {}
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		usrID = json['usrID']
		cursor.execute('''
		SELECT * FROM hour  
		LEFT   JOIN teach
		USING (course_id)
		WHERE 
		day ='MONDAY'
		AND 
		userid = %s
		ORDER BY hour_id ; 
		''',usrID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["MONDAY"]=json_data
		##EXECUTING FOR TUESDAY
		cursor.execute('''
		SELECT * FROM hour  
		LEFT   JOIN teach
		USING (course_id)
		WHERE 
		day ='TUESDAY'
		AND 
		userid = %s
		ORDER BY hour_id ; 
		''',usrID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["TUESDAY"]=json_data
		##EXECUTING FOR WEDNESDAY
		cursor.execute('''
		SELECT * FROM hour  
		LEFT   JOIN teach
		USING (course_id)
		WHERE 
		day ='WEDNESDAY'
		AND 
		userid = %s
		ORDER BY hour_id ; 
		''',usrID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["WEDNESDAY"]=json_data
		##EXECUTING FOR THURSDAY
		cursor.execute('''
		SELECT * FROM hour  
		LEFT   JOIN teach
		USING (course_id)
		WHERE 
		day ='THURSDAY'
		AND 
		userid = %s
		ORDER BY hour_id ;  
		''',usrID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["THURSDAY"]=json_data
		##EXECUTING FOR FRIDAY
		cursor.execute('''
		SELECT * FROM hour  
		LEFT   JOIN teach
		USING (course_id)
		WHERE 
		day ='FRIDAY'
		AND 
		userid = %s
		ORDER BY hour_id ; 
		''',usrID)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))

		message["FRIDAY"]=json_data
		respone = jsonify(message)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
		message = {
		'status': 500,
		'message': 'error in method ',
		}
		respone = jsonify(message)
		respone.status_code = 500
		return respone
	finally:
		cursor.close()
		conn.close()
###########################################################################################################


##///////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/get_user_data',methods=['POST'])
def get_user_data():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		json = request.get_json(force=True)
		usrName = json['usrName']
		cursor.execute('''
		SELECT * FROM (
		(SELECT Concat(COALESCE(Upper(first_name),'')," ",COALESCE(Upper(middle_name),'')," ",COALESCE(upper(last_name),'')) As 'Name',
		userid,teacher_email AS email,"" AS batch_id
		FROM teacher)
		UNION
		(SELECT Concat(COALESCE(Upper(first_name),'')," ",COALESCE(Upper(middle_name),'')," ",COALESCE(upper(last_name),'')) As 'Name',
		userid,student_email AS email,batch_id
		FROM student)) H
		NATURAL JOIN
		user_table
		WHERE
		login_username =%s
		''',usrName)
		row_headers=[x[0] for x in cursor.description]
		empRows = cursor.fetchall()
		json_data=[]
		for result in empRows:
			json_data.append(dict(zip(row_headers,result)))
		respone = jsonify(json_data)
		respone.status_code = 200
		return respone

	except Exception as e:
		print(e)
		message = {
		'status': 500,
		'message': 'error in method ',
		}
		respone = jsonify(message)
		respone.status_code = 500
		return respone
	finally:
		cursor.close()
		conn.close()
###########################################################################################################
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