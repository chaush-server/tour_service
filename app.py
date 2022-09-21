# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

app.secret_key = 'M-s-i-k'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'tour_service'

mysql = MySQL(app)


@app.route('/home/')
@app.route('/home')
def home():
    if session.get('logged'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM service')
        data = cursor.fetchall()
        return render_template('home.html', data=data)
    else:
        return redirect("/login")


@app.route('/home/service/<int:service_id>')
def service(service_id):
    return str(service_id)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = 'Hello'
    if session.get('logged'):
        return redirect('/home')
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account and pbkdf2_sha256.verify(request.form['password'], account['password']):
            session['logged'] = True
            session['id'] = account['user_id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('logged', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('logged'):
        return redirect('/home')
    msg = ''
    if request.method == 'POST' and 'username' in request.form \
            and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = pbkdf2_sha256.hash(request.form['password'])
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return redirect('/login')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/about')
def about():
    return render_template('about.html')
