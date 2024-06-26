from flask import render_template, request, Flask, flash, redirect, url_for, session
from app import app
from models import db, User, Category, Product, Cart, Transaction, Order
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    # Check if user_id is in session
    if 'user_id' in session:
        return render_template('index.html')
    else:
        flash('Please login to continue')
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')    
    if not username or not password:
        flash('Please fill out all fields')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Username does not exist')
        return redirect(url_for('login'))
    
    if not check_password_hash(user.passhash, password):
        flash('Incorrect password')
        return redirect(url_for('login'))
    
    session['user_id'] = user.userid
    return redirect(url_for('profile'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if not username or not password or not confirm_password:
        flash('Please fill out all the fields')
        return redirect(url_for('register'))
    
    if password != confirm_password:
        flash('Passwords don\'t match')
        return redirect(url_for('register'))
    
    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists')
        return redirect(url_for('register'))
    
    pass_hash = generate_password_hash(password)
    new_user = User(username=username, passhash=pass_hash, name=name)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login to continue')
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
