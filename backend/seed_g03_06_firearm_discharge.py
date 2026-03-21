import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


async def seed_g03_06_questions(ext_db=None):
    """Seed 50 ranking questions from the 2026 Part 2 Study Guide.

    All questions are RANKING format — 6 items to prioritize.
    Covers ALL general orders referenced in G03-06:
      - G03-06: Firearm Discharge & OID Response/Investigation
      - G03-02: De-escalation, Response to Resistance, Use of Force
      - G03-02-01: Response to Resistance and Force Options
      - G03-02-03: Firearm Discharge — Authorized Use and Post-Discharge
      - G03-02-08: Department Review of Use of Force Incidents
      - G04-02: Crime Scene Protection and Processing
      - S03-14: Body Worn Cameras
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
            "2026 Part 2 Study Guide — 50 ranking questions covering CPD General Orders referenced in "
            "G03-06: Firearm Discharge and Officer-Involved Death Incident Response. "
            "Rank 6 actions in correct priority order for each scenario. "
            "Scored using the I/O Solutions methodology."
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

    # Clean up ALL old questions from previous versions
    old_deleted = await db.questions.delete_many({
        "question_id": {"$regex": "^(g0306_|rank_go_|go_q|go_rank_q)"},
        "category_id": "cat_g03_06_firearm_discharge"
    })
    if old_deleted.deleted_count:
        print(f"  Cleaned up {old_deleted.deleted_count} old questions from previous versions")

    # ================================================================
    # 50 RANKING QUESTIONS — 2026 Part 2 General Orders Study Guide
    # ================================================================

    questions = [
        # ============================================================
        # G03-02: DE-ESCALATION, RESPONSE TO RESISTANCE, USE OF FORCE
        # ============================================================

        # --- Q1 ---
        {
            "question_id": "go_rank_q01",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "De-escalation — Mental Health Crisis on Bridge",
            "content": (
                "You respond to a man standing on a bridge overpass threatening to jump. "
                "He is unarmed and does not pose a threat to anyone other than himself. "
                "Multiple officers are on scene. Traffic is heavy below. Rank the following "
                "actions in the correct priority order per G03-02."
            ),
            "items": [
                {"label": "A", "text": "Establish a dialogue using calm, non-threatening verbal communication to build rapport with the subject"},
                {"label": "B", "text": "Request a Crisis Intervention Team (CIT) trained officer to respond to the scene"},
                {"label": "C", "text": "Secure the area below the bridge and redirect vehicle and pedestrian traffic for public safety"},
                {"label": "D", "text": "Notify a supervisor and request CFD/EMS to stage nearby in case of a medical emergency"},
                {"label": "E", "text": "Maintain a safe distance and positioning — avoid cornering or rushing the subject"},
                {"label": "F", "text": "Document the incident details, actions taken, and outcome in a case report"},
            ],
            "correct_order": [4, 0, 2, 1, 3, 5],
            "explanation": (
                "Maintain safe distance and positioning (E) first — force mitigation through space prevents "
                "escalation. Establish dialogue (A) immediately — de-escalation through communication is "
                "mandated by G03-02. Secure the area below (C) for public safety. Request CIT officer (B) "
                "for specialized crisis response. Notify supervisor and stage EMS (D). Document (F) after "
                "the incident is resolved.\n\n"
                "KEY REFERENCE: G03-02, Section III (De-escalation); CIT Protocol"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02, Section III (De-escalation); CIT Protocol",
        },

        # --- Q2 ---
        {
            "question_id": "go_rank_q02",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force — Proportional Response to Fleeing Shoplifter",
            "content": (
                "An officer encounters a shoplifting suspect walking away from a store with "
                "a bag of stolen merchandise valued at approximately $40. The suspect ignores "
                "verbal commands to stop but is not armed and not threatening anyone. "
                "Rank the following actions in the correct priority order per G03-02."
            ),
            "items": [
                {"label": "A", "text": "Issue clear verbal commands identifying yourself as police and directing the suspect to stop"},
                {"label": "B", "text": "Follow the suspect at a safe distance while broadcasting description and direction of travel on the radio"},
                {"label": "C", "text": "Request additional units to set up a containment perimeter in the direction of travel"},
                {"label": "D", "text": "Attempt to obtain the suspect's identity from store employees and surveillance footage"},
                {"label": "E", "text": "Contact the store manager to confirm the theft and obtain a signed complaint"},
                {"label": "F", "text": "Complete an Investigatory Stop Report (ISR) or arrest report documenting all actions taken"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Issue verbal commands (A) first — verbal direction is always the first force option. "
                "Follow and broadcast (B) to maintain visual contact without escalating. Request "
                "containment (C) for a coordinated response. Obtain identity from store (D) as an "
                "investigative step. Confirm the complaint (E) for charging purposes. Document (F) "
                "after the incident. NOTE: Physical force is disproportionate for a non-violent "
                "misdemeanor — Tennessee v. Garner prohibits deadly force for non-dangerous fleeing suspects.\n\n"
                "KEY REFERENCE: G03-02, Section IV (Proportionality); Tennessee v. Garner"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-02, Section IV (Proportionality); Tennessee v. Garner",
        },

        # --- Q3 ---
        {
            "question_id": "go_rank_q03",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Duty to Intervene — Excessive Force by Fellow Officer",
            "content": (
                "You observe a fellow officer applying a chokehold to a handcuffed subject who "
                "is no longer resisting. The subject is turning blue and gasping for air. "
                "Your partner tells you to mind your own business. Rank the following "
                "actions in the correct priority order per G03-02."
            ),
            "items": [
                {"label": "A", "text": "Physically intervene to stop the chokehold and remove the officer's arm from the subject's neck"},
                {"label": "B", "text": "Verbally order the officer to release the chokehold immediately"},
                {"label": "C", "text": "Request EMS to respond for the subject and begin rendering first aid once the hold is released"},
                {"label": "D", "text": "Notify a supervisor immediately and report the use of unauthorized force"},
                {"label": "E", "text": "Identify and separate any witnesses and obtain their account of what occurred"},
                {"label": "F", "text": "Ensure your BWC is recording and document the incident in detail including timestamps"},
            ],
            "correct_order": [1, 0, 2, 5, 3, 4],
            "explanation": (
                "Verbally order release (B) first — attempt verbal intervention before physical. "
                "Physically intervene (A) if verbal fails — G03-02 imposes an affirmative DUTY TO "
                "INTERVENE when excessive or unauthorized force is observed. Request EMS and render "
                "aid (C) — subject's life is in danger. Ensure BWC recording (F) to preserve evidence. "
                "Notify supervisor (D) to report the unauthorized force. Identify witnesses (E) for "
                "the investigation. Chokeholds are PROHIBITED under CPD policy.\n\n"
                "KEY REFERENCE: G03-02, Section V (Duty to Intervene); Prohibited Force Techniques"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02, Section V (Duty to Intervene); Prohibited Force Techniques",
        },

        # --- Q4 ---
        {
            "question_id": "go_rank_q04",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force Reporting — Emergency Takedown Documentation",
            "content": (
                "During an arrest, you use an emergency takedown to control a combative subject. "
                "The subject sustains a minor scrape on his elbow. The arrest is completed without "
                "further incident. The subject is now in custody. Rank the following "
                "actions in the correct priority order per G03-02."
            ),
            "items": [
                {"label": "A", "text": "Assess the subject for injuries and request EMS if needed — document refusal of medical treatment if applicable"},
                {"label": "B", "text": "Complete a Tactical Response Report (TRR) documenting the force used, subject's actions, and any injuries"},
                {"label": "C", "text": "Notify your immediate supervisor that force was used during the arrest"},
                {"label": "D", "text": "Ensure your BWC captured the entire encounter including the events leading to the takedown"},
                {"label": "E", "text": "Have the subject photographed showing the injury and document the photos in the TRR"},
                {"label": "F", "text": "Complete the arrest report with a detailed narrative of the circumstances requiring force"},
            ],
            "correct_order": [0, 3, 2, 1, 4, 5],
            "explanation": (
                "Assess for injuries and render aid (A) first — duty of care to persons in custody. "
                "Ensure BWC footage (D) is preserved — critical evidence for the TRR review. Notify "
                "supervisor (C) that force was used. Complete TRR (B) — required for ANY force beyond "
                "verbal commands, regardless of how minor the injury. Photograph injuries (E) for "
                "documentation. Complete arrest report (F) with detailed narrative.\n\n"
                "KEY REFERENCE: G03-02, Section VI (Reporting Requirements); TRR Procedures"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-02, Section VI (Reporting Requirements); TRR Procedures",
        },

        # --- Q5 ---
        {
            "question_id": "go_rank_q05",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Mitigation — Barricaded Subject with Knife",
            "content": (
                "Officers respond to a domestic disturbance. The male subject has locked himself "
                "in a bedroom with a kitchen knife and is threatening to hurt himself. The victim "
                "(his wife) is safely outside the apartment. No children are present. "
                "Rank the following actions in the correct priority order per G03-02."
            ),
            "items": [
                {"label": "A", "text": "Create distance and time — establish a perimeter outside the bedroom and evacuate adjacent units"},
                {"label": "B", "text": "Attempt verbal communication through the door using de-escalation techniques"},
                {"label": "C", "text": "Request a CIT-trained officer and notify SWAT if the situation becomes prolonged"},
                {"label": "D", "text": "Gather intelligence from the victim about the subject's mental state, medications, and history"},
                {"label": "E", "text": "Ensure EMS stages nearby and request the Chaplain Unit if the subject is in a mental health crisis"},
                {"label": "F", "text": "Notify a supervisor and establish an incident command structure for the barricade situation"},
            ],
            "correct_order": [0, 3, 1, 5, 2, 4],
            "explanation": (
                "Create distance and time (A) first — force mitigation through containment when there "
                "is no immediate threat to others. Gather intelligence (D) from the victim to understand "
                "the subject's state. Begin verbal de-escalation (B) through the door. Notify supervisor "
                "and establish command (F). Request CIT/SWAT (C) for specialized response. Stage EMS "
                "and Chaplain (E) for support. The key principle: when a subject is contained and only "
                "threatening self-harm, TIME IS YOUR ALLY.\n\n"
                "KEY REFERENCE: G03-02, Section III (Force Mitigation); Barricade Protocols"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02, Section III (Force Mitigation); Barricade Protocols",
        },

        # --- Q6 ---
        {
            "question_id": "go_rank_q06",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Prohibited Techniques — Officer Using Knee on Neck",
            "content": (
                "While backing up officers on an arrest, you arrive to find an officer with "
                "his knee on a prone, handcuffed subject's neck. The subject is crying out that "
                "he cannot breathe. Other officers are standing nearby watching. "
                "Rank the following actions in the correct priority order per G03-02."
            ),
            "items": [
                {"label": "A", "text": "Direct the officer to immediately remove his knee from the subject's neck — this is a prohibited technique"},
                {"label": "B", "text": "If the officer does not comply, physically remove his knee and reposition the subject to allow breathing"},
                {"label": "C", "text": "Roll the subject onto his side in the recovery position and assess his breathing and consciousness"},
                {"label": "D", "text": "Request EMS immediately and monitor the subject's breathing until paramedics arrive"},
                {"label": "E", "text": "Ensure all BWC cameras on scene are activated and recording"},
                {"label": "F", "text": "Notify a supervisor, report the prohibited technique, and begin documenting the incident"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Direct removal verbally (A) — immediate verbal intervention for a life-threatening "
                "prohibited technique. Physically remove if needed (B) — duty to intervene requires "
                "escalation if verbal fails. Recovery position (C) — address positional asphyxia risk. "
                "Request EMS (D) — subject complained of breathing difficulty. Ensure BWC (E) — "
                "preserve evidence. Notify supervisor and document (F).\n\n"
                "KEY REFERENCE: G03-02, Section V (Duty to Intervene); Prohibited Techniques; "
                "Positional Asphyxia Policy"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02, Section V; Prohibited Techniques; Positional Asphyxia",
        },

        # --- Q7 ---
        {
            "question_id": "go_rank_q07",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Use of Force — Handcuffed Subject Medical Emergency",
            "content": (
                "After a foot chase and struggle, a handcuffed subject suddenly becomes "
                "unresponsive in the back of your squad car. He was combative during the arrest "
                "and was placed face-down briefly during handcuffing. His lips are turning blue. "
                "Rank the following actions in the correct priority order per G03-02."
            ),
            "items": [
                {"label": "A", "text": "Immediately remove the subject from the squad car and place him on his side in the recovery position"},
                {"label": "B", "text": "Check for breathing and pulse — begin CPR if the subject is not breathing and has no pulse"},
                {"label": "C", "text": "Request EMS on an emergency basis — report an unresponsive person in custody"},
                {"label": "D", "text": "Remove or loosen the handcuffs if they may be restricting breathing or circulation"},
                {"label": "E", "text": "Notify your supervisor of a medical emergency involving a subject in custody"},
                {"label": "F", "text": "Preserve the scene and ensure BWC is recording — this may become an in-custody death investigation"},
            ],
            "correct_order": [0, 3, 1, 2, 4, 5],
            "explanation": (
                "Remove from car and recovery position (A) — address positional asphyxia immediately. "
                "Remove/loosen handcuffs (D) — relieve any breathing restriction. Check breathing and "
                "begin CPR (B) if needed. Request emergency EMS (C). Notify supervisor (E) — in-custody "
                "medical emergency requires immediate notification. Preserve scene and BWC (F) — may "
                "become an in-custody death investigation.\n\n"
                "KEY REFERENCE: G03-02, Section VII (Medical Attention); Positional Asphyxia; "
                "In-Custody Death Protocol"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02, Section VII; Positional Asphyxia; In-Custody Death",
        },

        # --- Q8 ---
        {
            "question_id": "go_rank_q08",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "De-escalation — Armed Subject in Public Park",
            "content": (
                "You respond to a call of a man sitting on a park bench waving a handgun. "
                "When you arrive, the man is alone on the bench, gun visible in his lap. "
                "He appears intoxicated. Several civilians are in the park nearby. "
                "Rank the following actions in the correct priority order per G03-02."
            ),
            "items": [
                {"label": "A", "text": "Take cover behind your vehicle and draw your firearm while issuing verbal commands to drop the weapon"},
                {"label": "B", "text": "Evacuate civilians from the immediate area and establish a safe perimeter"},
                {"label": "C", "text": "Request backup units, a supervisor, and have dispatch attempt to identify the subject"},
                {"label": "D", "text": "Begin de-escalation dialogue — use calm communication while maintaining cover"},
                {"label": "E", "text": "Request a CIT officer if the subject appears to be in a mental health crisis"},
                {"label": "F", "text": "If the subject drops the weapon, direct him to move away from it before approaching to secure it"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Take cover and verbal commands (A) — officer safety and initial commands to address "
                "the immediate lethal threat. Evacuate civilians (B) — public safety is paramount. "
                "Request backup and supervisor (C) — do not handle alone. De-escalation dialogue (D) — "
                "once cover is established, begin communication. Request CIT (E) if mental health "
                "indicators present. Secure weapon (F) only after the subject complies.\n\n"
                "KEY REFERENCE: G03-02, Section III (De-escalation); Section IV (Armed Subject Response)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02, Sections III-IV (De-escalation; Armed Subject)",
        },

        # ============================================================
        # G03-02-01: RESPONSE TO RESISTANCE AND FORCE OPTIONS
        # ============================================================

        # --- Q9 ---
        {
            "question_id": "go_rank_q09",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — OC Spray Deployment at Domestic Battery",
            "content": (
                "You respond to a domestic battery in progress. The male offender is actively "
                "punching the victim when you arrive. He turns toward you aggressively with "
                "clenched fists. He is larger than you and appears intoxicated. Your partner "
                "is 30 seconds behind. Rank the following actions in the correct priority "
                "order per G03-02-01."
            ),
            "items": [
                {"label": "A", "text": "Issue clear verbal commands: 'Police! Stop! Get on the ground now!'"},
                {"label": "B", "text": "Deploy OC spray if the subject advances aggressively — target the facial area from 3-12 feet"},
                {"label": "C", "text": "After OC deployment, direct the subject to the ground and handcuff when safe to do so"},
                {"label": "D", "text": "Request EMS to respond for the victim's injuries and to decontaminate the subject from OC exposure"},
                {"label": "E", "text": "Separate the offender from the victim and secure both in different areas"},
                {"label": "F", "text": "Complete a TRR documenting the OC spray deployment, the subject's resistance level, and any injuries"},
            ],
            "correct_order": [0, 1, 2, 4, 3, 5],
            "explanation": (
                "Verbal commands (A) always first — the initial force option. OC spray (B) if the subject "
                "advances — justified for active aggression when the subject is within effective range. "
                "Control and handcuff (C) once the OC takes effect. Separate parties (E) to prevent further "
                "violence. Request EMS (D) for the victim and OC decontamination. Complete TRR (F) to "
                "document all force used.\n\n"
                "KEY REFERENCE: G03-02-01, Section IV (OC Spray); Effective Range 3-12 Feet"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-02-01, Section IV (OC Spray Deployment)",
        },

        # --- Q10 ---
        {
            "question_id": "go_rank_q10",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — Taser Restrictions and Medical Protocol",
            "content": (
                "During a foot chase, your partner deploys a Taser in probe mode striking a fleeing "
                "burglary suspect in the back. The suspect falls to the ground. One probe is embedded "
                "in his upper back, the other in his lower back. The suspect is now compliant and "
                "handcuffed. Rank the following actions in the correct priority order per G03-02-01."
            ),
            "items": [
                {"label": "A", "text": "Do NOT remove the Taser probes — only qualified medical personnel should remove embedded probes"},
                {"label": "B", "text": "Request EMS to respond for probe removal and mandatory medical evaluation after Taser deployment"},
                {"label": "C", "text": "Monitor the subject continuously for signs of medical distress including breathing difficulty"},
                {"label": "D", "text": "Place the subject in a seated or recovery position — do NOT leave face-down after Taser use"},
                {"label": "E", "text": "Notify a supervisor that a Taser was deployed in probe mode"},
                {"label": "F", "text": "Complete a TRR documenting the Taser deployment, number of cycles, probe placement, and medical response"},
            ],
            "correct_order": [3, 0, 2, 1, 4, 5],
            "explanation": (
                "Recovery/seated position (D) first — prevent positional asphyxia after exertion and "
                "Taser exposure. Leave probes in place (A) — only medical personnel remove embedded probes. "
                "Monitor continuously (C) for excited delirium or respiratory distress. Request EMS (B) "
                "for mandatory medical evaluation. Notify supervisor (E) of Taser deployment. Complete "
                "TRR (F) with all deployment details.\n\n"
                "KEY REFERENCE: G03-02-01, Section V (Taser); Post-Deployment Medical Protocol"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-01, Section V (Taser); Medical Protocol",
        },

        # --- Q11 ---
        {
            "question_id": "go_rank_q11",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — Impact Weapon Response to Aggressive Subject",
            "content": (
                "You encounter a subject armed with a metal pipe who is smashing car windows "
                "on a residential street. He has swung the pipe at two civilians who fled. "
                "OC spray was deployed by another officer but had no effect. The subject is "
                "now advancing toward officers. Rank the following actions in the correct "
                "priority order per G03-02-01."
            ),
            "items": [
                {"label": "A", "text": "Deploy Taser in probe mode if within effective range (7-15 feet) to incapacitate the subject"},
                {"label": "B", "text": "If Taser fails or is unavailable, use expandable baton strikes to large muscle groups (thighs, arms) to gain compliance"},
                {"label": "C", "text": "Maintain reactionary gap — do NOT close distance on a subject armed with a striking weapon"},
                {"label": "D", "text": "Continue verbal commands directing the subject to drop the pipe while creating tactical positioning"},
                {"label": "E", "text": "Once the subject is disarmed and controlled, request EMS for any injuries from the baton or Taser"},
                {"label": "F", "text": "Notify a supervisor and complete separate TRRs for each force option deployed (OC, Taser, baton)"},
            ],
            "correct_order": [2, 3, 0, 1, 4, 5],
            "explanation": (
                "Maintain reactionary gap (C) first — officer safety against an armed subject. Continue "
                "verbal commands (D) while positioning tactically. Deploy Taser (A) as a less-lethal "
                "option before baton. Baton strikes to large muscle groups (B) if Taser fails — "
                "authorized target areas only. Request EMS (E) after the subject is controlled. "
                "Supervisor notification and TRRs (F) for each force option used.\n\n"
                "KEY REFERENCE: G03-02-01, Section IV (Force Continuum); Impact Weapons Policy"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-01, Section IV (Force Continuum); Impact Weapons",
        },

        # --- Q12 ---
        {
            "question_id": "go_rank_q12",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — Positional Asphyxia After Ground Struggle",
            "content": (
                "After a prolonged ground struggle, you and your partner handcuff a large, "
                "obese subject who was resisting arrest. He was face-down for approximately "
                "two minutes during the struggle. He is now handcuffed but breathing heavily "
                "and sweating profusely. He says 'I can't breathe.' "
                "Rank the following actions in the correct priority order per G03-02-01."
            ),
            "items": [
                {"label": "A", "text": "Immediately roll the subject onto his side or sit him upright — do NOT keep a handcuffed subject face-down"},
                {"label": "B", "text": "Request EMS to respond immediately — report breathing difficulty in a subject in custody"},
                {"label": "C", "text": "Loosen clothing around the neck and chest area to aid breathing"},
                {"label": "D", "text": "Monitor the subject's breathing, skin color, and consciousness continuously until EMS arrives"},
                {"label": "E", "text": "Do NOT apply any additional body weight or pressure on the subject's back or torso"},
                {"label": "F", "text": "Notify your supervisor of a potential medical emergency involving positional asphyxia"},
            ],
            "correct_order": [0, 4, 2, 1, 3, 5],
            "explanation": (
                "Roll to side or sit upright (A) — immediately address positional asphyxia risk, the #1 "
                "priority. Remove all pressure (E) — no weight on torso. Loosen clothing (C) to aid "
                "breathing. Request EMS (B) for breathing difficulty in custody. Monitor continuously "
                "(D) for deterioration. Notify supervisor (F) of the medical emergency.\n\n"
                "KEY REFERENCE: G03-02-01, Positional Asphyxia Protocol; In-Custody Medical Emergencies"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-01, Positional Asphyxia Protocol",
        },

        # --- Q13 ---
        {
            "question_id": "go_rank_q13",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Escalation — Resistant Subject at Traffic Stop",
            "content": (
                "During a traffic stop for a stolen vehicle, the driver refuses to exit. "
                "He grips the steering wheel tightly and begins screaming. He has not made "
                "any threatening gestures or displayed weapons. A passenger is in the front "
                "seat. Rank the following actions in the correct priority order per G03-02 "
                "and G03-02-01."
            ),
            "items": [
                {"label": "A", "text": "Issue clear, repeated verbal commands directing the driver to exit the vehicle with hands visible"},
                {"label": "B", "text": "Request backup and wait for additional units before attempting to physically remove the driver"},
                {"label": "C", "text": "Direct the passenger to exit the vehicle first to reduce the number of subjects to manage"},
                {"label": "D", "text": "If the driver still refuses after backup arrives, use joint manipulation or escort holds to remove him"},
                {"label": "E", "text": "Once removed, place the driver in handcuffs and conduct a pat-down for officer safety"},
                {"label": "F", "text": "Complete a TRR if any physical force was used beyond verbal commands during the removal"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Verbal commands (A) first — always start with the lowest force option. Request backup "
                "(B) — do not attempt physical removal alone. Remove passenger (C) to simplify the "
                "encounter. Joint manipulation/escort holds (D) with backup — appropriate for passive "
                "resistance. Handcuff and pat-down (E) for officer safety. TRR (F) for any physical "
                "force used. Key: passive resistance does NOT justify higher-level force.\n\n"
                "KEY REFERENCE: G03-02, Force Mitigation; G03-02-01, Section IV (Force Options)"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-02, Force Mitigation; G03-02-01, Section IV",
        },

        # --- Q14 ---
        {
            "question_id": "go_rank_q14",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Options — Subject Exhibiting Excited Delirium Symptoms",
            "content": (
                "Officers are called to a gas station where a naked man is running in traffic, "
                "screaming incoherently, and displaying superhuman strength. He has already thrown "
                "a garbage can through a window. He is sweating profusely, has dilated pupils, "
                "and appears impervious to pain. Rank the following actions in the correct "
                "priority order per G03-02-01."
            ),
            "items": [
                {"label": "A", "text": "Request EMS immediately — these symptoms indicate excited delirium, a life-threatening medical emergency"},
                {"label": "B", "text": "Coordinate a team approach with multiple officers to safely restrain the subject using minimal force duration"},
                {"label": "C", "text": "Once restrained, do NOT keep the subject face-down — position on his side and monitor breathing continuously"},
                {"label": "D", "text": "Avoid prolonged struggle — excited delirium subjects are at extreme risk of sudden cardiac arrest"},
                {"label": "E", "text": "Use de-escalation first if safe — avoid chase or confrontation that increases the subject's physiological stress"},
                {"label": "F", "text": "Transport to hospital immediately via EMS — do NOT transport in a squad car for an excited delirium subject"},
            ],
            "correct_order": [0, 4, 1, 3, 2, 5],
            "explanation": (
                "Request EMS (A) immediately — excited delirium is a medical emergency first, law "
                "enforcement encounter second. Attempt de-escalation (E) if safe. Team approach (B) "
                "to minimize struggle duration. Avoid prolonged struggle (D) — cardiac arrest risk. "
                "Recovery position and monitor (C) after restraint. EMS transport to hospital (F) — "
                "never squad car transport for excited delirium.\n\n"
                "KEY REFERENCE: G03-02-01, Excited Delirium Protocol; Medical Emergency Response"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-01, Excited Delirium Protocol",
        },

        # ============================================================
        # G03-02-03: FIREARM DISCHARGE — AUTHORIZED USE
        # ============================================================

        # --- Q15 ---
        {
            "question_id": "go_rank_q15",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Firearm Discharge — Armed Robbery Fleeing Suspect",
            "content": (
                "You respond to an armed robbery in progress. As you arrive, the suspect runs "
                "out of the store carrying a gun and a bag of cash. He fires one shot in the air "
                "and runs into a residential neighborhood. He has already shot and wounded the "
                "store clerk inside. Rank the following actions in the correct priority order "
                "per G03-02-03 and G03-02."
            ),
            "items": [
                {"label": "A", "text": "Pursue on foot while broadcasting suspect description, direction of travel, and that the suspect is armed and has discharged a firearm"},
                {"label": "B", "text": "Check on the wounded store clerk and request EMS for the gunshot wound victim"},
                {"label": "C", "text": "Request backup, K-9, helicopter, and establish a perimeter in the direction of flight"},
                {"label": "D", "text": "Only discharge your firearm if the suspect presents an imminent deadly threat — do NOT shoot at a fleeing subject merely to prevent escape"},
                {"label": "E", "text": "Warn nearby civilians to take cover and stay inside their homes if the suspect enters the residential area"},
                {"label": "F", "text": "Preserve the crime scene at the store including shell casings, security footage, and witness statements"},
            ],
            "correct_order": [1, 0, 2, 4, 3, 5],
            "explanation": (
                "Aid the wounded clerk (B) first — duty to render aid to the shooting victim. Pursue "
                "and broadcast (A) — maintain contact with the armed dangerous suspect. Request backup "
                "and perimeter (C) — coordinate containment. Warn civilians (E) — public safety in "
                "residential area. Firearm use only for imminent threat (D) — per G03-02-03, you cannot "
                "shoot a fleeing subject merely to prevent escape, even an armed one, unless there is "
                "imminent threat of death or great bodily harm. Preserve store scene (F) after the "
                "immediate threat is addressed.\n\n"
                "KEY REFERENCE: G03-02-03, Section III (Authorized Use); Tennessee v. Garner"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-03, Section III; Tennessee v. Garner",
        },

        # --- Q16 ---
        {
            "question_id": "go_rank_q16",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Firearm Discharge — Shooting at Moving Vehicles",
            "content": (
                "During a traffic stop on a wanted felony suspect, the suspect puts the car in "
                "drive and accelerates directly toward your partner who is standing in front of "
                "the vehicle. Your partner dives out of the way. The suspect speeds off. You are "
                "positioned to the side of the vehicle. Rank the following actions in the correct "
                "priority order per G03-02-03."
            ),
            "items": [
                {"label": "A", "text": "Do NOT fire at the moving vehicle — G03-02-03 prohibits shooting at moving vehicles unless deadly force other than the vehicle is being used"},
                {"label": "B", "text": "Check on your partner immediately to ensure she is not injured from diving out of the way"},
                {"label": "C", "text": "Broadcast the vehicle description, license plate, and direction of travel for a fleeing felony suspect"},
                {"label": "D", "text": "Request supervisor and air support to track the vehicle — do NOT engage in a high-speed pursuit without authorization"},
                {"label": "E", "text": "Preserve the scene — your BWC, the location of the traffic stop, and any tire marks or evidence"},
                {"label": "F", "text": "Notify OEMC that the suspect used a vehicle as a weapon — attempted murder of a police officer"},
            ],
            "correct_order": [0, 1, 2, 5, 3, 4],
            "explanation": (
                "Do NOT shoot at the vehicle (A) — G03-02-03 specifically PROHIBITS firing at moving "
                "vehicles unless the occupant is using deadly force OTHER than the vehicle itself. "
                "Check on your partner (B) — immediate welfare. Broadcast (C) for coordinated response. "
                "Notify OEMC of vehicle used as weapon (F) — upgrade the offense. Request supervisor and "
                "air support (D). Preserve the scene (E) for investigation.\n\n"
                "KEY REFERENCE: G03-02-03, Section IV (Shooting at Vehicles — PROHIBITED)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-03, Section IV (Shooting at Vehicles)",
        },

        # --- Q17 ---
        {
            "question_id": "go_rank_q17",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Post-Discharge — Immediate Obligations After Shooting",
            "content": (
                "You have just discharged your firearm at an armed subject who pointed a gun "
                "at you. The subject is down with a gunshot wound to the chest. Your partner "
                "secured the subject's weapon. You are physically uninjured but shaken. "
                "Rank the following actions in the correct priority order per G03-02-03."
            ),
            "items": [
                {"label": "A", "text": "Request EMS immediately and render first aid to the subject until paramedics arrive"},
                {"label": "B", "text": "Secure the scene and protect all evidence — do NOT move shell casings, weapons, or other items"},
                {"label": "C", "text": "Notify OEMC of a police-involved shooting and provide the location for responding units"},
                {"label": "D", "text": "Holster your weapon and remain on scene — do NOT leave the scene of a firearm discharge"},
                {"label": "E", "text": "Do NOT discuss the details of the incident with other officers — wait for your attorney and FOP representative"},
                {"label": "F", "text": "Provide a public safety statement to the first supervisor on scene (threats, direction of flight, injuries, weapon location)"},
            ],
            "correct_order": [0, 2, 3, 1, 5, 4],
            "explanation": (
                "Request EMS and render aid (A) — the constitutional duty to provide medical care applies "
                "even to the person you shot. Notify OEMC (C) of the shooting. Remain on scene (D) — "
                "mandatory obligation. Secure evidence (B) — protect shell casings and weapons in place. "
                "Provide public safety statement (F) — limited to immediate threats and safety info. "
                "Do NOT discuss details (E) until attorney/FOP present — you have the right to "
                "representation before providing a detailed statement.\n\n"
                "KEY REFERENCE: G03-02-03, Section VI (Post-Discharge Obligations)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-03, Section VI (Post-Discharge Obligations)",
        },

        # --- Q18 ---
        {
            "question_id": "go_rank_q18",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Firearm Discharge — Warning Shots Are Prohibited",
            "content": (
                "You are pursuing an armed carjacking suspect through a dark alley. The suspect "
                "is running ahead of you and has not turned to face you. A civilian steps out "
                "of a doorway between you and the suspect. You want to stop the suspect before "
                "he enters a crowded street. Rank the following actions in the correct priority "
                "order per G03-02-03."
            ),
            "items": [
                {"label": "A", "text": "Do NOT fire a warning shot — warning shots are PROHIBITED under G03-02-03 due to the risk of hitting unintended targets"},
                {"label": "B", "text": "Direct the civilian to get back inside immediately and take cover"},
                {"label": "C", "text": "Continue pursuing while broadcasting the suspect's direction of travel toward the crowded street"},
                {"label": "D", "text": "Request units to set up at the street ahead to intercept the suspect before he reaches the crowd"},
                {"label": "E", "text": "Only discharge your firearm if the suspect turns and presents an imminent deadly threat to you or others"},
                {"label": "F", "text": "Maintain visual contact and be prepared to disengage if the risk to civilians becomes too great"},
            ],
            "correct_order": [0, 1, 2, 3, 5, 4],
            "explanation": (
                "No warning shots (A) — absolutely prohibited under G03-02-03. Protect the civilian "
                "(B) — direct them to safety. Continue pursuit and broadcast (C). Request intercepting "
                "units (D) ahead. Prepare to disengage (F) if civilian risk is too high — you cannot "
                "endanger bystanders. Firearm only for imminent threat (E).\n\n"
                "KEY REFERENCE: G03-02-03, Section V (Warning Shots PROHIBITED)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-03, Section V (Warning Shots Prohibited)",
        },

        # --- Q19 ---
        {
            "question_id": "go_rank_q19",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Firearm Discharge — Off-Duty Encounter with Armed Robber",
            "content": (
                "While off-duty at a restaurant, you witness an armed robbery. The offender "
                "has a gun pointed at the cashier. You are armed with your off-duty weapon. "
                "Your family is seated nearby. Other patrons are in the restaurant. "
                "Rank the following actions in the correct priority order per G03-02-03."
            ),
            "items": [
                {"label": "A", "text": "Call 911 immediately and provide the location, description of the offender, and that he is armed"},
                {"label": "B", "text": "If safe to do so, move your family and nearby patrons away from the offender's line of sight"},
                {"label": "C", "text": "Do NOT draw your weapon unless there is an imminent threat of death or great bodily harm to someone"},
                {"label": "D", "text": "Be a good witness — observe and memorize details about the offender's appearance, weapon, and vehicle"},
                {"label": "E", "text": "If you do engage, clearly identify yourself as a police officer before taking any action"},
                {"label": "F", "text": "If responding officers arrive, put your weapon away immediately to avoid being mistaken for the offender"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Call 911 (A) — get on-duty units responding. Move family to safety (B) — protect "
                "civilians. Do NOT draw unless imminent threat (C) — off-duty engagement creates "
                "enormous risk. Be a witness (D) — your observations are valuable. If engaging, "
                "identify yourself (E) — mandatory before using force. Weapon away when units arrive "
                "(F) — prevent friendly fire. Off-duty officers should be WITNESSES first, not "
                "tactical responders.\n\n"
                "KEY REFERENCE: G03-02-03, Section VII (Off-Duty Firearm Discharge)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-03, Section VII (Off-Duty Considerations)",
        },

        # --- Q20 ---
        {
            "question_id": "go_rank_q20",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Authorized Firearm Use — Subject Holding Hostage at Knifepoint",
            "content": (
                "You respond to a convenience store where a subject is holding a knife to a "
                "clerk's throat. The subject is demanding money and threatening to kill the hostage. "
                "You have a clear line of sight from the doorway. The subject has not seen you yet. "
                "Rank the following actions in the correct priority order per G03-02-03 and G03-02."
            ),
            "items": [
                {"label": "A", "text": "Request a supervisor, SWAT, and a hostage negotiator immediately — do NOT attempt a solo tactical resolution"},
                {"label": "B", "text": "Attempt verbal contact using de-escalation — 'I'm here to help. Let's talk about what you need'"},
                {"label": "C", "text": "Establish a position of cover and concealment that maintains your line of sight to the subject"},
                {"label": "D", "text": "Evacuate any other civilians from the store without alerting the subject if possible"},
                {"label": "E", "text": "Deadly force is authorized ONLY if the subject begins actively cutting or stabbing the hostage"},
                {"label": "F", "text": "Secure the perimeter outside the store and prevent anyone from entering the danger zone"},
            ],
            "correct_order": [2, 3, 0, 5, 1, 4],
            "explanation": (
                "Position of cover (C) — maintain tactical advantage without alerting. Evacuate other "
                "civilians (D) quietly if possible. Request SWAT and negotiator (A) — hostage situations "
                "require specialized response. Secure perimeter (F) to control access. Attempt verbal "
                "de-escalation (B) — try to establish dialogue. Deadly force (E) only if imminent threat "
                "of death — the standard requires the subject to be ACTIVELY using deadly force.\n\n"
                "KEY REFERENCE: G03-02-03, Section III (Authorized Use); Hostage Protocol"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-03, Section III; Hostage Protocol",
        },

        # ============================================================
        # G03-02-08: DEPARTMENT REVIEW OF USE OF FORCE
        # ============================================================

        # --- Q21 ---
        {
            "question_id": "go_rank_q21",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "TRR Review — Supervisor Investigation Process",
            "content": (
                "As a sergeant, you receive a TRR from one of your officers who used an "
                "emergency takedown and OC spray during an arrest. The subject was treated "
                "at the hospital and released. You must review and investigate the use of force. "
                "Rank the following actions in the correct priority order per G03-02-08."
            ),
            "items": [
                {"label": "A", "text": "Review the officer's TRR narrative for completeness, accuracy, and whether the force described was within policy"},
                {"label": "B", "text": "Review all available BWC footage from the officer and any other officers on scene"},
                {"label": "C", "text": "Interview the subject and any independent witnesses about the use of force"},
                {"label": "D", "text": "Review the officer's previous TRR history for patterns of force use"},
                {"label": "E", "text": "Complete your supervisor's TRR investigation report with findings and forward to your commanding officer"},
                {"label": "F", "text": "Determine if the force was within policy, and if not, refer to COPA or initiate a CR investigation"},
            ],
            "correct_order": [0, 1, 2, 3, 5, 4],
            "explanation": (
                "Review TRR narrative (A) — start with the officer's account. Review BWC footage (B) — "
                "compare the video to the written account. Interview subject and witnesses (C) — get "
                "all perspectives. Review TRR history (D) — check for patterns. Determine if within "
                "policy (F) — make the finding. Complete investigation report (E) and forward.\n\n"
                "KEY REFERENCE: G03-02-08, Section IV (Supervisor TRR Investigation)"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-02-08, Section IV (TRR Investigation)",
        },

        # --- Q22 ---
        {
            "question_id": "go_rank_q22",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Review — BWC Discrepancy in TRR Investigation",
            "content": (
                "While reviewing a TRR, you notice the officer's written narrative states the "
                "subject 'charged at me swinging his fists.' However, the BWC footage shows the "
                "subject standing still with arms at his sides when the officer tackled him. "
                "Rank the following actions in the correct priority order per G03-02-08."
            ),
            "items": [
                {"label": "A", "text": "Interview the officer about the discrepancy between the TRR narrative and the BWC footage"},
                {"label": "B", "text": "Preserve and secure all BWC footage — ensure it is flagged as evidence and cannot be altered or deleted"},
                {"label": "C", "text": "Interview any other witnesses including other officers and civilians who observed the incident"},
                {"label": "D", "text": "Refer the matter to COPA for investigation as a potential excessive force and false reporting violation"},
                {"label": "E", "text": "Notify your commanding officer of the discrepancy before taking further action"},
                {"label": "F", "text": "Document the discrepancy in your supervisor's investigation report with specific timestamps from the BWC"},
            ],
            "correct_order": [1, 4, 0, 2, 5, 3],
            "explanation": (
                "Preserve BWC footage (B) first — the primary evidence must be secured. Notify "
                "commanding officer (E) — a serious discrepancy requires chain of command notification. "
                "Interview the officer (A) about the discrepancy. Interview other witnesses (C) for "
                "corroboration. Document findings (F) with timestamps. Refer to COPA (D) if the "
                "evidence supports false reporting or excessive force.\n\n"
                "KEY REFERENCE: G03-02-08, Section V (BWC in TRR Review); False Report Protocol"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-08, Section V (BWC in TRR Review)",
        },

        # --- Q23 ---
        {
            "question_id": "go_rank_q23",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Review — Pattern of Repeated Force Use",
            "content": (
                "During TRR reviews, you notice the same officer has submitted five TRRs in "
                "three months — significantly more than any other officer on the watch. Each "
                "individual use of force appeared within policy. The officer works a high-crime "
                "beat. Rank the following actions in the correct priority order per G03-02-08."
            ),
            "items": [
                {"label": "A", "text": "Review each TRR individually to confirm they were all properly investigated and within policy"},
                {"label": "B", "text": "Analyze the pattern — look for common factors such as time of day, beat assignment, type of force, and subject demographics"},
                {"label": "C", "text": "Meet with the officer to discuss the pattern and assess whether additional de-escalation training would be beneficial"},
                {"label": "D", "text": "Refer the officer for a personnel intervention through the early warning system for additional support"},
                {"label": "E", "text": "Consult with your commanding officer about the pattern and whether assignment changes should be considered"},
                {"label": "F", "text": "Document the pattern analysis and your recommendations in a memorandum to the unit commanding officer"},
            ],
            "correct_order": [0, 1, 2, 4, 3, 5],
            "explanation": (
                "Review each TRR (A) — confirm each incident was properly investigated. Analyze the "
                "pattern (B) — look for systemic issues. Meet with officer (C) — non-punitive discussion. "
                "Consult commanding officer (E) about the pattern. Refer for intervention (D) — the early "
                "warning system provides training and support, NOT discipline, when individual incidents "
                "are within policy. Document and recommend (F).\n\n"
                "KEY REFERENCE: G03-02-08, Section VI (Early Intervention); Pattern Review"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-08, Section VI (Early Intervention)",
        },

        # --- Q24 ---
        {
            "question_id": "go_rank_q24",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Force Review — Findings and Recommendations After TRR",
            "content": (
                "After completing your TRR investigation, you determine the officer's use of "
                "a Taser on a passive, non-threatening subject was NOT within policy. The subject "
                "was handcuffed and merely arguing verbally. No injuries resulted. "
                "Rank the following actions in the correct priority order per G03-02-08."
            ),
            "items": [
                {"label": "A", "text": "Document your finding that the Taser deployment was not within policy in your investigation report"},
                {"label": "B", "text": "Forward the investigation to your commanding officer with a recommendation for corrective action"},
                {"label": "C", "text": "Notify COPA of the out-of-policy use of force for potential misconduct investigation"},
                {"label": "D", "text": "Counsel the officer on the appropriate use of Taser and review the force options continuum"},
                {"label": "E", "text": "Review whether the subject filed a complaint and ensure the subject was informed of the complaint process"},
                {"label": "F", "text": "Consider whether additional training for the entire watch on Taser policy is warranted"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Document the finding (A) — the investigation report must reflect the out-of-policy "
                "determination. Forward to CO (B) with recommendations. Notify COPA (C) — out-of-policy "
                "force requires COPA notification. Counsel the officer (D) on correct Taser use. Check "
                "complaint status (E) — ensure subject's rights are protected. Consider unit training "
                "(F) — systemic improvement.\n\n"
                "KEY REFERENCE: G03-02-08, Section VII (Findings); COPA Notification Requirements"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-02-08, Section VII (Findings and Recommendations)",
        },

        # ============================================================
        # G04-02: CRIME SCENE PROTECTION AND PROCESSING
        # ============================================================

        # --- Q25 ---
        {
            "question_id": "go_rank_q25",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — First Responding Officer at Homicide",
            "content": (
                "You are the first officer to arrive at a reported homicide. The victim is "
                "lying in the living room of an apartment. A family member is performing CPR. "
                "You confirm the victim has no pulse and see multiple stab wounds. A bloody "
                "knife is on the kitchen counter. Rank the following actions in the correct "
                "priority order per G04-02."
            ),
            "items": [
                {"label": "A", "text": "Confirm death by checking for signs of life — if no pulse and obvious fatal injuries, note the time"},
                {"label": "B", "text": "Secure the scene with crime scene tape — establish an inner perimeter around the apartment and outer perimeter at the building entrance"},
                {"label": "C", "text": "Start a crime scene log documenting every person who enters or exits the scene with their name, badge, and time"},
                {"label": "D", "text": "Protect evidence pathways — limit foot traffic through the apartment to a single entry/exit path"},
                {"label": "E", "text": "Request detectives, Evidence Technicians, and the Medical Examiner to respond to the scene"},
                {"label": "F", "text": "Identify and separate the family member and any other potential witnesses — do NOT let them leave"},
            ],
            "correct_order": [0, 1, 3, 5, 2, 4],
            "explanation": (
                "Confirm death (A) — assess for signs of life first. Secure the scene (B) with inner "
                "and outer perimeters. Protect evidence pathways (D) — limit foot traffic. Identify "
                "and separate witnesses (F) — the family member may have critical information. Start "
                "crime scene log (C) — document everyone who enters. Request detectives and ET (E) — "
                "beat officers do NOT process homicide scenes.\n\n"
                "KEY REFERENCE: G04-02, Section III (First Responder Duties); Scene Security"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G04-02, Section III (First Responder Duties)",
        },

        # --- Q26 ---
        {
            "question_id": "go_rank_q26",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — Evidence Integrity After Contamination",
            "content": (
                "At an officer-involved death scene, you discover that a responding officer "
                "picked up shell casings from the street and placed them on the hood of a "
                "squad car 'so they wouldn't get run over.' The original locations are unknown. "
                "Rank the following actions in the correct priority order per G04-02."
            ),
            "items": [
                {"label": "A", "text": "Do NOT return the casings to the street — placing them in approximate locations creates false evidence positioning"},
                {"label": "B", "text": "Photograph the casings in their current location on the squad car hood"},
                {"label": "C", "text": "Document the chain of custody breach — who moved them, from where (if known), to where, and when"},
                {"label": "D", "text": "Interview the officer who moved them to determine if he remembers the approximate original locations"},
                {"label": "E", "text": "Collect and inventory the casings with a note in the evidence report about the custody breach"},
                {"label": "F", "text": "Brief the lead detective and COPA investigator about the evidence contamination"},
            ],
            "correct_order": [0, 1, 2, 3, 5, 4],
            "explanation": (
                "Do NOT return casings (A) — this would create false documentation, which is worse "
                "than the original contamination. Photograph current location (B) — document the actual "
                "state. Document the breach (C) — who, what, when. Interview the officer (D) for "
                "approximate originals. Brief lead detective and COPA (F) about the contamination. "
                "Collect and inventory (E) with breach documentation. The casings still have forensic "
                "value (fingerprints, ballistic matching) despite the location contamination.\n\n"
                "KEY REFERENCE: G04-02, Section IV (Evidence Integrity); Chain of Custody"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G04-02, Section IV (Evidence Integrity)",
        },

        # --- Q27 ---
        {
            "question_id": "go_rank_q27",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — Expanding the Scene After New Evidence",
            "content": (
                "At a shooting scene, you have secured a perimeter around the victim's body "
                "and shell casings. A witness now tells you the shooter ran through the alley "
                "behind the building and dropped a gun in a dumpster two blocks away. "
                "Rank the following actions in the correct priority order per G04-02."
            ),
            "items": [
                {"label": "A", "text": "Immediately dispatch officers to secure the dumpster area and prevent anyone from accessing it"},
                {"label": "B", "text": "Extend the crime scene perimeter to include the alley and the path the suspect reportedly took"},
                {"label": "C", "text": "Do NOT retrieve the gun from the dumpster yourself — wait for Evidence Technicians to process it properly"},
                {"label": "D", "text": "Document the witness's statement in detail including the time, route described, and dumpster location"},
                {"label": "E", "text": "Canvas the alley for additional evidence — discarded clothing, blood trail, additional witnesses"},
                {"label": "F", "text": "Notify the lead detective of the expanded scene and request additional ET resources"},
            ],
            "correct_order": [0, 1, 2, 5, 3, 4],
            "explanation": (
                "Dispatch to secure dumpster (A) — prevent evidence loss or tampering. Extend perimeter "
                "(B) to include the flight path. Do NOT retrieve gun yourself (C) — ET must process for "
                "prints, DNA. Notify lead detective (F) for additional resources. Document the witness "
                "statement (D) in detail. Canvas the alley (E) for more evidence.\n\n"
                "KEY REFERENCE: G04-02, Section V (Scene Expansion); Evidence Recovery"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G04-02, Section V (Scene Expansion)",
        },

        # --- Q28 ---
        {
            "question_id": "go_rank_q28",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — Weather Threats to Evidence",
            "content": (
                "You are securing a shooting scene on an open street. It begins to rain heavily. "
                "Blood evidence, shell casings, and a discarded weapon are exposed to the rain. "
                "Evidence Technicians are 30 minutes away. Rank the following actions in the "
                "correct priority order per G04-02."
            ),
            "items": [
                {"label": "A", "text": "Cover exposed evidence with tarps, cones, or squad car placement to protect it without moving it from its location"},
                {"label": "B", "text": "Photograph all evidence in its current position immediately before the rain washes it away"},
                {"label": "C", "text": "Document the weather conditions, the time rain began, and all protective measures you took in your notes"},
                {"label": "D", "text": "If evidence is at immediate risk of being destroyed, carefully collect and package it noting its original location with measurements"},
                {"label": "E", "text": "Contact Evidence Technicians to request expedited response due to weather threatening evidence"},
                {"label": "F", "text": "Establish traffic control to prevent vehicles from driving through the scene and splashing water onto evidence"},
            ],
            "correct_order": [5, 0, 1, 4, 3, 2],
            "explanation": (
                "Traffic control (F) — prevent vehicles from destroying evidence. Cover evidence (A) — "
                "protect in place without moving. Photograph immediately (B) — document before further "
                "deterioration. Request expedited ET (E) due to weather. Collect at-risk evidence (D) — "
                "last resort if evidence would otherwise be destroyed, with detailed location notes. "
                "Document conditions (C) in your notes.\n\n"
                "KEY REFERENCE: G04-02, Section III (Evidence Protection); Environmental Threats"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G04-02, Section III (Evidence Protection)",
        },

        # --- Q29 ---
        {
            "question_id": "go_rank_q29",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Crime Scene — Crime Scene Log and Access Control",
            "content": (
                "You are maintaining the crime scene log at a homicide. A deputy chief arrives "
                "and demands to walk through the scene without signing in. Your sergeant tells "
                "you to let the deputy chief through. Several media crews are also requesting "
                "access. Rank the following actions in the correct priority order per G04-02."
            ),
            "items": [
                {"label": "A", "text": "Respectfully inform the deputy chief that EVERYONE entering the scene must be logged — no exceptions regardless of rank"},
                {"label": "B", "text": "Log the deputy chief's name, rank, badge number, time of entry, and reason for entering the scene"},
                {"label": "C", "text": "Deny all media access to the crime scene — direct them to the PIO for information"},
                {"label": "D", "text": "Provide the deputy chief with a designated pathway through the scene to avoid evidence areas"},
                {"label": "E", "text": "Notify the lead detective that a command staff member has entered the scene"},
                {"label": "F", "text": "Document any evidence that may have been disturbed and note who was present in the affected area"},
            ],
            "correct_order": [0, 1, 3, 2, 4, 5],
            "explanation": (
                "Log everyone — no exceptions (A) — G04-02 requires ALL persons to be documented, "
                "regardless of rank. Log the deputy chief (B) per procedure. Provide designated pathway "
                "(D) — minimize contamination. Deny media (C) — crime scenes are closed to press. Notify "
                "lead detective (E) of command staff entry. Document any disturbance (F) for the record.\n\n"
                "KEY REFERENCE: G04-02, Section VI (Crime Scene Log); Access Control"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G04-02, Section VI (Crime Scene Log)",
        },

        # ============================================================
        # S03-14: BODY WORN CAMERAS
        # ============================================================

        # --- Q30 ---
        {
            "question_id": "go_rank_q30",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "BWC — Mandatory Activation at Traffic Stop Shooting",
            "content": (
                "You initiate a traffic stop. As you approach the driver's window, the driver "
                "suddenly produces a firearm and fires at you. You return fire and the driver "
                "is struck. You realize your BWC was not activated before the encounter. "
                "Rank the following actions in the correct priority order per S03-14."
            ),
            "items": [
                {"label": "A", "text": "Activate your BWC immediately — the pre-event buffer will capture the last 2 minutes of video without audio"},
                {"label": "B", "text": "Request EMS for the driver and render first aid while the BWC records the post-shooting scene"},
                {"label": "C", "text": "Notify your supervisor that the BWC was not activated prior to the encounter and explain the circumstances"},
                {"label": "D", "text": "Ensure other responding officers' BWCs are activated and recording as they arrive on scene"},
                {"label": "E", "text": "Do NOT review your BWC footage — per S03-14, involved members shall not review BWC before providing a statement"},
                {"label": "F", "text": "Complete a BWC metadata log noting the activation time, pre-event buffer status, and any gaps in recording"},
            ],
            "correct_order": [0, 1, 3, 4, 2, 5],
            "explanation": (
                "Activate BWC immediately (A) — the pre-event buffer captures 2 minutes of video, which "
                "may include the shooting. Render aid (B) while recording. Ensure other BWCs are on (D). "
                "Do NOT review footage (E) — involved officers cannot review before providing statements. "
                "Notify supervisor (C) of the late activation. Complete metadata log (F).\n\n"
                "KEY REFERENCE: S03-14, Section IV (Mandatory Activation); Pre-Event Buffer; "
                "Involved Member Review Restrictions"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "S03-14, Section IV (Mandatory Activation)",
        },

        # --- Q31 ---
        {
            "question_id": "go_rank_q31",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "BWC — Prohibited Actions and Sensitive Locations",
            "content": (
                "While investigating a domestic battery, the female victim invites you inside "
                "her apartment. She begins changing clothes in the bedroom while talking to you "
                "about the assault. Her 10-year-old child is present and wants to describe what "
                "happened. A confidential informant calls your phone during the interview. "
                "Rank the following actions in the correct priority order per S03-14."
            ),
            "items": [
                {"label": "A", "text": "Step out of the bedroom or avert the camera while the victim changes — do NOT record someone in a state of undress"},
                {"label": "B", "text": "When interviewing the minor child, ensure a parent or guardian is present and the BWC is recording"},
                {"label": "C", "text": "Do NOT record the confidential informant conversation — step away and deactivate BWC for the CI call"},
                {"label": "D", "text": "Reactivate BWC immediately after the CI call and verbally note the reason for the gap in recording"},
                {"label": "E", "text": "The victim can request recording stop in her home — but you should explain why recording is important for her case"},
                {"label": "F", "text": "Do NOT use BWC footage for personal purposes, to record other officers during non-enforcement activities, or share with unauthorized persons"},
            ],
            "correct_order": [0, 2, 3, 1, 4, 5],
            "explanation": (
                "Privacy during changing (A) — recording someone in a state of undress is prohibited. "
                "CI call protection (C) — confidential informant conversations must NOT be recorded. "
                "Reactivate and note gap (D) — document the reason. Interview minor with guardian (B) — "
                "BWC should record but with proper safeguards. Victim's right to request (E) — explain "
                "importance but honor the request. Prohibited uses (F) — general prohibition.\n\n"
                "KEY REFERENCE: S03-14, Section VI (Prohibited Actions); Section V (Sensitive Locations)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "S03-14, Sections V-VI (Sensitive Locations; Prohibited Actions)",
        },

        # --- Q32 ---
        {
            "question_id": "go_rank_q32",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "BWC — End of Encounter Documentation",
            "content": (
                "After completing an arrest involving a use of force, you are preparing to "
                "transport the subject to the district. The subject is secured in the back "
                "of your squad. Your sergeant asks when you can deactivate your BWC. "
                "Rank the following actions in the correct priority order per S03-14."
            ),
            "items": [
                {"label": "A", "text": "Do NOT deactivate until the entire encounter is complete — including transport, processing, and lockup"},
                {"label": "B", "text": "Record a verbal summary on BWC before deactivation: date, time, RD number, charges, force used"},
                {"label": "C", "text": "Ensure the BWC footage is properly categorized and flagged as a use-of-force event in the system"},
                {"label": "D", "text": "Upload/dock the BWC at the end of your tour of duty — do NOT wait until the next day"},
                {"label": "E", "text": "Notify your supervisor if any portion of the encounter was NOT recorded and document the reason"},
                {"label": "F", "text": "Do NOT delete, alter, or copy BWC footage — any tampering is a serious policy violation"},
            ],
            "correct_order": [0, 4, 1, 2, 3, 5],
            "explanation": (
                "Keep recording through completion (A) — BWC must remain active through the entire "
                "encounter including transport and processing. Report gaps (E) if any portion was "
                "missed. Verbal summary (B) before deactivation. Categorize footage (C) as use-of-force. "
                "Upload at end of tour (D) — timely docking is required. No tampering (F) — deletion "
                "or alteration is a terminable offense.\n\n"
                "KEY REFERENCE: S03-14, Section VII (End of Encounter); Section VIII (Upload/Retention)"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "S03-14, Sections VII-VIII",
        },

        # --- Q33 ---
        {
            "question_id": "go_rank_q33",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "BWC — Recording Inside a Hospital",
            "content": (
                "You transport a shooting victim to the emergency room. The victim is conscious "
                "and wants to make a dying declaration identifying the shooter. Medical staff "
                "are performing emergency treatment. Other patients are visible in the ER. "
                "Rank the following actions in the correct priority order per S03-14."
            ),
            "items": [
                {"label": "A", "text": "Keep BWC activated to capture the dying declaration — this is critical evidence for the investigation"},
                {"label": "B", "text": "Minimize recording of other patients and medical procedures not related to your investigation"},
                {"label": "C", "text": "Request medical staff allow a brief recorded statement from the victim before treatment if time permits"},
                {"label": "D", "text": "Position yourself and the camera to focus on the victim's face and avoid capturing other patients"},
                {"label": "E", "text": "If hospital security objects to recording, explain that BWC activation is mandatory during law enforcement encounters"},
                {"label": "F", "text": "Document the dying declaration in your notes as well — record the victim's exact words, time, and witnesses present"},
            ],
            "correct_order": [0, 3, 1, 2, 4, 5],
            "explanation": (
                "Keep BWC active (A) — a dying declaration is critical evidence and BWC must remain "
                "on during law enforcement encounters. Position to focus on victim (D) — minimize "
                "other patients. Minimize non-relevant recording (B) — privacy consideration. Request "
                "brief statement (C) — coordinate with medical staff. Address hospital objections (E) — "
                "BWC is mandatory per policy. Written documentation (F) backs up the recording.\n\n"
                "KEY REFERENCE: S03-14, Section V (Sensitive Locations — Hospitals); "
                "Dying Declaration Protocol"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "S03-14, Section V (Hospitals); Dying Declaration",
        },

        # ============================================================
        # G03-06: OID RESPONSE AND INVESTIGATION
        # ============================================================

        # --- Q34 ---
        {
            "question_id": "go_rank_q34",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Definition and Scope of Officer-Involved Death",
            "content": (
                "A subject in custody dies after officers delayed calling for medical attention "
                "for over an hour despite the subject complaining of chest pains. The officers "
                "were on duty at the time. The watch commander must determine how to classify "
                "this incident. Rank the following actions in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Classify this as an officer-involved death — G03-06 includes deaths from intentional omissions such as unreasonable delay in seeking medical attention"},
                {"label": "B", "text": "Notify COPA immediately — they have investigative authority over all officer-involved deaths"},
                {"label": "C", "text": "Activate the full G03-06 notification chain including CPIC, Deputy Chief, State's Attorney, and Medical Examiner"},
                {"label": "D", "text": "Separate the involved officers and instruct them not to discuss the incident with each other or anyone else"},
                {"label": "E", "text": "Preserve all evidence including lockup video, medical request logs, BWC footage, and radio transmissions"},
                {"label": "F", "text": "Secure the area where the subject was held in custody as a crime scene — no one enters without authorization"},
            ],
            "correct_order": [0, 3, 5, 4, 1, 2],
            "explanation": (
                "Classify as OID (A) — per 50 ILCS 727/1-5, 'officer-involved death' includes deaths "
                "resulting from intentional omissions INCLUDING unreasonable delay in seeking medical "
                "attention. The definition is BROADER than most think. Separate officers (D) immediately. "
                "Secure the scene (F) — the custody area is now a crime scene. Preserve evidence (E) — "
                "video, logs, BWC. Notify COPA (B) — mandatory for OID. Full notification chain (C).\n\n"
                "KEY REFERENCE: G03-06, Section II-A-3; 50 ILCS 727/1-5"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-06, Section II-A-3; 50 ILCS 727/1-5",
        },

        # --- Q35 ---
        {
            "question_id": "go_rank_q35",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — First Supervisor at Officer-Involved Shooting",
            "content": (
                "You are the first supervisor to arrive at an officer-involved shooting. "
                "The subject is down with gunshot wounds. The involved officer is standing "
                "nearby, visibly shaken but physically uninjured. EMS has not been called. "
                "Several witness officers are discussing what happened. Rank the following "
                "actions in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Request EMS for the subject and render first aid until they arrive — duty to provide medical care"},
                {"label": "B", "text": "Separate the involved officer from witness officers and instruct ALL members not to discuss the incident"},
                {"label": "C", "text": "Obtain a public safety statement from the involved officer — limited to threats, outstanding suspects, direction of flight, and injuries"},
                {"label": "D", "text": "Secure the scene, establish a perimeter, and begin a crime scene log of everyone present"},
                {"label": "E", "text": "Notify CPIC to initiate the required notification chain — COPA, SAO, Deputy Chief, Medical Examiner"},
                {"label": "F", "text": "Recover the involved officer's firearm — secure it as evidence and provide a replacement weapon"},
            ],
            "correct_order": [0, 3, 1, 2, 4, 5],
            "explanation": (
                "Request EMS and render aid (A) — ALWAYS the top priority. Secure the scene (D) to "
                "preserve evidence and control access. Separate all members (B) to prevent cross-"
                "contamination of accounts. Obtain public safety statement (C) — limited to immediate "
                "threats and safety. Notify CPIC (E) to activate notifications. Recover firearm (F) "
                "after immediate priorities.\n\n"
                "KEY REFERENCE: G03-06, Sections V-VII; G03-02-03, Section VI (Duty to Render Aid)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-06, Sections V-VII",
        },

        # --- Q36 ---
        {
            "question_id": "go_rank_q36",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — COPA vs. CPD Investigative Authority",
            "content": (
                "An officer-involved shooting has occurred where the subject was struck and "
                "seriously injured but survived. Both COPA investigators and CPD detectives "
                "are responding to the scene. There is confusion about who controls what. "
                "Rank the following roles and responsibilities in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "COPA has primary authority over the officer's use of force investigation — the misconduct/accountability track"},
                {"label": "B", "text": "CPD Bureau of Detectives investigates the criminal incident that led to the encounter — the criminal investigation track"},
                {"label": "C", "text": "The scene must be jointly processed — COPA and CPD conduct a coordinated scene walk-through before evidence is moved"},
                {"label": "D", "text": "Witness officers provide statements to COPA — they are ordered to cooperate with the misconduct investigation"},
                {"label": "E", "text": "The involved officer provides a public safety statement only — detailed statements come later with legal representation"},
                {"label": "F", "text": "Both investigations run in parallel — neither takes precedence over the other and both must be accommodated at the scene"},
            ],
            "correct_order": [5, 2, 0, 1, 4, 3],
            "explanation": (
                "Parallel investigations (F) — neither COPA nor CPD takes precedence; both must be "
                "accommodated. Joint scene processing (C) — coordinated walk-through before evidence "
                "moves. COPA authority (A) over the force investigation. CPD authority (B) over the "
                "criminal investigation. Involved officer public safety statement only (E) — detailed "
                "statement later. Witness officer statements to COPA (D) — ordered to cooperate.\n\n"
                "KEY REFERENCE: G03-06, Section IV (Dual-Track Investigation); COPA Jurisdiction"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-06, Section IV (Investigative Authority)",
        },

        # --- Q37 ---
        {
            "question_id": "go_rank_q37",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Involved Member Immediate Duties After Shooting",
            "content": (
                "You have just been involved in a shooting where you fired your weapon, striking "
                "the subject. The subject is down and not moving. Your partner is with you. "
                "You are physically uninjured. Rank the following actions YOU must take in the "
                "correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Approach and render first aid to the subject — request EMS on an emergency basis"},
                {"label": "B", "text": "Secure the subject's weapon if one is present — do NOT touch it if it can be secured by perimeter alone"},
                {"label": "C", "text": "Notify OEMC that shots have been fired by police and provide your exact location"},
                {"label": "D", "text": "Remain on the scene and do NOT discuss what happened with anyone except your attorney or FOP representative"},
                {"label": "E", "text": "Provide a public safety statement to the first responding supervisor — threats, suspects, weapons, injuries only"},
                {"label": "F", "text": "Do NOT handle or alter evidence — leave shell casings, weapons, and your firearm for investigators"},
            ],
            "correct_order": [0, 2, 1, 5, 3, 4],
            "explanation": (
                "Render aid (A) — constitutional and policy obligation, even to the person you shot. "
                "Notify OEMC (C) — shots fired by police notification. Secure subject's weapon (B) — "
                "for safety only, secure by perimeter if possible. Do NOT alter evidence (F). Remain "
                "on scene (D) — mandatory, and do not discuss details. Public safety statement (E) — "
                "provide when supervisor arrives.\n\n"
                "KEY REFERENCE: G03-06, Section V (Involved Member Duties)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-06, Section V (Involved Member Duties)",
        },

        # --- Q38 ---
        {
            "question_id": "go_rank_q38",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — CPIC Notification Chain",
            "content": (
                "An officer-involved death has occurred. As the on-scene supervisor, you must "
                "initiate the notification chain through CPIC (Crime Prevention and Information "
                "Center). The subject is deceased. COPA has been called. Rank the following "
                "notifications in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Notify CPIC with the basic facts — location, nature of incident, involved member information, and subject status"},
                {"label": "B", "text": "CPIC notifies the Deputy Chief of the affected area to respond to the scene"},
                {"label": "C", "text": "CPIC notifies the Superintendent's office and the Chief of Detectives"},
                {"label": "D", "text": "CPIC notifies the Cook County State's Attorney's Office for Felony Review"},
                {"label": "E", "text": "CPIC notifies the Medical Examiner to respond for the deceased subject"},
                {"label": "F", "text": "CPIC notifies the Office of News Affairs for media management and public communication"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Notify CPIC with facts (A) — initiates the entire chain. Deputy Chief (B) — "
                "responds to scene as incident commander. Superintendent and Chief of Detectives "
                "(C) — command notification. State's Attorney (D) — for criminal investigation "
                "authority. Medical Examiner (E) — for the deceased. News Affairs (F) — for media "
                "management. Each notification triggers automatically once CPIC is contacted.\n\n"
                "KEY REFERENCE: G03-06, Section VI (CPIC Notification Requirements)"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-06, Section VI (CPIC Notifications)",
        },

        # --- Q39 ---
        {
            "question_id": "go_rank_q39",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Firearm Recovery from Involved Officer",
            "content": (
                "At an officer-involved shooting scene, the street deputy tells you to recover "
                "the involved officer's firearm. The officer is upset and holding his duty weapon "
                "at his side. He has already been separated from witnesses. "
                "Rank the following actions in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Approach the officer calmly and explain that firearm recovery is standard procedure for all police shootings"},
                {"label": "B", "text": "Have the officer make the weapon safe (magazine out, chamber clear) and hand it to you — do NOT grab it from him"},
                {"label": "C", "text": "Photograph the firearm before securing it — document the model, serial number, round count, and condition"},
                {"label": "D", "text": "Place the firearm in an evidence bag, seal it, and start a chain of custody log"},
                {"label": "E", "text": "Provide the officer with a replacement duty weapon so he is not unarmed for the remainder of his tour"},
                {"label": "F", "text": "Document the recovery in your notes — who recovered it, from whom, time, location, and condition of the weapon"},
            ],
            "correct_order": [0, 1, 2, 3, 5, 4],
            "explanation": (
                "Approach calmly and explain (A) — the officer is likely in distress; treat with "
                "dignity. Officer makes weapon safe and hands it over (B) — do not forcibly take it. "
                "Photograph the weapon (C) — document before bagging. Evidence bag with chain of "
                "custody (D). Document the recovery (F) in notes. Provide replacement weapon (E).\n\n"
                "KEY REFERENCE: G03-06, Section VII (Firearm Recovery); Evidence Handling"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-06, Section VII (Firearm Recovery)",
        },

        # --- Q40 ---
        {
            "question_id": "go_rank_q40",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Witness Officer Separation and Statements",
            "content": (
                "At an OID scene, there are four witness officers who saw the shooting. They "
                "are standing together near their squad cars talking about what happened. The "
                "involved officer is nearby listening. COPA investigators are en route. "
                "Rank the following actions in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Immediately separate ALL witness officers from each other and from the involved officer — each must be isolated"},
                {"label": "B", "text": "Instruct each witness officer not to discuss the incident with anyone until they provide a formal statement"},
                {"label": "C", "text": "Collect each witness officer's BWC and secure the footage — do NOT allow them to review their own recordings"},
                {"label": "D", "text": "Assign a non-witness officer to stay with the involved member for welfare support"},
                {"label": "E", "text": "Obtain identifying information from each witness officer — name, star, unit, and their location during the incident"},
                {"label": "F", "text": "When COPA arrives, direct the witness officers to cooperate — they are ORDERED to provide statements to COPA investigators"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Separate immediately (A) — cross-contamination of accounts is the biggest threat "
                "to investigative integrity. Instruct no discussion (B) — reinforce separation. "
                "Secure BWC footage (C) — witnesses cannot review their own recordings. Assign "
                "welfare officer (D) to involved member. Obtain identifying info (E) from each. "
                "COPA cooperation (F) — witness officers ARE ordered to cooperate.\n\n"
                "KEY REFERENCE: G03-06, Section VIII (Witness Officers); Separation Protocol"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-06, Section VIII (Witness Officers)",
        },

        # --- Q41 ---
        {
            "question_id": "go_rank_q41",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Video Evidence Review Protocol",
            "content": (
                "As the lead detective at an OID scene, you learn that a POD camera, two "
                "private surveillance cameras, a Ring doorbell, and a bystander's cell phone "
                "may have captured the incident. BWC footage from 6 officers also exists. "
                "Rank the following actions in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Secure all BWC footage from every officer on scene — flag as OID evidence and restrict access"},
                {"label": "B", "text": "Request OEMC to preserve the POD camera footage before it is automatically overwritten"},
                {"label": "C", "text": "Contact the bystander and request their cell phone video — offer to copy it on scene if they will not surrender the phone"},
                {"label": "D", "text": "Serve emergency preservation requests on the private surveillance camera owners before footage is overwritten"},
                {"label": "E", "text": "Coordinate with COPA on a joint review of all video evidence before either agency views it independently"},
                {"label": "F", "text": "Create a video evidence log documenting every source identified, its status, who secured it, and chain of custody"},
            ],
            "correct_order": [0, 1, 3, 2, 5, 4],
            "explanation": (
                "Secure BWC (A) — department-controlled footage first, easiest to preserve. POD camera "
                "(B) — request OEMC preservation before auto-overwrite. Private surveillance (D) — serve "
                "emergency preservation before business owners delete or overwrite. Bystander video (C) — "
                "request cooperation. Video log (F) — document all sources. Joint COPA review (E) — "
                "coordinate before independent viewing.\n\n"
                "KEY REFERENCE: G03-06, Section VIII-E (Video Evidence); S03-14 (BWC Preservation)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-06, Section VIII-E; S03-14",
        },

        # --- Q42 ---
        {
            "question_id": "go_rank_q42",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Involved Member Support and Welfare",
            "content": (
                "An officer involved in a fatal shooting is at the scene. He is emotionally "
                "distraught, shaking, and repeating 'I had no choice.' His partner, who was "
                "a witness to the shooting, wants to comfort him and asks you what to do. "
                "Rank the following actions in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Separate the partner (witness) from the involved officer — witnesses and involved members MUST be kept apart"},
                {"label": "B", "text": "Assign a non-witness peer support officer to stay with the involved member for emotional support"},
                {"label": "C", "text": "Instruct the peer support officer that the involved member should NOT discuss details of the incident"},
                {"label": "D", "text": "Request the Chaplain Unit to respond for the involved member's spiritual and emotional welfare"},
                {"label": "E", "text": "Contact the Employee Assistance Program (EAP) to arrange professional counseling support"},
                {"label": "F", "text": "Ensure the involved member knows he has the right to FOP representation before any detailed statement"},
            ],
            "correct_order": [0, 1, 2, 5, 3, 4],
            "explanation": (
                "Separate partner/witness (A) — investigative integrity requires separation even "
                "though the partner wants to help. Assign peer support (B) — a non-witness officer "
                "provides companionship without contamination. No incident discussion (C) — support "
                "without details. Right to representation (F) — inform of FOP rights. Chaplain (D) "
                "for spiritual support. EAP (E) for professional counseling.\n\n"
                "KEY REFERENCE: G03-06, Section IX (Member Welfare); Peer Support; EAP"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-06, Section IX (Member Welfare)",
        },

        # --- Q43 ---
        {
            "question_id": "go_rank_q43",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Street Deputy Incident Commander Responsibilities",
            "content": (
                "The street deputy arrives at an officer-involved shooting scene. The first "
                "supervisor has rendered aid, separated officers, and secured a basic perimeter. "
                "COPA is 15 minutes away. Media vans are arriving. The deputy assumes command. "
                "Rank the following actions in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Assess and expand the perimeter if needed — ensure all evidence areas are within the secured zone"},
                {"label": "B", "text": "Confirm that the involved and witness officers are separated and have been given non-discussion orders"},
                {"label": "C", "text": "Designate a media staging area and direct News Affairs personnel to handle all press inquiries"},
                {"label": "D", "text": "Review the public safety statement obtained from the involved officer and assess for outstanding threats"},
                {"label": "E", "text": "Coordinate with the arriving COPA team on scene access, evidence walk-through, and interview scheduling"},
                {"label": "F", "text": "Brief the Chief of Detectives or designee and ensure the lead detective has been assigned and briefed"},
            ],
            "correct_order": [0, 1, 3, 5, 2, 4],
            "explanation": (
                "Assess perimeter (A) — first command action is to ensure scene security. Confirm "
                "separation (B) — verify the most critical investigative safeguard. Review public "
                "safety statement (D) — check for ongoing threats. Brief Chief of Detectives (F) — "
                "ensure investigative leadership. Media staging (C) — manage the press. Coordinate "
                "with COPA (E) when they arrive.\n\n"
                "KEY REFERENCE: G03-06, Section VI (Incident Commander); Street Deputy Duties"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-06, Section VI (Incident Commander)",
        },

        # --- Q44 ---
        {
            "question_id": "go_rank_q44",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Lead Investigator Certification Requirements",
            "content": (
                "You are a detective assigned as lead investigator on an officer-involved death. "
                "This is a complex scene with multiple shooters (officers), one deceased subject, "
                "and numerous witnesses. You have never been a lead on an OID before. "
                "Rank the following actions in the correct priority order per G03-06."
            ),
            "items": [
                {"label": "A", "text": "Confirm with your commanding officer that you meet the certification requirements to serve as lead OID investigator"},
                {"label": "B", "text": "Conduct a scene walk-through with COPA investigators before any evidence is collected or moved"},
                {"label": "C", "text": "Create a master witness list and coordinate with COPA on who interviews which witnesses"},
                {"label": "D", "text": "Assign tasks to assisting detectives — scene processing, canvass, video recovery, hospital follow-up"},
                {"label": "E", "text": "Review all BWC footage identified so far and create a timeline of events"},
                {"label": "F", "text": "Prepare a preliminary report for the Chief of Detectives summarizing initial findings"},
            ],
            "correct_order": [0, 1, 3, 2, 4, 5],
            "explanation": (
                "Confirm certification (A) — G03-06 requires lead OID investigators to meet specific "
                "training and certification requirements. Joint walk-through with COPA (B) — mandatory "
                "before evidence collection. Assign detective tasks (D) — organize the investigation. "
                "Master witness list with COPA (C) — coordinate parallel interviews. Review BWC and "
                "timeline (E). Preliminary report (F) to command.\n\n"
                "KEY REFERENCE: G03-06, Section VIII (Lead Investigator); Certification Requirements"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-06, Section VIII (Lead Investigator)",
        },

        # --- Q45 ---
        {
            "question_id": "go_rank_q45",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "OID — Accidental Discharge Investigation",
            "content": (
                "An officer accidentally discharges his weapon inside the district station. "
                "The round strikes the floor and no one is injured. The officer immediately "
                "reports it to the desk sergeant. Rank the following actions in the correct "
                "priority order per G03-06 and G03-02-03."
            ),
            "items": [
                {"label": "A", "text": "Confirm no one is injured — check for ricochets and ensure the area is safe"},
                {"label": "B", "text": "Recover the officer's firearm for inspection — determine if there is a mechanical defect or if it was officer error"},
                {"label": "C", "text": "Secure the discharge scene — locate the bullet or bullet fragment and photograph the impact point"},
                {"label": "D", "text": "Notify CPIC — all firearm discharges require notification regardless of whether anyone is injured"},
                {"label": "E", "text": "Complete a TRR and firearm discharge report documenting the circumstances of the accidental discharge"},
                {"label": "F", "text": "The officer should provide a detailed written statement explaining exactly how the discharge occurred"},
            ],
            "correct_order": [0, 2, 3, 1, 5, 4],
            "explanation": (
                "Confirm safety (A) — ensure no one is hurt and the area is safe. Secure scene and "
                "evidence (C) — locate the bullet and document. Notify CPIC (D) — ALL firearm discharges "
                "require notification. Recover firearm (B) for inspection. Officer's written statement "
                "(F) explaining circumstances. TRR and discharge report (E).\n\n"
                "KEY REFERENCE: G03-06, Section II (All Discharges); G03-02-03, Section VIII "
                "(Accidental/Unintentional Discharge)"
            ),
            "difficulty": "medium",
            "is_premium": True,
            "reference": "G03-06, Section II; G03-02-03, Section VIII",
        },

        # ============================================================
        # CROSS-DIRECTIVE INTEGRATION
        # ============================================================

        # --- Q46 ---
        {
            "question_id": "go_rank_q46",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — BWC at OID Scene (S03-14 + G03-06)",
            "content": (
                "Officers have used force to arrest a subject after a foot chase. One officer "
                "deployed a Taser, another used a control hold. The subject is now in custody "
                "and complaining of pain. Multiple officers have BWC. A bystander recorded "
                "on a cell phone. Rank the following BWC-related actions in the correct "
                "priority order per S03-14 and G03-02."
            ),
            "items": [
                {"label": "A", "text": "Confirm all officers' BWCs are still recording — do not deactivate until the entire encounter is complete including medical treatment"},
                {"label": "B", "text": "Request EMS for the subject and document the medical response on BWC"},
                {"label": "C", "text": "Identify all officers whose BWC captured the incident and note their star numbers for the BWC log"},
                {"label": "D", "text": "Request the bystander's cell phone video or obtain their contact information for follow-up"},
                {"label": "E", "text": "Ensure involved officers do NOT review their own BWC footage until authorized by the investigating supervisor"},
                {"label": "F", "text": "Complete the BWC metadata log noting activation time, deactivation time, and any gaps in recording for each officer"},
            ],
            "correct_order": [0, 1, 4, 2, 3, 5],
            "explanation": (
                "Confirm BWCs still recording (A) — must remain active through the entire encounter. "
                "Request EMS (B) — medical care documented on BWC. No self-review (E) — involved "
                "officers cannot review before statements. Identify all BWC sources (C). Request "
                "bystander video (D). Complete metadata logs (F).\n\n"
                "KEY REFERENCE: S03-14, Section IV (Mandatory Activation); G03-02, Section VII"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "S03-14, Section IV; G03-02, Section VII",
        },

        # --- Q47 ---
        {
            "question_id": "go_rank_q47",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — Crime Scene at OID (G04-02 + G03-06)",
            "content": (
                "You are the lead detective at an officer-involved death scene. The subject "
                "was shot and killed after pointing a replica firearm at officers. The replica "
                "is on the ground near the body. Shell casings are in the street. COPA is "
                "en route. Rank the following evidence processing actions in the correct "
                "priority order per G04-02 and G03-06."
            ),
            "items": [
                {"label": "A", "text": "Preserve all BWC footage — identify every officer's camera and flag the recordings as OID evidence"},
                {"label": "B", "text": "Coordinate with COPA on a joint scene walk-through before any evidence is moved or collected"},
                {"label": "C", "text": "Photograph the entire scene with the replica firearm, body, and casings in place — use measurement markers"},
                {"label": "D", "text": "Request Evidence Technicians for forensic processing — fingerprints on the replica, ballistic analysis of casings"},
                {"label": "E", "text": "Canvas for additional video sources — POD cameras, private surveillance, Ring doorbells in the area"},
                {"label": "F", "text": "Collect physical evidence only AFTER all documentation, photography, and processing is complete"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Preserve BWC (A) — digital evidence first, can be overwritten. Joint COPA walk-through "
                "(B) — mandatory before evidence collection per G03-06. Photograph everything in place "
                "(C) — document before disturbing. Request ET (D) for professional processing. Canvas "
                "for video (E) before it's overwritten. Collect physical evidence (F) — always the LAST "
                "step after all documentation.\n\n"
                "KEY REFERENCE: G04-02, Section IV; G03-06, Section VIII-E"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G04-02, Section IV; G03-06, Section VIII-E",
        },

        # --- Q48 ---
        {
            "question_id": "go_rank_q48",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — De-escalation Failure Leading to OID (G03-02 + G03-06)",
            "content": (
                "During a mental health crisis call, de-escalation fails and the subject charges "
                "at officers with a large kitchen knife. An officer fires, killing the subject. "
                "The CIT officer had been en route but hadn't arrived yet. The subject's family "
                "is on scene screaming. Rank the following actions in the correct priority "
                "order per G03-02 and G03-06."
            ),
            "items": [
                {"label": "A", "text": "Request EMS and attempt to render aid to the subject — duty to provide medical care even after a fatal shooting"},
                {"label": "B", "text": "Secure the knife and establish a perimeter — the scene is now both a crime scene and an OID scene"},
                {"label": "C", "text": "Separate the involved officer from the family and all witness officers immediately"},
                {"label": "D", "text": "Assign officers to manage the family — keep them away from the scene but do NOT let them leave without being identified"},
                {"label": "E", "text": "Notify CPIC to activate the full OID notification chain — COPA, SAO, Deputy Chief, ME"},
                {"label": "F", "text": "The arriving CIT officer should be assigned to the family for crisis support — they have specialized training for this"},
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": (
                "Render aid (A) — always first, even after a fatal shooting. Secure scene (B) — "
                "the knife is evidence and the area must be preserved. Separate involved officer (C) — "
                "from family and witnesses. Manage family (D) — compassion AND investigation. CPIC "
                "notification (E) — full OID chain. Assign CIT to family (F) — their training is "
                "valuable for the family in crisis.\n\n"
                "KEY REFERENCE: G03-02, Section III; G03-06, Sections V-VII"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02, Section III; G03-06, Sections V-VII",
        },

        # --- Q49 ---
        {
            "question_id": "go_rank_q49",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — Force Continuum and Firearm Use (G03-02-01 + G03-02-03)",
            "content": (
                "You respond to a robbery in progress at a gas station. The suspect has a "
                "baseball bat and has already struck the clerk in the head. The clerk is "
                "unconscious on the floor bleeding heavily. The suspect turns toward you "
                "with the bat raised. You are alone. Backup is 3 minutes away. "
                "Rank the following actions in the correct priority order per G03-02-01 "
                "and G03-02-03."
            ),
            "items": [
                {"label": "A", "text": "Draw your firearm and issue commands to drop the bat — a baseball bat is a deadly weapon when used to strike the head"},
                {"label": "B", "text": "Create distance and find cover if available — do NOT close distance on a subject with a striking weapon"},
                {"label": "C", "text": "If the suspect charges with the bat raised, lethal force is authorized — imminent threat of death or great bodily harm"},
                {"label": "D", "text": "Once the threat is neutralized, immediately render aid to the clerk and the suspect if injured — request EMS for both"},
                {"label": "E", "text": "If the suspect drops the bat and complies, transition to handcuffing and secure the bat as evidence"},
                {"label": "F", "text": "Notify OEMC of the situation and request backup on an emergency basis"},
            ],
            "correct_order": [5, 1, 0, 2, 4, 3],
            "explanation": (
                "Notify OEMC (F) — request emergency backup. Create distance (B) — force mitigation "
                "through space. Draw and command (A) — appropriate force display for a deadly weapon "
                "threat. If charged, lethal force authorized (C) — a bat used to strike heads constitutes "
                "deadly force. If compliant, handcuff (E) and secure evidence. Render aid (D) to all "
                "injured parties.\n\n"
                "KEY REFERENCE: G03-02-01, Section IV (Force Continuum); G03-02-03, Section III "
                "(Authorized Firearm Use)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-01, Section IV; G03-02-03, Section III",
        },

        # --- Q50 ---
        {
            "question_id": "go_rank_q50",
            "type": "ranking",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "2026 Part 2: General Orders Study Guide",
            "title": "Integration — Reviewing Supervisor Public Safety Investigation (G03-02-08 + G03-06)",
            "content": (
                "After an officer-involved shooting, the reviewing supervisor must conduct "
                "a public safety investigation while COPA handles the misconduct track. The "
                "subject survived with serious injuries. The involved officer used a Taser "
                "first, then transitioned to his firearm. Rank the following actions in the "
                "correct priority order per G03-02-08 and G03-06."
            ),
            "items": [
                {"label": "A", "text": "Review the TRR for both the Taser deployment and the firearm discharge — separate force entries are required for each"},
                {"label": "B", "text": "Review all BWC footage from the involved officer and witnesses to compare against the TRR narrative"},
                {"label": "C", "text": "Interview the involved officer only after his FOP representative and attorney are present"},
                {"label": "D", "text": "Coordinate with COPA to avoid duplicating interview efforts and share relevant non-privileged information"},
                {"label": "E", "text": "Determine if the force continuum escalation from Taser to firearm was justified based on the changing threat level"},
                {"label": "F", "text": "Forward your completed investigation to the Deputy Chief with findings on whether each use of force was within policy"},
            ],
            "correct_order": [0, 1, 2, 4, 3, 5],
            "explanation": (
                "Review TRRs (A) — separate TRRs for Taser and firearm are required. Review BWC (B) — "
                "compare video to written account. Interview with representation (C) — officer's right "
                "to FOP and attorney. Evaluate escalation (E) — was the transition from Taser to firearm "
                "justified by increasing threat. Coordinate with COPA (D) on parallel investigation. "
                "Forward to Deputy Chief (F) with policy findings.\n\n"
                "KEY REFERENCE: G03-02-08, Section IV; G03-06, Section X (Reviewing Supervisor)"
            ),
            "difficulty": "hard",
            "is_premium": True,
            "reference": "G03-02-08, Section IV; G03-06, Section X",
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

    print(f"✓ Seeded {count} General Orders ranking questions (2026 Part 2 Study Guide)")
    print(f"  Category: cat_g03_06_firearm_discharge")
    print(f"  Directives covered: G03-02, G03-02-01, G03-02-03, G03-02-08, G04-02, S03-14, G03-06")
    print(f"  Scoring: I/O Solutions ranking format")
    print(f"  All questions: Ranking (6 items)")
    print(f"  Leaderboard: Enabled")
    print(f"  Premium: Part 2 only")


async def main():
    await seed_g03_06_questions()
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
