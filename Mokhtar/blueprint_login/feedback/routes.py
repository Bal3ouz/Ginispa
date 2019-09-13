
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
		choices={ '1': 'Feedback', '2': 'Report a bug','3': 'Other'}
		if form.mail_me.data :
			msg=Message(choices[form.feedback.data],sender="Genispai@gmail.com",
				recipients=["Genispai@gmail.com",current_user.email])
		else :
			msg=Message(choices[form.feedback.data],sender="Genispai@gmail.com",
				recipients=["Genispai@gmail.com"])
		msg.body=form.message.data
		
		mail.send(msg)
		
		return redirect(url_for('main.home'))
		
	return render_template('contact_us.html',user=current_user,name="contact_us",form=form)