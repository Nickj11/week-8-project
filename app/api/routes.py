from flask import render_template, request, redirect, url_for, flash, Blueprint
from ..models import User, Cart, Product
from ..forms import LoginForm, UserCreationForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from .apihelperauth.authh import basic_auth, token_auth



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
    if item:
        return{
            'status': 'ok',
            'total_result': 1,
            'item':
            item.to_dict()
        }

    else:
        return{
        'status': 'not'
    }







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
        'user': user.to_dict(),
    }

@api.route('/api/addcart/<int:item_id>', methods=["POST"])
@token_auth.login_required
def addCart():
        data = request.json
        
        Get_item = data['item_id']
        item = Product.query.get(Get_item)
        user = token_auth.current_user()
        
        recipt = Cart(Get_item, user.id)
        recipt.saveToDB()

        return {
            'status': 'ok',
            'message': f'Item successfully added {item.name} to cart.',
            
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
        product.deletefromDB()

    return {
        'status': 'ok',
        'message': 'Successfully deleted all products from cart'
    }



@api.route('/api/cart/delete', methods=["POST"])
@token_auth.login_required()
def Delete():

    user = token_auth.current_user()
    data = request.json
    print(data['itemId'])
    item = Cart.query.filter_by( user_id = user.id).filter_by(item_id = data['itemId']).first()
    print(item)

    item.deleteFromDB()
   

    return {
        'status': 'ok',
        'message': 'Item successfully deleted from cart'
    }