from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app import db
from app.stories import bp
from app.models import Story, Category, Notification


class StoryForm(FlaskForm):
    title = StringField(
        'Story Title', validators=[DataRequired(), Length(min=10, max=300)]
    )
    body = TextAreaField(
        'Your Story',
        validators=[DataRequired(), Length(min=100, max=10000)]
    )
    category_id = SelectField('Health Topic', coerce=int)
    submit = SubmitField('Publish Story')


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    stories = Story.query.order_by(
        Story.created_at.desc()
    ).paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        'stories/index.html',
        stories=stories,
        categories=categories
    )


@bp.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = StoryForm()
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]
    if form.validate_on_submit():
        story = Story(
            title=form.title.data.strip(),
            body=form.body.data.strip(),
            author_id=current_user.id,
            category_id=form.category_id.data
        )
        db.session.add(story)
        current_user.add_points('post_story')
        db.session.commit()
        flash('Your story has been published!', 'success')
        return redirect(url_for('stories.read', id=story.id))

    categories = Category.query.order_by(Category.name).all()
    return render_template('stories/write.html', form=form, categories=categories)


@bp.route('/<int:id>')
def read(id):
    story = Story.query.get_or_404(id)
    story.view_count += 1
    db.session.commit()
    categories = Category.query.order_by(Category.name).all()
    return render_template('stories/read.html', story=story, categories=categories)
