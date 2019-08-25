from flask import render_template, url_for, redirect, flash, request,Blueprint
from blueprint_login import db, bcrypt
from datetime import datetime
from blueprint_login.models import User
from blueprint_login.users.log import  LoginForm
from blueprint_login.users.reg import  RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
    refresh=True 
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #next_page = request.args.get('next')
            #return redirect(next_page) if next_page else redirect(url_for('home'))
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            refresh=False
    return render_template('login.html', title='Login', form=form,refresh=refresh,name="login")

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logout_user()
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)
