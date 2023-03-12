from flask import Blueprint, render_template, request, redirect, url_for
from ..models import User
from ..forms import UserCreationForm, LoginForm
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserCreationForm()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            print(first_name, last_name, username, email, password)

            # add user to database
            user = User(first_name, last_name, username, email, password)
     

            user.saveToDB()

            return redirect(url_for('auth.login'))


    return render_template('signup.html', form = form )

@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            # check is user with that username even exists
            user = User.query.filter_by(username=username).first()
            if user:
                #if user ecxists, check if passwords match
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('homepage'))
                else:
                    print('wrong password')

            else:
                print('user doesnt exist')
            return redirect(url_for('auth.login'))


    return render_template('login.html', form = form)

@auth.route('/logout', methods=["GET"])
@login_required
def logoutRoute():
    logout_user()
    return redirect(url_for('auth.login'))