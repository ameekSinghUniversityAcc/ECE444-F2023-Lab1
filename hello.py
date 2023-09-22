from flask import Flask, render_template, session, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

def UofTEmailValidator(email):
    return True if "utoronto" in email else False

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("What is your UofT email address?", validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = '2Ap2ri001l'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route("/", methods = ['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        # Flash warning message if user changed name
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")

        # If valid UofT email entered, clear out fields and preserve the value
        if UofTEmailValidator(form.email.data):
            session['name'] = form.name.data
            session['email'] = form.email.data
            return redirect(url_for('index'))

        # Else, flash a warning
        else:
            flash("Please use a valid UofT email")
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), time_stamp=datetime.utcnow())
 
@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name, time_stamp=datetime.utcnow())