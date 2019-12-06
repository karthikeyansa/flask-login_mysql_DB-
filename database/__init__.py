from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

class UserDb():
	def __init__(self, app):
		key = os.urandom(24) #random number
		key = str(key)
		app = app
		app.secret_key = key
		#database connection
		app.config['MYSQL_HOST'] = 'localhost' 
		app.config['MYSQL_USER'] = 'root'	   
		app.config['MYSQL_PASSWORD'] = '12345' 
		app.config['MYSQL_DB'] = 'pythonlogin'   
		self.app = app
		self.mysql = MySQL(app)
	def get_account(self, username, password):
		cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s',(username,password))
		return cursor.fetchone()
	def get_registered(self,username):
		cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s', [username])
		return cursor.fetchone()
	def get_register(self,username, password, email):
		cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', [username, password, email])
		return self.mysql.connection.commit()
	def get_profile(self,s):
		cursor =self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = %s', [s])
		return cursor.fetchone()