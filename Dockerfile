FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["bash", "-c", "python -c 'from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print(\"DB tables created\")' && python scripts/seed_categories.py && gunicorn --bind 0.0.0.0:5000 run:app"]
