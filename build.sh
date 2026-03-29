#!/usr/bin/env bash
set -e

pip install -r requirements.txt

# Create database tables
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database tables created')
"

# Seed categories
python scripts/seed_categories.py

echo "Build complete"
