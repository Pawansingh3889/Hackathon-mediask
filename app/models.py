from datetime import datetime, timezone, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# ===== REPUTATION LEVELS =====
LEVELS = [
    (0, 'Newcomer', 'fa-seedling', '#94a3b8'),
    (50, 'Contributor', 'fa-leaf', '#22c55e'),
    (150, 'Helper', 'fa-hand-holding-heart', '#3b82f6'),
    (400, 'Expert', 'fa-star', '#f59e0b'),
    (1000, 'Guardian', 'fa-shield-check', '#8b5cf6'),
    (2500, 'Legend', 'fa-crown', '#ef4444'),
]

# Points for actions
POINTS = {
    'ask_question': 5,
    'post_answer': 10,
    'receive_upvote': 3,
    'receive_downvote': -1,
    'answer_accepted': 15,
    'post_story': 8,
    'daily_login': 2,
}


# ===== ASSOCIATION TABLES =====
user_interests = db.Table('user_interests',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=True)
    oauth_provider = db.Column(db.String(20), nullable=True)
    oauth_id = db.Column(db.String(100), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    is_system_account = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    onboarded = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Reputation
    reputation_points = db.Column(db.Integer, default=0)
    streak_days = db.Column(db.Integer, default=0)
    last_active_date = db.Column(db.Date, nullable=True)

    # Relationships
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author', lazy='dynamic')
    votes = db.relationship('Vote', backref='user', lazy='dynamic')
    stories = db.relationship('Story', backref='author', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    interests = db.relationship('Category', secondary=user_interests,
                                backref=db.backref('interested_users', lazy='dynamic'))

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def level(self):
        for min_pts, name, icon, color in reversed(LEVELS):
            if self.reputation_points >= min_pts:
                return {'name': name, 'icon': icon, 'color': color, 'min_pts': min_pts}
        return {'name': 'Newcomer', 'icon': 'fa-seedling', 'color': '#94a3b8', 'min_pts': 0}

    @property
    def next_level(self):
        for min_pts, name, icon, color in LEVELS:
            if self.reputation_points < min_pts:
                return {'name': name, 'min_pts': min_pts,
                        'progress': int(self.reputation_points / min_pts * 100)}
        return None

    @property
    def unread_count(self):
        return self.notifications.filter_by(read=False).count()

    def add_points(self, action):
        pts = POINTS.get(action, 0)
        self.reputation_points = max(0, self.reputation_points + pts)
        # Update streak
        today = datetime.now(timezone.utc).date()
        if self.last_active_date:
            if today - self.last_active_date == timedelta(days=1):
                self.streak_days += 1
            elif today != self.last_active_date:
                self.streak_days = 1
        else:
            self.streak_days = 1
        self.last_active_date = today

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True)

    questions = db.relationship('Question', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=False
    )
    source = db.Column(db.String(50), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    answers = db.relationship(
        'Answer', backref='question', lazy='dynamic',
        order_by='Answer.created_at'
    )

    @property
    def answer_count(self):
        return self.answers.count()

    @property
    def human_answer_count(self):
        return self.answers.filter_by(auth_level='human_experience').count()

    @property
    def is_official(self):
        return self.source is not None

    def get_related(self, limit=5):
        """Get related questions from same category."""
        words = self.title.lower().split()
        related = Question.query.filter(
            Question.id != self.id,
            Question.category_id == self.category_id
        ).order_by(Question.view_count.desc()).limit(limit).all()

        if len(related) < limit:
            extra = Question.query.filter(
                Question.id != self.id,
                Question.id.notin_([q.id for q in related])
            ).order_by(Question.view_count.desc()).limit(limit - len(related)).all()
            related.extend(extra)
        return related

    def __repr__(self):
        return f'<Question {self.title[:50]}>'


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey('questions.id'), nullable=False
    )
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_accepted = db.Column(db.Boolean, default=False)
    auth_level = db.Column(db.String(20), default='human_experience')
    source = db.Column(db.String(50), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    votes = db.relationship('Vote', backref='answer', lazy='dynamic')

    @property
    def score(self):
        return sum(v.value for v in self.votes)

    @property
    def auth_badge(self):
        badges = {
            'nhs_verified': ('NHS Verified', 'fa-shield-check', 'badge-nhs'),
            'ai_assistant': ('AI Assistant', 'fa-robot', 'badge-ai'),
            'human_experience': ('Human Experience', 'fa-user', 'badge-human'),
            'govuk': ('GOV.UK', 'fa-landmark', 'badge-govuk'),
        }
        return badges.get(self.auth_level, badges['human_experience'])

    def __repr__(self):
        return f'<Answer {self.id} on Q{self.question_id}>'


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answer_id = db.Column(
        db.Integer, db.ForeignKey('answers.id'), nullable=False
    )
    value = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'answer_id', name='one_vote_per_user'),
    )


class Story(db.Model):
    """Long-form health journey stories."""
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=False
    )
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    category = db.relationship('Category')

    @property
    def reading_time(self):
        words = len(self.body.split())
        return max(1, words // 200)


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(300), nullable=True)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )


class HazardReport(db.Model):
    """Health & Safety hazard reports submitted by workers."""
    __tablename__ = 'hazard_reports'

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reporter_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    suggested_action = db.Column(db.Text, nullable=True)
    urgency = db.Column(db.String(10), default='medium')  # low, medium, high
    status = db.Column(db.String(20), default='submitted')  # submitted, acknowledged, resolved
    resolved_by = db.Column(db.String(100), nullable=True)
    resolved_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    resolved_at = db.Column(db.DateTime, nullable=True)

    reporter = db.relationship('User', backref='hazard_reports')


class WorkplacePost(db.Model):
    __tablename__ = 'workplace_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic = db.Column(db.String(50), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    author = db.relationship('User', backref='workplace_posts')
    comments = db.relationship(
        'WorkplaceComment', backref='post', lazy='dynamic',
        order_by='WorkplaceComment.created_at'
    )


class WorkplaceComment(db.Model):
    __tablename__ = 'workplace_comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    post_id = db.Column(
        db.Integer, db.ForeignKey('workplace_posts.id'), nullable=False
    )
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    author = db.relationship('User', backref='workplace_comments')
