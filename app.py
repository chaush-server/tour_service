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
        if session.get('cart'):
            cart_data = session['cart']
        else:
            cart_data = []
        return render_template('home.html', data=data, cart=cart_data)
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
            return render_template('home.html', data=data, cart=session['cart'])
        else:
            return render_template('home.html', cart=session['cart'])
    else:
        return redirect("/login")


@app.route('/service/<int:service_id>')
def service(service_id):
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM service WHERE service_id = {service_id}')
    data = cursor.fetchone()
    return render_template('service.html', data=data, cart=session['cart'])


@app.route('/cart')
def cart():
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    data = []
    for i in session['cart']:
        cursor.execute(f"""SELECT * FROM service WHERE service_id  = {i} """)
        data.append(cursor.fetchone())
    return render_template('cart.html', data=data)


@app.route('/remove_from_cart/<int:service_id>', methods=['POST', 'GET', 'DELETE'])
def remove_from_cart(service_id):
    session['cart'].remove(service_id)
    ses = session['cart']
    if ses:
        session['cart'] = ses
    else:
        session['cart'] = []
    return redirect('/cart')


@app.route('/add_to_cart/<int:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id):
    if session.get('cart') and product_id not in session['cart']:
        session['cart'] += [product_id]
    elif not session.get('cart'):
        session['cart'] = [product_id]
    return redirect('/home')


@app.route('/buy')
def buy():
    session['cart'] = []
    return render_template('payment.html')


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
    if request.method == 'POST' and request.args.get('username') and request.args.get('password') \
            and request.args.get('email'):
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
