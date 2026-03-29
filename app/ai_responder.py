"""MediAsk AI Auto-Responder with Gemini LLM integration.

Uses Google Gemini API when available, falls back to
category-based NHS templates when no API key is set.
"""
import os
from app import db
from app.models import User, Answer

# Try to import Gemini (new SDK)
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


SYSTEM_PROMPT = """You are MediAsk AI, a helpful health information assistant for a UK-based health Q&A platform.

RULES:
1. Provide helpful, accurate health information based on NHS and GOV.UK guidance
2. ALWAYS include a disclaimer that you are not a doctor and this is not medical advice
3. Recommend seeing a GP or calling NHS 111 when appropriate
4. For emergencies, always say call 999
5. For mental health crises, mention Samaritans (116 123) and Crisis Text Line (text SHOUT to 85258)
6. Be empathetic and non-judgmental
7. Use UK medical terminology (GP not PCP, A&E not ER, paracetamol not acetaminophen)
8. Structure your answer with clear sections using line breaks
9. Keep answers concise but thorough (200-400 words)
10. Never diagnose — suggest possible explanations and recommend professional assessment

FORMAT YOUR RESPONSE LIKE THIS:
- Start with the most relevant information
- Use bullet points for lists
- End with when to see a GP/seek urgent help
- Final line: disclaimer about AI-generated content"""

# Category-specific fallback templates (used when no Gemini key)
FALLBACK_RESPONSES = {
    'mental-health': (
        'Based on NHS mental health guidance:\n\n'
        'Mental health conditions are real medical conditions that deserve '
        'proper attention and care. The NHS recommends:\n\n'
        '- Speaking with your GP as the first step — they can assess '
        'your symptoms and refer you to appropriate support\n'
        '- NHS Talking Therapies (self-refer at nhs.uk/talk) — free CBT, '
        'counselling, and guided self-help without needing a GP referral\n'
        '- Keeping a symptom diary to help your GP understand patterns\n'
        '- Regular exercise, good sleep, and social connection all '
        'support mental wellbeing\n\n'
        'Urgent support:\n'
        '- Samaritans: 116 123 (free, 24/7)\n'
        '- Crisis Text Line: text SHOUT to 85258\n'
        '- NHS 111 for urgent medical advice\n'
        '- 999 for emergencies\n\n'
        'Remember: seeking help is a sign of strength, not weakness.'
    ),
    'cardiovascular': (
        'Based on NHS cardiovascular guidance:\n\n'
        'Heart and circulatory conditions are common but many are '
        'preventable or manageable with early detection.\n\n'
        'Key recommendations:\n'
        '- Monitor blood pressure regularly (ideal: below 120/80)\n'
        '- Get cholesterol checked (target: total below 5 mmol/L)\n'
        '- Exercise: 150 minutes moderate activity per week\n'
        '- Diet: low salt, low saturated fat, plenty of fruit and veg\n'
        '- Stop smoking — the single biggest risk factor you can change\n'
        '- Limit alcohol to 14 units per week\n\n'
        'Call 999 immediately if you experience: chest pain, '
        'pain spreading to arm or jaw, sudden breathlessness, '
        'or sudden severe headache.'
    ),
    'general': (
        'Based on NHS general health guidance:\n\n'
        'For this type of health concern, here are some general '
        'recommendations:\n\n'
        '- Book an appointment with your GP to discuss your symptoms\n'
        '- Keep a diary of when symptoms occur, how severe they are, '
        'and any potential triggers\n'
        '- Bring a list of any medications you are currently taking\n'
        '- The NHS website (nhs.uk) has detailed information on most '
        'health conditions\n\n'
        'For urgent but non-emergency concerns, contact NHS 111 '
        '(available 24/7) for advice on next steps.\n\n'
        'In an emergency, always call 999.'
    ),
}


def get_ai_user():
    """Get or create the AI system user."""
    ai_user = User.query.filter_by(email='ai@mediask.org').first()
    if not ai_user:
        ai_user = User(
            first_name='MediAsk',
            last_name='AI',
            email='ai@mediask.org',
            is_system_account=True,
            bio='AI health assistant providing initial guidance based on NHS resources.'
        )
        ai_user.set_password('system-account-no-login')
        db.session.add(ai_user)
        db.session.commit()
    return ai_user


def generate_with_gemini(question):
    """Generate response using Google Gemini API (new SDK)."""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or not GEMINI_AVAILABLE:
        return None

    try:
        client = genai.Client(api_key=api_key)

        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"CATEGORY: {question.category.name}\n"
            f"QUESTION: {question.title}\n"
            f"DETAILS: {question.body}\n\n"
            f"Provide a helpful, NHS-aligned response:"
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f'Gemini API error: {e}')
        return None


def generate_fallback(question):
    """Generate response using category templates (no API needed)."""
    slug = question.category.slug if question.category else 'general'
    base = FALLBACK_RESPONSES.get(slug, FALLBACK_RESPONSES['general'])
    return base


def auto_respond(question):
    """Create an automatic AI response for a new question."""
    ai_user = get_ai_user()

    # Check if AI already answered
    existing = Answer.query.filter_by(
        question_id=question.id,
        author_id=ai_user.id
    ).first()
    if existing:
        return existing

    # Try Gemini first, fall back to templates
    response_text = generate_with_gemini(question)
    source = 'Gemini AI'

    if not response_text:
        response_text = generate_fallback(question)
        source = 'MediAsk AI'

    # Add disclaimer
    response_text += (
        '\n\n---\n'
        '*This is an AI-generated response based on NHS and GOV.UK '
        'health guidance. It is not a substitute for professional '
        'medical advice. Please consult a qualified healthcare '
        'professional for personalised guidance.*'
    )

    answer = Answer(
        body=response_text,
        question_id=question.id,
        author_id=ai_user.id,
        auth_level='ai_assistant',
        source=source,
    )
    db.session.add(answer)
    db.session.commit()
    return answer
