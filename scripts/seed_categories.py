"""Seed the database with medical categories."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Category

CATEGORIES = [
    ('Mental Health', 'mental-health', 'Anxiety, depression, stress, therapy', 'fa-brain'),
    ('Cancer', 'cancer', 'Diagnosis, treatment, chemotherapy, support', 'fa-ribbon'),
    ('Cardiovascular', 'cardiovascular', 'Heart disease, blood pressure, cholesterol', 'fa-heart-pulse'),
    ('Surgery', 'surgery', 'Pre-op, post-op, procedures, recovery', 'fa-user-doctor'),
    ('Blood Disorders', 'blood-disorders', 'Anaemia, clotting, transfusions', 'fa-droplet'),
    ('Eye & Vision', 'eye-vision', 'Eye conditions, vision correction, screenings', 'fa-eye'),
    ('Ear, Nose & Throat', 'ent', 'Hearing, sinuses, throat conditions', 'fa-ear-listen'),
    ('Infections', 'infections', 'Bacterial, viral, fungal infections', 'fa-virus'),
    ('Skin Conditions', 'skin', 'Eczema, acne, dermatitis, rashes', 'fa-hand-dots'),
    ('Stroke', 'stroke', 'Prevention, recovery, rehabilitation', 'fa-bolt'),
    ('Congenital Disorders', 'congenital', 'Birth conditions, genetic disorders', 'fa-baby'),
    ('Immune System', 'immune-system', 'Autoimmune diseases, allergies, inflammation', 'fa-shield-virus'),
    ('Metabolic & Endocrine', 'metabolic', 'Diabetes, thyroid, hormonal conditions', 'fa-syringe'),
    ('Allergies', 'allergies', 'Food, seasonal, drug allergies', 'fa-allergens'),
    ('Memory & Neurology', 'neurology', "Alzheimer's, dementia, memory loss", 'fa-head-side-virus'),
    ('Relationships & Emotions', 'emotions', 'Emotional wellbeing, relationship health', 'fa-comments'),
    ('General Health', 'general', 'Fitness, nutrition, preventive care', 'fa-apple-whole'),
]


def seed():
    app = create_app()
    with app.app_context():
        for name, slug, desc, icon in CATEGORIES:
            existing = Category.query.filter_by(slug=slug).first()
            if not existing:
                cat = Category(
                    name=name, slug=slug,
                    description=desc, icon=icon
                )
                db.session.add(cat)
                print(f'  + {name}')
            else:
                print(f'  = {name} (exists)')
        db.session.commit()
        print(f'\nDone. {Category.query.count()} categories total.')


if __name__ == '__main__':
    seed()
