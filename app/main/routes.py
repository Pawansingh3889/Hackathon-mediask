from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.models import Question, Answer, Category, User, Vote, HazardReport, Notification
from sqlalchemy import func
import random
import requests as http_requests

# Daily question prompts to encourage participation
DAILY_PROMPTS = [
    "What is one thing you wish you had known earlier about managing stress?",
    "Have you ever experienced a health scare that turned out to be nothing?",
    "What is the best health advice you have ever received?",
    "How do you maintain your mental health during difficult times?",
    "What is a common health myth you used to believe?",
    "Have you ever delayed seeing a doctor? What happened?",
    "What small lifestyle change made the biggest difference to your health?",
    "How has your relationship with exercise changed over the years?",
    "What do you wish more people understood about living with a chronic condition?",
    "How do you deal with health anxiety?",
    "What is your experience with the NHS? Good, bad, or mixed?",
    "Have you ever helped someone through a health crisis? What did you learn?",
    "What do you do when you cannot sleep?",
    "How do you manage work-life balance without burning out?",
    "What health topic do you think is not talked about enough?",
]


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'recent', type=str)
    categories = Category.query.order_by(Category.name).all()

    # Sort options
    if sort == 'trending':
        questions = Question.query.order_by(
            Question.view_count.desc()
        ).paginate(page=page, per_page=20, error_out=False)
    elif sort == 'unanswered':
        # Questions with only AI answer or no answers
        questions = Question.query.filter(
            ~Question.answers.any(Answer.auth_level == 'human_experience')
        ).order_by(
            Question.created_at.desc()
        ).paginate(page=page, per_page=20, error_out=False)
    else:  # recent
        questions = Question.query.order_by(
            Question.created_at.desc()
        ).paginate(page=page, per_page=20, error_out=False)

    # Stats for hero
    stats = {
        'total_questions': Question.query.count(),
        'total_answers': Answer.query.count(),
        'total_users': User.query.count(),
        'unanswered_count': Question.query.filter(
            ~Question.answers.any(Answer.auth_level == 'human_experience')
        ).count(),
    }

    # Daily prompt
    daily_prompt = random.choice(DAILY_PROMPTS)

    return render_template(
        'index.html',
        questions=questions,
        categories=categories,
        stats=stats,
        sort=sort,
        daily_prompt=daily_prompt
    )


@bp.route('/search')
def search():
    q = request.args.get('q', '', type=str).strip()
    page = request.args.get('page', 1, type=int)
    if q:
        questions = Question.query.filter(
            Question.title.ilike(f'%{q}%')
            | Question.body.ilike(f'%{q}%')
        ).order_by(
            Question.created_at.desc()
        ).paginate(page=page, per_page=20, error_out=False)
    else:
        questions = Question.query.filter(False).paginate(
            page=page, per_page=20, error_out=False
        )
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        'search.html',
        questions=questions,
        categories=categories,
        query=q
    )


@bp.route('/mental-health')
def mental_health():
    mh_slugs = ['mental-health', 'emotions']
    mh_categories = Category.query.filter(Category.slug.in_(mh_slugs)).all()
    mh_cat_ids = [c.id for c in mh_categories]
    page = request.args.get('page', 1, type=int)
    questions = Question.query.filter(
        Question.category_id.in_(mh_cat_ids)
    ).order_by(
        Question.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    categories = Category.query.order_by(Category.name).all()

    stats = {
        'total_questions': Question.query.filter(
            Question.category_id.in_(mh_cat_ids)
        ).count(),
        'total_users': User.query.count(),
    }
    return render_template(
        'mental_health.html',
        questions=questions,
        categories=categories,
        mh_categories=mh_categories,
        stats=stats
    )


@bp.route('/workers-health')
def workers_health():
    wh_slugs = ['workers-health', 'mental-health', 'general']
    wh_categories = Category.query.filter(Category.slug.in_(wh_slugs)).all()
    wh_cat = Category.query.filter_by(slug='workers-health').first()

    page = request.args.get('page', 1, type=int)
    if wh_cat:
        questions = Question.query.filter_by(
            category_id=wh_cat.id
        ).order_by(
            Question.created_at.desc()
        ).paginate(page=page, per_page=20, error_out=False)
    else:
        questions = Question.query.filter(False).paginate(
            page=page, per_page=20, error_out=False
        )
    categories = Category.query.order_by(Category.name).all()

    stats = {
        'total_questions': Question.query.filter_by(
            category_id=wh_cat.id
        ).count() if wh_cat else 0,
        'total_users': User.query.count(),
    }
    return render_template(
        'workers_health.html',
        questions=questions,
        categories=categories,
        stats=stats
    )


@bp.route('/category/<slug>')
def category(slug):
    cat = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    questions = Question.query.filter_by(
        category_id=cat.id
    ).order_by(
        Question.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        'questions/category.html',
        questions=questions,
        categories=categories,
        current_category=cat
    )
@bp.route('/submit-hazard', methods=['POST'])
def submit_hazard():
    name = request.form.get('name')
    department = request.form.get('department')
    description = request.form.get('description')

    # Save to database
    hazard = HazardReport(name=name, department=department, description=description)
    db.session.add(hazard)
    db.session.commit()

    # This prints to your local terminal so you can verify it works
    print(f"\n--- NEW HAZARD REPORT ---")
    print(f"From: {name} ({department})")
    print(f"Issue: {description}")
    print(f"-------------------------\n")

    # Flash a success message to the user
    flash("Your report has been submitted to management successfully.", "success")

    # Redirect them back to the workers health page
    return redirect(url_for('main.workers_health'))


# ===== ADMIN DASHBOARD =====
@bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.index'))

    page_q = request.args.get('page_q', 1, type=int)
    page_u = request.args.get('page_u', 1, type=int)

    stats = {
        'total_questions': Question.query.count(),
        'total_answers': Answer.query.count(),
        'total_users': User.query.filter_by(is_system_account=False).count(),
        'total_categories': Category.query.count(),
        'ai_answers': Answer.query.filter_by(auth_level='ai_assistant').count(),
        'total_hazards': HazardReport.query.count(),
        'open_hazards': HazardReport.query.filter(HazardReport.status != 'resolved').count(),
    }

    questions = Question.query.order_by(
        Question.created_at.desc()
    ).paginate(page=page_q, per_page=15, error_out=False)

    users = User.query.filter_by(
        is_system_account=False
    ).order_by(User.created_at.desc()).paginate(page=page_u, per_page=15, error_out=False)

    hazards = HazardReport.query.order_by(
        HazardReport.created_at.desc()
    ).all()

    categories = Category.query.order_by(Category.name).all()

    active_tab = request.args.get('tab', 'questions')

    return render_template(
        'admin.html',
        stats=stats,
        questions=questions,
        users=users,
        hazards=hazards,
        categories=categories,
        active_tab=active_tab
    )


@bp.route('/admin/user/<int:id>/toggle-admin', methods=['POST'])
@login_required
def toggle_admin(id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    user.is_admin = not user.is_admin
    db.session.commit()
    status = 'promoted to admin' if user.is_admin else 'removed from admin'
    flash(f'{user.full_name} has been {status}.', 'success')
    return redirect(request.referrer or url_for('main.admin_dashboard'))


@bp.route('/admin/user/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot delete yourself.', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    if user.is_system_account:
        flash('Cannot delete system accounts.', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    # Delete user's votes, answers, questions
    for answer in user.answers:
        Vote.query.filter_by(answer_id=answer.id).delete()
    Answer.query.filter_by(author_id=user.id).delete()
    for question in user.questions:
        for ans in question.answers:
            Vote.query.filter_by(answer_id=ans.id).delete()
            db.session.delete(ans)
        db.session.delete(question)
    Vote.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.full_name} has been deleted.', 'success')
    return redirect(url_for('main.admin_dashboard'))


# ===== NOTIFICATION API (for browser push notifications) =====
@bp.route('/api/notifications/check')
@login_required
def check_notifications():
    unread = Notification.query.filter_by(
        user_id=current_user.id, read=False
    ).count()
    latest = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).first()
    return jsonify({
        'unread': unread,
        'latest': {
            'id': latest.id,
            'message': latest.message,
            'link': latest.link,
            'type': latest.type
        } if latest else None
    })


# ===== HAZARD REPORT MANAGEMENT =====
@bp.route('/admin/hazard/<int:id>/update', methods=['POST'])
@login_required
def update_hazard(id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    hazard = HazardReport.query.get_or_404(id)
    new_status = request.form.get('status', hazard.status)
    notes = request.form.get('resolved_notes', '')
    hazard.status = new_status
    if new_status == 'resolved':
        hazard.resolved_by = current_user.full_name
        hazard.resolved_notes = notes
        from datetime import datetime, timezone
        hazard.resolved_at = datetime.now(timezone.utc)
    elif new_status == 'acknowledged':
        hazard.resolved_notes = notes
    db.session.commit()
    flash(f'Hazard report #{hazard.id} updated to {new_status}.', 'success')
    return redirect(url_for('main.admin_dashboard') + '?tab=hazards')


# ===== NHS API INTEGRATION =====
NHS_API_BASE = 'https://api.nhs.uk/conditions'
NHS_API_HEADERS = {'subscription-key': 'placeholder', 'Content-Type': 'application/json'}


@bp.route('/nhs-lookup')
def nhs_lookup():
    query = request.args.get('q', '').strip()
    results = []
    error = None
    if query:
        try:
            resp = http_requests.get(
                NHS_API_BASE,
                params={'category': query},
                headers=NHS_API_HEADERS,
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get('significantLink', data.get('relatedLink', []))[:10]:
                    results.append({
                        'name': item.get('name', ''),
                        'description': item.get('description', ''),
                        'url': item.get('url', ''),
                    })
            else:
                # Fallback: use local search
                error = 'NHS API unavailable, showing local results'
                local = Question.query.filter(
                    Question.title.ilike(f'%{query}%')
                ).limit(10).all()
                for q in local:
                    results.append({
                        'name': q.title,
                        'description': q.body[:200],
                        'url': url_for('questions.detail', id=q.id),
                    })
        except Exception:
            error = 'NHS API unavailable, showing local results'
            local = Question.query.filter(
                Question.title.ilike(f'%{query}%')
            ).limit(10).all()
            for q in local:
                results.append({
                    'name': q.title,
                    'description': q.body[:200],
                    'url': url_for('questions.detail', id=q.id),
                })
    categories = Category.query.order_by(Category.name).all()
    return render_template('nhs_lookup.html', query=query, results=results, error=error, categories=categories)
