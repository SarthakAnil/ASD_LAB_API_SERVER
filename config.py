from flask import Flask
from flaskext.mysql  import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'sql12379361'
app.config['MYSQL_DATABASE_PASSWORD'] = '46kms1WZC1'
app.config['MYSQL_DATABASE_DB'] = 'sql12379361'
app.config['MYSQL_DATABASE_HOST'] = 'sql12.freemysqlhosting.net'

mysql = MySQL(app)