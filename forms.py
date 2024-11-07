from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class FlashcardForm(FlaskForm):
    term = StringField('Term', validators=[DataRequired()])
    definition = TextAreaField('Definition', validators=[DataRequired()])
    submit = SubmitField('Add Flashcard')

class QuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired()])
    submit = SubmitField('Create Quiz')
