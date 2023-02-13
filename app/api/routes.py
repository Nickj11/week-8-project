from flask import render_template, request, redirect, url_for, flash, Blueprint
from forms import Usercreationform,Loginform
from models import User, Cart, Product
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, basic
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

api = Blueprint('api', __name__)


@api.route('/api/products', methods=["GET", "POST"])
def shopPageAPI():

    products = Product.query.all()

    new_products = []
    for i in products:
        new_products.append(i.to_dict())
    
    return {
        'status': 'ok',
        'totalResults': len(products),
        'items': [i.to_dict() for i in products]
    }

@api.route('/api/products/<int:item_id>', methods=["GET"])
def singleItem(item_id):

    item = Product.query.get(item_id)

    return item.to_dict()







@basic_auth.verify_password
def verifyPassword(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            return user

@token_auth.verify_token
def verifyToken(token):
    user = User.query.filter_by(apitoken=token).first()
    if user:
        return user




@api.route('/api/signup', methods=["POST"])
def signUpAPI():
    data = request.json
    first = data['first']
    last = data['last']
    username = data['username']
    email = data['email']
    password = data['password']

    user = User(last,first,username, email, password,)

    user.saveToDB()

    return {
        'status': 'ok',
        'message': ' successfully created '
    }


@api.route('/api/login', methods=["POST"])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
        'status': 'ok',
        'user': user.to_dict()
    }


@api.route('/api/addcart/<int:item_id>', methods=["GET", "POST"])
@login_required
def addCart(item_id):
    
    recipt = Cart(item_id, current_user.id)
    recipt.saveToDB()

    return {
        'status': 'ok',
        'message': 'Product successfully added to cart.'
    } 

@api.route('/api/mycart', methods=["GET", "POST"])
@login_required
def myCart():

    mycart = Cart.query.filter_by( user_id = current_user.id).all()

    total = 0
    for p in mycart:
        total += float(p.info.price)

    return {
        'status': 'ok',
        'my_cart': mycart,
        'total': total
    }



@api.route('/api/cart/deleteall', methods=["GET", "POST"])
@login_required
def deleteAll():

    cart = Cart.query.all()
    for product in cart:
        product.deleteFromDB()

    return {
        'status': 'ok',
        'message': 'Successfully deleted all products from cart'
    }



@api.route('/api/cart/<int:item_id>/delete', methods=["GET", "POST"])
@login_required
def delete(item_id):
    item = Cart.query.get(item_id)

    item.deleteFromDB()

    return {
        'status': 'ok',
        'message': 'products successfully deleted from cart'
    }

