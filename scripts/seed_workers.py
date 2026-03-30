"""Seed factory worker health Q&A with worldwide sources."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Question, Answer, Category
from datetime import datetime, timezone, timedelta
import random
import time

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


GEMINI_SYSTEM_PROMPT = """You are MediAsk AI, a friendly and practical health assistant for a UK-based health Q&A platform focused on factory and manual workers.

YOUR STYLE:
- Talk like a knowledgeable friend, not a medical textbook
- Give PRACTICAL, actionable advice FIRST
- Use simple everyday language
- Be warm, reassuring and direct

RESPONSE STRUCTURE:
1. Brief empathetic acknowledgement
2. PRACTICAL STEPS — numbered list of what to do right now
3. Warning signs that need professional help
4. Key contact numbers if relevant (HSE: 0300 003 1647, ACAS: 0300 123 1100, NHS 111)
5. One-line disclaimer: "Please note: this is general health information, not a substitute for professional medical advice."

RULES:
- UK terminology: GP not PCP, A&E not ER, paracetamol not acetaminophen
- Keep it 100-200 words
- Do NOT start with 'Based on NHS guidance' — just answer naturally
- Practical advice FIRST, NHS referral SECOND
- Reference UK workplace law where relevant (HSE, COSHH, RIDDOR)"""


def _generate_ai_with_gemini(title, body, answers_data):
    """Generate an AI response using the Gemini API."""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or not GEMINI_AVAILABLE:
        return None
    try:
        client = genai.Client(api_key=api_key)
        # Include existing answers as context
        context_parts = []
        for a_first, a_last, a_body, a_source, a_url in answers_data:
            source_label = f' ({a_source})' if a_source else ''
            context_parts.append(f'{a_first} {a_last}{source_label}: {a_body[:300]}')
        context = '\n\n'.join(context_parts)

        prompt = (
            f"{GEMINI_SYSTEM_PROMPT}\n\n"
            f"QUESTION: {title}\n"
            f"DETAILS: {body}\n\n"
            f"OTHER ANSWERS ALREADY PROVIDED:\n{context}\n\n"
            f"Provide a helpful AI summary response that adds value beyond the existing answers. "
            f"Focus on practical next steps the person can take right now:"
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f'  Gemini API error: {e}')
        return None

# Add Workers Health category if not exists
def ensure_category():
    app = create_app()
    with app.app_context():
        cat = Category.query.filter_by(slug='workers-health').first()
        if not cat:
            cat = Category(
                name='Workers Health',
                slug='workers-health',
                description='Health guidance for factory workers, food processors, and manual labourers',
                icon='fa-hard-hat'
            )
            db.session.add(cat)
            db.session.commit()
            print(f'  + Workers Health category created')
        return cat.id


WORKERS_QA = [
    # === BACK PAIN & LIFTING ===
    ('workers-health', 'How do I prevent back pain from lifting heavy trays all day?',
     'I work in a food processing factory lifting 15-20kg trays for 10 hours. My lower back is in constant pain.',
     None,
     [('NHS', 'Official', 'The HSE and NHS recommend the following for manual handling:\n\n- Always bend your knees, not your back, when lifting\n- Hold loads close to your body at waist height\n- Avoid twisting your body while carrying\n- Push rather than pull where possible\n- Ask for help with loads over 25kg\n- Take micro-breaks every 30 minutes\n- Stretch your hamstrings and hip flexors daily\n\nYour employer is legally required to provide manual handling training and reduce risks. If they have not done this, they are breaking the law under the Manual Handling Operations Regulations 1992.', 'nhs.uk', 'https://www.nhs.uk/live-well/exercise/strength-and-flexibility-exercises/lower-back-pain-exercises/'),
      ('WHO', 'Official', 'Musculoskeletal disorders are the leading cause of disability worldwide, affecting 1.71 billion people globally. The World Health Organization recommends that workplaces implement ergonomic interventions including job rotation, mechanical lifting aids, adjustable workstation heights, and regular rest breaks to prevent work-related back injuries.', 'who.int', 'https://www.who.int/news-room/fact-sheets/detail/musculoskeletal-conditions'),
      ('MediAsk', 'AI', 'Here is a quick summary of what you can do right now:\n\n1. Use correct lifting technique — bend at the knees, keep the load close to your waist, and avoid twisting\n2. Ask your employer for manual handling training and mechanical aids (trolleys, hoists)\n3. Take micro-breaks every 30 minutes to stretch your lower back, hamstrings, and hip flexors\n4. See your GP if pain persists — they can refer you for physiotherapy\n5. Your employer is legally required to reduce manual handling risks under the Manual Handling Operations Regulations 1992\n\nPlease note: this is general guidance and not a substitute for professional medical advice. Always consult your GP for persistent pain.', 'MediAsk AI', None),
     ]),

    ('workers-health', 'Is it normal to have back pain at 25 from factory work?',
     'I am 25 and already have chronic lower back pain from 3 years of factory work. Is this normal?',
     None,
     [('Dr Sarah', 'Mitchell', 'Unfortunately this is very common but it is NOT normal or acceptable. Back pain at 25 from work means your workplace is not managing manual handling risks properly. You should:\n\n1. See your GP — they can refer you for physiotherapy\n2. Report the issue to your employer in writing\n3. Request an occupational health assessment\n4. Contact HSE if your employer does not act\n\nYou may also be entitled to compensation if your employer failed to provide proper training, equipment, or breaks. Keep a diary of your symptoms and when they occur.', None, None),
     ]),

    # === COLD EXPOSURE ===
    ('workers-health', 'Can working in a cold room (0-4°C) all day damage my health?',
     'I work in a fish processing cold room at 2°C for 8-10 hours. My fingers go numb and I get headaches.',
     None,
     [('NHS', 'Official', 'Prolonged cold exposure can cause several health problems:\n\n- Raynaud\'s phenomenon (fingers turning white/blue due to restricted blood flow)\n- Hypothermia risk if core body temperature drops below 35°C\n- Increased risk of respiratory infections\n- Joint stiffness and muscle pain\n- Chilblains (painful red swellings on fingers and toes)\n\nYour employer must provide adequate thermal clothing, regular warm-up breaks, and hot drinks. The minimum workplace temperature for physical work is not legally defined for cold storage, but HSE guidance says employers must take reasonable steps to keep workers safe.', 'nhs.uk', 'https://www.nhs.uk/conditions/raynauds/'),
      ('GOV.UK', 'Health', 'Under the Workplace (Health, Safety and Welfare) Regulations 1992, employers must provide a reasonable working temperature. For cold storage facilities, this means providing adequate PPE (thermal jackets, insulated gloves, warm footwear), scheduled warm-up breaks, and limiting continuous cold exposure time.', 'gov.uk', 'https://www.hse.gov.uk/temperature/employer/index.htm'),
     ]),

    ('workers-health', 'My fingers turn white and numb in the cold room. Is this serious?',
     'When I work in the freezer section, my fingers go completely white and I lose feeling. My supervisor says it is normal.',
     None,
     [('Dr Sarah', 'Mitchell', 'This sounds like Raynaud\'s phenomenon, where blood vessels in your fingers spasm in cold conditions, cutting off blood supply. It is NOT normal and your supervisor is wrong to dismiss it.\n\nYou should:\n1. See your GP immediately — Raynaud\'s can be primary (harmless but uncomfortable) or secondary (linked to an underlying condition)\n2. Report this to your employer — they must provide thermal gloves and warm-up breaks\n3. Keep your hands warm before entering cold areas\n4. Avoid caffeine before shifts (it constricts blood vessels)\n\nIf your fingers stay blue or you develop sores, seek urgent medical attention.', None, None),
     ]),

    # === REPETITIVE STRAIN ===
    ('workers-health', 'I have constant wrist pain from packing on the production line. What is RSI?',
     'I pack fish fillets into trays for 8 hours straight. My wrists and forearms ache constantly. Could this be RSI?',
     None,
     [('NHS', 'Official', 'Repetitive strain injury (RSI) is a general term for pain in muscles, nerves, and tendons caused by repetitive movement and overuse. Symptoms include pain, aching, tenderness, stiffness, throbbing, tingling, numbness, and weakness in the affected area.\n\nTreatment includes:\n- Rest from the activity causing pain\n- Ice packs, anti-inflammatory painkillers\n- Physiotherapy exercises\n- Wrist splints\n\nYour employer should rotate tasks, provide ergonomic tools, and allow regular breaks. If they do not, they are failing their duty of care under the Health and Safety at Work Act 1974.', 'nhs.uk', 'https://www.nhs.uk/conditions/repetitive-strain-injury-rsi/'),
      ('CDC', 'Official', 'The US Centers for Disease Control reports that work-related musculoskeletal disorders account for 30% of all worker compensation claims. NIOSH recommends employers implement ergonomic programs including workstation design, tool modifications, work practice controls, and administrative controls such as job rotation and rest breaks.', 'cdc.gov', 'https://www.cdc.gov/niosh/topics/ergonomics/'),
     ]),

    # === SKIN PROBLEMS ===
    ('workers-health', 'My hands are cracked and bleeding from constant washing and glove use at work.',
     'I work in food processing and have to wash my hands 30+ times a day and wear latex gloves. My skin is raw and cracking.',
     None,
     [('NHS', 'Official', 'Occupational contact dermatitis is very common in food processing workers. Frequent hand washing strips natural oils from the skin, and gloves can trap moisture and cause irritation.\n\nManagement:\n- Use emollient moisturiser (like Doublebase or Cetraben) after every hand wash\n- Ask your employer for non-latex, powder-free nitrile gloves\n- Pat hands dry, do not rub\n- Use lukewarm water, not hot\n- Apply barrier cream before starting work\n- See your GP if skin is infected (red, hot, weeping)\n\nYour employer must provide suitable gloves and barrier cream as PPE. Occupational dermatitis can be reported as an industrial disease.', 'nhs.uk', 'https://www.nhs.uk/conditions/contact-dermatitis/'),
     ]),

    ('workers-health', 'Can cleaning chemicals at work damage my skin and lungs?',
     'We use strong bleach and industrial cleaners to sanitise equipment. I get headaches and my hands burn even through gloves.',
     None,
     [('GOV.UK', 'Health', 'Under COSHH (Control of Substances Hazardous to Health) Regulations 2002, your employer MUST:\n\n- Provide Safety Data Sheets for all chemicals used\n- Conduct a COSHH risk assessment\n- Provide appropriate PPE (chemical-resistant gloves, eye protection, respiratory protection if needed)\n- Train you on safe handling\n- Provide adequate ventilation\n- Provide emergency washing facilities\n\nIf you are experiencing burns through gloves, the gloves are not suitable for the chemicals being used. Report this to your employer immediately. If they do not act, contact HSE on 0300 003 1647.', 'gov.uk', 'https://www.hse.gov.uk/coshh/'),
     ]),

    # === SHIFT WORK & SLEEP ===
    ('workers-health', 'How do I cope with rotating shift patterns? I cannot sleep properly.',
     'My factory does 6am-2pm one week, 2pm-10pm the next, then 10pm-6am. I am exhausted and cannot sleep.',
     None,
     [('NHS', 'Official', 'Shift work disorder affects up to 40% of shift workers. Tips for managing:\n\n- Keep your bedroom dark (blackout curtains are essential for day sleeping)\n- Maintain a consistent sleep routine even on days off\n- Avoid caffeine 6 hours before bed\n- Take a short nap before a night shift (20-30 minutes)\n- Use bright light at the start of your shift to reset your body clock\n- Eat small, regular meals rather than one large meal\n\nIf sleep problems persist for more than 3 months, see your GP. Chronic shift work disorder increases risk of heart disease, diabetes, and depression.', 'nhs.uk', 'https://www.nhs.uk/live-well/sleep-and-tiredness/how-to-get-to-sleep/'),
      ('WHO', 'Official', 'The World Health Organization has classified night shift work as a Group 2A probable carcinogen due to disruption of circadian rhythms. WHO recommends minimising consecutive night shifts, providing forward-rotating shift patterns (morning→afternoon→night rather than reverse), and allowing at least 11 hours between shifts for recovery.', 'who.int', 'https://www.who.int/news-room/questions-and-answers/item/radiation-night-shift-work'),
     ]),

    # === STANDING ALL DAY ===
    ('workers-health', 'My feet and legs hurt from standing on concrete for 10 hours. What can I do?',
     'I stand on a concrete factory floor for my entire shift. My heels, knees, and calves are in agony by the end.',
     None,
     [('Emily', 'Chen', 'I worked a packing line for 2 years and went through exactly this. What helped:\n\n1. Insoles — get proper anti-fatigue insoles (Dr Scholl\'s Work insoles are about 10 pounds and last 3 months)\n2. Compression socks — they reduce swelling and improve circulation. Game changer.\n3. Anti-fatigue mat — if you stand in one spot, ask your employer to provide one. They are legally recommended by HSE.\n4. Stretch calves during breaks — stand on a step and let your heels drop\n5. Elevate feet when you get home — put them up for 15 minutes\n\nYour employer should provide anti-fatigue mats and seating for rest breaks.', None, None),
     ]),

    # === MENTAL HEALTH IN FACTORIES ===
    ('workers-health', 'I feel isolated working in a factory where nobody speaks my language.',
     'I moved to the UK from India and work in a food factory. Most workers speak Eastern European languages and I feel completely alone during 10-hour shifts.',
     None,
     [('Ahmed', 'Malik', 'I understand this deeply — I am from Pakistan and experienced the same thing in my first factory job. What helped:\n\n1. Learn a few phrases in the main language spoken (even "hello", "thank you", "break?" makes a difference)\n2. Look for cultural/community groups in your area — many UK cities have Indian/South Asian community centres\n3. Use your breaks to call family or friends\n4. Ask if there is a buddy system at work for new starters\n5. The Migrant Help charity (0808 8010 503) offers free support\n\nThe loneliness is real but it does get better. It took me about 6 months to build friendships at work.', None, None),
      ('NHS', 'Official', 'Loneliness and social isolation can seriously affect mental and physical health. The NHS recommends talking to your GP if loneliness is affecting your mood. Free support is available through:\n- Samaritans: 116 123 (available in many languages)\n- Mind: 0300 123 3393\n- Migrant Help: 0808 8010 503\n- Your local Citizens Advice Bureau can help with workplace issues', 'nhs.uk', 'https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/loneliness/'),
     ]),

    ('workers-health', 'Night shifts are making me depressed. Is this normal?',
     'I have been doing permanent night shifts for 6 months. I never see daylight, I have no social life, and I feel deeply unhappy.',
     None,
     [('Dr Sarah', 'Mitchell', 'Night shift depression is a real and recognised condition. The lack of sunlight disrupts your serotonin and melatonin production, which directly affects mood.\n\nWhat you can do:\n1. Get outside in daylight even briefly on your days off\n2. Consider a SAD lamp (10,000 lux light therapy) — use it for 30 minutes when you wake up\n3. Vitamin D supplements (many night workers are severely deficient)\n4. Exercise, even if it is just a 20-minute walk\n5. Talk to your GP — they can screen for depression and offer treatment\n6. Ask your employer about rotating shifts rather than permanent nights\n\nYou are not weak for struggling with this. The human body is not designed for permanent night work.', None, None),
     ]),

    # === WORKERS' RIGHTS ===
    ('workers-health', 'What are my rights to sick pay if I am injured at work in the UK?',
     'I hurt my back lifting at work but my employer says I have no right to sick pay because I am on a zero-hours contract.',
     None,
     [('GOV.UK', 'Health', 'Your employer is WRONG. ALL employees and workers (including zero-hours contracts) are entitled to Statutory Sick Pay (SSP) if they:\n\n- Earn at least 123 pounds per week on average\n- Have been off sick for 4 or more days in a row\n- Have given proper notice\n\nSSP is 116.75 pounds per week for up to 28 weeks. If your employer refuses, contact HMRC on 0300 200 3500.\n\nAdditionally, if your injury was caused by your employer\'s negligence (inadequate training, no equipment, unsafe conditions), you may be entitled to compensation. Contact Citizens Advice (0800 144 8848) for free legal guidance.', 'gov.uk', 'https://www.gov.uk/statutory-sick-pay'),
     ]),

    ('workers-health', 'Can my employer sack me for being off sick with a work injury?',
     'I injured my wrist at work and have been off for 2 weeks. My manager is threatening to fire me.',
     None,
     [('GOV.UK', 'Health', 'Your employer CANNOT dismiss you simply for being off sick, especially if the injury was caused at work. Under the Employment Rights Act 1996, dismissal while on sick leave can be classed as unfair dismissal if:\n\n- You have worked for the employer for 2+ years\n- The dismissal is not for a fair reason\n- Proper procedures were not followed\n\nIf your injury qualifies as a disability under the Equality Act 2010 (substantial and long-term impact on daily activities), your employer must make reasonable adjustments.\n\nKeep ALL communications in writing. If threatened, contact:\n- ACAS helpline: 0300 123 1100\n- Citizens Advice: 0800 144 8848\n- Your trade union (if you are a member)', 'gov.uk', 'https://www.gov.uk/dismissal'),
     ]),

    ('workers-health', 'My employer does not provide safety gloves or protective equipment. Is this legal?',
     'I work with sharp knives cutting fish and my employer has never provided cut-resistant gloves. I have cut myself 3 times.',
     None,
     [('GOV.UK', 'Health', 'This is ILLEGAL. Under the Personal Protective Equipment at Work Regulations 1992, your employer MUST:\n\n- Assess the risks in your workplace\n- Provide suitable PPE free of charge (cut-resistant gloves, safety boots, ear protection, eye protection)\n- Train you in how to use PPE properly\n- Replace PPE when it is worn or damaged\n- Ensure PPE is properly maintained\n\nFor knife work in food processing, cut-resistant gloves are essential PPE. Your employer is breaking the law.\n\nReport this to HSE: 0300 003 1647 or online at hse.gov.uk/contact. You can report anonymously. You are legally protected from being sacked for raising health and safety concerns.', 'gov.uk', 'https://www.hse.gov.uk/toolbox/ppe.htm'),
     ]),

    # === RESPIRATORY ===
    ('workers-health', 'Can working in cold rooms cause breathing problems?',
     'I have developed a persistent cough and wheeze since starting work in a 2°C fish processing room. Could this be related?',
     None,
     [('Dr Sarah', 'Mitchell', 'Yes, cold air exposure can trigger or worsen respiratory conditions. Cold, dry air irritates the airways, causing them to constrict. This is called cold-induced bronchoconstriction and is common in cold storage workers.\n\nPossible causes of your symptoms:\n- Occupational asthma (triggered by cold air, fish proteins, or chemicals)\n- Cold-induced bronchospasm\n- Respiratory infections (cold environments suppress local immune responses)\n\nSee your GP urgently. Mention:\n1. Your work environment (temperature, chemicals, fish processing)\n2. Whether symptoms improve on days off\n3. Whether you have a history of asthma or allergies\n\nOccupational asthma is a reportable industrial disease. Your GP can refer you to an occupational health specialist.', None, None),
     ]),

    # === FOOD SAFETY & PERSONAL HEALTH ===
    ('workers-health', 'I keep getting stomach bugs. Could it be from working with raw food?',
     'I work handling raw fish and chicken. I wash my hands frequently but get stomach upsets almost every month.',
     None,
     [('NHS', 'Official', 'Working with raw meat and fish increases exposure to bacteria like Salmonella, E. coli, Campylobacter, and Listeria. While good hygiene should prevent illness, repeated stomach infections could indicate:\n\n- Inadequate handwashing technique (wash for 20+ seconds with soap)\n- Cross-contamination from work clothes to personal items\n- Inadequate cleaning of shared facilities\n- A weakened immune system from stress, poor sleep, or poor nutrition\n\nSee your GP if you are getting monthly stomach infections. They can test for specific bacteria and check if you have a carrier state. Always change out of work clothes before eating and never eat in processing areas.', 'nhs.uk', 'https://www.nhs.uk/conditions/food-poisoning/'),
     ]),

    # === HEARING ===
    ('workers-health', 'The factory is very loud. At what point does noise damage my hearing?',
     'The machinery in my factory is extremely loud. I sometimes have ringing in my ears after my shift.',
     None,
     [('GOV.UK', 'Health', 'Under the Control of Noise at Work Regulations 2005, your employer must:\n\n- Assess noise levels in the workplace\n- Provide hearing protection if noise exceeds 80 dB (lower action level)\n- Make hearing protection mandatory above 85 dB (upper action level)\n- Provide health surveillance (hearing tests) for exposed workers\n- Reduce noise at source where possible\n\nRinging in your ears after a shift (tinnitus) is a WARNING sign of noise damage. This damage is permanent and cumulative.\n\nAlways wear hearing protection in noisy areas. If your employer is not providing it or not enforcing it, they are breaking the law. Report to HSE: 0300 003 1647.', 'gov.uk', 'https://www.hse.gov.uk/noise/'),
      ('CDC', 'Official', 'The US CDC reports that approximately 22 million American workers are exposed to hazardous noise levels annually. NIOSH recommends an exposure limit of 85 dB for 8 hours. For every 3 dB increase above this, the safe exposure time halves. At 88 dB, safe exposure is only 4 hours. At 91 dB, only 2 hours.', 'cdc.gov', 'https://www.cdc.gov/niosh/topics/noise/'),
     ]),

    # === FATIGUE ===
    ('workers-health', 'Is it legal to work 12-hour shifts 6 days a week?',
     'My factory makes us work 12 hours a day, 6 days a week during peak season. I am exhausted but scared to say no.',
     None,
     [('GOV.UK', 'Health', 'Under the Working Time Regulations 1998:\n\n- Maximum average working week: 48 hours (averaged over 17 weeks)\n- You CAN opt out of the 48-hour limit voluntarily, but it must be in writing and you can opt back in with 7 days notice\n- You are entitled to 11 consecutive hours rest between shifts\n- You are entitled to one day off per week (or 2 days per fortnight)\n- You are entitled to a 20-minute rest break if working 6+ hours\n\n72 hours per week exceeds the limit unless you signed an opt-out. Even with an opt-out, your employer has a duty of care to prevent fatigue-related health risks and accidents.\n\nIf you feel pressured to work excessive hours, contact ACAS: 0300 123 1100.', 'gov.uk', 'https://www.gov.uk/maximum-weekly-working-hours'),
     ]),

    # === IMMIGRANT WORKER SPECIFIC ===
    ('workers-health', 'Can I access the NHS if I am on a work visa in the UK?',
     'I am on a Skilled Worker visa. Do I have to pay to see a GP? I am scared to use the NHS in case it affects my visa.',
     None,
     [('NHS', 'Official', 'If you are living and working legally in the UK (including Skilled Worker visa, Student visa, PSW visa, or any visa where you paid the Immigration Health Surcharge), you are entitled to FULL NHS services including:\n\n- GP registration and appointments (FREE)\n- Hospital treatment (FREE)\n- A&E treatment (FREE for everyone, regardless of immigration status)\n- Mental health services (FREE)\n- Prescriptions (with valid exemption or 9.90 per item)\n\nUsing the NHS will NOT affect your visa status. Your health data is not shared with the Home Office. Please register with a local GP — you do not need proof of address or immigration documents to register.', 'nhs.uk', 'https://www.nhs.uk/nhs-services/visiting-or-moving-to-england/how-to-access-nhs-services-in-england/'),
     ]),

    ('workers-health', 'What should I do if I have a workplace accident but my employer says not to report it?',
     'I fell on a wet floor at the factory and injured my knee. My supervisor told me not to report it officially.',
     None,
     [('GOV.UK', 'Health', 'Your employer is BREAKING THE LAW. Under RIDDOR (Reporting of Injuries, Diseases and Dangerous Occurrences Regulations 2013), employers MUST report:\n\n- Fractures (other than fingers, thumbs, toes)\n- Injuries causing more than 7 days off work\n- Hospital admissions\n- Specified injuries (amputations, loss of sight, etc.)\n\nYou should:\n1. Report the accident in the workplace accident book (your employer must have one)\n2. Take photos of the hazard (wet floor)\n3. Get witness names\n4. See a doctor and keep records\n5. Report to HSE yourself if your employer refuses: 0300 003 1647\n\nYou are legally protected from dismissal for reporting health and safety concerns under the Employment Rights Act 1996.', 'gov.uk', 'https://www.hse.gov.uk/riddor/'),
     ]),

    # === HEAT STRESS ===
    ('workers-health', 'How do I deal with extreme heat in a factory with no air conditioning?',
     'Our factory has ovens and fryers running constantly. In summer the temperature reaches 40°C on the production floor. I feel dizzy and sick.',
     None,
     [('GOV.UK', 'Health', 'While there is no maximum workplace temperature in UK law, your employer has a legal duty under the Workplace (Health, Safety and Welfare) Regulations 1992 to provide a reasonable temperature. For hot environments, employers must:\n\n- Provide fans or local cooling\n- Ensure adequate ventilation\n- Provide free cold drinking water\n- Allow rest breaks in cool areas\n- Adjust work schedules to avoid peak heat\n- Provide lightweight, breathable workwear\n\nHeat stress can cause heat exhaustion and heatstroke, which is a medical emergency. Symptoms include confusion, hot dry skin, and loss of consciousness — call 999 immediately.', 'gov.uk', 'https://www.hse.gov.uk/temperature/employer/index.htm'),
      ('Emily', 'Chen', 'I worked in a bakery factory with similar conditions. What saved me: I froze a flannel overnight and wore it round my neck during shifts. Drank a glass of water every 30 minutes, not just when thirsty. Also, electrolyte tablets from the chemist help replace the salts you lose from sweating. If your employer is ignoring the heat, put it in writing and copy your union rep if you have one.', None, None),
     ]),

    # === VIBRATION INJURIES ===
    ('workers-health', 'My hands tingle and go numb after using power tools all day. Is this serious?',
     'I use a pneumatic impact wrench and angle grinder for 6-8 hours a day in an engineering factory. My fingers tingle at night and I am losing grip strength.',
     None,
     [('GOV.UK', 'Health', 'This sounds like Hand-Arm Vibration Syndrome (HAVS), a serious and permanent condition caused by regular use of vibrating tools. Under the Control of Vibration at Work Regulations 2005, your employer must:\n\n- Assess vibration exposure levels\n- Provide low-vibration tools where possible\n- Limit daily exposure time\n- Provide health surveillance (annual checks)\n- Rotate tasks to reduce continuous exposure\n\nHAVS is irreversible once advanced. Early symptoms include tingling, numbness, and white finger attacks. See your GP urgently and tell them about your vibration exposure at work. This is a reportable industrial disease.', 'gov.uk', 'https://www.hse.gov.uk/vibration/hav/'),
      ('Dr Sarah', 'Mitchell', 'Do not ignore this. The tingling and numbness you describe are early-stage HAVS symptoms. If left untreated, you risk permanent nerve damage and loss of hand function. Your GP can refer you to occupational health for a formal HAVS assessment. In the meantime, keep your hands warm, avoid smoking (it worsens circulation), and report your symptoms to your employer in writing.', None, None),
     ]),

    # === DUST & LUNG DISEASE ===
    ('workers-health', 'I cough up dust after every shift in the woodworking factory. Can this cause long-term damage?',
     'I work cutting MDF and plywood all day. There is sawdust everywhere and the extraction system is broken. I cough constantly.',
     None,
     [('GOV.UK', 'Health', 'Wood dust is a serious health hazard. Hardwood dust is classified as a Group 1 carcinogen (causes cancer in humans). Under COSHH regulations, your employer MUST:\n\n- Provide effective dust extraction at source (LEV systems)\n- Maintain extraction equipment in working order\n- Provide RPE (respiratory protective equipment) as a secondary measure\n- Monitor dust exposure levels\n- Provide health surveillance for exposed workers\n\nA broken extraction system is a serious legal breach. Report this to HSE immediately: 0300 003 1647. Long-term wood dust exposure can cause occupational asthma, chronic obstructive pulmonary disease (COPD), and nasal cancer.', 'gov.uk', 'https://www.hse.gov.uk/woodworking/health-risks.htm'),
     ]),

    # === FORKLIFT & VEHICLE SAFETY ===
    ('workers-health', 'I drive a forklift 8 hours a day and my whole body vibrates. What health risks does this cause?',
     'I am a full-time forklift operator in a warehouse. My lower back aches constantly and I get pins and needles in my legs.',
     None,
     [('GOV.UK', 'Health', 'Whole-body vibration (WBV) from driving forklifts, dump trucks, or tractors can cause:\n\n- Lower back pain and spinal damage\n- Sciatica-like symptoms (leg numbness, pins and needles)\n- Digestive problems\n- Damage to spinal discs\n\nUnder the Control of Vibration at Work Regulations 2005, your employer must assess whole-body vibration exposure, maintain seats and suspension on vehicles, provide training on correct seating position, limit continuous driving time, and provide health surveillance. Ask your employer to check the seat suspension and replace it if worn out.', 'gov.uk', 'https://www.hse.gov.uk/vibration/wbv/'),
      ('Ahmed', 'Malik', 'I drove a forklift for 4 years and had the same back pain. Three things that helped: 1) A proper air-suspension seat — insist your employer replaces the old seat, it is their legal obligation. 2) Get off the truck every hour and stretch. 3) Core strengthening exercises — planks and dead bugs twice a day. My physiotherapist said most forklift drivers have weak core muscles from sitting all day.', None, None),
     ]),

    # === SLIP AND TRIP HAZARDS ===
    ('workers-health', 'The floors in our factory are always wet and slippery. Three people have fallen this month.',
     'We work in a food processing plant and the floors are constantly wet from cleaning and spillages. People keep slipping. Management says it is our fault for not being careful.',
     None,
     [('GOV.UK', 'Health', 'Slips and trips are the most common cause of workplace injury in the UK, accounting for over a third of all major injuries. Management is WRONG to blame workers. Under the Health and Safety at Work Act 1974, your employer must:\n\n- Keep floors in good condition and free from obstructions\n- Provide effective drainage in wet areas\n- Use anti-slip floor coatings or matting\n- Provide non-slip safety footwear\n- Clean spills immediately\n- Use appropriate warning signs\n\nThree falls in one month is a pattern that indicates systemic failure. Report to HSE: 0300 003 1647. Each injured worker should document their injury in the accident book.', 'gov.uk', 'https://www.hse.gov.uk/slips/'),
     ]),

    # === MUSCULOSKELETAL - SHOULDERS ===
    ('workers-health', 'My shoulder is agony from reaching above my head on the production line all day.',
     'I work on an overhead conveyor line loading products onto hooks. I reach above shoulder height hundreds of times per shift. My right shoulder is now in constant pain.',
     None,
     [('Dr Sarah', 'Mitchell', 'Repeated overhead reaching is one of the highest-risk movements for shoulder injury. You may have developed shoulder impingement, rotator cuff tendinitis, or a rotator cuff tear. See your GP urgently — they can examine your shoulder and may refer you for an ultrasound or MRI.\n\nIn the meantime:\n- Do NOT push through the pain as it will worsen\n- Apply ice for 15 minutes after each shift\n- Ask your employer to adjust the conveyor height or rotate you to a different task\n\nYour employer must conduct a workstation ergonomic assessment under the Manual Handling Operations Regulations 1992. Repeated overhead reaching without mitigation is a failure of their duty of care.', None, None),
      ('WHO', 'Official', 'The World Health Organization estimates that work-related musculoskeletal disorders account for 70 million disability-adjusted life years (DALYs) globally. Overhead work is a recognised high-risk ergonomic posture. WHO recommends job rotation, mechanical aids, adjustable work heights, and regular rest breaks to prevent upper limb disorders.', 'who.int', 'https://www.who.int/news-room/fact-sheets/detail/musculoskeletal-conditions'),
     ]),

    # === STRESS IN AGENCY WORKERS ===
    ('workers-health', 'I am an agency worker and feel like I have no rights. Can I refuse unsafe work?',
     'I work through an agency at different factories. I am often asked to operate machines I have not been trained on. I am scared to say no because they will just replace me.',
     None,
     [('GOV.UK', 'Health', 'Agency workers have the SAME health and safety protections as permanent staff. Under the Health and Safety at Work Act 1974:\n\n- You must receive adequate training before operating any machinery\n- You can refuse work you believe is dangerous without facing retaliation\n- Both the agency AND the host employer share responsibility for your safety\n- You must be provided with appropriate PPE\n\nIf you are asked to do something unsafe, say: "I have not been trained on this and I am not comfortable operating it until I have." Put it in writing to both your agency and the factory manager. If they penalise you for this, contact ACAS: 0300 123 1100 or HSE: 0300 003 1647.', 'gov.uk', 'https://www.gov.uk/agency-workers-your-rights'),
     ]),

    # === EYE INJURIES ===
    ('workers-health', 'I got metal fragments in my eye at work. My employer did not provide safety glasses.',
     'I was using a grinding wheel and a small piece of metal flew into my eye. It was extremely painful and I had to go to A&E. My employer has never provided eye protection.',
     None,
     [('NHS', 'Official', 'A foreign body in the eye from grinding or cutting metal is a medical emergency. Metal fragments can rust in the eye within hours and cause permanent scarring if not removed properly. NEVER rub the eye or try to remove metal yourself.\n\nGo straight to A&E or an eye casualty unit where they can:\n- Examine with a slit lamp\n- Remove the fragment safely\n- Check for corneal damage\n- Prescribe antibiotic drops to prevent infection\n\nKeep a record of the incident for a potential workplace injury claim.', 'nhs.uk', 'https://www.nhs.uk/conditions/minor-eye-injuries/'),
      ('GOV.UK', 'Health', 'Your employer has broken the law. Under the Personal Protective Equipment at Work Regulations 1992, safety goggles or glasses must be provided free of charge for any task involving flying particles, sparks, or dust. This includes grinding, cutting, drilling, and welding. Report this to HSE immediately. You may also be entitled to compensation for your injury.', 'gov.uk', 'https://www.hse.gov.uk/toolbox/ppe.htm'),
     ]),

    # === PREGNANCY IN THE WORKPLACE ===
    ('workers-health', 'I am pregnant and work in a factory. What are my rights?',
     'I am 14 weeks pregnant and work on a production line that involves heavy lifting and standing for 10 hours. My employer says I should just get on with it.',
     None,
     [('GOV.UK', 'Health', 'Your employer is REQUIRED by law to protect pregnant workers. Under the Management of Health and Safety at Work Regulations 1999, once you notify your employer in writing that you are pregnant, they must:\n\n- Conduct a specific risk assessment for your role\n- Remove or reduce risks (heavy lifting, prolonged standing, chemical exposure, excessive heat)\n- Offer alternative suitable work on the same pay if risks cannot be removed\n- Suspend you on full pay if no suitable alternative exists\n\nYou are also entitled to paid time off for antenatal appointments. It is automatically unfair dismissal to sack someone for being pregnant.', 'gov.uk', 'https://www.gov.uk/working-when-pregnant-your-rights'),
      ('NHS', 'Official', 'During pregnancy, you should avoid heavy lifting, prolonged standing (increases risk of varicose veins and pre-term labour), exposure to chemicals and biological agents, and excessive heat. Speak to your midwife about your working conditions at your next appointment. They can write to your employer if adjustments are needed.', 'nhs.uk', 'https://www.nhs.uk/pregnancy/keeping-well/your-health-at-work/'),
     ]),

    # === NIGHT SHIFT EATING ===
    ('workers-health', 'What should I eat on night shifts to stay healthy?',
     'I work 10pm to 6am and end up eating junk food from the vending machine. I have gained 2 stone since starting nights.',
     None,
     [('Dr Sarah', 'Mitchell', 'Night shift weight gain is extremely common because your body clock affects digestion and metabolism. Practical tips:\n\n1. Eat your main meal BEFORE your shift starts (around 7-8pm)\n2. During the shift, eat small, light snacks — nuts, fruit, yoghurt, wholegrain crackers\n3. Avoid heavy meals between midnight and 4am (your digestion is slowest)\n4. Bring food from home — vending machines are a trap\n5. Stay hydrated with water, not sugary energy drinks\n6. When you get home, have a light snack (toast, banana) before sleeping\n\nAvoid large caffeine doses after 3am as it will disrupt your daytime sleep.', None, None),
      ('Emily', 'Chen', 'Meal prepping on my days off was the biggest change for me. I batch cook chicken stir-fry, pasta salads, and soups on Sunday. I portion them into containers for the week. Saves money, stops me eating rubbish, and I lost the weight I gained within 4 months.', None, None),
     ]),

    # === BULLYING AT WORK ===
    ('workers-health', 'My line manager bullies me constantly. I feel sick every morning before work.',
     'My manager shouts at me in front of others, gives me the worst jobs, and mocks my accent. I am from Romania and feel targeted.',
     None,
     [('GOV.UK', 'Health', 'Workplace bullying and harassment are unacceptable and may be illegal. If the behaviour targets your nationality or accent, this could constitute racial harassment under the Equality Act 2010. Your employer has a legal duty to prevent harassment.\n\nSteps to take:\n1. Keep a written diary of every incident (date, time, what was said, witnesses)\n2. Report to HR or a more senior manager in writing\n3. If your employer does not act, contact ACAS: 0300 123 1100\n4. You can make a claim to an Employment Tribunal within 3 months of the incident\n\nFree support: Equality Advisory Support Service (EASS): 0808 800 0082.', 'gov.uk', 'https://www.gov.uk/workplace-bullying-and-harassment'),
      ('NHS', 'Official', 'The physical symptoms you describe — feeling sick before work — are a stress response and should be taken seriously. Workplace bullying can cause anxiety, depression, post-traumatic stress, and physical symptoms like headaches, stomach problems, and insomnia. See your GP for support. You can also self-refer to NHS talking therapies for free.', 'nhs.uk', 'https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/stress/'),
     ]),

    # === FIRST AID RIGHTS ===
    ('workers-health', 'There is no first aider on our shift. Is this legal?',
     'I work nights and there are 40 of us in the factory but no trained first aider. Last week someone fainted and nobody knew what to do.',
     None,
     [('GOV.UK', 'Health', 'This is a legal requirement your employer is failing to meet. Under the Health and Safety (First-Aid) Regulations 1981, employers MUST provide:\n\n- Adequate first aid equipment and facilities\n- An appropriate number of trained first aiders (based on workplace risk and number of employees)\n- A first aider present at all times during working hours\n\nFor a higher-risk workplace like a factory with 40+ workers, there should be at least 1 trained first aider per shift. A first aid needs assessment must be carried out. Report this to HSE: 0300 003 1647.', 'gov.uk', 'https://www.hse.gov.uk/firstaid/'),
     ]),

    # === DEHYDRATION ===
    ('workers-health', 'My employer locks the water fountain during shifts to prevent people wasting time.',
     'We are only allowed water during our 2 breaks (15 min each). In a hot factory with physical work, this feels dangerous.',
     None,
     [('GOV.UK', 'Health', 'This is ILLEGAL. Under the Workplace (Health, Safety and Welfare) Regulations 1992, Regulation 22, your employer MUST provide an adequate supply of wholesome drinking water, readily accessible at all times, at suitable and clearly marked locations.\n\nRestricting water access during physical work in a hot environment is extremely dangerous and could lead to dehydration, heat exhaustion, kidney damage, and even heatstroke. Report this immediately to HSE: 0300 003 1647. You can report anonymously.', 'gov.uk', 'https://www.hse.gov.uk/temperature/employer/index.htm'),
      ('NHS', 'Official', 'Dehydration during physical work can cause headaches, dizziness, confusion, dark urine, fatigue, and in severe cases, heatstroke. Adults should drink at least 6-8 glasses of water per day, more during physical activity or in hot environments. Signs of dehydration include dark yellow urine, feeling thirsty, tired, dizzy, dry mouth, and passing urine less than 4 times a day.', 'nhs.uk', 'https://www.nhs.uk/conditions/dehydration/'),
     ]),

    # === ZERO HOURS CONTRACTS ===
    ('workers-health', 'Can my employer cut my hours to zero because I complained about safety?',
     'Since I raised concerns about broken machinery, my employer has stopped giving me shifts. I am on a zero-hours contract.',
     None,
     [('GOV.UK', 'Health', 'What you are describing is likely unlawful detriment for raising health and safety concerns. Under Section 44 of the Employment Rights Act 1996, workers are protected from being subjected to any detriment (including loss of shifts) for raising legitimate health and safety concerns.\n\nThis protection applies regardless of your employment status or contract type, including zero-hours contracts. You can bring a claim to an Employment Tribunal. You do NOT need 2 years service for this type of claim.\n\nContact ACAS immediately: 0300 123 1100. Also report the broken machinery to HSE: 0300 003 1647.', 'gov.uk', 'https://www.gov.uk/raise-grievance-at-work'),
     ]),
]


# Pre-written AI summaries keyed by question title (first 40 chars)
AI_SUMMARIES = {
    'How do I prevent back pain from lifting': 'Based on NHS and WHO guidance, here are the key steps to protect your back:\n\n1. Always lift with your knees bent, keeping the load close to your waist\n2. Never twist while carrying — turn with your feet instead\n3. Ask for help with loads over 25kg and request mechanical aids\n4. Take a 2-minute break every 30 minutes to stretch\n5. Your employer must provide manual handling training by law\n\nIf pain persists, see your GP for a physiotherapy referral. Keeping a symptom diary will help them assess your condition.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'Is it normal to have back pain at 25 fr': 'No, chronic back pain at 25 is not normal and should not be accepted as part of the job. Here is what to do:\n\n1. Book a GP appointment — ask for physiotherapy and a possible occupational health referral\n2. Report the problem to your employer in writing (email is best for records)\n3. Request a manual handling risk assessment for your role\n4. If your employer ignores you, contact HSE on 0300 003 1647\n5. Keep a daily diary of pain levels and what tasks trigger it\n\nYou may be entitled to compensation if your employer failed to manage risks properly.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'Can working in a cold room (0-4°C) all': 'Yes, prolonged cold exposure can cause real health problems. Key points:\n\n1. Raynaud\'s phenomenon, chilblains, and hypothermia are all risks\n2. Your employer must provide thermal PPE (jacket, gloves, warm boots) and hot drinks\n3. You are entitled to regular warm-up breaks\n4. Report numbness, headaches, or white/blue fingers to your GP\n5. HSE guidance requires employers to take reasonable steps even though there is no legal minimum temperature for cold storage\n\nIf your employer is not providing adequate protection, report to HSE: 0300 003 1647.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'My fingers turn white and numb in the c': 'Your symptoms strongly suggest Raynaud\'s phenomenon — this is NOT normal despite what your supervisor says. Take action:\n\n1. See your GP urgently — Raynaud\'s needs proper diagnosis\n2. Report the issue to your employer in writing\n3. Request thermal gloves and scheduled warm-up breaks\n4. Avoid caffeine before cold room shifts as it restricts blood flow\n5. If fingers stay blue or you develop sores, go to A&E\n\nYour employer has a duty to protect you from cold-related health risks.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'I have constant wrist pain from packing': 'Your symptoms are consistent with RSI (Repetitive Strain Injury). Here is what to do:\n\n1. See your GP — they can diagnose RSI and refer you for physiotherapy\n2. Rest the affected area as much as possible outside work\n3. Apply ice and consider anti-inflammatory painkillers\n4. Ask your employer for task rotation, ergonomic tools, and regular breaks\n5. A wrist splint worn at night can help reduce symptoms\n\nYour employer has a legal duty under the Health and Safety at Work Act 1974 to prevent RSI through proper workplace design.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'My hands are cracked and bleeding from': 'Occupational contact dermatitis is common in food processing. Practical steps:\n\n1. Apply emollient moisturiser (Doublebase, Cetraben, or E45) after every hand wash\n2. Request non-latex, powder-free nitrile gloves from your employer\n3. Use lukewarm water and pat dry gently\n4. Apply barrier cream before starting work\n5. See your GP if skin is red, hot, or weeping — this could indicate infection\n\nYour employer must provide suitable PPE including appropriate gloves.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'Can cleaning chemicals at work damage m': 'Chemical exposure at work is regulated by COSHH. Your employer must:\n\n1. Provide Safety Data Sheets for all chemicals\n2. Give you chemical-resistant gloves (not just standard ones)\n3. Ensure proper ventilation where chemicals are used\n4. Train you on safe handling procedures\n5. Provide emergency wash facilities\n\nIf you are getting headaches and burns through gloves, the PPE is inadequate. Report to your employer in writing first, then HSE (0300 003 1647) if they do not act.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'How do I cope with rotating shift patte': 'Shift work disrupts your body clock. Evidence-based tips:\n\n1. Use blackout curtains for daytime sleeping\n2. Keep a consistent routine even on days off\n3. Avoid caffeine 6 hours before sleep\n4. Take a 20-30 minute nap before night shifts\n5. Use bright light exposure at the start of your shift\n6. Eat small, regular meals instead of one large meal\n\nIf sleep problems persist beyond 3 months, see your GP — chronic sleep disruption increases risk of heart disease and depression.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'My feet and legs hurt from standing on': 'Prolonged standing on hard floors is a common factory issue. Try these:\n\n1. Anti-fatigue insoles (around 10 pounds from a pharmacy)\n2. Compression socks to reduce swelling and improve circulation\n3. Ask your employer for anti-fatigue mats — HSE recommends them\n4. Stretch your calves during every break\n5. Elevate your feet for 15 minutes when you get home\n6. Request seating for rest breaks\n\nYour employer should provide anti-fatigue mats for static standing positions.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'I feel isolated working in a factory wh': 'Language barriers and isolation at work are serious wellbeing issues. Here is what can help:\n\n1. Learn a few key phrases in the main language spoken at your workplace\n2. Look for local community groups or cultural centres\n3. Use break times to stay connected with family and friends\n4. Ask your employer about buddy systems for new workers\n5. Free support: Migrant Help (0808 8010 503), Samaritans (116 123)\n\nLoneliness does improve with time — it often takes 6 months to build workplace friendships.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'Night shifts are making me depressed. I': 'Night shift depression is a recognised condition caused by lack of sunlight. Steps to take:\n\n1. Get outside in daylight on your days off, even briefly\n2. Use a SAD lamp (10,000 lux) for 30 minutes when you wake up\n3. Take vitamin D supplements — night workers are often severely deficient\n4. Exercise daily, even a 20-minute walk helps\n5. Talk to your GP — they can screen for depression and discuss treatment\n6. Ask about rotating shifts rather than permanent nights\n\nYou are not weak for struggling with this. Seek help early.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'What are my rights to sick pay if I am': 'Your employer is wrong. Key facts about sick pay:\n\n1. ALL workers including zero-hours contracts are entitled to SSP\n2. You must earn at least 123 pounds per week on average\n3. SSP is 116.75 pounds per week for up to 28 weeks\n4. If your employer refuses, contact HMRC: 0300 200 3500\n5. If your injury was caused by employer negligence, you may claim compensation\n6. Contact Citizens Advice (0800 144 8848) for free legal guidance\n\nKeep all medical records and correspondence with your employer.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'Can my employer sack me for being off s': 'Your employer cannot dismiss you simply for being off sick. Key protections:\n\n1. Dismissal during sick leave can be unfair dismissal (if 2+ years service)\n2. Work-related injuries may qualify as disability under the Equality Act 2010\n3. Your employer must make reasonable adjustments\n4. Keep ALL communications in writing\n5. Contact ACAS (0300 123 1100) or Citizens Advice (0800 144 8848) for free advice\n\nDo not resign under pressure. Get legal advice first.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'My employer does not provide safety glo': 'This is illegal. Under the PPE at Work Regulations 1992:\n\n1. Your employer must provide cut-resistant gloves free of charge\n2. All PPE must be maintained and replaced when worn\n3. You must be trained on proper PPE use\n4. Report to HSE: 0300 003 1647 (you can report anonymously)\n5. You are legally protected from retaliation for raising safety concerns\n6. You may be entitled to compensation for your injuries\n\nDocument every incident in the accident book.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'Can working in cold rooms cause breathi': 'Yes, cold air can trigger respiratory problems. You should:\n\n1. See your GP urgently — mention your cold room work environment\n2. Note whether symptoms improve on days off (this helps diagnosis)\n3. Tell your GP about any chemicals or fish proteins you are exposed to\n4. Request an occupational health referral\n5. Occupational asthma is a reportable industrial disease\n\nYour employer should provide respiratory protection and adequate warm-up breaks.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'I keep getting stomach bugs. Could it b': 'Frequent stomach infections from handling raw food are concerning. Key steps:\n\n1. Ensure you wash hands for 20+ seconds with soap every time\n2. Change out of work clothes before eating or going home\n3. Never eat in food processing areas\n4. See your GP for testing if infections occur monthly\n5. Your employer should ensure shared facilities are properly cleaned\n\nYour GP can test for specific bacteria and check for a carrier state.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'The factory is very loud. At what point': 'Ringing ears after a shift (tinnitus) is a warning sign of permanent hearing damage. Key facts:\n\n1. Your employer must provide hearing protection above 80 dB\n2. Protection is mandatory above 85 dB\n3. Safe exposure halves for every 3 dB increase (88 dB = 4 hours, 91 dB = 2 hours)\n4. Always wear hearing protection in noisy areas\n5. Your employer must provide annual hearing tests for exposed workers\n6. Report failures to HSE: 0300 003 1647\n\nHearing damage is permanent and cumulative. Do not ignore tinnitus.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'Is it legal to work 12-hour shifts 6 da': '72 hours per week exceeds the legal limit unless you opted out in writing. Your rights:\n\n1. Maximum average is 48 hours per week (over 17 weeks)\n2. You can opt back in to the 48-hour limit with 7 days notice\n3. You are entitled to 11 hours rest between shifts\n4. You are entitled to 1 day off per week\n5. You must get a 20-minute break for shifts over 6 hours\n6. Contact ACAS (0300 123 1100) if pressured to work excessive hours\n\nEven with an opt-out, your employer must manage fatigue-related risks.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'Can I access the NHS if I am on a work': 'Yes, you are entitled to full NHS services. Here is what you need to know:\n\n1. GP registration and appointments are FREE\n2. Hospital treatment is FREE\n3. A&E is FREE for everyone regardless of immigration status\n4. Mental health services are FREE\n5. Using the NHS will NOT affect your visa status\n6. Your health data is NOT shared with the Home Office\n\nRegister with a local GP — you do not need proof of address to register.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'What should I do if I have a workplace': 'Your employer is breaking the law by telling you not to report. Take these steps:\n\n1. Write the accident in the workplace accident book yourself\n2. Take photos of the hazard\n3. Get names of any witnesses\n4. See a doctor and keep all records\n5. Report to HSE if your employer refuses: 0300 003 1647\n6. You are legally protected from dismissal for reporting safety concerns\n\nUnder RIDDOR, employers must report serious injuries to the HSE.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'How do I deal with extreme heat in a fa': 'Heat stress at work is dangerous. Here is what to do:\n\n1. Drink water every 30 minutes, not just when thirsty\n2. Use electrolyte tablets to replace lost salts\n3. Request fans, ventilation, and cool rest areas from your employer\n4. Wear lightweight, breathable clothing\n5. Know the signs of heatstroke: confusion, hot dry skin — call 999\n6. Put concerns in writing to your employer\n\nYour employer must provide a reasonable temperature under workplace regulations.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'My hands tingle and go numb after using': 'These are early symptoms of HAVS (Hand-Arm Vibration Syndrome), a serious condition. Act now:\n\n1. See your GP urgently and tell them about your vibration exposure\n2. Report symptoms to your employer in writing\n3. Request low-vibration tools and task rotation\n4. Keep hands warm and avoid smoking\n5. Your employer must limit daily vibration exposure by law\n6. HAVS is irreversible once advanced — early action is critical\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'I cough up dust after every shift in th': 'Wood dust is a serious carcinogen. Take immediate action:\n\n1. Report the broken extraction system to HSE: 0300 003 1647\n2. Request respiratory protective equipment (RPE) from your employer\n3. See your GP about your persistent cough\n4. Your employer is legally required to maintain dust extraction under COSHH\n5. Long-term exposure can cause occupational asthma, COPD, and nasal cancer\n\nDo not wait — this is a serious health risk.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'I drive a forklift 8 hours a day and my': 'Whole-body vibration from forklifts can cause spinal damage. Steps to take:\n\n1. Ask your employer to check and replace worn seat suspension\n2. Get off the truck every hour and stretch\n3. Strengthen your core with exercises like planks\n4. See your GP if back pain or leg numbness persists\n5. Your employer must assess vibration exposure and provide health surveillance\n\nAn air-suspension seat can significantly reduce vibration exposure.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'The floors in our factory are always we': 'Three falls in one month indicates a systemic problem, not worker carelessness. Actions:\n\n1. Report to HSE: 0300 003 1647\n2. Each injured worker should record their injury in the accident book\n3. Your employer must provide anti-slip flooring, drainage, and safety footwear\n4. Take photos of hazardous conditions as evidence\n5. Slips and trips cause over a third of all major workplace injuries in the UK\n\nManagement cannot legally blame workers for what are employer responsibilities.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'My shoulder is agony from reaching abov': 'Repeated overhead reaching is a high-risk movement. What to do:\n\n1. See your GP urgently — you may need an ultrasound or MRI\n2. Do NOT push through the pain\n3. Apply ice for 15 minutes after each shift\n4. Ask your employer to adjust the conveyor height or rotate you to different tasks\n5. Your employer must conduct an ergonomic assessment of your workstation\n\nShoulder injuries can become chronic without proper treatment.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'I am an agency worker and feel like I h': 'Agency workers have the SAME health and safety protections as permanent staff. Remember:\n\n1. You must receive training before operating any machinery\n2. You can legally refuse unsafe work\n3. Both your agency and the host employer share responsibility for your safety\n4. You must be provided with PPE\n5. If penalised for raising safety concerns, contact ACAS: 0300 123 1100\n\nPut any concerns in writing to both your agency and the factory.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'I got metal fragments in my eye at work': 'A metal foreign body in the eye is a medical emergency. Key points:\n\n1. Go to A&E immediately — do NOT rub or try to remove the metal\n2. Metal can rust in the eye within hours causing permanent damage\n3. Your employer broke the law by not providing safety goggles\n4. Report to HSE and document everything for a potential injury claim\n5. Safety goggles are required PPE for grinding, cutting, and drilling\n\nKeep all medical records from your A&E visit.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'I am pregnant and work in a factory. Wh': 'Your employer is legally required to protect you during pregnancy. Your rights:\n\n1. A specific risk assessment must be done for your role\n2. Heavy lifting and prolonged standing risks must be removed\n3. You must be offered alternative work on the same pay\n4. If no safe alternative exists, you must be suspended on full pay\n5. You are entitled to paid time off for antenatal appointments\n6. It is automatically unfair dismissal to sack someone for being pregnant\n\nNotify your employer in writing that you are pregnant to trigger these protections.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'What should I eat on night shifts to st': 'Night shift nutrition is important for your health and weight. Tips:\n\n1. Eat your main meal before your shift (around 7-8pm)\n2. During shifts, eat light snacks: nuts, fruit, yoghurt\n3. Avoid heavy meals between midnight and 4am\n4. Bring food from home instead of relying on vending machines\n5. Stay hydrated with water, avoid sugary energy drinks\n6. Meal prep on days off to save time and money\n\nAvoid caffeine after 3am to protect your daytime sleep.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'My line manager bullies me constantly.': 'Workplace bullying targeting your nationality or accent may be racial harassment under the Equality Act 2010. Take action:\n\n1. Keep a written diary of every incident with dates, times, and witnesses\n2. Report to HR or a senior manager in writing\n3. Contact ACAS: 0300 123 1100 for free advice\n4. You can make an Employment Tribunal claim within 3 months\n5. See your GP about the physical symptoms of stress\n6. Free support: EASS: 0808 800 0082\n\nYour employer has a legal duty to prevent harassment.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'There is no first aider on our shift. I': 'This is a legal breach. Your employer must provide:\n\n1. Trained first aiders on every shift\n2. For 40+ workers in a higher-risk workplace, at least 1 first aider per shift\n3. Adequate first aid equipment and facilities\n4. A completed first aid needs assessment\n\nReport this to HSE: 0300 003 1647. In an emergency, always call 999.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'My employer locks the water fountain du': 'Restricting water access at work is ILLEGAL. Key facts:\n\n1. Employers must provide drinking water accessible at all times (Regulation 22)\n2. Restricting water during physical work is extremely dangerous\n3. Dehydration can cause heat exhaustion, kidney damage, and heatstroke\n4. Report immediately to HSE: 0300 003 1647 (anonymous reporting available)\n5. Signs of dehydration: dark urine, dizziness, confusion, headaches\n\nThis is a serious health and safety breach.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',

    'Can my employer cut my hours to zero be': 'What you describe is likely unlawful detriment. Your protections:\n\n1. Section 44 of the Employment Rights Act 1996 protects workers who raise safety concerns\n2. This applies to ALL contract types including zero-hours\n3. You do NOT need 2 years service to bring this claim\n4. Contact ACAS immediately: 0300 123 1100\n5. Also report the broken machinery to HSE: 0300 003 1647\n\nKeep records of your shift patterns before and after the complaint.\n\nPlease note: this is general health information, not a substitute for professional medical advice.',
}


def _generate_ai_summary(title, body, answers_data):
    """Generate AI response: try Gemini API first, fall back to pre-written summaries."""
    # Try Gemini API first
    gemini_response = _generate_ai_with_gemini(title, body, answers_data)
    if gemini_response:
        # Add disclaimer if not already present
        if 'not a substitute' not in gemini_response:
            gemini_response += '\n\nPlease note: this is general health information, not a substitute for professional medical advice.'
        print(f'    [Gemini] Generated AI response for: {title[:50]}...')
        time.sleep(1)  # Rate limit
        return gemini_response

    # Fall back to pre-written summaries
    key = title[:40]
    if key in AI_SUMMARIES:
        print(f'    [Fallback] Using pre-written AI response for: {title[:50]}...')
        return AI_SUMMARIES[key]

    # Generic fallback
    print(f'    [Generic] Using generic AI response for: {title[:50]}...')
    return (
        'This is an important workplace health question. Based on the information above, '
        'we recommend speaking with your GP if you have health concerns and contacting '
        'HSE (0300 003 1647) if your employer is not meeting their legal obligations. '
        'Keep written records of all incidents and communications.\n\n'
        'Please note: this is general health information, not a substitute for professional medical advice.'
    )


def seed():
    app = create_app()
    with app.app_context():
        # Ensure category exists
        cat = Category.query.filter_by(slug='workers-health').first()
        if not cat:
            cat = Category(
                name='Workers Health',
                slug='workers-health',
                description='Health guidance for factory workers, food processors, and manual labourers',
                icon='fa-hard-hat'
            )
            db.session.add(cat)
            db.session.commit()
            print('  + Workers Health category created')

        # Get/create source users
        source_users = {}
        sources = [
            ('NHS', 'Official', 'nhs@mediask.org'),
            ('GOV.UK', 'Health', 'govuk@mediask.org'),
            ('WHO', 'Official', 'who@mediask.org'),
            ('CDC', 'Official', 'cdc@mediask.org'),
            ('Dr Sarah', 'Mitchell', 'sarah.m@mediask.org'),
            ('Emily', 'Chen', 'emily.c@mediask.org'),
            ('Ahmed', 'Malik', 'ahmed.m@mediask.org'),
            ('MediAsk', 'AI', 'ai@mediask.org'),
        ]
        for first, last, email in sources:
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    first_name=first, last_name=last, email=email,
                    is_system_account=(first in ('NHS', 'GOV.UK', 'WHO', 'CDC'))
                )
                user.set_password('seed-user-no-login')
                db.session.add(user)
                db.session.flush()
            source_users[f'{first} {last}'] = user
        db.session.commit()

        # Seed Q&A
        categories = {c.slug: c for c in Category.query.all()}
        base_time = datetime.now(timezone.utc) - timedelta(days=45)
        q_count = a_count = 0

        for i, (cat_slug, title, body, source, answers_data) in enumerate(WORKERS_QA):
            cat = categories.get(cat_slug)
            if not cat:
                continue

            existing = Question.query.filter_by(title=title).first()
            if existing:
                continue

            author_name = random.choice(
                [k for k in source_users.keys()
                 if 'NHS' not in k and 'GOV' not in k and 'WHO' not in k and 'CDC' not in k and 'MediAsk' not in k]
            )
            author = source_users.get(author_name, list(source_users.values())[4])
            q_time = base_time + timedelta(days=i * 2, hours=random.randint(6, 22))

            question = Question(
                title=title, body=body,
                author_id=author.id, category_id=cat.id,
                source=source, view_count=random.randint(50, 800),
                created_at=q_time
            )
            db.session.add(question)
            db.session.flush()
            q_count += 1

            for j, (a_first, a_last, a_body, a_source, a_url) in enumerate(answers_data):
                a_name = f'{a_first} {a_last}'
                a_user = source_users.get(a_name, list(source_users.values())[4])

                if a_name == 'MediAsk AI':
                    auth_level = 'ai_assistant'
                elif a_source and 'nhs' in a_source:
                    auth_level = 'nhs_verified'
                elif a_source and ('gov' in a_source or 'hse' in a_source):
                    auth_level = 'govuk'
                elif a_source and ('who' in a_source or 'cdc' in a_source):
                    auth_level = 'nhs_verified'  # treat WHO/CDC as verified
                else:
                    auth_level = 'human_experience'

                answer = Answer(
                    body=a_body, question_id=question.id,
                    author_id=a_user.id, auth_level=auth_level,
                    source=a_source, source_url=a_url,
                    created_at=q_time + timedelta(hours=random.randint(1, 48))
                )
                db.session.add(answer)
                a_count += 1

            # Auto-generate AI summary answer for each question
            has_ai = any(f'{a[0]} {a[1]}' == 'MediAsk AI' for a in answers_data)
            if not has_ai:
                ai_user = source_users.get('MediAsk AI')
                if ai_user:
                    ai_body = _generate_ai_summary(title, body, answers_data)
                    ai_answer = Answer(
                        body=ai_body, question_id=question.id,
                        author_id=ai_user.id, auth_level='ai_assistant',
                        source='MediAsk AI', source_url=None,
                        created_at=q_time + timedelta(hours=random.randint(2, 72))
                    )
                    db.session.add(ai_answer)
                    a_count += 1

        db.session.commit()
        print(f'Workers Health: {q_count} questions, {a_count} answers created')


if __name__ == '__main__':
    seed()
