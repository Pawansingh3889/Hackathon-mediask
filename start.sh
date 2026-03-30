#!/bin/bash
set -e

echo "=== MediAsk Startup ==="

# Create DB tables
echo "Creating database tables..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('DB tables ready')"

# Seed categories
echo "Seeding categories..."
python scripts/seed_categories.py

# Seed main Q&A data (includes Gemini AI answers)
echo "Seeding Q&A data..."
python scripts/seed_qa.py

# Seed workers health Q&A (includes Gemini AI answers)
echo "Seeding workers health data..."
python scripts/seed_workers.py

# Backfill AI answers for any questions missing them
echo "Backfilling AI answers..."
python scripts/backfill_ai_answers.py

echo "=== Seeding complete, starting server ==="

# Start gunicorn
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 run:app
