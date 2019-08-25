from flask import render_template, url_for, redirect, flash, request,Blueprint
from blueprint_login import  db,bcrypt
from datetime import datetime
from blueprint_login.models import User
from blueprint_login.users.log import  LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from blueprint_login.ml.utils import  create_table
import pandas as pd
main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html',user=current_user,name="home")

@main.route("/infos", methods=['GET', 'POST'])
@login_required
def infos():
    return render_template('infos.html',user=current_user,name="infos",data=create_table())

@main.route("/heatmap", methods=['GET', 'POST'])
@login_required
def heatmap():
    return render_template('heatmap.html',user=current_user,name="heatmap")

@main.route("/news", methods=['GET', 'POST'])
@login_required
def news():
    return render_template('news.html',user=current_user,name="news")

@main.route("/contact_us", methods=['GET', 'POST'])
@login_required
def contact_us():
    return render_template('contact_us.html',user=current_user,name="contact_us")

@main.route("/yt", methods=['GET', 'POST'])
def yt():
    return render_template('youtube_sidebar.html',user=current_user,name="contact_us")



