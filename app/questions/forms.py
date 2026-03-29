from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class AskForm(FlaskForm):
    title = StringField(
        'Question Title',
        validators=[DataRequired(), Length(min=10, max=300)]
    )
    body = TextAreaField(
        'Details (optional)',
        validators=[Length(max=5000)]
    )
    category_id = SelectField(
        'Category', coerce=int, validators=[DataRequired()]
    )
    submit = SubmitField('Post Question')


class AnswerForm(FlaskForm):
    body = TextAreaField(
        'Your Answer',
        validators=[DataRequired(), Length(min=10, max=5000)]
    )
    submit = SubmitField('Post Answer')
