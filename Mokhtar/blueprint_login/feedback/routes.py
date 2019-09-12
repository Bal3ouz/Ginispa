
from flask import render_template, url_for, redirect, flash, request,Blueprint,jsonify,send_file
from blueprint_login.feedback.feedback import FeedbackForm
from flask_login import login_user, current_user, logout_user, login_required
from blueprint_login import mail
from flask_mail import Message
feedback = Blueprint('feedback', __name__)

@feedback.route("/contact_us", methods=['GET', 'POST'])
@login_required
def contact_us():
	form = FeedbackForm()
	if form.validate_on_submit():
		test=True
	return render_template('contact_us.html',user=current_user,name="contact_us",form=form)