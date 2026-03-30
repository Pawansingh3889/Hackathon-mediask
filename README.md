# MediAsk - Health Q&A for Workers

**Live Demo:** [hackathon-ioqp.onrender.com](https://hackathon-ioqp.onrender.com)

MediAsk is a community health Q&A platform designed for factory workers, food processors, and manual labourers in the UK. It combines NHS-verified guidance, real worker experiences, and AI-powered responses to answer health questions that matter most to working people.

## Why MediAsk?

Factory workers face unique health risks - back injuries from heavy lifting, cold exposure in processing plants, chemical burns, hearing damage, and mental health struggles from isolation and shift work. Most health platforms don't address these workplace-specific issues. MediAsk does.

- **70%** of factory workers report musculoskeletal pain
- **40%** of shift workers suffer from sleep disorders
- Many immigrant workers don't know their NHS rights or workplace protections

## Features

### For Workers
- **Ask Health Questions** - get answers from NHS sources, experienced workers, and AI
- **Voice Input** - speak your question instead of typing (useful with gloves/dirty hands)
- **Multi-Language Support** - Google Translate with 18 languages (Hindi, Polish, Romanian, Urdu, Bengali, Arabic, and more)
- **Workers Health Hub** - dedicated section for factory-specific issues (back pain, cold rooms, RSI, chemicals, shift work, legal rights)
- **NHS Health Lookup** - search NHS conditions database in real-time
- **Hazard Reporting** - report unsafe conditions directly to management

### For the Community
- **Vote on Answers** - upvote helpful responses, downvote unhelpful ones
- **Reputation System** - earn points for asking, answering, and helping (Newcomer > Contributor > Helper > Expert > Guardian > Legend)
- **Stories** - share longer health journey articles
- **Workplace Support** - anonymous discussion boards for workplace wellbeing

### AI-Powered
- **Gemini AI Responses** - every question gets an instant AI answer using Google Gemini 2.5 Flash
- **Practical Advice First** - AI trained to give actionable steps before medical referrals
- **NHS-Aligned** - uses UK terminology (GP, A&E, paracetamol) and references UK law

### Admin Dashboard
- **Full Control** - delete questions/answers, manage users, promote/demote admins
- **Hazard Report Management** - acknowledge and resolve workplace hazard reports
- **Site Statistics** - questions, answers, users, AI answers at a glance
- **Browser Push Notifications** - real-time alerts when questions get answered

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | PostgreSQL (production), SQLite (development) |
| ORM | SQLAlchemy with Flask-Migrate |
| Auth | Flask-Login, Google OAuth 2.0 |
| AI | Google Gemini 2.5 Flash API |
| Frontend | Jinja2, Vanilla JavaScript, CSS |
| Voice | Web Speech API (browser-native) |
| Translation | Google Translate Widget |
| Health Data | NHS API Integration |
| Deployment | Docker, Render |

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (or SQLite for dev)

### Setup

```bash
# Clone
git clone https://github.com/Pawansingh3889/Hackathon-mediask.git
cd Hackathon-mediask

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///mediask.db
export GEMINI_API_KEY=your-gemini-key        # optional, for AI answers
export GOOGLE_CLIENT_ID=your-oauth-id        # optional, for Google login
export GOOGLE_CLIENT_SECRET=your-oauth-secret # optional, for Google login

# Initialize database and seed data
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
python scripts/seed_categories.py
python scripts/seed_qa.py
python scripts/seed_workers.py

# Run
python run.py
```

Open [http://localhost:5000](http://localhost:5000)

### Docker

```bash
docker build -t mediask .
docker run -p 5000:5000 -e DATABASE_URL=sqlite:///mediask.db mediask
```

## Project Structure

```
Hackathon-mediask/
|-- app/
|   |-- __init__.py          # Flask app factory
|   |-- models.py            # SQLAlchemy models (User, Question, Answer, Vote, etc.)
|   |-- ai_responder.py      # Gemini AI auto-responder
|   |-- config.py            # Configuration
|   |-- auth/                # Authentication (login, register, Google OAuth)
|   |-- main/                # Homepage, search, admin dashboard, NHS API
|   |-- questions/           # Q&A (ask, detail, vote, delete)
|   |-- users/               # Profiles, notifications, reputation
|   |-- workplace/           # Workplace wellbeing boards
|   |-- stories/             # Health journey stories
|   |-- templates/           # Jinja2 HTML templates
|   |-- static/              # CSS, JavaScript, images
|-- scripts/
|   |-- seed_categories.py   # 17 health categories
|   |-- seed_qa.py           # 40+ health Q&A with AI answers
|   |-- seed_workers.py      # 30+ factory worker Q&A with AI answers
|   |-- backfill_ai_answers.py # Add AI answers to existing questions
|-- Dockerfile
|-- requirements.txt
|-- run.py
```

## Data Sources

- **NHS UK** - Official health guidance (nhs.uk)
- **GOV.UK / HSE** - Workplace health & safety regulations
- **WHO** - World Health Organization recommendations
- **CDC** - US Centers for Disease Control data
- **NHS API** - Live condition search

## Health Categories

Mental Health, Cancer, Cardiovascular, Surgery, Blood Disorders, Eye & Vision, ENT, Infections, Skin Conditions, Stroke, Congenital Disorders, Immune System, Metabolic & Endocrine, Allergies, Memory & Neurology, Relationships & Emotions, General Health, Workers Health

## Author

**Pawan Singh Kapkoti**
- MSc Data Analytics, Aston University
- GitHub: [@Pawansingh3889](https://github.com/Pawansingh3889)
- Location: Hull, UK

## License

This project was built for a hackathon. All health information is sourced from public NHS and GOV.UK resources.
