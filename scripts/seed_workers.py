"""Seed factory worker health Q&A with worldwide sources."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Question, Answer, Category
from datetime import datetime, timezone, timedelta
import random

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
]


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
                 if 'NHS' not in k and 'GOV' not in k and 'WHO' not in k and 'CDC' not in k]
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

                if a_source and 'nhs' in a_source:
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

        db.session.commit()
        print(f'Workers Health: {q_count} questions, {a_count} answers created')


if __name__ == '__main__':
    seed()
