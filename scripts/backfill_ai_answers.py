"""Backfill AI answers for all existing questions that don't have one.

Uses the Gemini API to generate responses, with fallback text if unavailable.
Run this after seeding to ensure every question has an AI response.
"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Question, Answer
from app.ai_responder import auto_respond


def backfill():
    app = create_app()
    with app.app_context():
        # Get or create AI user
        ai_user = User.query.filter_by(email='ai@mediask.org').first()
        if not ai_user:
            ai_user = User(
                first_name='MediAsk',
                last_name='AI',
                email='ai@mediask.org',
                is_system_account=True,
                bio='AI health assistant providing practical guidance.'
            )
            ai_user.set_password('system-account-no-login')
            db.session.add(ai_user)
            db.session.commit()
            print('  + Created MediAsk AI user')

        # Find questions without AI answers
        all_questions = Question.query.all()
        missing = []
        for q in all_questions:
            has_ai = any(a.auth_level == 'ai_assistant' for a in q.answers)
            if not has_ai:
                missing.append(q)

        print(f'Found {len(missing)} questions without AI answers (out of {len(all_questions)} total)')

        if not missing:
            print('All questions already have AI answers. Nothing to do.')
            return

        count = 0
        for q in missing:
            print(f'  [{count + 1}/{len(missing)}] Generating AI answer for: {q.title[:60]}...')
            try:
                auto_respond(q)
                count += 1
                time.sleep(1)  # Rate limit for Gemini API
            except Exception as e:
                print(f'    Error: {e}')

        print(f'\nDone. Added AI answers to {count} questions.')


if __name__ == '__main__':
    backfill()
