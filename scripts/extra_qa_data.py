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

    # ===== MORE CANCER =====
    ('cancer', 'What happens during chemotherapy and what are the side effects?',
     'My mum has been told she needs chemotherapy for breast cancer. We are terrified. What should we expect?',
     None,
     [('NHS', 'Official', 'Chemotherapy uses anti-cancer drugs to destroy cancer cells. It is given in cycles — usually a treatment session followed by a rest period. Common side effects include tiredness, feeling sick, hair loss, increased risk of infections, bruising and bleeding, sore mouth, and changes in appetite. Not everyone gets all side effects, and there are medicines to help manage many of them.', 'nhs.uk', 'https://www.nhs.uk/conditions/chemotherapy/'),
      ('Rachel', 'Hughes', 'My sister went through breast cancer chemo last year. Three practical things: 1) Stock up on ginger tea and plain crackers for nausea. 2) Get a good water bottle — staying hydrated reduces side effects significantly. 3) Ask the oncology nurse about the cold cap to help prevent hair loss. Also, Macmillan Cancer Support (0808 808 00 00) were absolutely brilliant — free practical and emotional support.', None, None),
     ]),

    ('cancer', 'How do I check for breast lumps and when should I be worried?',
     'I am 35 and have never checked my breasts properly. How do I do it and what am I looking for?',
     None,
     [('NHS', 'Official', 'There is no special technique for checking your breasts. The important thing is to get to know how your breasts normally look and feel so you notice any changes. Look at and feel each breast, including the armpits and up to the collarbone. See your GP if you notice a lump or area of thickened tissue, a change in the size or shape of a breast, dimpling of the skin, a rash on or around the nipple, discharge from a nipple, or a change in the position of the nipple.', 'nhs.uk', 'https://www.nhs.uk/conditions/breast-cancer/symptoms/'),
      ('Priya', 'Sharma', 'I found a lump at 32 and panicked. It turned out to be a fibroadenoma — completely benign. But I am so glad I went to my GP immediately. They referred me for an ultrasound within 2 weeks. The key message: most lumps are NOT cancer, but always get them checked. Do not wait and worry — the 2-week urgent referral pathway exists for exactly this situation.', None, None),
     ]),

    # ===== MORE SURGERY =====
    ('surgery', 'What questions should I ask my surgeon before an operation?',
     'I am scheduled for surgery next month and feel I do not know enough about what is going to happen.',
     None,
     [('James', 'Thornton', 'From my experience with two surgeries, these are the most useful questions: 1) What are the risks and benefits? 2) How long is the recovery? 3) When can I return to work? 4) What pain management will I have afterwards? 5) What are the alternatives to surgery? 6) How many of these procedures have you performed? 7) What should I do to prepare? Write your questions down and bring someone with you — you will be nervous and may forget things.', None, None),
      ('Dr Sarah', 'Mitchell', 'Always ask about the specific risks for YOUR situation, not just general risks. Also ask about the anaesthetic — general, local, or spinal — and what to expect when you wake up. Request written information you can take home and review. Do not be afraid to ask for time to think about it if you are unsure. Informed consent means you truly understand what is being proposed.', None, None),
     ]),

    # ===== MORE ENT =====
    ('ent', 'Why do I keep getting sore throats every few weeks?',
     'I get a sore throat almost every month. Sometimes with white patches on my tonsils. My GP just gives me antibiotics each time.',
     None,
     [('Dr Sarah', 'Mitchell', 'Recurrent tonsillitis — more than 7 episodes in a year, or 5 per year for 2 years, or 3 per year for 3 years — is a guideline for referral to ENT to discuss tonsillectomy. If you are getting this frequently, repeated antibiotics alone are not the answer. Ask your GP for an ENT referral. In the meantime, gargling with warm salt water, staying hydrated, and taking paracetamol can help manage symptoms.', None, None),
     ]),

    ('ent', 'I have had a blocked nose for months. Could it be more than a cold?',
     'My nose has been blocked on one side for about 3 months. I have tried decongestants but nothing works.',
     None,
     [('NHS', 'Official', 'A persistently blocked nose can be caused by several conditions: nasal polyps (non-cancerous growths), a deviated septum, chronic sinusitis, or allergies. If it has lasted more than 3 months and is not responding to treatment, your GP should consider an ENT referral. A one-sided blockage that does not improve should always be investigated.', 'nhs.uk', 'https://www.nhs.uk/conditions/nasal-polyps/'),
      ('David', 'Kapoor', 'I had this exact issue — turned out to be nasal polyps. My GP referred me to ENT, they did a nasal endoscopy (not painful, just uncomfortable for 10 seconds), and I started on a steroid nasal spray. Cleared up within 6 weeks. Push for a referral if your GP just keeps suggesting decongestants.', None, None),
     ]),

    # ===== MORE CONGENITAL =====
    ('congenital', 'What genetic tests are available during pregnancy?',
     'I am 12 weeks pregnant and have been offered screening tests. What do they test for and are they safe?',
     None,
     [('NHS', 'Official', 'The NHS offers screening tests during pregnancy to check for certain conditions in the baby. The combined test (at 10-14 weeks) checks for Down syndrome, Edwards syndrome, and Patau syndrome using a blood test and ultrasound. If the screening suggests a higher chance, you will be offered diagnostic tests such as amniocentesis or chorionic villus sampling (CVS). These carry a small risk of miscarriage (less than 1%).', 'nhs.uk', 'https://www.nhs.uk/pregnancy/your-pregnancy-care/screening-tests/'),
      ('Emily', 'Chen', 'I had the combined screening at 12 weeks. The blood test and scan together are completely safe — there is no risk. It was only if I needed the follow-up amniocentesis that there would be a small risk. The screening is optional, and the results give you a probability, not a definitive answer. Take time to discuss with your partner and midwife what you would want to do with the information before deciding.', None, None),
     ]),

    # ===== MORE BLOOD DISORDERS =====
    ('blood-disorders', 'What is sickle cell disease and who is at risk?',
     'My friend was recently diagnosed with sickle cell trait. What does this mean and could my children be at risk?',
     None,
     [('NHS', 'Official', 'Sickle cell disease is an inherited blood disorder that affects the shape of red blood cells. It mainly affects people of African, Caribbean, Middle Eastern, Eastern Mediterranean, and Asian descent. Sickle cell trait means carrying one copy of the gene — this usually does not cause symptoms but can be passed to children. If both parents have the trait, there is a 1 in 4 chance their child will have sickle cell disease.', 'nhs.uk', 'https://www.nhs.uk/conditions/sickle-cell-disease/'),
      ('Dr Sarah', 'Mitchell', 'If you are planning a family and your partner has sickle cell trait, ask your GP for a haemoglobinopathy screen. This is a simple blood test that checks whether you also carry the trait. The NHS Sickle Cell and Thalassaemia Screening Programme offers testing to all pregnant women in England. Early knowledge allows you to make informed decisions and access genetic counselling.', None, None),
     ]),

    # ===== MORE IMMUNE SYSTEM =====
    ('immune-system', 'What are autoimmune diseases and why is my body attacking itself?',
     'I have been diagnosed with rheumatoid arthritis at 30. My doctor says it is autoimmune. What does this mean?',
     None,
     [('Dr Sarah', 'Mitchell', 'Autoimmune diseases occur when your immune system mistakenly attacks healthy cells in your body. In rheumatoid arthritis, it attacks the lining of your joints, causing inflammation, pain, and swelling. There are over 80 autoimmune conditions. The cause is not fully understood, but genetic factors, environmental triggers, and hormonal factors play a role. Treatment focuses on reducing inflammation and managing symptoms with disease-modifying drugs (DMARDs).', None, None),
      ('NHS', 'Official', 'Rheumatoid arthritis is a long-term condition that causes pain, swelling, and stiffness in the joints. It usually affects the hands, feet, and wrists. Treatment includes disease-modifying anti-rheumatic drugs (DMARDs) to slow the condition and reduce the risk of joint damage. The earlier treatment is started, the more effective it is likely to be.', 'nhs.uk', 'https://www.nhs.uk/conditions/rheumatoid-arthritis/'),
     ]),

    # ===== MORE METABOLIC =====
    ('metabolic', 'What are the symptoms of an underactive thyroid?',
     'I have been gaining weight, feeling exhausted, and my hair is thinning. My mum has thyroid problems. Could I have it too?',
     None,
     [('NHS', 'Official', 'An underactive thyroid (hypothyroidism) is where your thyroid gland does not produce enough hormones. Common symptoms include tiredness, weight gain, feeling cold, dry skin, thinning hair, muscle aches, depression, and a slow heart rate. It is more common in women and runs in families. Diagnosis is made with a simple blood test measuring TSH and T4 levels. Treatment is daily levothyroxine tablets, which you will need for life.', 'nhs.uk', 'https://www.nhs.uk/conditions/underactive-thyroid-hypothyroidism/'),
      ('Rachel', 'Hughes', 'I had exactly these symptoms and it took 2 years to get diagnosed because I kept being told it was stress. Push your GP for a full thyroid panel blood test — not just TSH, but also free T4 and thyroid antibodies. Once I started levothyroxine, it took about 6-8 weeks to feel a difference, but now I feel completely normal. The weight came off gradually too.', None, None),
     ]),

    # ===== MORE EYE =====
    ('eye-vision', 'What is glaucoma and how would I know if I have it?',
     'My optician mentioned checking for glaucoma at my last eye test. I am 42. What is it?',
     None,
     [('NHS', 'Official', 'Glaucoma is a group of eye conditions where the optic nerve is damaged, often by high pressure in the eye. It usually develops slowly and can affect your peripheral (side) vision first. Without treatment, it can lead to blindness. It is more common over 40, in people of African or Caribbean descent, and in those with a family history. Regular eye tests are the best way to detect it early.', 'nhs.uk', 'https://www.nhs.uk/conditions/glaucoma/'),
      ('James', 'Thornton', 'My dad lost peripheral vision in one eye before glaucoma was caught. He had no pain, no symptoms — just gradually lost side vision without realising. Now he uses eye drops daily and his vision is stable. The key takeaway: get your eyes tested every 2 years (free on the NHS if over 40 with a family history). If caught early, eye drops can prevent damage.', None, None),
     ]),

    # ===== MORE WORKERS HEALTH IN GENERAL CATEGORIES =====
    ('general', 'How do I eat healthy on a tight budget?',
     'I am a factory worker earning minimum wage. Fresh food seems so expensive. How can I eat healthily without spending a fortune?',
     None,
     [('Emily', 'Chen', 'I feed my family of 4 healthily on about 40 pounds a week. My tips: 1) Frozen veg is just as nutritious as fresh and costs a fraction. 2) Tinned beans, lentils, and chickpeas are cheap protein powerhouses. 3) Buy a whole chicken and use it for 3 meals. 4) Porridge oats are the cheapest, most nutritious breakfast. 5) Plan meals for the week before shopping and stick to a list. 6) Aldi and Lidl are genuinely cheaper without sacrificing quality. 7) Cook in batches and freeze portions.', None, None),
      ('NHS', 'Official', 'Eating well does not have to be expensive. The Eatwell Guide recommends basing meals on potatoes, bread, rice, pasta, or other starchy carbohydrates, eating at least 5 portions of fruit and veg a day (fresh, frozen, tinned, or dried all count), and choosing beans, pulses, fish, eggs, and lean meat for protein. Frozen and tinned options are often cheaper and just as nutritious.', 'nhs.uk', 'https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/the-eatwell-guide/'),
     ]),

    ('general', 'I work 12-hour shifts and have no energy to cook. What are quick healthy meals?',
     'After a 12-hour factory shift I am too tired to cook. I end up eating takeaways or microwave meals most nights.',
     None,
     [('Ahmed', 'Malik', 'I work 12-hour shifts too and meal prepping on my day off changed everything. I spend 2 hours on Sunday making: 1) A big pot of chicken curry (portions for 4 dinners). 2) Overnight oats in jars for breakfasts. 3) Wraps with pre-cooked chicken, salad, and hummus for lunches. Everything goes in the fridge or freezer. When I get home, it is 5 minutes to microwave a proper meal instead of waiting 30 minutes for a takeaway.', None, None),
      ('David', 'Kapoor', 'Quick meals that take under 10 minutes: scrambled eggs on toast with spinach, beans on toast with cheese, tuna pasta with sweetcorn, a jacket potato (microwave 8 minutes) with beans. None of these cost more than 2 pounds and they are all genuinely nutritious. Save the elaborate cooking for your days off.', None, None),
     ]),

    # ===== MORE CARDIOVASCULAR =====
    ('cardiovascular', 'What lifestyle changes can lower my blood pressure without medication?',
     'My GP says my blood pressure is 150/95 and wants to put me on tablets. Can I try lifestyle changes first?',
     None,
     [('Dr Sarah', 'Mitchell', 'At 150/95, lifestyle changes can make a real difference. The biggest impact comes from: 1) Reducing salt to under 6g per day — check labels, processed foods are the main culprit. 2) Losing weight if overweight — even 5kg can drop your reading by 5-10 points. 3) Exercise — 30 minutes of brisk walking 5 times a week. 4) Limiting alcohol. 5) Reducing caffeine. Most GPs will give you 3-6 months to try this before starting medication. Monitor at home to track progress.', None, None),
      ('NHS', 'Official', 'High blood pressure can often be prevented or reduced by eating healthily, maintaining a healthy weight, exercising regularly, drinking less alcohol, and stopping smoking. Cutting down on salt is one of the most effective changes. The NHS recommends eating no more than 6g of salt a day. If lifestyle changes alone are not enough, your doctor may recommend medication.', 'nhs.uk', 'https://www.nhs.uk/conditions/high-blood-pressure-hypertension/prevention/'),
     ]),

    # ===== MORE INFECTIONS =====
    ('infections', 'How do I know if a wound is infected?',
     'I cut my hand on a machine at work 3 days ago. It is now red, swollen, and warm to touch. Should I be worried?',
     None,
     [('NHS', 'Official', 'Signs that a wound may be infected include increasing redness, swelling, or pain around the wound, the area feeling warm, pus or discharge coming from the wound, a high temperature, and red streaks spreading from the wound. If you notice any of these signs, see your GP urgently or go to a minor injuries unit. Infected wounds can become serious if not treated with antibiotics.', 'nhs.uk', 'https://www.nhs.uk/conditions/infected-wounds/'),
      ('Dr Sarah', 'Mitchell', 'Based on your description — redness, swelling, and warmth at 3 days — this wound may be infected and you should see a GP or walk-in centre today, not tomorrow. Red streaks spreading up your arm or a high temperature mean go to A&E immediately. Also make sure this was recorded in your workplace accident book and check when your last tetanus vaccination was.', None, None),
     ]),

    # ===== MORE SKIN =====
    ('skin', 'Why do I keep getting boils and how can I prevent them?',
     'I get painful boils on my inner thighs and armpits regularly. It is embarrassing and very painful.',
     None,
     [('NHS', 'Official', 'A boil is a painful, pus-filled bump under the skin caused by infected hair follicles. They are most common in areas where you sweat, have friction, or shave. To help prevent boils: wash the area gently with antibacterial soap, keep the area clean and dry, avoid squeezing or bursting boils, use a fresh towel each time, and wash bedding and clothes regularly. See your GP if boils keep coming back — they may test for diabetes or refer you to a dermatologist.', 'nhs.uk', 'https://www.nhs.uk/conditions/boils/'),
      ('Priya', 'Sharma', 'I suffered with recurrent boils for a year before my GP diagnosed hidradenitis suppurativa (HS). It is an under-diagnosed condition, especially in areas like armpits, groin, and under the breasts. If boils keep returning in the same areas, ask your GP specifically about HS. It is not just boils — it is a chronic inflammatory skin condition that needs proper treatment.', None, None),
     ]),

    # ===== MORE EMOTIONS =====
    ('emotions', 'How do I cope with grief after losing someone close?',
     'I lost my dad 3 months ago and I cannot stop crying. Some days I cannot get out of bed. People say I should be over it by now.',
     None,
     [('Emily', 'Chen', 'Three months is nothing in grief terms. There is no timeline for grief and anyone who says otherwise has either never lost someone close or has forgotten what it felt like. Let yourself feel whatever you feel — anger, sadness, numbness, guilt — it is all normal. Be gentle with yourself. Eat even when you do not want to. Get outside even if just for 5 minutes.', None, None),
      ('NHS', 'Official', 'Grief is a natural response to loss. There is no right or wrong way to grieve, and no set timeline. It is common to feel shock, sadness, guilt, anger, anxiety, and physical symptoms like tiredness, poor appetite, and difficulty sleeping. If grief is significantly affecting your daily life after several months, speaking to your GP can help. They can refer you to bereavement counselling. Cruse Bereavement Support (0808 808 1677) offers free support.', 'nhs.uk', 'https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/grief-bereavement-loss/'),
     ]),
]
