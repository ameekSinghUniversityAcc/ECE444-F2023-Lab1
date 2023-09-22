from flask import Flask, render_template, session, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
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

        session['name'] = form.name.data
        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), time_stamp=datetime.utcnow())
 
@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name, time_stamp=datetime.utcnow())