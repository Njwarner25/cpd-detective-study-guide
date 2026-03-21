import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


async def seed_g03_06_questions(ext_db=None):
    """Seed 50 I/O-style questions from the 2026 Part 2 Study Guide.

    Covers ALL general orders referenced in G03-06:
      - G03-06: Firearm Discharge & OID Response/Investigation
      - G03-02: De-escalation, Response to Resistance, Use of Force
      - G03-02-01: Response to Resistance and Force Options
      - G03-02-03: Firearm Discharge — Authorized Use and Post-Discharge
      - G03-02-08: Department Review of Use of Force Incidents
      - G04-02: Crime Scene Protection and Processing
      - S03-14: Body Worn Cameras

    This study guide has been compiled based on CPD General Order G03-06
    and all directives referenced within that document.

    SCORING (I/O Solutions Format):
      +2 = Best/correct answer
      +1 = Acceptable but not ideal
       0 = Neutral / no impact
      -1 = Poor choice
      -2 = Worst choice / policy violation

    GRADING SCALE:
      90-100% = A (Superior)
      80-89%  = B (Above Average)
      70-79%  = C (Average)
      60-69%  = D (Below Average)
      <60%    = F (Failing)

    Args:
        ext_db: Optional external database connection.
    """
    global db
    if ext_db is not None:
        db = ext_db

    now = datetime.now(timezone.utc)

    # ======== CATEGORY ========
    category = {
        "category_id": "cat_g03_06_firearm_discharge",
        "name": "2026 Part 2: General Orders Study Guide",
        "description": (
            "2026 Part 2 Study Guide — 50 questions covering CPD General Orders referenced in "
            "G03-06: Firearm Discharge and Officer-Involved Death Incident Response. "
            "This study guide has been compiled based on G03-06 and all directives referenced "
            "within that document, including G03-02 (Use of Force), G03-02-01 (Force Options), "
            "G03-02-03 (Authorized Firearm Use), G03-02-08 (Review of Use of Force), "
            "G04-02 (Crime Scene Protection), and S03-14 (Body Worn Cameras). "
            "Questions are scored using the I/O Solutions methodology. "
            "AI grading provides a detailed response after each question is completed."
        ),
        "order": 30,
        "exam_source": "2026 Part 2 Detective Exam Study Guide",
        "scoring_method": "io_solutions",
        "grading_scale": {
            "A": {"min": 90, "max": 100, "label": "Superior"},
            "B": {"min": 80, "max": 89, "label": "Above Average"},
            "C": {"min": 70, "max": 79, "label": "Average"},
            "D": {"min": 60, "max": 69, "label": "Below Average"},
            "F": {"min": 0, "max": 59, "label": "Failing"},
        },
        "leaderboard_enabled": True,
    }

    await db.categories.update_one(
        {"category_id": category["category_id"]},
        {"$set": category},
        upsert=True
    )

    # ================================================================
    # 50 QUESTIONS — 2026 Part 2 General Orders Study Guide
    # ================================================================

    questions = [
        # ============================================================
        # G03-02: DE-ESCALATION, RESPONSE TO RESISTANCE, USE OF FORCE
        # ============================================================

        # --- Q1 ---
        {
            "question_id": "go_q01",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "De-escalation — Primary Objective",
            "content": (
                "You respond to a call of a man standing on a bridge overpass threatening "
                "to jump. He is unarmed and does not pose a threat to anyone other than himself. "
                "Multiple officers are on scene."
            ),
            "question": "Under G03-02, what is the MOST appropriate initial action?",
            "options": [
                {"label": "A", "text": "Immediately rush the subject and physically restrain him for his own safety"},
                {"label": "B", "text": "Establish a dialogue, employ de-escalation techniques, and request a CIT-trained officer"},
                {"label": "C", "text": "Deploy a Taser to incapacitate the subject before he jumps"},
                {"label": "D", "text": "Maintain distance and wait for a supervisor before taking any action"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02 mandates that officers use de-escalation techniques "
                "as a first response whenever safe and feasible. Crisis Intervention Team (CIT) "
                "trained officers should be requested for behavioral health crises. The goal is "
                "to reduce the intensity of the situation through communication.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Rushing could cause the subject to jump — directly contrary to de-escalation.\n"
                "C (-2): Taser use near an elevated edge creates serious risk of a fatal fall.\n"
                "D (-1): Waiting passively without engaging is not de-escalation — officers should "
                "begin dialogue immediately."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-02, Section III (De-escalation); CIT Protocol",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q2 ---
        {
            "question_id": "go_q02",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force — Proportionality Standard",
            "content": (
                "An officer encounters a shoplifting suspect who is walking away from the store. "
                "The suspect is carrying a bag of stolen merchandise valued at approximately $40. "
                "The suspect ignores verbal commands to stop."
            ),
            "question": "Under G03-02, what is the MOST appropriate response?",
            "options": [
                {"label": "A", "text": "Deploy OC spray to stop the suspect from fleeing"},
                {"label": "B", "text": "Follow the suspect while broadcasting a description and direction of travel"},
                {"label": "C", "text": "Tackle the suspect to prevent escape with the stolen property"},
                {"label": "D", "text": "Draw your firearm and order the suspect to stop"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02 requires force to be proportional to the threat. "
                "A misdemeanor shoplifting suspect walking away does not present an imminent threat "
                "of death or great bodily harm. Following and broadcasting allows apprehension "
                "without unnecessary force. Tennessee v. Garner prohibits deadly force for "
                "non-dangerous fleeing felons — even more so for misdemeanors.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): OC spray is disproportionate for a non-violent, non-threatening misdemeanor.\n"
                "C (-1): Physical takedown risks injury and is disproportionate.\n"
                "D (-2): Drawing a firearm for petty theft is a gross overreaction and policy violation."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-02, Section IV (Proportionality); Tennessee v. Garner",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q3 ---
        {
            "question_id": "go_q03",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force — Duty to Intervene",
            "content": (
                "You observe a fellow officer applying a chokehold to a handcuffed subject who "
                "is no longer resisting. The subject is turning blue and gasping for air. "
                "Your partner tells you to mind your own business."
            ),
            "question": "Under G03-02, what is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Physically intervene to stop the chokehold and render aid to the subject"},
                {"label": "B", "text": "Verbally order the officer to release the chokehold immediately"},
                {"label": "C", "text": "Comply with your partner's request and look the other way"},
                {"label": "D", "text": "Request a supervisor to the scene and document what you witnessed"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER (LEAST APPROPRIATE): C. G03-02 imposes an affirmative DUTY TO "
                "INTERVENE when an officer observes another officer using excessive or unauthorized "
                "force. Looking the other way is a direct violation of department policy and can "
                "result in discipline up to and including separation. Chokeholds are prohibited "
                "under CPD policy.\n\n"
                "WHY OTHER ANSWERS ARE BETTER:\n"
                "A (+2): Physical intervention is the best response when someone's life is in danger.\n"
                "B (+1): Verbal commands are appropriate but may not be sufficient alone.\n"
                "D (+1): Requesting a supervisor is appropriate but the immediate threat must be "
                "addressed first."
            ),
            "io_scores": {"A": 2, "B": 1, "C": -2, "D": 1},
            "difficulty": "hard",
            "reference": "G03-02, Section V (Duty to Intervene); Prohibited Force Techniques",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q4 ---
        {
            "question_id": "go_q04",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force — Reporting Requirements",
            "content": (
                "During an arrest, you use an emergency takedown to control a combative subject. "
                "The subject sustains a minor scrape on his elbow but is otherwise uninjured. "
                "The arrest is completed without further incident."
            ),
            "question": "What is the MOST appropriate documentation requirement under G03-02?",
            "options": [
                {"label": "A", "text": "No documentation needed since the injury was minor and incidental to a lawful arrest"},
                {"label": "B", "text": "Complete a Tactical Response Report (TRR) documenting the force used and the subject's injury"},
                {"label": "C", "text": "Include a brief note in the arrest report mentioning the takedown"},
                {"label": "D", "text": "Only document if the subject files a complaint about the force used"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02 requires a TRR for ANY use of force beyond verbal "
                "commands, including emergency takedowns. The TRR must document the type of force "
                "used, the subject's actions that necessitated force, and any injuries sustained. "
                "This applies regardless of how minor the injury.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): All force beyond verbal commands requires TRR documentation.\n"
                "C (-1): An arrest report note is insufficient — a TRR is specifically required.\n"
                "D (-2): Reactive documentation violates the mandatory reporting requirement."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-02, Section VI (Reporting Requirements); TRR Procedures",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q5 ---
        {
            "question_id": "go_q05",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force — Force Mitigation",
            "content": (
                "You and two other officers are attempting to take a burglary suspect into "
                "custody. The suspect is verbally aggressive and clenching his fists but has "
                "not made any physical moves toward the officers. No weapons are visible."
            ),
            "question": "Under G03-02, what is the MOST appropriate approach?",
            "options": [
                {"label": "A", "text": "Use verbal direction and positioning to create time and distance while maintaining a tactical advantage"},
                {"label": "B", "text": "Immediately take the suspect to the ground before he becomes physically violent"},
                {"label": "C", "text": "Deploy a Taser preemptively since he is clenching his fists"},
                {"label": "D", "text": "Withdraw from the scene and set up a perimeter until the suspect calms down"}
            ],
            "correct_answer": "A",
            "explanation": (
                "CORRECT ANSWER: A. G03-02 emphasizes force mitigation — using time, distance, "
                "and positioning to reduce the need for force. Verbal aggression and clenched fists "
                "alone do not justify physical force. With three officers present, the numerical "
                "advantage supports a verbal approach. Creating distance provides reaction time.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "B (-2): Preemptive physical force is not justified without an active physical threat.\n"
                "C (-2): Taser deployment requires active resistance or an imminent threat.\n"
                "D (-1): Complete withdrawal abandons the lawful arrest — officers should maintain "
                "presence while de-escalating."
            ),
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-02, Section III (Force Mitigation Principles)",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # ============================================================
        # G03-02-01: RESPONSE TO RESISTANCE AND FORCE OPTIONS
        # ============================================================

        # --- Q6 ---
        {
            "question_id": "go_q06",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — OC Spray Deployment",
            "content": (
                "A subject is passively resisting arrest by going limp and refusing to stand. "
                "The subject is not making any aggressive movements and is not threatening "
                "officers. Two officers are on scene."
            ),
            "question": "Under G03-02-01, is OC spray deployment appropriate?",
            "options": [
                {"label": "A", "text": "Yes, OC spray can be used for any level of resistance to gain compliance"},
                {"label": "B", "text": "No, OC spray requires active resistance or an assaultive threat — passive resistance does not justify chemical agents"},
                {"label": "C", "text": "Yes, but only if the officer gives a verbal warning first"},
                {"label": "D", "text": "Only if a supervisor authorizes it on scene"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-01 establishes a force continuum. OC spray is classified "
                "as an intermediate force option appropriate for active resistance or above. Passive "
                "resistance (going limp, not moving) should be addressed with verbal direction and "
                "physical escort techniques — not chemical agents.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): OC spray is NOT authorized for passive resistance.\n"
                "C (-1): Even with a warning, OC spray is disproportionate for passive resistance.\n"
                "D (-1): Supervisor authorization does not change the force-level analysis."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-02-01, Section IV (Force Options); OC Spray Guidelines",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q7 ---
        {
            "question_id": "go_q07",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — Taser Restrictions",
            "content": (
                "Officers are attempting to arrest a suspect who is actively resisting. "
                "The suspect is standing at the edge of an elevated CTA platform, approximately "
                "15 feet above street level."
            ),
            "question": "Under G03-02-01, what restriction applies to Taser deployment in this scenario?",
            "options": [
                {"label": "A", "text": "No restriction — the Taser can be used since the suspect is actively resisting"},
                {"label": "B", "text": "The Taser should NOT be deployed because the subject is in an elevated position where a fall could cause serious injury or death"},
                {"label": "C", "text": "The Taser can be used if officers are positioned to catch the suspect"},
                {"label": "D", "text": "Only a supervisor can authorize Taser use in elevated positions"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-01 specifically prohibits Taser use when the subject "
                "is in an elevated position where incapacitation could result in a fall causing "
                "serious injury or death. This includes rooftops, bridges, elevated platforms, "
                "ladders, and similar positions. Neuromuscular incapacitation causes an uncontrolled "
                "fall.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): The elevated position restriction overrides the resistance level.\n"
                "C (-1): Attempting to catch a falling incapacitated person is impractical and unsafe.\n"
                "D (-1): This is a categorical prohibition, not a supervisor-discretion issue."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "G03-02-01, Section V (Taser Restrictions); Elevated Positions",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q8 ---
        {
            "question_id": "go_q08",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — Impact Weapon Use",
            "content": (
                "An officer is struggling with an actively resisting subject during an arrest. "
                "The officer draws his baton. The subject has his arms tucked under his body "
                "while prone on the ground."
            ),
            "question": "Under G03-02-01, which target area is LEAST appropriate for baton strikes?",
            "options": [
                {"label": "A", "text": "The subject's thigh (large muscle group)"},
                {"label": "B", "text": "The subject's head, neck, or spine"},
                {"label": "C", "text": "The subject's calf area"},
                {"label": "D", "text": "The subject's forearm to release the tucked arms"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER (LEAST APPROPRIATE): B. G03-02-01 explicitly prohibits baton "
                "strikes to the head, neck, throat, and spine unless deadly force is justified. "
                "These are considered lethal target areas. Baton strikes should target large "
                "muscle groups (thigh, calf, forearm) to gain compliance while minimizing risk "
                "of serious injury.\n\n"
                "WHY OTHER ANSWERS ARE BETTER:\n"
                "A (+2): Thigh is an approved large muscle group target.\n"
                "C (+1): Calf is an acceptable secondary target area.\n"
                "D (+1): Forearm strikes to release tucked arms are a recognized technique."
            ),
            "io_scores": {"A": 2, "B": -2, "C": 1, "D": 1},
            "difficulty": "medium",
            "reference": "G03-02-01, Section VI (Impact Weapons); Prohibited Target Areas",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q9 ---
        {
            "question_id": "go_q09",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — Post-Taser Medical Protocol",
            "content": (
                "An officer has successfully deployed a Taser on an actively resisting suspect. "
                "The suspect is now in custody and the Taser probes are still embedded in the "
                "suspect's torso."
            ),
            "question": "What is the MOST appropriate medical protocol under G03-02-01?",
            "options": [
                {"label": "A", "text": "Remove the probes yourself at the scene and transport to the district for processing"},
                {"label": "B", "text": "Leave the probes in place and request EMS for medical evaluation and probe removal"},
                {"label": "C", "text": "Remove the probes and apply first aid if there is minimal bleeding"},
                {"label": "D", "text": "Only request EMS if the suspect complains of pain or difficulty breathing"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-01 requires that Taser probes embedded in a subject's "
                "skin be removed ONLY by qualified medical personnel. EMS must be requested for "
                "ALL subjects who have been Tased, regardless of whether the subject complains of "
                "injury. This is a mandatory medical evaluation — not discretionary.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Officers should NOT remove embedded probes — risk of tissue damage.\n"
                "C (-2): Same issue — probes must be removed by medical personnel.\n"
                "D (-1): EMS is mandatory for ALL Taser deployments, not just when complaints arise."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-02-01, Section V (Post-Taser Procedures); Medical Protocol",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q10 ---
        {
            "question_id": "go_q10",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — Positional Asphyxia Awareness",
            "content": (
                "After a foot chase and physical struggle, officers place a large, obese "
                "subject in handcuffs while he is lying face-down (prone position). The subject "
                "is breathing heavily and complaining he cannot breathe."
            ),
            "question": "Under G03-02-01, what is the MOST appropriate immediate action?",
            "options": [
                {"label": "A", "text": "Keep the subject prone until transport arrives to maintain control"},
                {"label": "B", "text": "Immediately place the subject on his side or in a seated position and monitor breathing while requesting EMS"},
                {"label": "C", "text": "Apply additional pressure to the subject's back to prevent him from getting up"},
                {"label": "D", "text": "Tell the subject that if he can talk, he can breathe"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-01 mandates awareness of positional asphyxia risk. "
                "Once handcuffed, subjects must be moved from a prone position as soon as "
                "practicable — especially if they are obese, under the influence, or have been "
                "in a physical struggle. The recovery position (on their side) or seated upright "
                "allows proper breathing. EMS must be requested.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Extended prone positioning after exertion can be fatal.\n"
                "C (-2): Additional pressure on the back directly increases asphyxia risk.\n"
                "D (-2): 'If you can talk you can breathe' is a dangerous myth — subjects have "
                "died in custody while still speaking."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "G03-02-01, Section VII (Positional Asphyxia); In-Custody Deaths",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # ============================================================
        # G03-02-03: FIREARM DISCHARGE — AUTHORIZED USE
        # ============================================================

        # --- Q11 ---
        {
            "question_id": "go_q11",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Authorized Firearm Use — Fleeing Felon",
            "content": (
                "Officers are pursuing a suspect who just committed an armed robbery. The "
                "suspect discards the firearm during the foot chase and continues running. "
                "The suspect is now unarmed and running through a residential neighborhood."
            ),
            "question": "Under G03-02-03, is deadly force authorized at this point?",
            "options": [
                {"label": "A", "text": "Yes, because the suspect committed an armed robbery which is a forcible felony"},
                {"label": "B", "text": "No, because the suspect discarded the weapon and no longer poses an imminent threat of death or great bodily harm to officers or others"},
                {"label": "C", "text": "Yes, but only if the officer reasonably believes the suspect will rearm himself"},
                {"label": "D", "text": "Only if a supervisor authorizes the use of deadly force over the radio"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-03 authorizes deadly force ONLY when the subject poses "
                "an imminent threat of death or great bodily harm. Once the suspect discards the "
                "weapon and is running away unarmed, the imminent threat has diminished. The prior "
                "armed robbery alone does not justify deadly force against a now-unarmed fleeing "
                "suspect. This aligns with Tennessee v. Garner.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): The prior crime does not authorize deadly force once the threat has ended.\n"
                "C (-1): Speculative belief about rearming is insufficient — must be imminent threat.\n"
                "D (-1): Deadly force decisions cannot be delegated to supervisors over the radio."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "G03-02-03, Section III (Authorized Use); Tennessee v. Garner",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q12 ---
        {
            "question_id": "go_q12",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Firearm Discharge — Shooting at Vehicles",
            "content": (
                "During a traffic stop, a suspect puts the car in drive and begins to accelerate "
                "toward officers. One officer is directly in the vehicle's path."
            ),
            "question": "Under G03-02-03, when is shooting at a moving vehicle authorized?",
            "options": [
                {"label": "A", "text": "Anytime a vehicle is used as a weapon against an officer"},
                {"label": "B", "text": "Only when the vehicle poses an imminent threat of death or great bodily harm AND the officer cannot move to safety"},
                {"label": "C", "text": "Never — officers must always move out of the vehicle's path"},
                {"label": "D", "text": "Only after a supervisor has been notified and approves"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-03 restricts shooting at moving vehicles. Officers "
                "should attempt to move out of the vehicle's path rather than discharge their "
                "firearm. Shooting is only authorized when the vehicle presents an imminent threat "
                "of death or great bodily harm AND the officer cannot reasonably move to safety. "
                "Additionally, officers must consider the risk to bystanders.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): 'Anytime' is too broad — must also consider ability to move to safety.\n"
                "C (-1): There may be situations where moving to safety is impossible.\n"
                "D (-2): Supervisor approval is not a prerequisite for deadly force in an imminent threat."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-02-03, Section IV (Vehicles); Shooting at Moving Vehicles",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q13 ---
        {
            "question_id": "go_q13",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Firearm Discharge — Warning Shots",
            "content": (
                "An officer is pursuing a fleeing suspect in a crowded public area. "
                "The suspect has a knife and is running toward a group of pedestrians."
            ),
            "question": "Under G03-02-03, which action is LEAST appropriate?",
            "options": [
                {"label": "A", "text": "Fire a warning shot into the air to get the suspect to stop"},
                {"label": "B", "text": "Give loud verbal commands to the suspect and bystanders"},
                {"label": "C", "text": "Use deadly force if the suspect is about to stab a bystander"},
                {"label": "D", "text": "Attempt to close distance and use a Taser if tactically feasible"}
            ],
            "correct_answer": "A",
            "explanation": (
                "CORRECT ANSWER (LEAST APPROPRIATE): A. G03-02-03 explicitly PROHIBITS warning "
                "shots. Warning shots create a serious risk to bystanders from falling bullets "
                "and ricochets, especially in a crowded area. Every round fired must be aimed "
                "at a specific target.\n\n"
                "WHY OTHER ANSWERS ARE BETTER:\n"
                "B (+1): Verbal commands are always appropriate.\n"
                "C (+2): Deadly force is justified when there is imminent threat to a third party.\n"
                "D (+1): Less-lethal options should be considered when feasible."
            ),
            "io_scores": {"A": -2, "B": 1, "C": 2, "D": 1},
            "difficulty": "medium",
            "reference": "G03-02-03, Section V (Prohibited Discharges); Warning Shots",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q14 ---
        {
            "question_id": "go_q14",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Post-Discharge — Immediate Obligations",
            "content": (
                "An officer has just discharged his firearm at a subject who was pointing a "
                "weapon at the officer. The subject is down and not moving. The threat appears "
                "to be neutralized."
            ),
            "question": "Under G03-02-03, what is the officer's FIRST obligation after the discharge?",
            "options": [
                {"label": "A", "text": "Holster your weapon and begin writing notes about what happened"},
                {"label": "B", "text": "Ensure the scene is safe, render first aid to the subject, and request EMS immediately"},
                {"label": "C", "text": "Call your union representative before speaking to anyone"},
                {"label": "D", "text": "Secure the subject's weapon and begin collecting other evidence"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-03 requires that after a firearm discharge, once the "
                "scene is safe, the officer's first obligation is to render first aid and request "
                "medical assistance. The duty to provide medical care applies to ALL persons — "
                "including the subject. This is both a policy requirement and a constitutional "
                "obligation (deliberate indifference standard).\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Writing notes is important but not the FIRST priority — medical aid comes first.\n"
                "C (-1): Union representation is a right but does not supersede the duty to render aid.\n"
                "D (-1): Evidence preservation matters but is secondary to medical care."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-02-03, Section VI (Post-Discharge Duties); Duty to Render Aid",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q15 ---
        {
            "question_id": "go_q15",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Firearm Discharge — Off-Duty Considerations",
            "content": (
                "An off-duty officer in plain clothes witnesses an armed robbery at a gas "
                "station. The armed suspect exits the store and begins walking toward his "
                "vehicle. No one else appears to be in immediate danger."
            ),
            "question": "Under G03-02-03, what is the MOST appropriate action for the off-duty officer?",
            "options": [
                {"label": "A", "text": "Draw your weapon and confront the suspect to effect an arrest"},
                {"label": "B", "text": "Be a good witness, call 911 with suspect and vehicle descriptions, and do not engage"},
                {"label": "C", "text": "Follow the suspect's vehicle and relay the location to dispatchers"},
                {"label": "D", "text": "Block the suspect's vehicle with your personal car to prevent escape"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-03 strongly discourages off-duty officers from "
                "engaging in enforcement action unless there is an imminent threat to life. The "
                "suspect is leaving and no one is in immediate danger. Off-duty officers in plain "
                "clothes risk being misidentified as threats by responding officers. Being a good "
                "witness is the safest and most effective response.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Confronting an armed suspect in plain clothes creates extreme danger.\n"
                "C (-1): Vehicle pursuits are dangerous and the officer lacks radio/backup.\n"
                "D (-2): Blocking a suspect vehicle escalates the situation unnecessarily."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-02-03, Section VII (Off-Duty Considerations)",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # ============================================================
        # G03-02-08: DEPARTMENT REVIEW OF USE OF FORCE
        # ============================================================

        # --- Q16 ---
        {
            "question_id": "go_q16",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force Review — TRR Investigation",
            "content": (
                "A sergeant is assigned to investigate a Tactical Response Report (TRR) "
                "submitted by one of his officers following a use of force incident. The "
                "sergeant was not present during the incident."
            ),
            "question": "Under G03-02-08, what is the reviewing sergeant's PRIMARY responsibility?",
            "options": [
                {"label": "A", "text": "Accept the TRR as written if the officer has a good track record"},
                {"label": "B", "text": "Conduct an independent investigation including reviewing BWC footage, interviewing witnesses, and determining if the force was within policy"},
                {"label": "C", "text": "Simply verify the TRR paperwork is complete and forward it to the lieutenant"},
                {"label": "D", "text": "Only investigate if the subject files a complaint about the force used"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-08 requires the reviewing supervisor to conduct an "
                "independent investigation of every TRR. This includes reviewing all available "
                "video (BWC, POD, third-party), interviewing the involved officers and witnesses, "
                "examining injuries, and making an independent determination of whether the force "
                "was within policy. The review must be thorough and objective.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Officer reputation does not replace independent investigation.\n"
                "C (-1): Paperwork review alone is insufficient — substantive investigation required.\n"
                "D (-2): Every TRR must be investigated regardless of complaints."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-02-08, Section III (Supervisory Review); TRR Investigation",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q17 ---
        {
            "question_id": "go_q17",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force Review — BWC in TRR Investigation",
            "content": (
                "While reviewing a TRR, the sergeant discovers that the involved officer's "
                "body-worn camera was not activated during the use of force incident. The "
                "officer claims he forgot to activate it due to the rapidly evolving situation."
            ),
            "question": "Under G03-02-08, what is the MOST appropriate response?",
            "options": [
                {"label": "A", "text": "Accept the explanation and note it in the TRR review — rapidly evolving situations are understandable"},
                {"label": "B", "text": "Document the BWC non-activation as a separate policy violation, review all other available video, and interview witnesses to corroborate the officer's account"},
                {"label": "C", "text": "Automatically find the use of force out of policy due to the lack of BWC footage"},
                {"label": "D", "text": "Have the officer write a supplemental report explaining why BWC was not activated and close the review"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-08 requires that BWC non-activation be documented and "
                "addressed as a separate issue. The TRR review must still be completed using all "
                "other available evidence. The failure to activate BWC does not automatically make "
                "the force out of policy, nor does it excuse the sergeant from a thorough review.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): The explanation may or may not be valid, but the non-activation must still "
                "be formally documented as a potential violation.\n"
                "C (-1): Lack of BWC alone does not determine whether force was within policy.\n"
                "D (-1): A supplemental report is insufficient — the TRR review must be completed "
                "independently."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "G03-02-08, Section IV (Video Review); S03-14 (BWC Activation)",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q18 ---
        {
            "question_id": "go_q18",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force Review — Findings and Recommendations",
            "content": (
                "After conducting a thorough TRR investigation, the reviewing sergeant "
                "determines that the officer used force that was not proportional to the "
                "resistance encountered. The officer punched a handcuffed subject in the face "
                "while the subject was only verbally abusive."
            ),
            "question": "Under G03-02-08, which action is LEAST appropriate?",
            "options": [
                {"label": "A", "text": "Find the force within policy because the subject was being verbally abusive"},
                {"label": "B", "text": "Refer the matter to COPA for further investigation"},
                {"label": "C", "text": "Document the finding as out of policy and recommend corrective action or discipline"},
                {"label": "D", "text": "Notify the chain of command and ensure the finding is reviewed at each level"}
            ],
            "correct_answer": "A",
            "explanation": (
                "CORRECT ANSWER (LEAST APPROPRIATE): A. G03-02-08 requires findings to be based "
                "on the proportionality of force. Verbal abuse alone NEVER justifies physical "
                "force, especially against a handcuffed subject. Finding this within policy would "
                "be a dereliction of supervisory duty and a misapplication of the force policy.\n\n"
                "WHY OTHER ANSWERS ARE BETTER:\n"
                "B (+1): COPA referral is appropriate for excessive force findings.\n"
                "C (+2): Documenting as out of policy with corrective action is the proper response.\n"
                "D (+1): Chain of command notification ensures proper oversight."
            ),
            "io_scores": {"A": -2, "B": 1, "C": 2, "D": 1},
            "difficulty": "medium",
            "reference": "G03-02-08, Section V (Findings); Proportionality Standard",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # ============================================================
        # G04-02: CRIME SCENE PROTECTION AND PROCESSING
        # ============================================================

        # --- Q19 ---
        {
            "question_id": "go_q19",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — First Responding Officer Duties",
            "content": (
                "You are the first officer to arrive at a reported homicide. The victim is "
                "lying in the living room of an apartment. A family member is performing CPR. "
                "You confirm the victim has no pulse."
            ),
            "question": "Under G04-02, what is the MOST appropriate sequence of actions?",
            "options": [
                {"label": "A", "text": "Confirm death, begin processing the crime scene immediately since evidence may be lost"},
                {"label": "B", "text": "Confirm death, secure the scene by establishing an inner and outer perimeter, protect evidence pathways, and request detectives and ET"},
                {"label": "C", "text": "Confirm death, then interview the family member who was performing CPR before securing the scene"},
                {"label": "D", "text": "Leave the victim in place and wait outside for detectives to arrive before entering the scene"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G04-02 establishes clear first-responder duties at crime "
                "scenes. After confirming death: (1) secure the scene with inner/outer perimeters, "
                "(2) protect evidence pathways by limiting foot traffic, (3) start a crime scene "
                "log of everyone who enters, and (4) request detectives and Evidence Technicians. "
                "Scene security is the foundation of all subsequent investigation.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Beat officers do NOT process crime scenes — that's for detectives and ET.\n"
                "C (-1): Interviews are important but securing the scene takes priority.\n"
                "D (-1): Officers must enter to confirm death and begin securing — waiting outside "
                "leaves the scene unprotected."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G04-02, Section III (First Responder Duties); Scene Security",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q20 ---
        {
            "question_id": "go_q20",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — Evidence Integrity and Chain of Custody",
            "content": (
                "At an OID scene, a detective notices that a responding officer picked up "
                "shell casings from the street and placed them on the hood of a squad car "
                "'so they wouldn't get run over.'"
            ),
            "question": "Under G04-02, what is the MOST appropriate response?",
            "options": [
                {"label": "A", "text": "Thank the officer for preserving the evidence and continue processing"},
                {"label": "B", "text": "Document the officer's actions, the original locations of the casings if known, photograph current positions, and note the chain of custody breach in the crime scene report"},
                {"label": "C", "text": "Return the casings to their approximate original locations and photograph them there"},
                {"label": "D", "text": "Discard the casings since their evidentiary value is now compromised"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G04-02 requires meticulous documentation of evidence handling. "
                "When evidence has been moved, the detective must document who moved it, from where, "
                "to where, and when. The original positions should be noted if they can be determined. "
                "The chain of custody breach must be documented but does NOT destroy evidentiary value — "
                "the evidence is still important.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): The officer's action was improper — it should be documented, not praised.\n"
                "C (-2): Returning evidence to 'approximate' locations creates false documentation.\n"
                "D (-2): Discarding evidence is destruction — the casings still have forensic value."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "G04-02, Section IV (Evidence Handling); Chain of Custody",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q21 ---
        {
            "question_id": "go_q21",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — Expanding the Scene",
            "content": (
                "Detectives are processing a shooting scene on a residential street. A witness "
                "approaches and says 'the shooter ran through the alley and dropped something "
                "near the dumpster two blocks east.' The current crime scene perimeter does not "
                "include that alley."
            ),
            "question": "Under G04-02, which action is LEAST appropriate?",
            "options": [
                {"label": "A", "text": "Immediately expand the crime scene perimeter to include the alley and dumpster area"},
                {"label": "B", "text": "Tell the witness the alley is outside your crime scene and it's not your responsibility"},
                {"label": "C", "text": "Send officers to secure the alley and dumpster area as an extension of the crime scene"},
                {"label": "D", "text": "Document the witness information and coordinate with ET to process the secondary location"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER (LEAST APPROPRIATE): B. G04-02 requires detectives to expand "
                "crime scenes when new evidence or information indicates additional areas are "
                "relevant. Dismissing a witness tip about discarded evidence is a failure of "
                "investigative duty. Crime scenes are not fixed — they grow as information develops.\n\n"
                "WHY OTHER ANSWERS ARE BETTER:\n"
                "A (+1): Expanding the perimeter is appropriate but may be impractical for two blocks.\n"
                "C (+2): Sending officers to secure the secondary location is the best immediate response.\n"
                "D (+1): Proper documentation and ET coordination ensures thorough processing."
            ),
            "io_scores": {"A": 1, "B": -2, "C": 2, "D": 1},
            "difficulty": "medium",
            "reference": "G04-02, Section V (Scene Expansion); Secondary Crime Scenes",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q22 ---
        {
            "question_id": "go_q22",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — Crime Scene Log",
            "content": (
                "You are the officer assigned to maintain the crime scene log at a homicide "
                "scene. A deputy chief arrives and wants to enter the crime scene to view the "
                "victim. He tells you not to log his entry because he doesn't want it documented."
            ),
            "question": "Under G04-02, what is the MOST appropriate response?",
            "options": [
                {"label": "A", "text": "Allow the deputy chief to enter without logging — he outranks you"},
                {"label": "B", "text": "Respectfully inform the deputy chief that ALL persons entering the scene must be logged per G04-02 and document his entry"},
                {"label": "C", "text": "Log the entry but mark it as 'anonymous' to avoid conflict"},
                {"label": "D", "text": "Refuse to let the deputy chief enter the scene entirely"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G04-02 requires that EVERY person entering the crime scene "
                "be documented on the crime scene log — no exceptions, regardless of rank. This "
                "ensures evidence integrity and accountability. The officer should be respectful "
                "but firm in following the policy.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Rank does not exempt anyone from crime scene logging requirements.\n"
                "C (-1): 'Anonymous' entries undermine the purpose of the log.\n"
                "D (-1): Refusing entry entirely may not be appropriate — the deputy chief can enter "
                "if he has a legitimate purpose, but he MUST be logged."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "G04-02, Section III (Crime Scene Log); Documentation Requirements",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # ============================================================
        # S03-14: BODY WORN CAMERAS
        # ============================================================

        # --- Q23 ---
        {
            "question_id": "go_q23",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "BWC — Mandatory Activation Events",
            "content": (
                "An officer equipped with a body-worn camera is dispatched to a call of a "
                "disturbance. While en route, the officer receives updated information that "
                "the disturbance involves a domestic battery in progress."
            ),
            "question": "Under S03-14, when must the officer activate the BWC?",
            "options": [
                {"label": "A", "text": "Upon arrival at the scene"},
                {"label": "B", "text": "Only if force is used during the encounter"},
                {"label": "C", "text": "As soon as reasonably practical — before exiting the vehicle or making contact"},
                {"label": "D", "text": "After making initial contact with the parties involved"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. S03-14 requires BWC activation as soon as reasonably practical "
                "when responding to calls for service that may involve law enforcement activity. "
                "This typically means before exiting the vehicle. Domestic battery calls are "
                "mandatory activation events. Waiting until arrival (A), contact (D), or force (B) "
                "misses critical preliminary interactions.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Activation should occur before arrival — not upon arrival.\n"
                "B (-2): BWC is not just for force encounters — all enforcement activity must be recorded.\n"
                "D (-1): Contact may happen before the officer can activate — too late."
            ),
            "io_scores": {"A": -1, "B": -2, "C": 2, "D": -1},
            "difficulty": "medium",
            "reference": "S03-14, Section IV (Mandatory Activation); Activation Timing",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q24 ---
        {
            "question_id": "go_q24",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "BWC — Prohibited Actions",
            "content": (
                "After a use of force incident, the involved officer reviews his BWC footage "
                "in the squad car before his sergeant arrives to begin the TRR investigation."
            ),
            "question": "Under S03-14, which aspect of this situation is LEAST appropriate?",
            "options": [
                {"label": "A", "text": "The officer reviewed BWC footage before providing a statement — this may allow him to tailor his account to match the video"},
                {"label": "B", "text": "The officer was trying to accurately recall events by reviewing the footage"},
                {"label": "C", "text": "The officer should wait for a supervisor before reviewing any footage"},
                {"label": "D", "text": "BWC footage review is completely prohibited for involved officers under any circumstances"}
            ],
            "correct_answer": "A",
            "explanation": (
                "CORRECT ANSWER (LEAST APPROPRIATE): A. S03-14 and G03-02-08 establish specific "
                "protocols for BWC review after use of force incidents. Involved officers reviewing "
                "footage before providing statements is problematic because it can allow them to "
                "tailor their account. The review process should be controlled and documented — "
                "supervisors should be present during any review.\n\n"
                "WHY OTHER ANSWERS ARE LESS PROBLEMATIC:\n"
                "B (+1): Accurate recall is a legitimate goal but must follow proper protocols.\n"
                "C (+1): Waiting for a supervisor is the correct approach.\n"
                "D (-1): Review is not completely prohibited — but it must follow specific procedures."
            ),
            "io_scores": {"A": -2, "B": 1, "C": 1, "D": -1},
            "difficulty": "hard",
            "reference": "S03-14, Section VI (Post-Incident Review); G03-02-08",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q25 ---
        {
            "question_id": "go_q25",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "BWC — Recording in Sensitive Locations",
            "content": (
                "Officers respond to a domestic violence call at a private residence. The "
                "victim, who has visible injuries, asks the officer to turn off the body-worn "
                "camera because she is embarrassed and does not want to be recorded."
            ),
            "question": "Under S03-14, what is the MOST appropriate response?",
            "options": [
                {"label": "A", "text": "Turn off the camera immediately — the victim has a right to privacy in her own home"},
                {"label": "B", "text": "Inform the victim that BWC must remain active during law enforcement activity but explain it is for her protection and the integrity of the investigation"},
                {"label": "C", "text": "Turn off the camera since domestic violence is a sensitive situation"},
                {"label": "D", "text": "Continue recording but do not tell the victim the camera is on"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. S03-14 requires BWC to remain active during all law enforcement "
                "activity, including domestic violence calls. Officers cannot deactivate based on a "
                "subject's request during an active investigation. However, officers should inform "
                "subjects they are being recorded and explain the purpose. The recording protects "
                "both the victim and the officers.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Officers cannot deactivate during mandatory recording events.\n"
                "C (-2): Sensitivity does not override the mandatory recording requirement.\n"
                "D (-1): Continuing without informing is less transparent than policy intends."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "S03-14, Section V (Recording Requirements); Victim Interactions",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # ============================================================
        # G03-06: OID RESPONSE AND INVESTIGATION (Core Directive)
        # ============================================================

        # --- Q26 ---
        {
            "question_id": "go_q26",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Definition and Scope",
            "content": (
                "A subject in custody dies after officers delayed calling for medical attention "
                "for over an hour despite the subject complaining of chest pains. The officers "
                "were on duty at the time."
            ),
            "question": "Under G03-06, does this incident qualify as an officer-involved death?",
            "options": [
                {"label": "A", "text": "No, because the officers did not use physical force against the subject"},
                {"label": "B", "text": "Yes, because it resulted from an intentional omission (unreasonable delay in seeking medical attention) by on-duty officers"},
                {"label": "C", "text": "Only if the Medical Examiner rules the death was preventable"},
                {"label": "D", "text": "No, because the death was caused by a medical condition, not police action"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06 and 50 ILCS 727/1-5, an 'officer-involved death' "
                "includes any death resulting directly from an intentional omission, INCLUDING "
                "unreasonable delay involving a person in custody OR intentional failure to seek "
                "medical attention when the need is apparent.\n\n"
                "STUDY TIP: The definition is BROADER than most people think. It covers omissions, "
                "delays, motor vehicle accidents during apprehension, and actions by off-duty "
                "officers performing law enforcement duties.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Physical force is NOT required — omissions count.\n"
                "C (-1): ME ruling is irrelevant to classification under the statute.\n"
                "D (-2): The statute explicitly covers failure to seek medical attention."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-06, Section II-A-3; 50 ILCS 727/1-5",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q27 ---
        {
            "question_id": "go_q27",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — COPA vs. CPD Investigative Authority",
            "content": (
                "An officer-involved shooting has occurred where the subject was struck and "
                "seriously injured but survived. Both COPA investigators and CPD detectives "
                "are responding to the scene."
            ),
            "question": "Under G03-06, who has primary investigative authority?",
            "options": [
                {"label": "A", "text": "CPD detectives have full authority since the subject survived"},
                {"label": "B", "text": "COPA has primary authority over the misconduct/force investigation, while CPD Bureau of Detectives handles the criminal investigation of the underlying incident"},
                {"label": "C", "text": "The State's Attorney's Office takes over all investigations involving officer shootings"},
                {"label": "D", "text": "The FBI automatically takes jurisdiction for all officer-involved shootings"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06 establishes a dual-track investigation model. COPA "
                "investigates the officer's use of force (the misconduct/accountability track). "
                "CPD Bureau of Detectives investigates the criminal incident that led to the "
                "encounter (e.g., the offense the subject committed). These are parallel but "
                "separate investigations.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): COPA has authority over the force investigation regardless of outcome.\n"
                "C (-1): The SAO may be consulted but does not take over the investigation.\n"
                "D (-2): The FBI does not automatically have jurisdiction."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-06, Section IV (Investigative Authority); COPA Jurisdiction",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q28 ---
        {
            "question_id": "go_q28",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Involved Member Immediate Duties",
            "content": (
                "An officer has just been involved in a shooting where the subject is deceased. "
                "Other officers have arrived on scene. The involved officer is physically uninjured."
            ),
            "question": "Under G03-06, what are the involved member's immediate duties?",
            "options": [
                {"label": "A", "text": "Provide a full detailed statement to the first supervisor on scene"},
                {"label": "B", "text": "Remain on scene, do not discuss the incident with other officers, provide a public safety statement, and request FOP representation"},
                {"label": "C", "text": "Immediately leave the scene and report to the district station"},
                {"label": "D", "text": "Begin securing evidence and shell casings from the scene"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06 requires involved members to: (1) remain on scene, "
                "(2) not discuss the incident with other involved members, (3) provide a public "
                "safety statement (limited to threats, direction of flight, outstanding suspects, "
                "injuries), and (4) request union representation before any further statements. "
                "The separation requirement prevents cross-contamination of accounts.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): A full detailed statement should NOT be given immediately — only a public "
                "safety statement.\n"
                "C (-2): Leaving the scene is prohibited.\n"
                "D (-1): Evidence collection is not the involved member's role."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "G03-06, Section VI (Involved Member Duties); Public Safety Statement",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q29 ---
        {
            "question_id": "go_q29",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — CPIC Notification Requirements",
            "content": (
                "An officer-involved death incident has just occurred. The watch commander "
                "is the first supervisor notified."
            ),
            "question": "Under G03-06, which entity must be notified through CPIC?",
            "options": [
                {"label": "A", "text": "Only the Area Detective Division"},
                {"label": "B", "text": "COPA, the State's Attorney's Office, the Independent Monitor, the Area Deputy Chief, and additional entities specified in the notification list"},
                {"label": "C", "text": "Only COPA — they handle all other notifications"},
                {"label": "D", "text": "Only the Superintendent's Office"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06 requires an extensive notification chain through CPIC "
                "(Chicago Police Information Center). Notifications must include COPA, the State's "
                "Attorney's Office, the Independent Monitor, the Area Deputy Chief, the Chaplain "
                "Unit, and other entities as specified in the order. This ensures all stakeholders "
                "are informed simultaneously.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Detective Division is just one of many required notifications.\n"
                "C (-1): COPA does not handle CPD's internal notifications.\n"
                "D (-1): The Superintendent's Office is one notification, not the only one."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section V-C (CPIC Notifications); Notification Chain",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q30 ---
        {
            "question_id": "go_q30",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Street Deputy / Incident Commander Role",
            "content": (
                "A high-profile officer-involved shooting has occurred. The Street Deputy "
                "(or designated incident commander) arrives on scene."
            ),
            "question": "Under G03-06, what is the Street Deputy's PRIMARY role?",
            "options": [
                {"label": "A", "text": "Conduct the criminal investigation of the shooting"},
                {"label": "B", "text": "Assume overall command of the scene, coordinate CPD and COPA activities, ensure all required protocols are followed, and manage resources"},
                {"label": "C", "text": "Interview the involved officer and witnesses"},
                {"label": "D", "text": "Hold a press conference about the incident"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06 designates the Street Deputy or incident commander as "
                "having overall scene authority. Their role is to coordinate all responding entities "
                "(CPD units, COPA, ET, medical), ensure compliance with protocols, manage resources, "
                "and serve as the single point of command. They do NOT conduct investigations or "
                "interviews themselves.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): The criminal investigation is handled by the Bureau of Detectives.\n"
                "C (-2): Interviews are conducted by COPA and/or detectives — not the IC.\n"
                "D (-1): Media communication goes through the Office of Communications."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section VII (Incident Commander); Street Deputy Role",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q31 ---
        {
            "question_id": "go_q31",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Firearm Recovery from Involved Officer",
            "content": (
                "An officer has discharged his firearm during an OID incident. COPA and "
                "detectives are on scene. The involved officer's firearm needs to be recovered "
                "as evidence."
            ),
            "question": "Under G03-06, what is the correct procedure for recovering the involved officer's firearm?",
            "options": [
                {"label": "A", "text": "The officer keeps his firearm until he returns to the district station"},
                {"label": "B", "text": "The involved officer's firearm is recovered at the scene by a supervisor, who provides a replacement weapon, and the discharged firearm is inventoried as evidence"},
                {"label": "C", "text": "COPA investigators take the firearm directly from the officer"},
                {"label": "D", "text": "The firearm is only recovered if the officer requests to surrender it"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06 requires that the involved officer's firearm be "
                "recovered at the scene by a CPD supervisor. The officer must be provided with "
                "a replacement/loaner weapon. The discharged firearm is inventoried into evidence "
                "for ballistic analysis and investigation purposes. This is a mandatory procedure — "
                "not discretionary.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): The firearm must be recovered at the scene — not later at the station.\n"
                "C (-1): CPD supervisors recover the firearm — not COPA investigators.\n"
                "D (-2): Recovery is mandatory — not dependent on the officer's request."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section VII (Firearm Recovery); Evidence Procedures",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q32 ---
        {
            "question_id": "go_q32",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Video Evidence Review Protocol",
            "content": (
                "At an OID scene, BWC and POD camera footage is available. Both COPA "
                "investigators and CPD detectives want to review the video evidence."
            ),
            "question": "Under G03-06, which action regarding video evidence is LEAST appropriate?",
            "options": [
                {"label": "A", "text": "COPA and CPD review the video independently without documenting who viewed it"},
                {"label": "B", "text": "Document each Department member who views video and whether COPA was present"},
                {"label": "C", "text": "COPA and CPD coordinate on the timing and process of video review"},
                {"label": "D", "text": "Preserve all original video files and maintain chain of custody documentation"}
            ],
            "correct_answer": "A",
            "explanation": (
                "CORRECT ANSWER (LEAST APPROPRIATE): A. G03-06 Section VIII-E-3-b requires that "
                "the Bureau of Detectives secondary case report document EACH Department member "
                "who viewed video evidence, including whether COPA was present during the viewing. "
                "Undocumented review undermines evidence integrity and accountability.\n\n"
                "WHY OTHER ANSWERS ARE BETTER:\n"
                "B (+2): Individual documentation is exactly what the order requires.\n"
                "C (+1): Coordination between COPA and CPD is expected.\n"
                "D (+1): Preservation and chain of custody are fundamental requirements."
            ),
            "io_scores": {"A": -2, "B": 2, "C": 1, "D": 1},
            "difficulty": "hard",
            "reference": "G03-06, Section VIII-E-3-b, c; Video Evidence Protocol",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q33 ---
        {
            "question_id": "go_q33",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Lead Investigator Certification",
            "content": (
                "An officer-involved death has occurred. The department is assembling the "
                "investigation team as required by Illinois law."
            ),
            "question": "What is the MINIMUM certification for the lead investigator under G03-06?",
            "options": [
                {"label": "A", "text": "Must be a sworn officer with at least 10 years of experience"},
                {"label": "B", "text": "Must be certified by the Illinois Law Enforcement Training Standards Board as a Lead Homicide Investigator, or have similar approved training"},
                {"label": "C", "text": "Must hold the rank of detective or above"},
                {"label": "D", "text": "Must have previously investigated at least 5 homicide cases"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06 and 50 ILCS 727/1-10(a), the lead investigator "
                "must be certified by the Illinois LETSB as a Lead Homicide Investigator or have "
                "completed equivalent training. This is a statutory requirement, not a department "
                "preference. Experience or rank alone is insufficient.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Years of experience alone do not satisfy the certification requirement.\n"
                "C (-1): Rank does not substitute for the specific LETSB certification.\n"
                "D (-1): Case count does not equal formal certification."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "G03-06, Section IV; 50 ILCS 727/1-10(a)",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q34 ---
        {
            "question_id": "go_q34",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Reviewing Supervisor Public Safety Investigation",
            "content": (
                "The reviewing supervisor arrives at the scene of an officer-involved shooting. "
                "The threat has been neutralized, EMS has been called, and the scene is being secured."
            ),
            "question": "Under G03-06, what is the reviewing supervisor's immediate task?",
            "options": [
                {"label": "A", "text": "Begin a detailed investigation of the officer's use of force"},
                {"label": "B", "text": "Conduct a public safety investigation: identify outstanding threats, ensure officer safety, coordinate medical response, and separate involved members"},
                {"label": "C", "text": "Contact the media to issue an initial statement"},
                {"label": "D", "text": "Interview the involved officer for a full account of events"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06 requires the reviewing supervisor to conduct a public "
                "safety investigation FIRST. This includes: (1) ensuring no outstanding threats, "
                "(2) coordinating medical care, (3) separating involved and witness members, "
                "(4) securing the scene, and (5) identifying immediate evidence preservation needs. "
                "The detailed investigation comes after the scene is safe.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Detailed investigation follows the public safety investigation.\n"
                "C (-2): Media contact is the Office of Communications' role.\n"
                "D (-2): Full interviews require union representation and COPA involvement."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section VII (Reviewing Supervisor); Public Safety Investigation",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q35 ---
        {
            "question_id": "go_q35",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Witness Officer Separation",
            "content": (
                "Four officers were present during an officer-involved shooting. Two officers "
                "discharged their firearms (involved members) and two witnessed the event "
                "(witness officers). All are gathered near the squad cars."
            ),
            "question": "Under G03-06, what is the correct approach to these officers?",
            "options": [
                {"label": "A", "text": "Keep all four officers together so they can support each other emotionally"},
                {"label": "B", "text": "Separate ALL four officers — involved members from each other and from witness officers — to prevent cross-contamination of accounts"},
                {"label": "C", "text": "Separate involved members but witness officers can remain together"},
                {"label": "D", "text": "Send all four officers back to the station immediately for debriefing"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06 mandates that ALL involved and witness members be "
                "separated as soon as practicable. This means involved members are separated from "
                "each other AND from witness officers, and witness officers are separated from "
                "each other. The purpose is to prevent cross-contamination of independent accounts.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Keeping officers together allows conscious or unconscious account alignment.\n"
                "C (-1): Witness officers must also be separated from each other.\n"
                "D (-1): Officers must remain on scene — not return to the station."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section VI (Member Separation); Account Integrity",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # ============================================================
        # CROSS-DIRECTIVE INTEGRATION QUESTIONS
        # ============================================================

        # --- Q36 ---
        {
            "question_id": "go_q36",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — BWC at OID Scene (S03-14 + G03-06)",
            "content": (
                "At an OID scene, a supervisor orders all officers to deactivate their BWCs "
                "'to protect the involved officer's privacy and legal rights.'"
            ),
            "question": "Under S03-14 and G03-06, is this order appropriate?",
            "options": [
                {"label": "A", "text": "Yes, the supervisor has authority to order BWC deactivation for privacy concerns"},
                {"label": "B", "text": "No, BWCs must remain active during active law enforcement activity at an OID scene — deactivation for this reason is improper and must be reported"},
                {"label": "C", "text": "Yes, but only after COPA investigators arrive on scene"},
                {"label": "D", "text": "The involved officer can choose to deactivate but witness officers cannot"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. S03-14 requires BWC activation during law enforcement "
                "activity. An OID scene is a mandatory recording event. Supervisors cannot order "
                "deactivation to 'protect' an officer — this undermines evidence integrity and "
                "accountability. G03-06 reinforces that all evidence, including BWC footage, must "
                "be preserved. An improper deactivation order should be documented and reported.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Privacy concerns do not override mandatory recording requirements.\n"
                "C (-1): COPA's arrival does not trigger deactivation.\n"
                "D (-1): Neither involved nor witness officers should deactivate."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "S03-14, Section IV; G03-06, Section VIII (Evidence Preservation)",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q37 ---
        {
            "question_id": "go_q37",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — Force Review After OID (G03-02-08 + G03-06)",
            "content": (
                "Following an officer-involved shooting where the subject survived, the TRR "
                "has been submitted. The reviewing sergeant must now investigate the use of force."
            ),
            "question": "How does G03-02-08's TRR review interact with G03-06's OID investigation?",
            "options": [
                {"label": "A", "text": "The TRR review replaces the need for a G03-06 investigation since it covers the force used"},
                {"label": "B", "text": "The TRR review and G03-06 investigation are separate processes — the TRR review by the sergeant proceeds in parallel with COPA's investigation under G03-06"},
                {"label": "C", "text": "The sergeant should wait for COPA's investigation to conclude before completing the TRR review"},
                {"label": "D", "text": "Only COPA can review the TRR in an OID incident — the sergeant has no role"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-08 and G03-06 create parallel but separate review "
                "processes. The sergeant completes the TRR review (internal force accountability) "
                "while COPA conducts its independent investigation under G03-06. Neither replaces "
                "the other. The sergeant's review should not wait for COPA and should not defer "
                "to COPA.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): The TRR review does not replace the G03-06 investigation.\n"
                "C (-1): Waiting would cause unreasonable delay in the supervisory review.\n"
                "D (-2): The sergeant retains TRR review responsibilities under G03-02-08."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-02-08, Section III; G03-06, Section IV",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q38 ---
        {
            "question_id": "go_q38",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — Crime Scene at OID (G04-02 + G03-06)",
            "content": (
                "At an OID scene where an officer shot a subject, the detective and COPA "
                "investigator both want to process the scene. COPA wants to begin their "
                "own evidence collection, and the detective wants to process the underlying "
                "criminal case evidence."
            ),
            "question": "Under G04-02 and G03-06, how should scene processing be coordinated?",
            "options": [
                {"label": "A", "text": "COPA processes the scene first, then CPD can process afterward"},
                {"label": "B", "text": "CPD and COPA coordinate joint scene processing, with Evidence Technicians handling physical evidence under the direction of both investigative tracks"},
                {"label": "C", "text": "CPD processes the scene and provides COPA with copies of reports"},
                {"label": "D", "text": "Each agency processes the scene independently at different times"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G04-02 and G03-06 require coordinated scene processing. "
                "Evidence Technicians process the physical evidence under direction from both "
                "the CPD criminal investigation and the COPA accountability investigation. This "
                "prevents duplicate processing, maintains evidence integrity, and ensures both "
                "tracks have access to the same evidence simultaneously.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): COPA does not have exclusive first access to the scene.\n"
                "C (-1): Simply providing copies is insufficient — COPA needs to be involved in processing.\n"
                "D (-2): Independent processing risks evidence contamination and duplication."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G04-02, Section IV; G03-06, Section VIII (Scene Processing)",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q39 ---
        {
            "question_id": "go_q39",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — De-escalation Failure Leading to OID (G03-02 + G03-06)",
            "content": (
                "Officers respond to a mental health crisis call. Despite CIT training, "
                "the situation escalates and the subject charges at officers with a knife. "
                "An officer discharges his firearm, fatally striking the subject."
            ),
            "question": "Under G03-02 and G03-06, which investigations will occur?",
            "options": [
                {"label": "A", "text": "Only a COPA investigation into the shooting"},
                {"label": "B", "text": "A COPA investigation into the use of force (G03-06), a CPD criminal investigation, AND a G03-02-08 supervisory review of the force and de-escalation efforts"},
                {"label": "C", "text": "Only an internal affairs investigation"},
                {"label": "D", "text": "A criminal investigation by the State's Attorney only"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Multiple parallel investigations are triggered. COPA "
                "investigates the use of force under G03-06. CPD Bureau of Detectives conducts "
                "the criminal investigation. G03-02-08 requires a supervisory review that includes "
                "evaluating whether de-escalation was properly attempted. Each investigation serves "
                "a different purpose and none replaces the others.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): COPA is one investigation but not the only one.\n"
                "C (-2): Internal affairs is not the sole investigating body.\n"
                "D (-2): The SAO may be involved but does not conduct the only investigation."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "G03-02, Section III; G03-06, Section IV; G03-02-08, Section III",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q40 ---
        {
            "question_id": "go_q40",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — Force Continuum and Firearm Use (G03-02-01 + G03-02-03)",
            "content": (
                "An officer encounters a subject armed with a baseball bat who is threatening "
                "bystanders. The subject is 30 feet away from the nearest bystander and has "
                "not yet swung the bat. Multiple officers are on scene."
            ),
            "question": "Under G03-02-01 and G03-02-03, what is the MOST appropriate approach?",
            "options": [
                {"label": "A", "text": "Immediately use deadly force since the bat is a deadly weapon"},
                {"label": "B", "text": "Create distance, establish a perimeter, give clear verbal commands to drop the bat, and have less-lethal options (Taser, OC spray) ready while maintaining lethal cover"},
                {"label": "C", "text": "Have all officers draw their firearms and give a single warning before firing"},
                {"label": "D", "text": "Approach the subject alone to establish rapport without backup"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-01 and G03-02-03 work together. While a baseball bat "
                "can be a deadly weapon, the 30-foot distance and multiple officers provide an "
                "opportunity to use force mitigation: distance, verbal commands, perimeter, and "
                "less-lethal options. Deadly force is reserved for when the imminent threat cannot "
                "be resolved by lesser means.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Immediate deadly force ignores available de-escalation opportunities.\n"
                "C (-1): Mass firearm display without attempting lesser means is disproportionate.\n"
                "D (-2): Approaching alone removes tactical options and increases danger."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-02-01, Section IV; G03-02-03, Section III",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # ============================================================
        # RANKING QUESTIONS (following seed_ranking_questions.py format)
        # ============================================================

        # --- Q41 (Ranking) ---
        {
            "question_id": f"rank_go_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Officer-Involved Shooting — First Supervisor Response Priority",
            "content": (
                "You are the first supervisor to arrive at an officer-involved shooting. "
                "The subject is down with gunshot wounds. The involved officer is standing "
                "nearby, visibly shaken but physically uninjured. EMS has not been called. "
                "Several witness officers are discussing what happened. Rank the following "
                "actions in the correct priority order."
            ),
            "items": [
                {"label": "A", "text": "Request EMS for the subject and render first aid until they arrive"},
                {"label": "B", "text": "Separate the involved officer from witness officers and instruct all not to discuss the incident"},
                {"label": "C", "text": "Obtain a public safety statement from the involved officer (threats, outstanding suspects, direction of flight, injuries)"},
                {"label": "D", "text": "Secure the scene, establish a perimeter, and begin a crime scene log"},
                {"label": "E", "text": "Notify CPIC to initiate the required notification chain (COPA, SAO, Deputy Chief, etc.)"},
                {"label": "F", "text": "Recover the involved officer's firearm and provide a replacement weapon"}
            ],
            "correct_order": [0, 3, 1, 2, 4, 5],
            "explanation": (
                "Request EMS and render aid (A) is always the top priority — duty to provide medical "
                "care is both a policy and constitutional requirement. Secure the scene (D) to preserve "
                "evidence and control access. Separate all members (B) to prevent cross-contamination "
                "of accounts. Obtain the public safety statement (C) — limited to immediate threats "
                "and safety information. Notify CPIC (E) to activate the notification chain. Recover "
                "the firearm (F) after immediate safety and separation are addressed.\n\n"
                "KEY REFERENCES: G03-06, Sections V-VII; G03-02-03, Section VI (Duty to Render Aid)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-06, Sections V-VII; G03-02-03, Section VI",
            "created_at": now,
            "updated_at": now
        },

        # --- Q42 (Ranking) ---
        {
            "question_id": f"rank_go_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force Escalation — Resistant Subject Response Priority",
            "content": (
                "You and your partner encounter a domestic battery suspect in the alley behind "
                "the victim's home. He is intoxicated, shouting threats, and clenching his fists. "
                "He has not yet made a physical move toward officers but is blocking the alley. "
                "No weapons are visible. Rank the following response actions in the correct "
                "priority order per G03-02 and G03-02-01."
            ),
            "items": [
                {"label": "A", "text": "Deploy your Taser in probe mode to immediately incapacitate the subject"},
                {"label": "B", "text": "Issue clear, firm verbal commands: 'Police — turn around and place your hands behind your back'"},
                {"label": "C", "text": "Request backup units to establish numerical advantage before making contact"},
                {"label": "D", "text": "Create distance and move to a position of tactical advantage while maintaining visual contact"},
                {"label": "E", "text": "Use OC spray if the subject advances aggressively toward officers"},
                {"label": "F", "text": "Complete a Tactical Response Report (TRR) documenting all force used and the subject's resistance level"}
            ],
            "correct_order": [3, 1, 2, 4, 0, 5],
            "explanation": (
                "Create distance and tactical positioning (D) first — force mitigation through time "
                "and distance. Issue verbal commands (B) — always the first force option attempted. "
                "Request backup (C) to achieve numerical advantage, which often resolves situations "
                "without physical force. OC spray (E) if the subject advances — appropriate for "
                "active aggression. Taser (A) is a higher force option reserved for when lesser "
                "means fail. Document everything in a TRR (F) after the incident is resolved.\n\n"
                "KEY REFERENCES: G03-02, Section III (Force Mitigation); G03-02-01, Section IV (Force Options)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02, Section III; G03-02-01, Section IV",
            "created_at": now,
            "updated_at": now
        },

        # --- Q43 (Ranking) ---
        {
            "question_id": f"rank_go_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene Processing at OID — Evidence Priority Order",
            "content": (
                "You are the lead detective at an officer-involved death scene. The subject "
                "was shot and killed after pointing a replica firearm at officers. The replica "
                "firearm is on the ground near the subject's body. Shell casings are in the "
                "street. BWC footage exists. COPA has been notified and is en route. Rank the "
                "following evidence processing actions in the correct priority order per "
                "G04-02 and G03-06."
            ),
            "items": [
                {"label": "A", "text": "Collect shell casings, the replica firearm, and other physical evidence for inventory"},
                {"label": "B", "text": "Photograph the entire scene, including the subject's body position, the replica firearm, and all evidence in place with measurement markers"},
                {"label": "C", "text": "Coordinate with COPA on a joint scene walk-through before any evidence is moved"},
                {"label": "D", "text": "Ensure all BWC footage is identified, preserved, and a chain of custody log is started"},
                {"label": "E", "text": "Request Evidence Technicians for forensic processing (fingerprints, DNA, ballistics)"},
                {"label": "F", "text": "Canvas for additional video sources (POD cameras, private surveillance, Ring doorbells)"}
            ],
            "correct_order": [3, 2, 1, 4, 5, 0],
            "explanation": (
                "Preserve BWC footage (D) immediately — digital evidence can be overwritten or lost. "
                "Coordinate with COPA for a joint walk-through (C) before anything is disturbed — "
                "G03-06 requires COPA involvement. Photograph everything in place (B) before any "
                "items are moved. Request ET (E) for professional forensic processing. Canvas for "
                "additional video (F) before it's overwritten by surveillance systems. Collect "
                "physical evidence (A) only after all documentation and processing is complete.\n\n"
                "KEY REFERENCES: G04-02, Section IV; G03-06, Section VIII-E"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G04-02, Section IV; G03-06, Section VIII-E",
            "created_at": now,
            "updated_at": now
        },

        # --- Q44 (Ranking) ---
        {
            "question_id": f"rank_go_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "TRR Review Process — Supervisor Investigation Steps",
            "content": (
                "A sergeant is assigned to review a TRR submitted after an officer used an "
                "emergency takedown and OC spray on a subject who was actively resisting arrest. "
                "The subject sustained a cut above his eye. The officer's BWC was active during "
                "the incident. Multiple witnesses were present. Rank the following review "
                "steps in the correct order per G03-02-08."
            ),
            "items": [
                {"label": "A", "text": "Make a final determination on whether the force was within policy and document findings"},
                {"label": "B", "text": "Review all available BWC and other video footage of the incident"},
                {"label": "C", "text": "Interview the involved officer about the force used and the subject's resistance"},
                {"label": "D", "text": "Interview civilian witnesses and other officers who were present"},
                {"label": "E", "text": "Examine and photograph the subject's injuries and review medical records if available"},
                {"label": "F", "text": "Review the TRR documentation for completeness and accuracy against the evidence"}
            ],
            "correct_order": [1, 4, 3, 2, 5, 0],
            "explanation": (
                "Review video first (B) — BWC provides the most objective account of events. "
                "Examine the subject's injuries (E) to understand the actual force impact. "
                "Interview witnesses (D) for independent accounts. Interview the involved officer (C) "
                "after reviewing other evidence to ask informed questions. Review the TRR documentation "
                "against evidence (F) for consistency. Make the final policy determination (A) only "
                "after all evidence has been considered.\n\n"
                "KEY REFERENCES: G03-02-08, Sections III-V"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-08, Sections III-V",
            "created_at": now,
            "updated_at": now
        },

        # --- Q45 (Ranking) ---
        {
            "question_id": f"rank_go_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "BWC Protocol at Use of Force Scene — Action Priority",
            "content": (
                "Officers have used force to arrest a subject after a foot chase. One officer "
                "deployed a Taser, another used a control hold. The subject is now in custody "
                "and complaining of pain. Multiple officers have BWC. A bystander recorded "
                "the incident on a cell phone. Rank the following BWC-related actions in the "
                "correct priority order per S03-14 and G03-02."
            ),
            "items": [
                {"label": "A", "text": "Have all officers with BWC keep cameras active — do not deactivate until the encounter is fully concluded including transport and medical evaluation"},
                {"label": "B", "text": "Request EMS for the subject and document the Taser probe removal by medical personnel on BWC"},
                {"label": "C", "text": "Identify all officers whose BWC captured the incident and note badge numbers and camera IDs"},
                {"label": "D", "text": "Request the bystander's cell phone video or obtain their contact information for follow-up"},
                {"label": "E", "text": "Ensure involved officers do not review their own BWC footage until the supervisor review process begins"},
                {"label": "F", "text": "Complete the BWC metadata log noting activation time, deactivation time, and any gaps in recording"}
            ],
            "correct_order": [0, 1, 4, 2, 3, 5],
            "explanation": (
                "Keep BWCs active (A) is paramount — deactivating prematurely loses critical evidence "
                "including medical care and statements. Request EMS and document medical on BWC (B) — "
                "medical care is a duty and recording it protects everyone. Prevent premature footage "
                "review (E) to preserve account integrity. Identify all BWC-equipped officers (C) for "
                "evidence tracking. Obtain bystander video (D) as supplemental evidence. Complete BWC "
                "metadata logs (F) as the administrative final step.\n\n"
                "KEY REFERENCES: S03-14, Sections IV-VI; G03-02, Section VI"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "S03-14, Sections IV-VI; G03-02, Section VI",
            "created_at": now,
            "updated_at": now
        },

        # ============================================================
        # ADDITIONAL MOST/LEAST APPROPRIATE QUESTIONS
        # ============================================================

        # --- Q46 ---
        {
            "question_id": "go_q46",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force — Prohibited Techniques",
            "content": (
                "An officer is struggling to control an actively resisting subject during an "
                "arrest. The subject is grabbing the officer's vest and attempting to headbutt. "
                "The officer's partner is en route but not yet on scene."
            ),
            "question": "Under G03-02, which technique is LEAST appropriate?",
            "options": [
                {"label": "A", "text": "Applying a lateral vascular neck restraint (chokehold) to gain control"},
                {"label": "B", "text": "Using closed-fist strikes to the subject's torso to break the grip"},
                {"label": "C", "text": "Using a knee strike to the subject's thigh to create distance"},
                {"label": "D", "text": "Deploying your Taser at close range in drive-stun mode"}
            ],
            "correct_answer": "A",
            "explanation": (
                "CORRECT ANSWER (LEAST APPROPRIATE): A. G03-02 PROHIBITS chokeholds and lateral "
                "vascular neck restraints (LVNR) except when deadly force is justified. A "
                "chokehold applied to someone who is actively resisting — but not presenting a "
                "deadly threat — is a prohibited technique and a serious policy violation.\n\n"
                "WHY OTHER ANSWERS ARE BETTER:\n"
                "B (+1): Closed-fist strikes are authorized for active resistance.\n"
                "C (+2): Knee strikes to large muscle groups are a recognized control technique.\n"
                "D (+1): Drive-stun mode is authorized for active resistance at close range."
            ),
            "io_scores": {"A": -2, "B": 1, "C": 2, "D": 1},
            "difficulty": "medium",
            "reference": "G03-02, Section IV (Prohibited Techniques); Chokehold Prohibition",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q47 ---
        {
            "question_id": "go_q47",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Accidental/Unintentional Discharge",
            "content": (
                "While clearing a building during a burglary search, an officer's finger slips "
                "on the trigger and a round is discharged into the floor. No one is injured. "
                "No suspect is present in the area."
            ),
            "question": "Under G03-06, how should this accidental discharge be handled?",
            "options": [
                {"label": "A", "text": "No report needed since it was accidental and no one was injured"},
                {"label": "B", "text": "The officer must report the discharge to a supervisor immediately; the incident must be documented and investigated per firearm discharge protocols"},
                {"label": "C", "text": "The officer should file a report only if a supervisor asks about it"},
                {"label": "D", "text": "Simply document it in the daily log and move on"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06 requires ALL firearm discharges to be reported, "
                "investigated, and documented — regardless of whether they are intentional, "
                "accidental, or unintentional, and regardless of whether anyone is injured. "
                "An accidental discharge triggers the same notification and reporting requirements.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): All discharges must be reported — 'accidental' is not an exemption.\n"
                "C (-1): The officer has an affirmative duty to report — not wait to be asked.\n"
                "D (-1): A daily log entry is insufficient — formal reporting is required."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section III (Reporting Requirements); All Discharges",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q48 ---
        {
            "question_id": "go_q48",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — Weather Threats to Evidence",
            "content": (
                "You are securing a shooting scene on an open street. It begins to rain heavily. "
                "Blood evidence, shell casings, and a discarded weapon are exposed to the rain. "
                "Evidence Technicians are 30 minutes away."
            ),
            "question": "Under G04-02, what is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Collect all evidence immediately to prevent it from being washed away"},
                {"label": "B", "text": "Cover exposed evidence with tarps, cones, or vehicles to protect it without moving it, photograph what you can, and document conditions in your notes"},
                {"label": "C", "text": "Leave everything as is and wait for ET — moving or covering evidence contaminates it"},
                {"label": "D", "text": "Move the evidence inside a nearby building for protection"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G04-02 authorizes first responders to take reasonable steps "
                "to protect evidence from destruction by environmental conditions. Covering evidence "
                "in place (without moving it) preserves its location while protecting from rain. "
                "Document everything including the weather conditions and protective measures taken.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Moving evidence should be a last resort — cover in place first.\n"
                "C (-1): Allowing evidence to be destroyed by rain is a failure to protect.\n"
                "D (-2): Moving evidence to another location destroys spatial relationships."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G04-02, Section III (Evidence Protection); Environmental Threats",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q49 ---
        {
            "question_id": "go_q49",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Review — Pattern Identification",
            "content": (
                "During TRR reviews, a lieutenant notices that the same officer has submitted "
                "five TRRs in three months — significantly more than any other officer on the "
                "watch. Each individual use of force appeared within policy."
            ),
            "question": "Under G03-02-08, what is the MOST appropriate supervisory action?",
            "options": [
                {"label": "A", "text": "Take no action since each individual TRR was within policy"},
                {"label": "B", "text": "Refer the officer for a personnel intervention — the pattern of frequent force use warrants review for additional training, counseling, or assignment change even if individual incidents were within policy"},
                {"label": "C", "text": "Discipline the officer for excessive use of force based on the volume of TRRs"},
                {"label": "D", "text": "Transfer the officer to a less active district to reduce encounters"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-02-08 establishes early intervention mechanisms for "
                "officers who show patterns of force use. Even when individual incidents are "
                "within policy, a pattern of frequent force may indicate a need for additional "
                "training, de-escalation coaching, or other non-disciplinary intervention. "
                "The goal is proactive improvement, not punishment.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Ignoring a pattern fails the supervisory duty to identify trends.\n"
                "C (-1): Discipline is inappropriate when individual incidents were within policy.\n"
                "D (-1): Transfer is reactive and doesn't address the underlying behavior."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "G03-02-08, Section VI (Early Intervention); Pattern Review",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q50 ---
        {
            "question_id": "go_q50",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Involved Member Support and Welfare",
            "content": (
                "An officer involved in a fatal shooting is at the scene. He is emotionally "
                "distraught, shaking, and repeating 'I had no choice.' His partner wants to "
                "comfort him and asks you what to do."
            ),
            "question": "Under G03-06, what is the MOST appropriate way to support the involved officer?",
            "options": [
                {"label": "A", "text": "Allow his partner to stay with him and discuss the incident to help him process"},
                {"label": "B", "text": "Assign a non-witness peer support officer to stay with the involved member, ensure he does not discuss the incident details, and request the Chaplain Unit and EAP"},
                {"label": "C", "text": "Tell the officer to 'tough it out' and focus on the investigation"},
                {"label": "D", "text": "Immediately transport the officer to the hospital for a psychological evaluation"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06 provides for involved member welfare while maintaining "
                "investigative integrity. A non-witness peer support officer can provide emotional "
                "support without contaminating accounts. The Chaplain Unit and Employee Assistance "
                "Program (EAP) offer professional support. The key balance is providing genuine "
                "support while preventing discussion of incident details.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): His partner may be a witness — they must be separated, and incident "
                "discussion is prohibited.\n"
                "C (-2): Dismissing emotional distress is harmful and contrary to department welfare policy.\n"
                "D (-1): Hospital transport may be appropriate if warranted but is not the first step."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section IX (Member Welfare); Peer Support; EAP",
            "exam_source": "2026 Part 2 Study Guide"
        },
    ]

    # ======== INSERT QUESTIONS ========
    count = 0
    for q in questions:
        q.setdefault("created_at", now)
        q.setdefault("updated_at", now)
        q["is_premium"] = True
        q["is_locked"] = True
        q["exam_source"] = "2026 Part 2 Study Guide"

        await db.questions.update_one(
            {"question_id": q["question_id"]},
            {"$set": q},
            upsert=True
        )
        count += 1

    print(f"✓ Seeded {count} General Orders questions (2026 Part 2 Study Guide)")
    print(f"  Category: cat_g03_06_firearm_discharge")
    print(f"  Directives covered: G03-02, G03-02-01, G03-02-03, G03-02-08, G04-02, S03-14, G03-06")
    print(f"  Scoring: I/O Solutions format (+2/+1/0/-1/-2)")
    print(f"  Question types: most_appropriate, least_appropriate, ranking")
    print(f"  Leaderboard: Enabled")
    print(f"  Premium: Part 2 only")


async def main():
    await seed_g03_06_questions()
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
