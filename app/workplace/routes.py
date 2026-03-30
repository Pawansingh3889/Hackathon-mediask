from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app import db
from app.workplace import bp
from app.models import WorkplacePost, WorkplaceComment


WORKPLACE_TOPICS = [
    ('stress', 'Stress'),
    ('burnout', 'Burnout'),
    ('anxiety', 'Anxiety'),
    ('workload', 'Workload'),
    ('bullying', 'Bullying'),
    ('loneliness', 'Loneliness'),
    ('work-life-balance', 'Work-Life Balance'),
    ('other', 'Other'),
]


class WorkplacePostForm(FlaskForm):
    title = StringField(
        'Title', validators=[DataRequired(), Length(min=5, max=300)]
    )
    body = TextAreaField(
        'Share your experience',
        validators=[DataRequired(), Length(min=20, max=5000)]
    )
    topic = SelectField('Topic', choices=WORKPLACE_TOPICS)
    submit = SubmitField('Post')


class WorkplaceCommentForm(FlaskForm):
    body = TextAreaField(
        'Your response',
        validators=[DataRequired(), Length(min=5, max=2000)]
    )
    submit = SubmitField('Reply')


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    topic = request.args.get('topic', '', type=str)

    query = WorkplacePost.query
    if topic:
        query = query.filter_by(topic=topic)
    posts = query.order_by(
        WorkplacePost.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)

    return render_template(
        'workplace/index.html',
        posts=posts,
        topics=WORKPLACE_TOPICS,
        current_topic=topic
    )


@bp.route('/post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = WorkplacePostForm()
    if form.validate_on_submit():
        post = WorkplacePost(
            title=form.title.data.strip(),
            body=form.body.data.strip(),
            author_id=current_user.id,
            topic=form.topic.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been shared.', 'success')
        return redirect(url_for('workplace.view_post', id=post.id))
    return render_template('workplace/post.html', form=form)


@bp.route('/<int:id>', methods=['GET', 'POST'])
def view_post(id):
    post = WorkplacePost.query.get_or_404(id)
    form = WorkplaceCommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please sign in to reply.', 'info')
            return redirect(url_for('auth.login'))
        comment = WorkplaceComment(
            body=form.body.data.strip(),
            post_id=post.id,
            author_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your reply has been posted.', 'success')
        return redirect(url_for('workplace.view_post', id=post.id))

    comments = post.comments.all()
    return render_template(
        'workplace/view.html', post=post, comments=comments, form=form
    )
