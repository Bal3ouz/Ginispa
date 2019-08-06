from flask import render_template, url_for, redirect, flash, request
from login import app, bcrypt
from datetime import datetime
from login.models import User
from login.log import  LoginForm
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html',user=current_user,name="home")

@app.route("/infos", methods=['GET', 'POST'])
@login_required
def infos():
    return render_template('infos.html',user=current_user,name="infos")

@app.route("/heatmap", methods=['GET', 'POST'])
@login_required
def heatmap():
    return render_template('heatmap.html',user=current_user,name="heatmap")

@app.route("/news", methods=['GET', 'POST'])
@login_required
def news():
    return render_template('news.html',user=current_user,name="news")

@app.route("/contact_us", methods=['GET', 'POST'])
@login_required
def contact_us():
    return render_template('contact_us.html',user=current_user,name="contact_us")


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
    return render_template('index.html', title='Login', form=form,refresh=refresh,name="login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))