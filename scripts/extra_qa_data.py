"""Extra Q&A data to bulk up the MediAsk platform."""

EXTRA_QA_DATA = [
    # MENTAL HEALTH - more
    ('mental-health', 'What does a panic attack actually feel like?',
     'I think I had a panic attack at work yesterday but I am not sure. My chest got tight, I could not breathe, and I thought I was dying.',
     None,
     [('NHS', 'Official', 'During a panic attack you may experience a racing heartbeat, feeling faint, sweating, nausea, chest pain, shortness of breath, trembling, hot flushes, chills, shaky limbs, a choking sensation, dizziness, numbness or pins and needles, dry mouth, a need to go to the toilet, ringing in your ears, and a feeling of dread or fear of dying. Most panic attacks last between 5 and 20 minutes.', 'nhs.uk', 'https://www.nhs.uk/mental-health/conditions/panic-disorder/'),
      ('Emily', 'Chen', 'I get panic attacks regularly. The first time I genuinely thought I was having a heart attack. What helps me: I use the 5-4-3-2-1 grounding technique — name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste. It pulls your brain out of the panic spiral. Also, splash cold water on your face — it triggers the dive reflex and slows your heart rate.', None, None),
     ]),

    ('mental-health', 'How do I know if I have ADHD as an adult?',
     'I have always struggled with focus, forget things constantly, start tasks but never finish them, and my mind races. Could this be ADHD?',
     None,
     [('Dr Sarah', 'Mitchell', 'Adult ADHD presents differently from childhood ADHD. Common signs include difficulty concentrating on tasks, poor time management, restlessness, impulsivity, trouble prioritising, mood swings, and difficulty coping with stress. Many adults are diagnosed later in life because their symptoms were masked by coping strategies. Ask your GP for a referral to a psychiatrist who specialises in ADHD assessment. The process typically involves questionnaires, clinical interviews, and sometimes input from someone who knew you as a child.', None, None),
     ]),

    ('mental-health', 'Is therapy worth it if I do not have a diagnosable condition?',
     'I am generally okay but feel stuck in life and my motivation is low. Is therapy only for people with serious mental health issues?',
     None,
     [('Priya', 'Sharma', 'Therapy is absolutely for everyone, not just crisis situations. I started therapy when I felt stuck, not because I had a diagnosis. It helped me understand patterns in my thinking, improve my relationships, and set better boundaries. Think of it like going to the gym for your mind — you do not wait until you are injured to exercise.', None, None),
      ('NHS', 'Official', 'NHS talking therapies are available for common problems like stress, anxiety, and depression. You can refer yourself directly without seeing a GP first. The service is free on the NHS and includes cognitive behavioural therapy (CBT), counselling, and guided self-help.', 'nhs.uk', 'https://www.nhs.uk/mental-health/talking-therapies-medicine-treatments/talking-therapies-and-counselling/nhs-talking-therapies/'),
     ]),

    ('mental-health', 'How do I stop overthinking everything?',
     'I spend hours replaying conversations in my head and worrying about things that have not happened. It is exhausting.',
     None,
     [('Ahmed', 'Malik', 'I used to do this constantly. Two things that genuinely helped: 1) Schedule worry time — set aside 15 minutes a day where you are allowed to worry, and when overthinking starts outside that time, tell yourself "I will think about this during worry time." Sounds silly but it works because it trains your brain to postpone rumination. 2) Write it down — when a thought loops, put it on paper. Once it is out of your head and on paper, the loop often breaks.', None, None),
     ]),

    ('mental-health', 'What are the signs of burnout vs just being tired?',
     'I sleep 8 hours but wake up exhausted. I used to love my job but now I dread it. Is this burnout?',
     None,
     [('Dr Sarah', 'Mitchell', 'Burnout is more than tiredness. The three key markers are: 1) Emotional exhaustion — feeling drained even after rest. 2) Depersonalisation — feeling cynical or detached from your work and colleagues. 3) Reduced personal accomplishment — feeling like nothing you do matters. If you are experiencing all three, especially over several weeks, this is likely burnout. Regular tiredness resolves with rest; burnout does not. You need structural changes — reduced workload, time off, or even a role change.', None, None),
     ]),

    # GENERAL HEALTH
    ('general', 'What is the best exercise for someone who hates the gym?',
     'I know I need to exercise but I absolutely hate gyms. What are good alternatives?',
     None,
     [('David', 'Kapoor', 'I despise gyms too. Here is what I do instead: walking 30 minutes a day (free, no equipment, works for every fitness level), swimming at my local leisure centre (easy on joints, burns loads of calories), and YouTube workout videos at home (I like Joe Wicks for quick 15-minute sessions). The best exercise is the one you will actually do consistently.', None, None),
      ('NHS', 'Official', 'Adults should aim for at least 150 minutes of moderate intensity activity a week or 75 minutes of vigorous intensity activity. This can include brisk walking, cycling, dancing, hiking, swimming, or even pushing a lawnmower. You do not need a gym membership to stay active.', 'nhs.uk', 'https://www.nhs.uk/live-well/exercise/exercise-guidelines/physical-activity-guidelines-for-adults-aged-19-to-64/'),
     ]),

    ('general', 'Why does my back hurt when I sit all day?',
     'I work at a desk and by 3pm my lower back is killing me. I am only 29.',
     None,
     [('James', 'Thornton', 'Same issue here. Three changes that fixed it for me: 1) Got a lumbar support cushion for my office chair — cost about 15 pounds and made a massive difference. 2) Set a timer to stand up every 30 minutes and walk around for 2 minutes. 3) Started doing 5 minutes of stretches before work — cat-cow stretches and hip flexor stretches specifically target the muscles that tighten from sitting.', None, None),
     ]),

    ('general', 'How much caffeine is too much?',
     'I drink about 5-6 cups of coffee a day. My partner says this is too much. Is it?',
     None,
     [('NHS', 'Official', 'The NHS advises that up to 400mg of caffeine a day is unlikely to cause problems for most adults. That is roughly 4 cups of brewed coffee, 8 cups of tea, or 10 cans of cola. Pregnant women should limit caffeine to 200mg a day. Too much caffeine can cause restlessness, insomnia, headaches, dizziness, and fast heartbeat.', 'nhs.uk', 'https://www.nhs.uk/live-well/eat-well/food-types/the-truth-about-caffeine/'),
      ('Rachel', 'Hughes', 'At 5-6 cups you are slightly over the recommended limit. I was at 7 cups a day and did not realise how much it was affecting my sleep and anxiety until I cut down to 3. Try replacing the afternoon coffees with decaf — you still get the ritual without the caffeine hit disrupting your sleep.', None, None),
     ]),

    ('general', 'What vitamins should I take in winter in the UK?',
     'I live in Hull and barely see sunlight from October to March. What supplements do I actually need?',
     None,
     [('NHS', 'Official', 'The Department of Health and Social Care recommends that everyone in the UK should consider taking a daily supplement containing 10 micrograms of vitamin D during autumn and winter. This is because it is difficult to get enough vitamin D from food alone, and the UK does not get enough sunlight for our bodies to make vitamin D between October and early March.', 'nhs.uk', 'https://www.nhs.uk/conditions/vitamins-and-minerals/vitamin-d/'),
      ('Ahmed', 'Malik', 'Living in Hull as well! Vitamin D is essential — I take 1000 IU daily from October to April. My GP also found I was low in B12 and iron from a routine blood test. Worth getting your levels checked rather than guessing which supplements you need.', None, None),
     ]),

    ('general', 'Is cracking your knuckles bad for you?',
     'I crack my knuckles all the time and people tell me I will get arthritis. Is this true?',
     None,
     [('Dr Sarah', 'Mitchell', 'This is one of the most common medical myths. Multiple studies have found no link between knuckle cracking and arthritis. The sound is caused by gas bubbles popping in the fluid around your joints. However, habitual knuckle cracking may lead to reduced grip strength over time and can cause joint swelling in some people. It will not give you arthritis though.', None, None),
     ]),

    # CARDIOVASCULAR
    ('cardiovascular', 'What does high cholesterol feel like? Are there symptoms?',
     'My GP says I need a cholesterol test at my next checkup. What symptoms should I look for?',
     None,
     [('NHS', 'Official', 'High cholesterol does not cause symptoms. You can only find out if you have it from a blood test. Your GP might suggest having a test if they think your cholesterol level could be high, based on your age, weight, family history, or other conditions you have like high blood pressure or diabetes.', 'nhs.uk', 'https://www.nhs.uk/conditions/high-cholesterol/'),
      ('Michael', "O'Brien", 'This is the scary part — there are no symptoms until it causes a serious problem like a heart attack or stroke. That is why regular testing is so important, especially if you have a family history. I had mine tested at 40, it was 6.8 (should be below 5), and I had no idea. Now I manage it with statins and diet changes.', None, None),
     ]),

    ('cardiovascular', 'Are heart palpitations dangerous?',
     'I sometimes feel my heart skip a beat or flutter in my chest. It happens a few times a week. Should I be worried?',
     None,
     [('Dr Sarah', 'Mitchell', 'Occasional palpitations are very common and usually harmless. They can be triggered by caffeine, alcohol, stress, anxiety, vigorous exercise, or certain medications. However, you should see your GP urgently if palpitations last more than a few minutes, you also have chest pain, you feel faint or dizzy, or you have a history of heart problems. An ECG or Holter monitor can help your GP assess whether there is an underlying issue.', None, None),
     ]),

    # INFECTIONS
    ('infections', 'What are the symptoms of long COVID?',
     'I had COVID 3 months ago and I still feel exhausted and my brain feels foggy. Could this be long COVID?',
     None,
     [('NHS', 'Official', 'Long COVID is when you continue to have symptoms more than 4 weeks after having COVID-19. Common symptoms include extreme tiredness (fatigue), shortness of breath, problems with memory and concentration (brain fog), joint pain, chest pain, depression and anxiety, tinnitus, and difficulty sleeping. If you have symptoms that continue for more than 4 weeks after COVID, contact your GP.', 'nhs.uk', 'https://www.nhs.uk/conditions/covid-19/long-term-effects-of-covid-19-long-covid/'),
      ('Rachel', 'Hughes', 'I had long COVID for 8 months. The brain fog was the worst part — I could not remember words mid-sentence. What helped: pacing (doing less than you think you can on good days), lots of omega-3 fatty acids, and my GP referred me to a long COVID clinic. Recovery is real but it is slow. Be patient with yourself.', None, None),
     ]),

    # METABOLIC
    ('metabolic', 'Can Type 2 diabetes be reversed?',
     'I was recently diagnosed with Type 2 diabetes. My HbA1c is 52. Is it possible to reverse this?',
     None,
     [('Dr Sarah', 'Mitchell', 'Yes, Type 2 diabetes can potentially go into remission, especially if caught early. An HbA1c of 52 is only just in the diabetic range (48+). The strongest evidence is for significant weight loss — studies show that losing 10-15% of body weight within the first few years of diagnosis can put Type 2 diabetes into remission in many cases. This means HbA1c drops below 48 without medication. It requires sustained dietary changes, not a quick fix, but it is absolutely achievable.', None, None),
      ('NHS', 'Official', 'The NHS England Type 2 Diabetes Path to Remission Programme helps people with Type 2 diabetes who have a BMI of 27 or above achieve remission through a total diet replacement approach. Speak to your GP about eligibility.', 'nhs.uk', 'https://www.nhs.uk/conditions/type-2-diabetes/'),
     ]),

    # SKIN
    ('skin', 'How do I get rid of acne in my 30s?',
     'I am 33 and still getting acne. I thought this would stop after my teens. What can I do?',
     None,
     [('Priya', 'Sharma', 'Adult acne is surprisingly common, especially in women. What worked for me: 1) Switched to a gentle cleanser (CeraVe) instead of harsh acne washes that were stripping my skin. 2) Started using niacinamide serum — it reduces inflammation and oil production without drying. 3) Got a GP prescription for adapalene (a retinoid) which was a game changer. Also — check your pillowcases. I change mine every 3 days and it made a noticeable difference.', None, None),
     ]),

    # ALLERGIES
    ('allergies', 'Can you suddenly develop a food allergy as an adult?',
     'I have eaten shellfish my whole life but last week I broke out in hives after eating prawns. Can allergies develop later in life?',
     None,
     [('NHS', 'Official', 'Although food allergies commonly develop in childhood, they can develop at any age. It is possible to develop an allergy to foods you have previously eaten without any problems. If you think you have a food allergy, see your GP. Do not attempt to diagnose a food allergy yourself. If you have had a severe reaction, carry 2 adrenaline auto-injectors at all times.', 'nhs.uk', 'https://www.nhs.uk/conditions/food-allergy/'),
      ('Dr Sarah', 'Mitchell', 'Adult-onset food allergies are well documented and becoming more common. Shellfish is actually the most common adult-onset food allergy. Your reaction with hives suggests an IgE-mediated allergy. Please see your GP for a referral to an allergy clinic. They can do skin prick tests and blood tests to confirm. Until then, avoid shellfish completely and ask your GP about carrying an antihistamine.', None, None),
     ]),

    # EYE
    ('eye-vision', 'Should I be worried about floaters in my vision?',
     'I have started seeing tiny spots and squiggly lines floating across my vision. Is this normal?',
     None,
     [('NHS', 'Official', 'Floaters are small dark shapes that float across your vision. They can look like dots, threads, or squiggly lines. They are usually harmless and are caused by small pieces of debris in the vitreous jelly of your eye. However, see an optician or go to A&E immediately if you suddenly get new floaters, floaters with flashes of light, a dark shadow or curtain over your vision, or a sudden increase in floaters. This could be a sign of retinal detachment.', 'nhs.uk', 'https://www.nhs.uk/conditions/floaters-and-flashes-in-the-eyes/'),
     ]),

    # SURGERY
    ('surgery', 'What should I eat before and after surgery?',
     'I am having gallbladder surgery next week. What should I eat to prepare and recover?',
     None,
     [('James', 'Thornton', 'Before surgery: eat a balanced diet rich in protein (chicken, fish, eggs, beans) and vitamin C (oranges, peppers, broccoli) — both help with wound healing. Stay well hydrated. After gallbladder removal: start with bland, low-fat foods. Your body needs time to adjust to digesting fat without a gallbladder. Avoid fried foods, fatty meats, and full-fat dairy for the first few weeks. Gradually reintroduce them. Most people can eat normally within a month.', None, None),
     ]),

    # NEUROLOGY
    ('neurology', 'What causes migraines and how are they different from headaches?',
     'I get intense headaches with nausea and sensitivity to light about twice a month. Are these migraines?',
     None,
     [('NHS', 'Official', 'A migraine is usually a moderate or severe headache felt as a throbbing pain on one side of the head. Many people also have symptoms such as feeling sick, being sick, and increased sensitivity to light or sound. Migraine is a common health condition, affecting around 1 in every 5 women and around 1 in every 15 men. Some people have migraines several times a week, while others only have them occasionally.', 'nhs.uk', 'https://www.nhs.uk/conditions/migraine/'),
      ('Emily', 'Chen', 'The nausea and light sensitivity are classic migraine indicators. Regular headaches do not usually cause those. I track mine with a migraine diary app — I found that mine are triggered by dehydration, skipping meals, and hormonal changes. Keeping a diary helped my GP prescribe sumatriptan as a rescue medication, which stops my migraines within 30 minutes.', None, None),
     ]),

    # EMOTIONS
    ('emotions', 'How do I set boundaries without feeling guilty?',
     'I always say yes to everything and then resent people for it. How do I learn to say no?',
     None,
     [('Priya', 'Sharma', 'I struggled with this for years. The key insight for me was: saying no to something is saying yes to something else (your energy, your time, your wellbeing). Start small — practice saying "Let me check my schedule and get back to you" instead of an immediate yes. This gives you time to decide without pressure. And remember: people who get angry when you set boundaries are the people who benefited from you having none.', None, None),
      ('Ahmed', 'Malik', 'A therapist once told me: "No is a complete sentence." You do not owe anyone an explanation for protecting your time and energy. The guilt fades with practice. Start with low-stakes situations (declining a social event) before tackling high-stakes ones (setting work boundaries). It gets easier every time.', None, None),
     ]),

    # IMMUNE
    ('immune-system', 'What is the difference between a cold and flu?',
     'How do I know if I have a cold or the flu? They seem the same to me.',
     None,
     [('NHS', 'Official', 'Cold and flu symptoms can be similar, but flu tends to be more severe. Flu symptoms come on suddenly and include a high temperature (38C or above), aching body, feeling exhausted, and a dry cough. A cold comes on gradually and mainly affects your nose and throat, with sneezing, a runny nose, and a sore throat but usually no fever.', 'nhs.uk', 'https://www.nhs.uk/conditions/flu/'),
     ]),

    # BLOOD
    ('blood-disorders', 'Why do I bruise so easily?',
     'I get bruises from the slightest bump and they take weeks to fade. I am a 28-year-old woman.',
     None,
     [('Dr Sarah', 'Mitchell', 'Easy bruising in young women is common and usually not serious. It can be caused by thinner skin, certain medications (aspirin, ibuprofen, blood thinners), vitamin C or K deficiency, or simply having fragile blood vessels. However, if bruising is accompanied by frequent nosebleeds, heavy periods, bleeding gums, or bruises that appear without any injury, your GP should check for a bleeding disorder or platelet issue. A simple blood test can rule out anything serious.', None, None),
     ]),

    # STROKE
    ('stroke', 'Can strokes be prevented?',
     'My uncle had a stroke at 55. What can I do to reduce my risk?',
     None,
     [('GOV.UK', 'Health', 'Up to 80% of strokes are preventable through lifestyle changes and managing medical conditions. Key prevention measures include: keeping blood pressure under control, maintaining a healthy weight, exercising regularly, eating a balanced diet low in salt and saturated fat, limiting alcohol, not smoking, and managing conditions like atrial fibrillation and diabetes.', 'gov.uk', 'https://www.gov.uk/government/collections/stroke'),
      ('Dr Sarah', 'Mitchell', 'With family history, I would recommend getting your blood pressure, cholesterol, and blood sugar checked annually from your 30s. The biggest modifiable risk factors for stroke are high blood pressure (causes about 50% of all strokes), smoking, and atrial fibrillation. Your GP can assess your overall cardiovascular risk and advise on preventive measures.', None, None),
     ]),

    # CONGENITAL
    ('congenital', 'When should developmental delays in toddlers be a concern?',
     'My 2-year-old is not talking yet. Other children his age are saying sentences. Should I be worried?',
     None,
     [('NHS', 'Official', 'Most children say their first words between 12 and 18 months and start putting 2 words together by age 2. However, every child develops at their own pace. You should speak to your health visitor or GP if your child is not saying any words by 18 months, is not combining 2 words by age 2, does not seem to understand simple instructions, or loses language skills they previously had.', 'nhs.uk', 'https://www.nhs.uk/conditions/baby/babys-development/speech-problems/'),
      ('Rachel', 'Hughes', 'My son did not talk until he was nearly 3 and I was terrified. We got a referral to a speech and language therapist through our health visitor. Turned out he had glue ear (fluid in the middle ear) affecting his hearing, which was delaying his speech. Once that was treated with grommets, his speech caught up within 6 months. Get a hearing test done — it is the first thing they check.', None, None),
     ]),

    # More workplace mental health
    ('mental-health', 'Can I get signed off work for mental health reasons?',
     'I am struggling badly with anxiety and cannot face going to work. Can my GP sign me off?',
     None,
     [('GOV.UK', 'Health', 'Your GP can issue a fit note (formerly sick note) for mental health conditions just as they would for physical conditions. Mental health is treated equally under the law. If you are off work for more than 7 days, you will need a fit note from your GP. Your employer cannot discriminate against you for taking time off for mental health reasons under the Equality Act 2010.', 'gov.uk', 'https://www.gov.uk/taking-sick-leave'),
      ('Michael', "O'Brien", 'Yes, absolutely. I was signed off for 4 weeks with anxiety and depression. Be honest with your GP about how you are feeling — they deal with this every day and will not judge you. During my time off, I started CBT through the NHS talking therapies self-referral. It was the best decision I made. Your health comes first.', None, None),
     ]),

    ('general', 'What are the benefits of cold water swimming?',
     'I keep seeing people talking about cold water swimming for mental and physical health. Is there actual evidence behind this?',
     None,
     [('David', 'Kapoor', 'I started cold water swimming in the Humber 6 months ago. The initial shock is brutal but the feeling afterwards is incredible — like a natural high that lasts for hours. Anecdotally, it has improved my mood, energy, and I sleep much better. I go with a group which makes it social too.', None, None),
      ('Dr Sarah', 'Mitchell', 'There is emerging research showing cold water immersion can trigger the release of endorphins and dopamine, reduce inflammation, and improve circulation. Some studies show benefits for depression and anxiety. However, it carries risks — cold water shock can cause cardiac arrhythmia, and hypothermia is a real danger. Never swim alone, acclimatise gradually, and consult your GP if you have heart conditions.', None, None),
     ]),
]
