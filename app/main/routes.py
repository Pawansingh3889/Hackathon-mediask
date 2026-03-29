from flask import render_template, request, redirect, url_for, flash
from app.main import bp
from app import db
from app.models import Question, Answer, Category, User, HazardReport
from sqlalchemy import func
import random

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
