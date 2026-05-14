#!/bin/bash
set -e

echo "=== MediAsk Startup ==="

# Create DB tables
echo "Creating database tables..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('DB tables ready')"

# Seed categories
echo "Seeding categories..."
python scripts/seed_categories.py

# Disable Gemini during seeding to avoid slow API calls on startup
# AI answers will use fast fallback text instead
export SKIP_GEMINI_SEED=1

# Seed main Q&A data
echo "Seeding Q&A data..."
python scripts/seed_qa.py

# Seed workers health Q&A
echo "Seeding workers health data..."
python scripts/seed_workers.py

# Backfill AI answers for any questions missing them
echo "Backfilling AI answers..."
python scripts/backfill_ai_answers.py

unset SKIP_GEMINI_SEED

echo "=== Seeding complete, starting server ==="

# Start gunicorn (port 7860 for Hugging Face Spaces, was 5000 on Render)
exec gunicorn --bind 0.0.0.0:7860 --workers 2 --timeout 120 run:app
