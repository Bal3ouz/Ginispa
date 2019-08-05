from flask import render_template, url_for, redirect, flash, request
from login import app, bcrypt
from datetime import datetime
from login.models import User
from login.log import  LoginForm
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/home")
def home():
    #home will be the client interface
    return "<h1>Hello user </h1>"


@app.route("/login", methods=['GET', 'POST'])
def login():
    refresh=True 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #next_page = request.args.get('next')
            #return redirect(next_page) if next_page else redirect(url_for('home'))
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            refresh=False
    return render_template('index.html', title='Login', form=form,refresh=refresh)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))