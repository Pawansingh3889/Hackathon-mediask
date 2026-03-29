"""Seed the database with realistic health Q&A content."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Question, Answer, Category, Vote
from datetime import datetime, timezone, timedelta
import random
from scripts.extra_qa_data import EXTRA_QA_DATA

# System users who "posted" the content
SYSTEM_USERS = [
    ('NHS', 'Official', 'nhs@mediask.org', True, 'nhs.uk'),
    ('GOV.UK', 'Health', 'govuk@mediask.org', True, 'gov.uk'),
    ('Dr Sarah', 'Mitchell', 'sarah.m@mediask.org', False, None),
    ('James', 'Thornton', 'james.t@mediask.org', False, None),
    ('Priya', 'Sharma', 'priya.s@mediask.org', False, None),
    ('Michael', 'O\'Brien', 'michael.o@mediask.org', False, None),
    ('Emily', 'Chen', 'emily.c@mediask.org', False, None),
    ('David', 'Kapoor', 'david.k@mediask.org', False, None),
    ('Rachel', 'Hughes', 'rachel.h@mediask.org', False, None),
    ('Ahmed', 'Malik', 'ahmed.m@mediask.org', False, None),
]

# (category_slug, title, body, source, answers_list)
QA_DATA = [
    # ===== MENTAL HEALTH =====
    ('mental-health', 'What are the early signs of anxiety?',
     'I have been feeling constantly worried about small things and my heart races for no reason. Is this anxiety?',
     None,
     [
         ('NHS', 'Official', 'Common signs of anxiety include feeling restless or worried, having trouble concentrating, having trouble sleeping, dizziness, and heart palpitations. Generalised anxiety disorder (GAD) can cause both psychological and physical symptoms. These vary from person to person but can include feeling restless, a sense of dread, difficulty concentrating, and irritability.', 'nhs.uk', 'https://www.nhs.uk/mental-health/conditions/generalised-anxiety-disorder/symptoms/'),
         ('Dr Sarah', 'Mitchell', 'What you are describing — persistent worry about small things plus racing heart — does sound like it could be generalised anxiety. The key differentiator is whether these feelings are disproportionate to the actual situation and whether they persist most days for at least 6 months. I would recommend speaking with your GP who can do a proper assessment.', None, None),
     ]),

    ('mental-health', 'How do I manage work-related stress before it becomes burnout?',
     'I work 50+ hours a week in a factory and I feel exhausted all the time. My sleep is terrible and I dread going to work. What can I do?',
     None,
     [
         ('Emily', 'Chen', 'I went through exactly this working in logistics. Three things that helped me: 1) Setting a hard boundary on overtime — I told my manager I could only do 45 hours max. 2) Taking my lunch break AWAY from the work area. 3) Starting a 10-minute walk before bed instead of scrolling my phone. It took about 3 weeks to feel different.', None, None),
         ('NHS', 'Official', 'Work-related stress, depression or anxiety accounted for 17.1 million working days lost in 2022/23 in Great Britain. Signs you may be heading towards burnout include emotional exhaustion, feeling detached from your work, and reduced performance. The NHS recommends speaking to your GP, using the NHS talking therapies service, and contacting your employer about workplace adjustments.', 'nhs.uk', 'https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/stress/'),
     ]),

    ('mental-health', 'Is it normal to feel lonely even when surrounded by people?',
     'I moved to a new city for work 6 months ago. I have colleagues but no real friends. I feel isolated even in a room full of people.',
     None,
     [
         ('Ahmed', 'Malik', 'Absolutely normal, especially after a big move. I moved from Pakistan to the UK for uni and felt this for almost a year. What helped was joining a local community group — for me it was a cricket club. Look for meetup groups, volunteering, or sports clubs in your area. The connections come, but they take time to build depth.', None, None),
         ('Priya', 'Sharma', 'This is incredibly common and there is nothing wrong with you. Research shows it takes about 50 hours of socialising to move from acquaintance to casual friend, and 200+ hours to become close friends. Give it time and be intentional about inviting people for coffee or walks outside of work.', None, None),
     ]),

    ('mental-health', 'What is the difference between feeling sad and clinical depression?',
     'I have been feeling down for about 3 weeks. How do I know if this is just sadness or if I need professional help?',
     None,
     [
         ('NHS', 'Official', 'Depression is more than simply feeling unhappy or fed up for a few days. If you have been feeling persistently sad for more than 2 weeks, have lost interest in things you used to enjoy, feel hopeless, have low energy, difficulty sleeping, changes in appetite, or thoughts of self-harm, you should see your GP. Depression is a real illness with real symptoms — it is not a sign of weakness.', 'nhs.uk', 'https://www.nhs.uk/mental-health/conditions/depression-in-adults/symptoms/'),
         ('Dr Sarah', 'Mitchell', 'The two-week mark is important. Sadness in response to life events is normal and healthy. But when low mood persists beyond 2 weeks, starts affecting your daily functioning (missing work, not eating, withdrawing from friends), and you cannot identify a clear cause — that is when it may be clinical depression. Please do not hesitate to speak with your GP.', None, None),
     ]),

    # ===== CARDIOVASCULAR =====
    ('cardiovascular', 'What blood pressure reading is considered high?',
     'My GP said my blood pressure was 145/92 and wants me to monitor it at home. Is this really high?',
     None,
     [
         ('NHS', 'Official', 'Blood pressure is recorded as 2 numbers: systolic (the higher number, pressure when heart pushes blood out) and diastolic (lower number, pressure when heart rests). High blood pressure is considered to be 140/90mmHg or higher. Ideal blood pressure is between 90/60 and 120/80. Your reading of 145/92 is in the Stage 1 hypertension range.', 'nhs.uk', 'https://www.nhs.uk/conditions/high-blood-pressure-hypertension/'),
         ('James', 'Thornton', 'I had similar readings last year. My GP put me on a home monitoring routine — twice a day for a week. Turns out my readings at the GP were higher due to white coat syndrome. My average at home was 132/85. Worth doing the home monitoring before worrying too much.', None, None),
     ]),

    ('cardiovascular', 'Can young people have heart attacks?',
     'I am 28 and have a family history of heart disease. My dad had a heart attack at 52. Should I be worried?',
     None,
     [
         ('Dr Sarah', 'Mitchell', 'While heart attacks are far more common in older adults, they can and do happen in younger people, especially with family history. With your dad having a heart attack at 52, you should ask your GP for a cardiovascular risk assessment. This includes checking cholesterol, blood pressure, blood sugar, and lifestyle factors. Early prevention is incredibly effective.', None, None),
         ('GOV.UK', 'Health', 'Cardiovascular disease (CVD) is one of the main causes of death and disability in the UK. Risk factors include smoking, high blood pressure, high cholesterol, diabetes, being overweight, lack of exercise, and family history of heart disease. The NHS Health Check programme offers free checks to adults aged 40-74.', 'gov.uk', 'https://www.gov.uk/government/collections/cardiovascular-disease-statistics'),
     ]),

    # ===== ALLERGIES =====
    ('allergies', 'Why do my allergies get worse in spring?',
     'Every March to May I get terrible sneezing, itchy eyes, and a blocked nose. It seems to get worse each year.',
     None,
     [
         ('NHS', 'Official', 'Hay fever is usually worse between late March and September, especially when it is warm, humid, and windy. This is when the pollen count is at its highest. Tree pollen is released in spring, grass pollen in late spring and summer, and weed pollen in late autumn.', 'nhs.uk', 'https://www.nhs.uk/conditions/hay-fever/'),
         ('Rachel', 'Hughes', 'I have suffered with this for years. What made the biggest difference for me: 1) Start taking antihistamines 2 weeks BEFORE your symptoms usually begin. 2) Vaseline around your nostrils to trap pollen. 3) Shower and change clothes when you come home. 4) Keep windows closed on high pollen days. Check the Met Office pollen forecast daily.', None, None),
     ]),

    # ===== SKIN =====
    ('skin', 'What is the difference between eczema and psoriasis?',
     'I have red, itchy patches on my elbows and knees. My GP is not sure if it is eczema or psoriasis. How can I tell?',
     None,
     [
         ('NHS', 'Official', 'Eczema (atopic dermatitis) causes skin to become itchy, dry, cracked, and sore. It often occurs on the inside of elbows, behind knees, and on the face. Psoriasis produces flaky patches of skin that form silvery-white scales. It commonly appears on elbows, knees, scalp, and lower back. The key visual difference is that psoriasis patches tend to be thicker with silvery scales, while eczema is thinner and more likely to weep.', 'nhs.uk', 'https://www.nhs.uk/conditions/atopic-eczema/'),
         ('David', 'Kapoor', 'I have psoriasis on my elbows and it took 3 GP visits to get a proper diagnosis. If your GP is unsure, ask for a dermatology referral. A dermatologist can usually tell immediately just by looking at it. In the meantime, keep the area moisturised — I use Cerave cream twice a day and it helps a lot.', None, None),
     ]),

    # ===== METABOLIC =====
    ('metabolic', 'What are the warning signs of Type 2 diabetes?',
     'I am overweight and my father has Type 2 diabetes. What symptoms should I watch out for?',
     None,
     [
         ('NHS', 'Official', 'The symptoms of Type 2 diabetes include peeing more than usual (particularly at night), feeling thirsty all the time, feeling very tired, losing weight without trying, itching around the genitals, blurred vision, and cuts or wounds that take longer to heal. Many people have Type 2 diabetes without realising because symptoms do not necessarily make you feel unwell.', 'nhs.uk', 'https://www.nhs.uk/conditions/type-2-diabetes/symptoms/'),
         ('Michael', "O'Brien", 'I was diagnosed at 45 after ignoring the tiredness and frequent urination for months. With your family history, please get an HbA1c blood test from your GP — it measures your average blood sugar over the past 2-3 months. Early detection makes management so much easier. I now control mine with diet and metformin alone.', None, None),
     ]),

    # ===== INFECTIONS =====
    ('infections', 'How long should I wait before seeing a GP for a cold that will not go away?',
     'I have had a cold for 2 weeks now. The cough is getting worse and I have yellow mucus. Should I see a doctor?',
     None,
     [
         ('NHS', 'Official', 'You should see a GP if your symptoms have not improved after 3 weeks, your symptoms are getting worse, you have a very high temperature or feel hot and shivery, you are concerned about your child\'s symptoms, you are finding it hard to breathe, or you have a long-term medical condition. Yellow or green mucus does not necessarily mean you need antibiotics.', 'nhs.uk', 'https://www.nhs.uk/conditions/common-cold/'),
         ('Priya', 'Sharma', 'Two weeks with worsening cough and yellow mucus could be a secondary bacterial infection developing after the initial viral cold. I would not wait the full 3 weeks in your case — see your GP now. They may want to listen to your chest to rule out a chest infection.', None, None),
     ]),

    # ===== EYE & VISION =====
    ('eye-vision', 'Is screen time really damaging my eyes?',
     'I work at a computer 8 hours a day and then use my phone in the evening. My eyes feel strained and dry. Is this doing permanent damage?',
     None,
     [
         ('Dr Sarah', 'Mitchell', 'Prolonged screen use causes digital eye strain (computer vision syndrome) but current evidence does not suggest it causes permanent damage to adults. The symptoms — dryness, blurred vision, headaches — are caused by reduced blinking (we blink 66% less when looking at screens) and sustained close focus. Follow the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds.', None, None),
         ('James', 'Thornton', 'I had terrible eye strain until I got blue light filtering glasses and adjusted my monitor. Set your screen brightness to match the ambient light in the room, position the monitor at arm\'s length, and use artificial tears if dryness is an issue. Made a huge difference for me.', None, None),
     ]),

    # ===== CANCER =====
    ('cancer', 'What does a suspicious mole look like?',
     'I have a mole on my back that seems to have changed shape recently. How do I know if I should be concerned?',
     None,
     [
         ('NHS', 'Official', 'Use the ABCDE checklist to assess moles: A (Asymmetry) — the 2 halves do not match, B (Border) — the edges are irregular or blurred, C (Colour) — the colour is uneven with different shades, D (Diameter) — it is larger than 6mm (the size of a pencil eraser), E (Evolving) — the mole is changing in size, shape, or colour. See your GP urgently if a mole has changed or you have a new mole that looks unusual.', 'nhs.uk', 'https://www.nhs.uk/conditions/melanoma-skin-cancer/symptoms/'),
     ]),

    # ===== NEUROLOGY =====
    ('neurology', 'Is forgetfulness at 30 normal or should I be worried?',
     'I keep forgetting where I put my keys, missing appointments, and losing my train of thought mid-sentence. I am only 32.',
     None,
     [
         ('Dr Sarah', 'Mitchell', 'At 32, this is almost certainly not dementia. Forgetfulness at this age is usually caused by stress, poor sleep, anxiety, multitasking overload, or depression. All of these affect working memory significantly. If you are sleeping less than 7 hours, are stressed at work, or dealing with anxiety — those are the most likely culprits. However, if it is significantly impacting your daily life, see your GP to rule out other causes like thyroid issues or vitamin B12 deficiency.', None, None),
         ('Emily', 'Chen', 'I went through exactly this and it turned out I was severely vitamin D and B12 deficient. A simple blood test revealed it. Once I started supplements, my brain fog cleared within a month. Definitely worth getting blood work done.', None, None),
     ]),

    # ===== GENERAL HEALTH =====
    ('general', 'How much water should I actually drink per day?',
     'I keep seeing different advice — 2 litres, 8 glasses, drink when thirsty. What is the actual recommendation?',
     None,
     [
         ('NHS', 'Official', 'The NHS recommends drinking 6 to 8 cups or glasses of fluid a day. Water, lower-fat milk, and sugar-free drinks including tea and coffee all count. You may need to drink more if you exercise, the weather is hot, or you are pregnant or breastfeeding.', 'nhs.uk', 'https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/water-drinks-nutrition/'),
         ('Ahmed', 'Malik', 'The "8 glasses" rule is a rough guide, not science. A better approach: check your urine colour. If it is pale straw colour, you are hydrated. If it is dark yellow, drink more. Simple as that. Also remember that food (especially fruit and vegetables) contributes about 20% of your daily water intake.', None, None),
     ]),

    ('general', 'Is intermittent fasting safe?',
     'I have been thinking about trying 16:8 intermittent fasting to lose weight. Is it safe and does it actually work?',
     None,
     [
         ('David', 'Kapoor', 'I have been doing 16:8 for over a year — eating between 12pm and 8pm. Lost 14kg in the first 6 months. The key is that you still need to eat a balanced diet during your eating window. It is not a licence to eat junk food. That said, it is not for everyone — people with diabetes, eating disorders, or who are pregnant should avoid it.', None, None),
         ('Dr Sarah', 'Mitchell', 'Research shows intermittent fasting can be effective for weight loss and may improve insulin sensitivity. The 16:8 method is the most studied and generally considered safe for healthy adults. However, it is not more effective than simply reducing calorie intake. The best diet is the one you can stick to long-term. Consult your GP before starting if you have any medical conditions.', None, None),
     ]),

    # ===== STROKE =====
    ('stroke', 'How do I recognise the signs of a stroke?',
     'My grandmother had a stroke and nobody recognised the signs quickly enough. What should I look out for?',
     None,
     [
         ('NHS', 'Official', 'Use the FAST test to recognise a stroke: Face — has their face fallen on one side? Can they smile? Arms — can they raise both arms and keep them there? Speech — is their speech slurred? Time — call 999 immediately if you see any of these signs. Acting FAST can reduce brain damage and improve chances of recovery. Other symptoms include sudden confusion, trouble seeing, severe headache, and dizziness.', 'nhs.uk', 'https://www.nhs.uk/conditions/stroke/symptoms/'),
     ]),

    # ===== IMMUNE SYSTEM =====
    ('immune-system', 'Why do I keep getting ill every few weeks?',
     'I seem to catch every cold and bug going around. I have been ill about 6 times in the past 4 months. Is my immune system weak?',
     None,
     [
         ('Dr Sarah', 'Mitchell', 'Frequent infections can have several causes: poor sleep (less than 7 hours weakens immune response by 4x), chronic stress (cortisol suppresses immune function), vitamin deficiencies (D, C, zinc), smoking, excessive alcohol, or an underlying condition. Six illnesses in 4 months is above average and worth investigating. I would recommend blood tests checking your full blood count, vitamin D, B12, iron, and thyroid function.', None, None),
         ('Rachel', 'Hughes', 'I was in this exact situation. Turned out I was severely vitamin D deficient (very common in the UK, especially in winter). My GP put me on high-dose supplements and I have been noticeably better since. Also worth considering if you work in a crowded environment where you are exposed to more germs.', None, None),
     ]),

    # ===== BLOOD DISORDERS =====
    ('blood-disorders', 'What causes iron deficiency anaemia and how is it treated?',
     'I have been feeling extremely tired and dizzy. Blood tests showed low iron. What causes this and how long until I feel better?',
     None,
     [
         ('NHS', 'Official', 'Iron deficiency anaemia is caused by lack of iron, often because of blood loss or pregnancy. It is the most common type of anaemia. Treatment usually involves taking iron supplements prescribed by your GP, usually ferrous sulphate tablets taken 2 to 3 times a day. Most people start to feel better within a few weeks, but it can take up to 6 months for iron levels to return to normal.', 'nhs.uk', 'https://www.nhs.uk/conditions/iron-deficiency-anaemia/'),
         ('Priya', 'Sharma', 'One tip they do not always tell you: take iron tablets with orange juice (vitamin C helps absorption) and avoid taking them with tea, coffee, or milk (these block absorption). Also, do not take them at the same time as antacids. I made all these mistakes initially and my levels were not improving until my pharmacist pointed this out.', None, None),
     ]),

    # ===== WORKPLACE =====
    ('mental-health', 'How do I tell my employer I am struggling with my mental health?',
     'I need time off for my mental health but I am scared my manager will not take it seriously. What are my rights?',
     None,
     [
         ('GOV.UK', 'Health', 'Under the Equality Act 2010, mental health conditions can be considered a disability if they have a substantial and long-term effect on your ability to carry out normal day-to-day activities. Your employer has a legal duty to make reasonable adjustments. You are not obligated to disclose your specific condition, only that you have a health condition that requires adjustment.', 'gov.uk', 'https://www.gov.uk/rights-disabled-person/employment'),
         ('Michael', "O'Brien", 'I went through this last year. Here is what worked: I requested a private meeting with my manager (not over email), kept it factual ("I am dealing with a health condition that is affecting my work performance"), and came prepared with what I needed (flexible hours, reduced workload temporarily). My manager was surprisingly supportive. Most companies have occupational health services too — ask HR about this.', None, None),
     ]),

    # ===== SURGERY =====
    ('surgery', 'How long does it take to recover from a knee replacement?',
     'My mother is 65 and scheduled for a total knee replacement next month. What should we expect for recovery time?',
     None,
     [
         ('NHS', 'Official', 'Recovery from a total knee replacement takes time. You will usually be in hospital for 1 to 3 days. Most people can stop using walking aids about 6 weeks after surgery and return to normal activities after about 3 months. Full recovery can take up to 2 years. Physiotherapy exercises are essential for recovery and should be started as soon as possible after surgery.', 'nhs.uk', 'https://www.nhs.uk/conditions/knee-replacement/recovery/'),
         ('James', 'Thornton', 'My mum had hers done at 67. The first 2 weeks were the hardest — she needed help with everything. Make sure the house is set up before surgery: raised toilet seat, grab rails, ice packs ready, and a comfortable chair with armrests. The physiotherapy exercises are boring but absolutely critical. She was back to gardening after 4 months.', None, None),
     ]),

    # ===== ENT =====
    ('ent', 'I keep getting recurring ear infections. What could be causing this?',
     'I have had 4 ear infections this year. My GP keeps giving me antibiotics but they keep coming back.',
     None,
     [
         ('Dr Sarah', 'Mitchell', 'Recurring ear infections in adults can be caused by: water getting trapped in the ear (common in swimmers), using cotton buds (pushes wax deeper and can damage the ear canal), eczema or psoriasis in the ear canal, or a narrow ear canal. If you are on your 4th infection this year, your GP should refer you to an ENT specialist for investigation. In the meantime, keep your ears dry, do not use cotton buds, and use ear plugs when swimming or showering.', None, None),
     ]),

    # ===== EMOTIONS =====
    ('emotions', 'How do I support a partner going through depression?',
     'My partner has been diagnosed with depression. I want to help but I do not know what to say or do. I feel helpless.',
     None,
     [
         ('Emily', 'Chen', 'The most important thing is to just be there. You do not need to fix it. Say "I am here for you" instead of "cheer up." Listen without trying to solve. Help with practical things they are struggling with — cooking, cleaning, remembering appointments. Encourage them to keep up with their treatment. And crucially — look after yourself too. You cannot pour from an empty cup.', None, None),
         ('NHS', 'Official', 'Supporting someone with depression can be challenging. The NHS recommends: learning about depression so you can understand what they are going through, being patient as recovery takes time, encouraging them to seek help and stick with treatment, and looking after your own wellbeing. Contact Samaritans (116 123) if you need someone to talk to yourself.', 'nhs.uk', 'https://www.nhs.uk/mental-health/conditions/depression-in-adults/support-for-depression/'),
     ]),

    ('general', 'How much sleep do adults actually need?',
     'I function fine on 5-6 hours of sleep. My friend says I need 8 hours minimum. Who is right?',
     None,
     [
         ('Dr Sarah', 'Mitchell', 'Most adults need 7 to 9 hours of sleep per night. While some people genuinely function well on less (there is a rare genetic variant that allows this), most people who think they are fine on 5-6 hours have simply adapted to feeling tired. Chronic sleep deprivation increases risk of heart disease, diabetes, obesity, and weakened immunity. The best test: if you need an alarm to wake up, you are probably not getting enough sleep.', None, None),
         ('NHS', 'Official', 'Most adults need between 6 and 9 hours of sleep every night. If you are consistently sleeping less than this, you may be building up a sleep debt that can affect your physical and mental health. Poor sleep has been linked to increased risk of obesity, heart disease, and diabetes, and can shorten your life expectancy.', 'nhs.uk', 'https://www.nhs.uk/live-well/sleep-and-tiredness/how-to-get-to-sleep/'),
     ]),
]


def seed():
    app = create_app()
    with app.app_context():
        # Create users
        users = {}
        for first, last, email, is_system, _ in SYSTEM_USERS:
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    first_name=first, last_name=last, email=email,
                    is_system_account=is_system
                )
                user.set_password('seed-user-no-login')
                db.session.add(user)
                db.session.flush()
            users[f'{first} {last}'] = user
        db.session.commit()
        print(f'Users: {len(users)} ready')

        # Create Q&A
        categories = {c.slug: c for c in Category.query.all()}
        q_count = 0
        a_count = 0
        base_time = datetime.now(timezone.utc) - timedelta(days=90)

        ALL_QA = QA_DATA + EXTRA_QA_DATA

        for i, (cat_slug, title, body, source, answers_data) in enumerate(ALL_QA):
            cat = categories.get(cat_slug)
            if not cat:
                print(f'  ! Category not found: {cat_slug}')
                continue

            existing = Question.query.filter_by(title=title).first()
            if existing:
                continue

            # Find author (use first answerer's source or community user)
            if source:
                author_name = 'NHS Official' if source == 'nhs.uk' else 'GOV.UK Health'
            else:
                author_name = random.choice(
                    [k for k in users.keys() if 'NHS' not in k and 'GOV' not in k]
                )

            author = users.get(author_name, list(users.values())[3])
            q_time = base_time + timedelta(days=i * 2, hours=random.randint(6, 22))

            question = Question(
                title=title, body=body,
                author_id=author.id, category_id=cat.id,
                source=source,
                view_count=random.randint(15, 500),
                created_at=q_time
            )
            db.session.add(question)
            db.session.flush()
            q_count += 1

            # Add answers
            for j, (a_first, a_last, a_body, a_source, a_url) in enumerate(answers_data):
                a_name = f'{a_first} {a_last}'
                a_user = users.get(a_name, list(users.values())[3])
                a_time = q_time + timedelta(hours=random.randint(1, 48))

                answer = Answer(
                    body=a_body,
                    question_id=question.id,
                    author_id=a_user.id,
                    source=a_source,
                    source_url=a_url,
                    created_at=a_time
                )
                db.session.add(answer)
                db.session.flush()
                a_count += 1

                # Add some random votes
                other_users = [u for u in users.values() if u.id != a_user.id]
                for voter in random.sample(other_users, min(len(other_users), random.randint(2, 6))):
                    vote = Vote(
                        user_id=voter.id,
                        answer_id=answer.id,
                        value=random.choice([1, 1, 1, 1, -1])  # mostly upvotes
                    )
                    db.session.add(vote)

        db.session.commit()
        print(f'Questions: {q_count} created')
        print(f'Answers: {a_count} created')
        print('Done seeding Q&A data.')


if __name__ == '__main__':
    seed()
