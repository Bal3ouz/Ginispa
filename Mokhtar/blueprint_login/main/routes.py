from flask import render_template, url_for, redirect, flash, request,Blueprint,jsonify,send_file
from blueprint_login import  db,bcrypt
from datetime import datetime
from blueprint_login.models import User
from blueprint_login.users.log import  LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from blueprint_login.ml.utils import create_table,change_table,create_instance,save_table
import pandas as pd

main = Blueprint('main', __name__)
@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
	return render_template('home.html',user=current_user,name="home")


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

@main.route("/delete_element/<name>", methods=['GET', 'POST'])
@login_required
def delete_element(name):
	if (name=="infos"):
		table_name="current_data"
	if (name=="infos_deleted"):
		table_name="deleted_data"
	if (name=="infos_saved"):
		table_name="saved_data"
	
	data=create_table(table_name).head(50)
	data.index=range(0,data.shape[0])
	ind = request.args.get('ind', default = 1, type = int)
	save_table("deleted_data",data.loc[ind:ind])
	data=data.drop([ind],axis=0)
	data.index=range(0,data.shape[0])
	change_table(data,table_name)
	return redirect(url_for("main."+name))
	#jsonify (result=data)

@main.route("/save_element/<name>", methods=['GET', 'POST'])
@login_required
def save_element(name):
	
	if (name=="infos"):
		table_name="current_data"
	if (name=="infos_deleted"):
		table_name="deleted_data"
	if (name=="infos_saved"):
		table_name="saved_data"
		
	data=create_table(table_name).head(50)
	data.index=range(0,data.shape[0])
	ind = request.args.get('ind', default = 1, type = int)
	save_table("saved_data",data.loc[ind:ind])
	data=data.drop([ind],axis=0)
	data.index=range(0,data.shape[0])
	change_table(data,table_name)
	return redirect(url_for("main."+name))
	#jsonify (result=data)

@main.route("/return_element/<name>", methods=['GET', 'POST'])
@login_required
def return_element(name):
	if (name=="infos"):
		table_name="current_data"
	if (name=="infos_deleted"):
		table_name="deleted_data"
	if (name=="infos_saved"):
		table_name="saved_data"
	data=create_table(table_name).head(50)
	data.index=range(0,data.shape[0])
	ind = request.args.get('ind', default = 1, type = int)
	save_table("current_data",data.loc[ind:ind])
	data=data.drop([ind],axis=0)
	data.index=range(0,data.shape[0])
	change_table(data,table_name)
	return redirect(url_for("main."+name))
@main.route("/save_progress", methods=['GET', 'POST'])
@login_required
def save_progress():
	
	return send_file('./saved_data.csv',
                     mimetype='text/csv',
                     attachment_filename='saved_data_download.csv',
                     as_attachment=True)
	#jsonify (result=data)







@main.route("/infos", methods=['GET', 'POST'])
@login_required
def infos():
	data=create_table("current_data").head(50)
	data.index=range(0,data.shape[0])
	return render_template('infos.html',user=current_user,name="infos",data=data)


@main.route("/infos/deleted", methods=['GET', 'POST'])
@login_required
def infos_deleted():
	data=create_table("deleted_data").head(50)
	data.index=range(0,data.shape[0])
	return render_template('infos_deleted.html',user=current_user,name="infos_deleted",data=data)


@main.route("/infos/saved", methods=['GET', 'POST'])
@login_required
def infos_saved():
	data=create_table("saved_data").head(50)
	data.index=range(0,data.shape[0])
	return render_template('infos_saved.html',user=current_user,name="infos_saved",data=data)

@main.route("/infos/reset", methods=['GET', 'POST'])
@login_required
def infos_reset():
	create_instance();
	return redirect(url_for("main.infos"));



