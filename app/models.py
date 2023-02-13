from  flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    carts = db.relationship("Cart", backref='user', lazy=True)

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()



class Product(db.Model):
    __tablename__= 'product'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50), nullable=False, unique=True)
    img_url = db.Column(db.String(1000), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False, unique=True)
    carts = db.relationship("Cart", backref='product', lazy=True)

    def __init__(self, item, img_url, price):
        self.item = item
        self.img_url = img_url
        self.price = price

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

  

class Cart(db.Model):
    __tablename__='cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # product_id = db.Column(db.Integer,db.Foreignkey('product_key'), nullable = False)
    item_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __init__(self, user_id, item_id):
        self.user_id = user_id
        self.item_id = item_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit


    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

