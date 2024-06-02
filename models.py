from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    
class Category(db.Model):
    categoryid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    
    products = db.relationship('Product', backref='category', lazy=True)
    
class Product(db.Model):
    productid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    categoryid = db.Column(db.Integer, db.ForeignKey('category.categoryid'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    manufacture = db.Column(db.Date, nullable=False)
    
    carts = db.relationship('Cart', backref='product', lazy=True)
    orders = db.relationship('Order', backref='product', lazy=True)
    
class Cart(db.Model):
    cartid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
class Transaction(db.Model):
    transactionid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='transaction', lazy=True)
    
class Order(db.Model):
    orderid = db.Column(db.Integer, primary_key=True)
    transactionid = db.Column(db.Integer, db.ForeignKey('transaction.transactionid'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        password_hash = generate_password_hash('admin')
        admin = User(username='admin', passhash=password_hash, name='Admin', is_admin=True)
        db.session.add(admin)
        db.session.commit()
