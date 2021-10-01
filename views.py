import os

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = os.environ.get('SECRET_KEY', 'dev')

class GameForm(FlaskForm):
    field = StringField('Describe the initial field: ', validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/', methods=['POST', 'GET'])
def index():
    form = GameForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template("index.html", form=form)