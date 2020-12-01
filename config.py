from flask import Flask
from flaskext.mysql  import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'sarthakanil'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Phoenix@777'
app.config['MYSQL_DATABASE_DB'] = 'sarthakanil$ocm'
app.config['MYSQL_DATABASE_HOST'] = 'sarthakanil.mysql.pythonanywhere-services.com'


mysql = MySQL(app)