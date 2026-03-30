from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.questions import bp
from app.questions.forms import AskForm, AnswerForm
from app.models import Question, Answer, Vote, Category, Notification
from app.ai_responder import auto_respond


@bp.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = AskForm()
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():
        question = Question(
            title=form.title.data.strip(),
            body=form.body.data.strip() or form.title.data.strip(),
            author_id=current_user.id,
            category_id=form.category_id.data
        )
        db.session.add(question)
        current_user.add_points('ask_question')
        db.session.commit()

        # AI auto-responds instantly
        auto_respond(question)

        flash(
            'Your question has been posted! '
            'Our AI has provided an initial response — '
            'community members will add their experiences soon.',
            'success'
        )
        return redirect(url_for('questions.detail', id=question.id))

    categories = Category.query.order_by(Category.name).all()
    return render_template(
        'questions/ask.html', form=form, categories=categories
    )


@bp.route('/<int:id>', methods=['GET', 'POST'])
def detail(id):
    question = Question.query.get_or_404(id)
    question.view_count += 1
    db.session.commit()

    form = AnswerForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please sign in to answer.', 'info')
            return redirect(url_for('auth.login'))
        answer = Answer(
            body=form.body.data.strip(),
            question_id=question.id,
            author_id=current_user.id,
            auth_level='human_experience'
        )
        db.session.add(answer)
        current_user.add_points('post_answer')

        # Notify question author
        if question.author_id != current_user.id:
            notif = Notification(
                user_id=question.author_id,
                type='answer',
                message=f'{current_user.full_name} answered your question: "{question.title[:60]}"',
                link=url_for('questions.detail', id=question.id)
            )
            db.session.add(notif)

        db.session.commit()
        flash('Your answer has been posted! +10 reputation points.', 'success')
        return redirect(url_for('questions.detail', id=question.id))

    answers = Answer.query.filter_by(question_id=question.id).all()
    # Sort by vote score descending
    answers.sort(key=lambda a: a.score, reverse=True)
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        'questions/detail.html',
        question=question,
        answers=answers,
        form=form,
        categories=categories
    )


@bp.route('/vote', methods=['POST'])
@login_required
def vote():
    data = request.get_json()
    answer_id = data.get('answer_id')
    value = data.get('value')  # +1 or -1

    if value not in (1, -1):
        return jsonify({'error': 'Invalid vote'}), 400

    answer = Answer.query.get_or_404(answer_id)

    existing_vote = Vote.query.filter_by(
        user_id=current_user.id, answer_id=answer_id
    ).first()

    if existing_vote:
        if existing_vote.value == value:
            # Same vote again = remove vote
            db.session.delete(existing_vote)
        else:
            # Change vote direction
            existing_vote.value = value
    else:
        new_vote = Vote(
            user_id=current_user.id,
            answer_id=answer_id,
            value=value
        )
        db.session.add(new_vote)

    db.session.commit()
    return jsonify({'score': answer.score})
