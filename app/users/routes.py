from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.users import bp
from app.models import User, Question, Answer, Notification, LEVELS


@bp.route('/<int:id>')
def profile(id):
    user = User.query.get_or_404(id)
    questions = Question.query.filter_by(author_id=user.id).order_by(
        Question.created_at.desc()
    ).limit(20).all()
    answers = Answer.query.filter_by(author_id=user.id).order_by(
        Answer.created_at.desc()
    ).limit(20).all()
    categories = []
    return render_template(
        'users/profile.html',
        user=user,
        questions=questions,
        answers=answers,
        categories=categories,
        levels=LEVELS
    )


@bp.route('/notifications')
@login_required
def notifications():
    notifs = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).limit(50).all()

    # Mark all as read
    for n in notifs:
        if not n.read:
            n.read = True
    db.session.commit()

    return render_template('users/notifications.html', notifications=notifs, categories=[])
