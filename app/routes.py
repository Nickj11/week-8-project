from app import app
from flask import render_template, flash, url_for, redirect
from .models import Product, Cart,User
from .forms import LoginForm, UserCreationForm
# api = Blueprint('api', __name__)
from flask import Blueprint, request
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@login_required
def homepage():
    posts = Product.query.all()
    print(posts)
    return render_template('products.html', posts = posts)
    
@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username= form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user:

                if user.password == password:
                    login_user(user)
                    flash("Successfully logged in", category="success")
                    
                else:
                    flash("Wrong password", category="danger")
            else:
                flash("This user does not exist.", category="danger")

        return redirect(url_for('shopPage'))
        
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Successfully logged out!", category="success")
    return redirect(url_for('loginPage'))



@app.route('/addcart/<int:item_id>', methods=["GET", "POST"])
@login_required
def addToCart(item_id):
    
    recipt = Cart(item_id, current_user.id)
    recipt.saveToDB()
    flash('Item successfully added to your cart!', category='success')

    return redirect(url_for('homepage'))
    


@app.route('/mycart', methods=["GET", "POST"])
@login_required
def my_cart():

    carts = Cart.query.filter_by(user_id = current_user.id).all()

    total = 0
    for item in carts:
        total += float(item.info.price)

    print(total)

    return render_template('cart.html', carts=carts, total=total)

# @app.route('/cart', methods = ['GET', 'POST'])
# @login_required
# def cart():
    
#     # usercart= current_user.cart
#     message = 'This item has been added to your cart!'
    
    
    

#     return render_template('cart.html', message = message)


@app.route('/cart/<int:item_id>/delete', methods=["GET", "POST"])
@login_required
def deletecart(item_id):
    item = Cart.query.get(item_id)

    item.deleteFromDB()

    return redirect(url_for('my_cart'))

@app.route('/cart/deleteall', methods=["GET", "POST"])
@login_required
def removeall():

    cart2 = Cart.query.all()
    for item in cart2:
        item.deleteFromDB()

    return redirect(url_for('homepage'))