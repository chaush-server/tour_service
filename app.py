# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
import re
import sqlite3
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

app.secret_key = 'M-s-i-kgh#$245rK:?/;!/?!/42-2'


@app.route('/home')
def home():
    if not session.get('logged'):
        return redirect("/login")
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('SELECT * FROM service')
    data = cursor.fetchall()
    if session.get('cart'):
        cart_data = session['cart']
    else:
        cart_data = []
    return render_template('home.html', data=data, cart=cart_data)


@app.route('/home', methods=["POST"])
def home_find():
    if not session.get('logged'):
        return redirect("/login")
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    name = request.form.get('id')
    cursor.execute(f"""SELECT * FROM service WHERE name LIKE '%{name}%'""")
    data = cursor.fetchall()
    if data:
        return render_template('home.html', data=data, cart=session['cart'])
    else:
        return render_template('home.html', cart=session['cart'])


@app.route('/service/<int:service_id>')
def service(service_id):
    if not session.get('logged'):
        return redirect("/login")
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM service WHERE service_id = {service_id}')
    data = cursor.fetchone()
    if not session.get('cart'):
        session['cart'] = []
    return render_template('service.html', data=data, cart=session['cart'])


@app.route('/cart')
def cart():
    if not session.get('logged'):
        return redirect("/login")
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
    if not session.get('logged'):
        return redirect("/login")
    session['cart'].remove(service_id)
    ses = session['cart']
    if ses:
        session['cart'] = ses
    else:
        session['cart'] = []
    return redirect('/cart')


@app.route('/add_to_cart/<int:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id):
    if not session.get('logged'):
        return redirect("/login")
    if session.get('cart') and product_id not in session['cart']:
        session['cart'] += [product_id]
    elif not session.get('cart'):
        session['cart'] = [product_id]
    return redirect('/home')


@app.route('/buy')
def buy():
    if not session.get('logged'):
        return redirect("/login")
    session['cart'] = []
    return render_template('payment.html')


@app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
def login():
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    msg = ''
    if session.get('logged'):
        return redirect('/home')
    reg_data = request.form
    data = {'username': reg_data.get('username'),
            'password': reg_data.get('password')}
    if request.method == 'POST' and data['username'] and data['password']:
        username = data['username']
        cursor.execute(f"SELECT * FROM user WHERE username = {username}")
        account = cursor.fetchone()
        if account and pbkdf2_sha256.verify(data['password'], account['password']):
            if account['admin']:
                session['admin'] = True
            else:
                session['admin'] = False
            session['logged'] = True
            session['id'] = account['user_id']
            session['username'] = account['username']
            session['cart'] = []
            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('logged'):
        return redirect('/home')
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    msg = ''
    reg_data = request.form
    data = {'username': reg_data.get('username'),
            'password': reg_data.get('password'),
            'email': reg_data.get('email')}
    print(reg_data)
    if data['username'] and data['password'] and data['email']:
        username = data['username']
        password = pbkdf2_sha256.hash(data['password'])
        email = data['email']
        cursor.execute(f'SELECT * FROM user WHERE username = {username}')
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
    if not session.get('logged'):
        return redirect("/login")
    return render_template('about.html')


@app.route('/admin')
def admin():
    if not session.get('logged'):
        return redirect("/login")
    if not session.get('admin'):
        return redirect('/home')
    db = sqlite3.connect("tour_service.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    data = cursor.execute('SELECT * FROM service')
    return render_template('admin.html', data=data)


@app.route('/admin/redact/<int:service_id>', methods=["GET", "POST"])
def redact_service(service_id):
    if not session.get('logged'):
        return redirect("/login")
    if not session.get('admin'):
        return redirect('/home')
    db = sqlite3.connect('tour_service.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM service WHERE service_id == {service_id}")
    data = cursor.fetchone()
    db.close()
    if request.method == "POST":
        db = sqlite3.connect('tour_service.db')
        cursor = db.cursor()
        reg_data = request.form
        data = {'price': reg_data.get('price'),
                'availability': reg_data.get('availability'),
                'name': reg_data.get('name'),
                'type': reg_data.get('type'),
                'date': reg_data.get('date'),
                'duration': reg_data.get('duration'),
                'route': reg_data.get('route'),
                'image': reg_data.get('image')}
        executable_string = f"""UPDATE service SET price = {int(data['price'])}, availability = {int(data['availability'])}, name="{data['name']}", type = "{data['type']}", date = "{data['date']}", duration = {data['duration']}, route = "{data['route']}", image = "{data['image']}" WHERE service_id={service_id};"""
        cursor.execute(executable_string)
        db.commit()
        return redirect('/admin')
    return render_template("redact.html", data=data)


@app.route('/admin/del/<int:service_id>')
def delete(service_id):
    if not session.get('logged'):
        return redirect("/login")
    if not session.get('admin'):
        return redirect('/home')
    db = sqlite3.connect('tour_service.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM service WHERE service_id = {service_id}")
    db.commit()
    return redirect(url_for('admin'))


@app.route('/admin/add', methods=["GET", "POST"])
def add_service():
    if not session.get('logged'):
        return redirect("/login")
    if not session.get('admin'):
        return redirect('/home')
    if request.method == "POST":
        reg_data = request.form
        print(reg_data)
        data = {'price': reg_data.get('price'),
                'availability': reg_data.get('availability'),
                'name': reg_data.get('name'),
                'type': reg_data.get('type'),
                'date': reg_data.get('date'),
                'duration': reg_data.get('duration'),
                'route': reg_data.get('route'),
                'image': reg_data.get('image')}
        db = sqlite3.connect('tour_service.db')
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO service VALUES (NULL, "{data['price']}", "{data['availability']}",
        "{data['name']}", "{data['type']}", "{data['date']}", "{data['duration']}", "{data['route']}", "{data['image']}"
        )""")
        db.commit()
        return redirect('/admin')
    return render_template('add.html')
