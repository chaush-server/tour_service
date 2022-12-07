# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
import re
import sqlite3
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

app.secret_key = 'M-s-i-kgh#$245rK:?/;!/?!/42-2'


@app.route('/home')
def home():
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    if session.get('logged'):
        cursor.execute('SELECT * FROM service')
        data = cursor.fetchall()
        print(data)
        return render_template('home.html', data=data)
    else:
        return redirect("/login")


@app.route('/find=<string:name>')
def home_find(name):
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    if session.get('logged'):
        cursor.execute(f"""SELECT * FROM service WHERE name LIKE '%{name}%'""")
        data = cursor.fetchall()
        if data:
            print(data)
            return render_template('home.html', data=data)
        else:
            return render_template('home.html')
    else:
        return redirect("/login")


@app.route('/service/<int:service_id>')
def service(service_id):
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM service WHERE service_id = {service_id}')
    data = cursor.fetchone()
    return render_template('service.html', data=data)


@app.route('/cart/<int:service_id>')
def buy(service_id):
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM service WHERE service_id = {service_id}')
    data = cursor.fetchone()
    print(data)
    return render_template("cart.html", data=data)


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/cart/<int:service_id>')
def buy_service(service_id):
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM service WHERE service_id = {service_id}')
    data = cursor.fetchone()
    return render_template('cart.html', data=data)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    msg = ''
    if session.get('logged'):
        return redirect('/home')
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        cursor.execute(f"SELECT * FROM user WHERE username = {username}")
        account = cursor.fetchone()
        if account and pbkdf2_sha256.verify(request.form['password'], account['password']):
            if account['admin']:
                session['admin'] = True
            else:
                session['admin'] = False
            session['logged'] = True
            session['id'] = account['user_id']
            session['username'] = account['username']
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
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    if session.get('logged'):
        return redirect('/home')
    msg = ''
    if request.method == 'POST' and 'username' in request.form \
            and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = pbkdf2_sha256.hash(request.form['password'])
        email = request.form['email']
        cursor.execute(f"SELECT * FROM user WHERE username = {username}")
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
            cursor.execute(f'INSERT INTO user VALUES (NULL, "{username}", "{password}", "{email}", 0)')
            db.commit()
            return redirect('/login')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/about')
def about():
    return render_template('about.html')
