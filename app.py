from flask import Flask,request,redirect,url_for,render_template,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re 
import os

app = Flask(__name__)
#generating secret key
key = os.urandom(24) #random number
key = str(key)
#secret_key generated
app.secret_key = key
#database connection
app.config['MYSQL_HOST'] = 'localhost' #changes based on your installation
app.config['MYSQL_USER'] = 'root'	   #changes based on your installation
app.config['MYSQL_PASSWORD'] = '12345' #changes based on your installation
app.config['MYSQL_DB'] = 'pythonlogin'   #changes based on your installation
#mysql instance creaion
mysql = MySQL(app)


#login
@app.route('/',methods=['GET','POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		#account fetch
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s',(username,password))
		account = cursor.fetchone()
		#if account exists
		if account:
			#session creation
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			#homepage
			return redirect(url_for('home'))
		else:
			#if account not found
			msg = 'invalid username and password!'
	return render_template('index.html',msg = msg)
#register 
@app.route('/register',methods = ['GET','POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
 		# Check if account exists using MySQL
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s', [username])
		account = cursor.fetchone()
        # If account exists show error and validation checks
		if account:
			msg = 'Account already exists!'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address!'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers!'
		elif not username or not password or not email:
			msg = 'Please fill out the form!'
# Account doesnt exists and the form data is valid, now insert new account into accounts table
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', [username, password, email])
			mysql.connection.commit()
			msg = 'You have successfully registered!'
	#empty form submission
	elif request.method == 'POST':
		msg = 'please fill the form'
	return render_template('register.html',msg = msg)
#homepage
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))
#profile
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))
#logout
@app.route('/logout')
def logout():
	#remove session data
	session.pop('loggedin',None)
	session.pop('id',None)
	session.pop('username',None)
	#loginpage
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug = True)
