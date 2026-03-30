"""MediAsk AI Auto-Responder with Gemini LLM integration."""
import os
from app import db
from app.models import User, Answer

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


SYSTEM_PROMPT = """You are MediAsk AI, a friendly and practical health assistant for a UK-based health Q&A platform.

YOUR STYLE:
- Talk like a knowledgeable friend, not a medical textbook
- Give PRACTICAL, actionable advice FIRST (home remedies, lifestyle steps, what to do right now)
- Then mention when to see a GP or NHS if needed
- Use simple everyday language
- Be warm, reassuring and direct

RESPONSE STRUCTURE (always follow this order):
1. Acknowledge the question briefly and empathetically
2. PRACTICAL STEPS FIRST — what they can do right now at home (drink water, rest, take paracetamol etc.)
3. What to watch out for — warning signs that mean they need professional help
4. When to contact NHS 111 or their GP
5. When to call 999 (only if genuinely relevant)
6. One-line disclaimer at the end

RULES:
- UK terminology: GP not PCP, A&E not ER, paracetamol not acetaminophen, NHS 111 not helpline
- Never diagnose — suggest possibilities and practical steps
- For mental health: mention Samaritans 116 123 and SHOUT text 85258
- Keep it 150-300 words — concise and useful
- Do NOT start with 'Based on NHS guidance' — just answer naturally
- Do NOT use overly formal language
- Practical home advice FIRST, NHS referral SECOND"""


FALLBACK_RESPONSES = {
    'mental-health': (
        'Feeling this way is more common than you might think, and it is okay to reach out for help.\n\n'
        'Things that can help right now:\n'
        '- Talk to someone you trust — a friend, family member, or colleague\n'
        '- Get outside for a short walk — even 10 minutes can lift your mood\n'
        '- Try the NHS Mood Self-Assessment at nhs.uk to understand your symptoms\n'
        '- Practice box breathing: breathe in for 4 counts, hold for 4, out for 4\n\n'
        'When to get professional support:\n'
        '- If feelings persist for more than 2 weeks, book a GP appointment\n'
        '- You can self-refer to NHS Talking Therapies (free CBT) without a GP referral at nhs.uk/talk\n\n'
        'Urgent support:\n'
        '- Samaritans: 116 123 (free, 24/7)\n'
        '- Crisis Text Line: text SHOUT to 85258\n'
        '- NHS 111 for urgent advice'
    ),
    'infections': (
        'Most infections can be managed at home with rest and simple remedies.\n\n'
        'What to do right now:\n'
        '- Stay hydrated — drink plenty of water, diluted juice, or clear broth\n'
        '- Rest as much as possible — your body needs energy to fight the infection\n'
        '- Take paracetamol or ibuprofen to reduce fever and ease discomfort\n'
        '- Eat light, easy-to-digest foods when you feel able\n\n'
        'See your GP if:\n'
        '- Symptoms have not improved after 7 days\n'
        '- You develop a high fever above 39°C\n'
        '- You have difficulty breathing or chest pain\n\n'
        'Call 999 or go to A&E if symptoms become severe or you feel very unwell very quickly.'
    ),
    'cardiovascular': (
        'Heart health improves significantly with consistent daily habits.\n\n'
        'Practical steps you can start today:\n'
        '- Cut down on salt — aim for less than 6g per day (check food labels)\n'
        '- Walk for 30 minutes daily — it genuinely makes a measurable difference\n'
        '- Swap processed foods for more fruit, veg, and whole grains\n'
        '- Check your blood pressure at your local pharmacy — it is free\n'
        '- If you smoke, talk to your GP about stop smoking support\n\n'
        'Book a GP appointment if:\n'
        '- You have not had a blood pressure or cholesterol check recently\n'
        '- You experience breathlessness, chest tightness, or palpitations\n\n'
        'Call 999 immediately for: chest pain, pain spreading to the arm or jaw, sudden severe breathlessness.'
    ),
    'skin-conditions': (
        'Most skin conditions can be managed effectively at home with the right routine.\n\n'
        'Practical steps:\n'
        '- Moisturise at least twice daily with a fragrance-free emollient\n'
        '- Use mild, fragrance-free soap and avoid hot showers\n'
        '- Wear loose cotton clothing to avoid irritation\n'
        '- Avoid known triggers like certain soaps, detergents, or foods\n'
        '- Antihistamines from the pharmacy can help with itching\n\n'
        'See your GP if:\n'
        '- The condition is not improving after 2 weeks of self-care\n'
        '- You notice a new or changing mole or skin lesion\n'
        '- There are signs of infection (increased redness, warmth, pus)'
    ),
    'general': (
        'Here are some practical steps to help with your concern:\n\n'
        '- Rest well and stay hydrated — this helps with most common health issues\n'
        '- Take over-the-counter remedies like paracetamol if you are in pain or have a fever\n'
        '- Monitor your symptoms and note when they are better or worse\n'
        '- The NHS website (nhs.uk) has detailed, reliable information on most conditions\n\n'
        'Contact NHS 111 (free, 24/7) if you need advice and cannot wait for a GP appointment.\n\n'
        'Book a GP appointment if symptoms persist for more than a week or are getting worse.\n\n'
        'Call 999 for life-threatening emergencies.'
    ),
}


def get_ai_user():
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
    return ai_user


def generate_with_gemini(question):
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
            f"Answer naturally and practically:"
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
    slug = question.category.slug if question.category else 'general'
    return FALLBACK_RESPONSES.get(slug, FALLBACK_RESPONSES['general'])


def auto_respond(question):
    ai_user = get_ai_user()
    existing = Answer.query.filter_by(
        question_id=question.id,
        author_id=ai_user.id
    ).first()
    if existing:
        return existing

    response_text = generate_with_gemini(question)
    source = 'Gemini AI'

    if not response_text:
        response_text = generate_fallback(question)
        source = 'MediAsk AI'

    response_text += (
        '\n\n---\n'
        '*This is AI-generated health information, not a substitute for professional medical advice. '
        'Always consult a qualified healthcare professional for personalised guidance.*'
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
