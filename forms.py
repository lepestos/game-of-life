from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

from validators import GameFieldValidator


class GameForm(FlaskForm):
    state = TextAreaField('Describe the initial state: ',
                          validators=[DataRequired(), GameFieldValidator(sep='\r\n')])
    submit = SubmitField("Submit")