from app import app
from flask import render_template, flash, url_for, redirect
from .models import Product, Cart
from flask_login import current_user, login_required
# api = Blueprint('api', __name__)
# from flask import Blueprint


@app.route('/')
@login_required
def homepage():
    posts = Product.query.all()
    print(posts)
    return render_template('home.html', posts = posts)
    

@app.route('/<int:item_id>', methods = ['GET', 'POST'])
@login_required
def addToCart(item_id):
    addedItem = Product.query.filter_by(id = item_id).first()
    print(addedItem)
    
    


    return redirect(url_for('cart'))

@app.route('/cart', methods = ['GET', 'POST'])
@login_required
def cart():
    
    # usercart= current_user.cart
    message = 'This item has been added to your cart!'
    
    
    

    return render_template('cart.html', message = message)

@app.route('/cart/<int:item_id>', methods=['GET', 'POST'])
@login_required
def removeFromCart(item_id):
    print(item_id)
    deletedcart = Cart.query.filter_by(item=item_id).first()
    # deletedcart = current_user.cart
    print(deletedcart)
    if deletedcart:
        current_user.deleteFromCart(deletedcart)

    return redirect(url_for('cart'))
    # return render_template('cart.html')