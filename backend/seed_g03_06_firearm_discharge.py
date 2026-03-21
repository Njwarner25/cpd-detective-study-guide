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
    """Seed 50 I/O-style questions from G03-06: Firearm Discharge and OID Response.

    SOURCE: 2026 Part 2 Detective Exam Study Guide
    DIRECTIVE: CPD General Order G03-06 (Effective 29 February 2020)

    These questions are designed to mirror the I/O Solutions scoring methodology
    used on the CPD Detective Examination. Each question provides:
      - Detailed scenario based on G03-06 procedures
      - Four answer options scored on the I/O Solutions scale (+2, +1, 0, -1, -2)
      - Comprehensive explanation with study tips and key references
      - Difficulty rating (easy, medium, hard)

    SCORING GUIDE (I/O Solutions Format):
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
        "name": "G03-06: Firearm Discharge & OID",
        "description": (
            "2026 Part 2 Study Guide — 50 questions covering CPD General Order G03-06: "
            "Firearm Discharge and Officer-Involved Death Incident Response and Investigation. "
            "Questions are scored using the I/O Solutions methodology. "
            "Study tips: Focus on notification chains, investigative authority (COPA vs. CPD), "
            "involved member responsibilities, evidence processing, and the role of the "
            "Street Deputy/designated incident commander. Pay close attention to who does what "
            "and when — the exam tests your understanding of the sequence of events and "
            "chain of command."
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
    # 50 QUESTIONS — G03-06 Firearm Discharge & OID
    # ================================================================

    questions = [
        # --- Q1: Definitions ---
        {
            "question_id": "g0306_q01",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Definition of Officer-Involved Death",
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
                "CORRECT ANSWER: B. Per G03-06 and 50 ILCS 727/1-5, an 'officer-involved death' includes "
                "any death resulting directly from an intentional omission, INCLUDING unreasonable delay "
                "involving a person in custody OR intentional failure to seek medical attention when the "
                "need for treatment is apparent. This is a critical definition to memorize.\n\n"
                "STUDY TIP: The definition is BROADER than most people think. It's not just shootings — "
                "it covers omissions, delays, motor vehicle accidents during apprehension, and actions "
                "by off-duty officers performing law enforcement duties. Look for keywords: 'intentional "
                "omission,' 'unreasonable delay,' 'failure to seek medical attention.'\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Physical force is NOT required. Omissions count.\n"
                "C (-1): The ME ruling is irrelevant to the classification under the statute.\n"
                "D (-2): The statute explicitly covers failure to seek medical attention."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-06, Section II-A-3; 50 ILCS 727/1-5",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q2: Investigation Requirements ---
        {
            "question_id": "g0306_q02",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Lead Investigator Certification",
            "content": (
                "An officer-involved death has occurred. The department is assembling the "
                "investigation team as required by Illinois law."
            ),
            "question": "What is the MINIMUM certification requirement for the lead investigator?",
            "options": [
                {"label": "A", "text": "Must be a sworn officer with at least 10 years of experience"},
                {"label": "B", "text": "Must be certified by the Illinois Law Enforcement Training Standards Board as a Lead Homicide Investigator, or have similar approved training"},
                {"label": "C", "text": "Must hold the rank of detective or above"},
                {"label": "D", "text": "Must have previously investigated at least 5 homicide cases"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per 50 ILCS 727/1-10(b), the lead investigator must be certified "
                "by the Illinois Law Enforcement Training Standards Board as a Lead Homicide Investigator, "
                "or have similar training approved by the Board, the Department of State Police, or an "
                "ILETSB-certified school.\n\n"
                "STUDY TIP: The statute sets specific CERTIFICATION requirements, not rank or experience "
                "requirements. Also remember: at least 2 investigators are required, and NO investigator "
                "can be employed by the same agency as the involved officer (unless ISP, different division).\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Experience alone doesn't satisfy the statutory requirement.\n"
                "C (-1): Rank is not the determining factor — certification is.\n"
                "D (-1): Case count is not a statutory requirement."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section II-B-2; 50 ILCS 727/1-10(b)",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q3: Motor Vehicle OID ---
        {
            "question_id": "g0306_q03",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Motor Vehicle OID Investigation",
            "content": (
                "During a vehicle pursuit, the fleeing suspect crashes and dies. The investigation "
                "team is being assembled. The OID involves a motor vehicle accident."
            ),
            "question": "What ADDITIONAL investigator requirement applies to motor vehicle OID cases?",
            "options": [
                {"label": "A", "text": "At least one investigator must be certified as a Crash Reconstruction Specialist"},
                {"label": "B", "text": "The investigation must be handled exclusively by the Major Accident Investigation Section"},
                {"label": "C", "text": "A traffic court judge must approve the investigation team"},
                {"label": "D", "text": "No additional requirements apply beyond the standard OID investigation team"}
            ],
            "correct_answer": "A",
            "explanation": (
                "CORRECT ANSWER: A. Per 50 ILCS 727/1-10(c), when an OID involves a motor vehicle "
                "accident, at least one investigator must be certified as a Crash Reconstruction "
                "Specialist by ILETSB, or have similar approved training. This is IN ADDITION to the "
                "standard lead investigator certification requirement.\n\n"
                "STUDY TIP: Motor vehicle OID cases have TWO certification requirements: (1) Lead "
                "Homicide Investigator certification AND (2) Crash Reconstruction Specialist certification. "
                "Also note: for motor vehicle OIDs, the agency MAY use its own certified Crash "
                "Reconstruction Specialist even though the general rule prohibits using same-agency investigators.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "B (-1): MAIS may assist but does not exclusively handle OID investigations.\n"
                "C (-2): No judicial approval is required for investigation team composition.\n"
                "D (-2): The statute explicitly requires an additional Crash Reconstruction certification."
            ),
            "io_scores": {"A": 2, "B": -1, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "G03-06, Section II-B-3; 50 ILCS 727/1-10(c)",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q4: Policy - Sanctity of Human Life ---
        {
            "question_id": "g0306_q04",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Sanctity of Human Life Policy",
            "content": (
                "You arrive at a firearm discharge scene. A suspect has been shot and is bleeding "
                "heavily. Several officers are focused on securing the firearm evidence."
            ),
            "question": "According to G03-06 policy, what should be the FOREMOST priority?",
            "options": [
                {"label": "A", "text": "Securing all firearm evidence before it is contaminated"},
                {"label": "B", "text": "Preservation of human life and safety of all persons involved"},
                {"label": "C", "text": "Notifying COPA before taking any action"},
                {"label": "D", "text": "Establishing the crime scene perimeter first"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. G03-06, Section III-A states: 'Sanctity of Human Life. All incidents "
                "will be resolved with the foremost regard for the preservation of human life and the "
                "safety of all persons involved.' This is THE overriding policy principle.\n\n"
                "STUDY TIP: When in doubt on any G03-06 question, remember that life safety ALWAYS "
                "comes first. Medical attention for the injured takes priority over evidence collection, "
                "notifications, and scene processing. This principle appears repeatedly throughout the directive.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Evidence is important but secondary to life safety.\n"
                "C (-2): COPA notification does not take priority over saving a life.\n"
                "D (-1): Perimeter is important but life safety comes first."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -1},
            "difficulty": "easy",
            "reference": "G03-06, Section III-A",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q5: Minimum Rank for Investigation ---
        {
            "question_id": "g0306_q05",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Minimum Rank to Direct Investigation",
            "content": (
                "A lieutenant wants to take command of a firearm discharge investigation at the scene."
            ),
            "question": "Per G03-06, what is the minimum rank required to DIRECT a firearm discharge or OID investigation?",
            "options": [
                {"label": "A", "text": "Lieutenant"},
                {"label": "B", "text": "Sergeant"},
                {"label": "C", "text": "Captain"},
                {"label": "D", "text": "Commander"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. G03-06, Section III-D states: 'No Department member below the "
                "rank of captain will direct any investigation into a firearm discharge or officer-involved "
                "death incident.'\n\n"
                "STUDY TIP: This is a commonly tested fact. Memorize it: CAPTAIN is the minimum rank. "
                "For animal-only discharges, the district XO (captain rank) responds. When the involved "
                "member outranks the incident commander, the Street Deputy takes over. When the involved "
                "member IS the Street Deputy or deputy chief+, the Chief of Operations takes over.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Lieutenant is below the minimum rank.\n"
                "B (-2): Sergeant is well below the minimum rank.\n"
                "D (0): Commander can direct, but captain is the MINIMUM."
            ),
            "io_scores": {"A": -1, "B": -2, "C": 2, "D": 0},
            "difficulty": "easy",
            "reference": "G03-06, Section III-D",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q6: COPA Jurisdiction ---
        {
            "question_id": "g0306_q06",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "COPA Investigative Authority",
            "content": (
                "An off-duty CPD officer, while performing a law enforcement arrest on his day off, "
                "discharges his firearm striking a suspect. A sergeant on scene questions whether "
                "COPA has jurisdiction since the officer was off duty."
            ),
            "question": "Does COPA have investigative authority over this incident?",
            "options": [
                {"label": "A", "text": "No, COPA only investigates on-duty incidents"},
                {"label": "B", "text": "Yes, COPA has jurisdiction over all firearm discharges that could potentially strike another individual, AND all OID incidents including off-duty officers performing law enforcement duties"},
                {"label": "C", "text": "Only if the suspect files a formal complaint"},
                {"label": "D", "text": "Only if the officer's commanding officer refers the case to COPA"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section IV-B, COPA investigates: (1) ALL incidents "
                "where a member discharges a firearm in a manner that could potentially strike another "
                "individual (Section 2-78-120(c)), including when a member HAS struck another individual; "
                "AND (2) ALL officer-involved deaths as defined by 50 ILCS 727/1-5, which INCLUDES "
                "off-duty officers performing law enforcement activities.\n\n"
                "STUDY TIP: COPA's jurisdiction is BROAD. Key phrase: 'including those in which no "
                "allegation of misconduct is made.' COPA investigates regardless of whether anyone "
                "complains. Off-duty + law enforcement activity = COPA jurisdiction.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): COPA jurisdiction explicitly covers off-duty law enforcement activities.\n"
                "C (-2): No complaint needed — COPA investigates ALL qualifying incidents.\n"
                "D (-1): No referral needed — COPA has independent jurisdiction."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section IV-B; Municipal Code 2-78-120(c)(e)",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q7: Street Deputy Oversight ---
        {
            "question_id": "g0306_q07",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Street Deputy Oversight Responsibility",
            "content": (
                "An on-duty officer unintentionally discharges a firearm at the station. No one is injured. "
                "The district commander arrives and begins directing the investigation."
            ),
            "question": "Who has oversight of the Department's on-scene investigative responsibilities for this incident?",
            "options": [
                {"label": "A", "text": "The district commander, since it occurred in his district"},
                {"label": "B", "text": "The Street Deputy, Office of Operations"},
                {"label": "C", "text": "COPA, since it's a firearm discharge"},
                {"label": "D", "text": "Bureau of Internal Affairs, since it was unintentional"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section IV-C-1, the Street Deputy, Office of Operations, "
                "oversees the Department's on-scene investigative responsibilities for ALL firearm discharge "
                "incidents, including unintentional discharges and all firearms discharge incidents with injuries. "
                "The ONLY exception is animal-only discharges with no human injuries (handled by district XO).\n\n"
                "STUDY TIP: The Street Deputy is the key CPD figure in G03-06. He/she oversees the "
                "Department side while COPA handles the misconduct investigation. Remember: Street "
                "Deputy = CPD investigation oversight; COPA = member conduct investigation.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): The commander may initially respond but Street Deputy has oversight.\n"
                "C (0): COPA investigates the member's actions, not the underlying criminal case.\n"
                "D (-2): BIA handles call-out notification, not the investigation itself."
            ),
            "io_scores": {"A": -1, "B": 2, "C": 0, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section IV-C-1",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q8: Animal Discharge Exception ---
        {
            "question_id": "g0306_q08",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Animal Discharge – Command Responsibility",
            "content": (
                "An officer discharges a firearm to destroy a dangerous dog that was attacking a child. "
                "No humans were injured. The district XO is currently off duty."
            ),
            "question": "Who will respond and assume command of this investigation?",
            "options": [
                {"label": "A", "text": "The Street Deputy must still respond for any firearm discharge"},
                {"label": "B", "text": "The commander of the district of occurrence"},
                {"label": "C", "text": "The watch operations lieutenant"},
                {"label": "D", "text": "COPA must take command since a firearm was discharged"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section IV-C-2, for firearm discharges solely for "
                "the destruction/deterrence of an animal with no human injuries, the district XO (captain) "
                "responds. If the XO is not on duty, the COMMANDER of the district of occurrence will "
                "respond and assume command.\n\n"
                "STUDY TIP: Animal-only discharges are the ONE exception to Street Deputy oversight. "
                "Know the chain: XO first → if unavailable, Commander. The Street Deputy does NOT "
                "need to respond for animal-only incidents.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Street Deputy is excluded for animal-only/no-injury discharges.\n"
                "C (-1): The lieutenant assists but does not assume command.\n"
                "D (-2): COPA does not take 'command' — they investigate independently."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section IV-C-2",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q9: Involved Member Same Rank ---
        {
            "question_id": "g0306_q09",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Involved Member Outranks Incident Commander",
            "content": (
                "A captain is involved in a firearm discharge incident. The designated incident "
                "commander for the investigation is also a captain."
            ),
            "question": "Who assumes the investigating command personnel responsibilities?",
            "options": [
                {"label": "A", "text": "The captain incident commander proceeds as normal since they are the same rank"},
                {"label": "B", "text": "The Street Deputy assumes the investigating command personnel responsibilities"},
                {"label": "C", "text": "The Bureau of Detectives commander takes over"},
                {"label": "D", "text": "COPA assumes full command of the investigation"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section IV-C-3, when the involved member is the "
                "SAME RANK or higher than the incident commander, the Street Deputy assumes "
                "investigating command responsibilities. When the involved member IS the Street Deputy "
                "or a deputy chief+, the Chief, Office of Operations, takes over.\n\n"
                "STUDY TIP: This is a chain-of-command escalation question. Memorize the hierarchy: "
                "Normal → captain+ commands. Same rank or higher → Street Deputy. Street Deputy or "
                "deputy chief+ involved → Chief of Operations.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Same rank creates a conflict — escalation is mandatory.\n"
                "C (-1): BofD supports but doesn't assume command role.\n"
                "D (-2): COPA investigates member actions, not command the CPD side."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-06, Section IV-C-3",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q10: Concurrent Investigations ---
        {
            "question_id": "g0306_q10",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Concurrent Investigations Priority",
            "content": (
                "A firearm discharge incident has occurred where an officer shot a robbery suspect. "
                "Both a criminal investigation (of the suspect) and a COPA investigation (of the officer) "
                "need to be conducted. Evidence needs to be collected immediately."
            ),
            "question": "What takes PRECEDENCE over all other investigations?",
            "options": [
                {"label": "A", "text": "The COPA investigation of the officer's actions"},
                {"label": "B", "text": "The criminal investigation of the suspect's robbery"},
                {"label": "C", "text": "On-scene activities to ensure public safety, preserve evidence, and secure the scene"},
                {"label": "D", "text": "The State's Attorney's review of the case"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. Per G03-06, Section IV-E-1, 'Any on-scene activities required to "
                "ensure public safety, preserve evidence, and secure the incident scene will be commenced "
                "immediately and led and coordinated by Department personnel consistent with Preliminary "
                "Investigations. These activities will take precedence over any other investigation.'\n\n"
                "STUDY TIP: Scene safety and evidence preservation ALWAYS come first, before any specific "
                "investigation begins. The criminal investigation of non-members is led by CPD (Force "
                "Investigation Division), while COPA leads the investigation of the officer's actions. Both run "
                "concurrently but neither starts until the scene is safe and secure.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): COPA's investigation runs concurrently but doesn't take precedence.\n"
                "B (-1): Criminal investigation is concurrent, not a priority over scene safety.\n"
                "D (-2): SA review comes much later in the process."
            ),
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section IV-E-1",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q11: Force Investigation Division Role ---
        {
            "question_id": "g0306_q11",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Force Investigation Division Responsibility",
            "content": (
                "After a firearm discharge incident where an officer shot a fleeing armed robbery suspect, "
                "multiple investigative teams are at the scene."
            ),
            "question": "What is the Force Investigation Division specifically responsible for?",
            "options": [
                {"label": "A", "text": "Investigating the officer's use of force and potential misconduct"},
                {"label": "B", "text": "Conducting the Department's investigation into the underlying criminal conduct of non-Department members AND the OID/firearm discharge incident"},
                {"label": "C", "text": "Processing all physical evidence at the scene"},
                {"label": "D", "text": "Providing legal advice to the incident commander"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section IV-C-5, the Force Investigation Division is "
                "responsible for conducting the Department's investigation into the underlying criminal "
                "conduct of non-Department members AND the officer-involved death or firearm discharge "
                "incident (excluding animal-only discharges with no human injuries).\n\n"
                "STUDY TIP: Don't confuse FID with COPA. FID = CPD's investigation (criminal case "
                "against the suspect + documenting the incident). COPA = investigation of the officer's "
                "actions. Forensic Services Division = evidence processing.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): That's COPA's role, not FID.\n"
                "C (-1): That's Forensic Services Division's role.\n"
                "D (-2): FID investigates; they don't provide legal advice."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section IV-C-5",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q12: Immediate Notification - Involved Member ---
        {
            "question_id": "g0306_q12",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Involved Member Immediate Notification",
            "content": (
                "An officer has just been involved in a firearm discharge incident. The suspect "
                "is down. The officer is uninjured."
            ),
            "question": "What is the involved member's FIRST notification responsibility?",
            "options": [
                {"label": "A", "text": "Call their immediate supervisor directly"},
                {"label": "B", "text": "Contact COPA to report the incident"},
                {"label": "C", "text": "Immediately notify OEMC, providing all relevant information and requesting additional resources"},
                {"label": "D", "text": "Call the district commander"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. Per G03-06, Section V-A, the involved member will IMMEDIATELY "
                "notify the Office of Emergency Management and Communications (OEMC) providing all "
                "relevant information and requesting additional resources. OEMC then triggers the entire "
                "notification chain.\n\n"
                "STUDY TIP: The notification chain is: Involved Member → OEMC → (OEMC notifies supervisor, "
                "field supervisor, watch ops LT, CPIC) → CPIC notifies everyone else (Street Deputy, "
                "district commander, COPA, BofD area commander, FID, area deputy chief, member's CO, "
                "MAIS if needed, BIA). Memorize this chain!\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): OEMC notifies the supervisor, not the member directly.\n"
                "B (-1): COPA is notified through CPIC, not by the involved member.\n"
                "D (-1): District commander is notified through CPIC."
            ),
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -1},
            "difficulty": "easy",
            "reference": "G03-06, Section V-A",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q13: OEMC Responsibilities ---
        {
            "question_id": "g0306_q13",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "OEMC Radio Broadcast Restriction",
            "content": (
                "OEMC has been notified of a firearm discharge incident involving Officer Smith. "
                "OEMC is dispatching units and making notifications."
            ),
            "question": "Which action would be LEAST appropriate for OEMC?",
            "options": [
                {"label": "A", "text": "Dispatching sufficient district law enforcement units to the scene"},
                {"label": "B", "text": "Broadcasting Officer Smith's name over the police radio as being involved in the discharge"},
                {"label": "C", "text": "Notifying CFD to dispatch emergency medical units"},
                {"label": "D", "text": "Assigning a field supervisor from the district of occurrence to the scene"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B (LEAST appropriate). Per G03-06, Section VI-A-4, OEMC will 'NOT "
                "broadcast the name of a Department member who has been involved in a firearm discharge "
                "incident or an officer-involved death incident over the police radio.' This is a STRICT "
                "prohibition.\n\n"
                "STUDY TIP: Officer identity protection is a key theme. The member's name is NOT broadcast "
                "over radio. This protects the officer from potential retaliation and preserves investigative "
                "integrity. All other OEMC actions (A, C, D) are required duties.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (+2): Dispatching units is OEMC's first duty.\n"
                "C (+1): Dispatching EMS is appropriate when warranted.\n"
                "D (+2): Assigning a field supervisor is required."
            ),
            "io_scores": {"A": 2, "B": -2, "C": 1, "D": 2},
            "difficulty": "easy",
            "reference": "G03-06, Section VI-A-4",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q14: Involved Member - Medical Attention ---
        {
            "question_id": "g0306_q14",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Involved Member First Duty at Scene",
            "content": (
                "An officer has just been involved in a firearm discharge. The suspect appears to be "
                "wounded. The officer is physically capable of taking action."
            ),
            "question": "What is the involved member's FIRST responsibility at the scene?",
            "options": [
                {"label": "A", "text": "Secure and holster the firearm immediately"},
                {"label": "B", "text": "Begin writing the incident report"},
                {"label": "C", "text": "Immediately request medical attention for the injured and may provide appropriate medical care consistent with training"},
                {"label": "D", "text": "Call COPA to report the incident"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. Per G03-06, Section VI-B-1, the involved member will 'immediately "
                "request medical attention for the injured and may provide appropriate medical care "
                "consistent with their training.' This aligns with the Sanctity of Human Life policy.\n\n"
                "STUDY TIP: The involved member's duties in order are: (1) Request medical attention for "
                "injured, (2) Attend to emergency/security duties including scene protection, (3) Remain "
                "on scene and report to field supervisor, (4) Keep recording equipment activated, "
                "(5) Keep firearm holstered and secured.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (0): Firearm should remain holstered but medical attention comes first.\n"
                "B (-2): Reports come much later in the process.\n"
                "D (-1): COPA is notified through the chain, not by the involved member."
            ),
            "io_scores": {"A": 0, "B": -2, "C": 2, "D": -1},
            "difficulty": "easy",
            "reference": "G03-06, Section VI-B-1",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q15: Body Worn Camera ---
        {
            "question_id": "g0306_q15",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Body Worn Camera Deactivation",
            "content": (
                "After a firearm discharge incident, the involved officer wants to turn off his body "
                "worn camera."
            ),
            "question": "When may the involved member deactivate Department-issued recording equipment?",
            "options": [
                {"label": "A", "text": "Immediately after the scene is secure"},
                {"label": "B", "text": "Only when directed by an on-scene supervisor in accordance with BWC and ICV directives"},
                {"label": "C", "text": "When COPA investigators arrive on scene"},
                {"label": "D", "text": "The member may deactivate at their own discretion"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VI-B-4, the involved member will 'not deactivate "
                "his or her activated Department-issued recording equipment until so directed by an on-scene "
                "supervisor' in accordance with BWC and ICV directives. The BWC of the involved member "
                "will be secured consistent with the BWC directive.\n\n"
                "STUDY TIP: The member CANNOT independently decide to stop recording. A supervisor "
                "must direct it. Also important: BWCs must be DEACTIVATED BEFORE the member provides "
                "oral responses to public safety questions (Section VII, NOTE).\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Scene being secure doesn't authorize deactivation.\n"
                "C (-1): COPA arrival doesn't trigger deactivation.\n"
                "D (-2): Members cannot deactivate at their own discretion."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section VI-B-4",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q16: Firearm Handling ---
        {
            "question_id": "g0306_q16",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Involved Member Firearm Handling",
            "content": (
                "After a firearm discharge, a sergeant at the scene asks to inspect the involved "
                "officer's weapon to count the remaining rounds."
            ),
            "question": "What is the correct procedure regarding the involved member's firearm?",
            "options": [
                {"label": "A", "text": "The sergeant may inspect the weapon as a supervisory duty"},
                {"label": "B", "text": "The firearm must remain holstered and secured until submitted to Forensic Services Division personnel"},
                {"label": "C", "text": "The weapon should be immediately placed in an evidence bag"},
                {"label": "D", "text": "The involved member should unload the weapon for safety"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VI-B-5-a, the involved member will 'ensure "
                "that his or her firearm remains holstered and secured until it is submitted to Forensic "
                "Services Division personnel.' No member of ANY rank other than FSD personnel may "
                "handle, inspect, unload, or tamper with the firearm.\n\n"
                "STUDY TIP: Only FORENSIC SERVICES DIVISION touches the gun. Not the sergeant, "
                "not the lieutenant, not even the Street Deputy. The only exception is if the member "
                "is injured and needs to be immediately relieved of the firearm — then another member "
                "takes the firearm AND duty belt, keeps it holstered and secured.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): No member of any rank may inspect — only FSD.\n"
                "C (-1): Don't bag it — keep it holstered for FSD processing.\n"
                "D (-2): Member should NOT unload the weapon."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section VI-B-5-a; Section XI-A",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q17: Public Safety Questions ---
        {
            "question_id": "g0306_q17",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Public Safety Investigation Scope",
            "content": (
                "A supervisor is conducting the public safety investigation with the involved member "
                "at a firearm discharge scene. The supervisor wants to ask detailed questions about "
                "why the officer fired."
            ),
            "question": "What types of questions are appropriate during the public safety investigation?",
            "options": [
                {"label": "A", "text": "Detailed questions about the officer's justification for using deadly force"},
                {"label": "B", "text": "General safety questions about injuries, weapons discharged, suspects at large, evidence locations, involved vehicles, and officer wellness"},
                {"label": "C", "text": "Questions about the officer's prior use of force history"},
                {"label": "D", "text": "Questions about whether the officer followed proper tactics"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VI-B-6, the public safety investigation consists "
                "of GENERAL safety questions concerning: (a) injuries to member or others, (b) whether "
                "weapons were discharged and direction, (c) subjects at large and descriptions, (d) victims, "
                "offenders, witnesses, evidence locations, (e) involved vehicles, (f) officer-wellness matters.\n\n"
                "STUDY TIP: The public safety questions are LIMITED in scope. They're about securing the "
                "scene and ensuring safety — NOT about evaluating the officer's decision to shoot. That's "
                "COPA's job later. Also critical: BWC must be DEACTIVATED before the member answers.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Justification questions are for COPA, not public safety interview.\n"
                "C (-2): Prior history is irrelevant to public safety investigation.\n"
                "D (-1): Tactical assessment is not part of public safety questions."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "G03-06, Section VI-B-6",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q18: BWC Before Public Safety Questions ---
        {
            "question_id": "g0306_q18",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Recording Equipment Before Public Safety Interview",
            "content": (
                "A supervisor is about to ask the involved member public safety questions. "
                "The member's body worn camera is still recording."
            ),
            "question": "What must happen BEFORE the member provides oral responses to the public safety questions?",
            "options": [
                {"label": "A", "text": "The BWC should continue recording to capture the member's statement"},
                {"label": "B", "text": "Department-issued recording equipment must be deactivated before providing oral responses"},
                {"label": "C", "text": "The BWC should be handed to COPA investigators"},
                {"label": "D", "text": "A union representative must be present before any questions are asked"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VI-B-6 NOTE, 'Department members will ensure "
                "Department-issued recording equipment (e.g., In-Car Video Systems, Body Worn Camera) "
                "are deactivated before providing oral responses to the public safety questions.'\n\n"
                "STUDY TIP: This is counterintuitive but critical. The BWC records the INCIDENT but is turned "
                "OFF for the public safety interview. The member's public safety responses are NOT recorded "
                "on BWC. This protects the member's rights under their collective bargaining agreement.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Directly contradicts the directive — BWC must be OFF.\n"
                "C (-1): BWC isn't handed to COPA at this point.\n"
                "D (0): Union rep is addressed separately under Bill of Rights."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": 0},
            "difficulty": "hard",
            "reference": "G03-06, Section VI-B-6 NOTE",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q19: Viewing BWC Video ---
        {
            "question_id": "g0306_q19",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Viewing In-Car or BWC Video",
            "content": (
                "After a firearm discharge, the involved officer asks to review his body worn "
                "camera footage before writing his report."
            ),
            "question": "When may the involved member view their BWC/ICV video?",
            "options": [
                {"label": "A", "text": "Immediately, as it's their own footage"},
                {"label": "B", "text": "Only after being authorized by an on-scene supervisor, in consultation with the FID investigator"},
                {"label": "C", "text": "Never — only COPA may view the footage"},
                {"label": "D", "text": "Only after their union representative reviews it first"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VI-B-7, the involved member will 'not view "
                "their in-car or body-worn camera videos until authorized by an on-scene supervisor, in "
                "consultation with the Force Investigation Division investigator.' However, per Section VII-A-6, "
                "members are afforded the opportunity to view THEIR OWN footage before completing reports, "
                "and this must be disclosed in all documentation.\n\n"
                "STUDY TIP: The key is AUTHORIZATION. Members can view their own footage but only "
                "with supervisor permission after consulting FID. Any viewing must be documented in the "
                "case report, TRR, and all applicable reports.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Cannot view without supervisor authorization.\n"
                "C (-2): Members CAN view their own footage — with authorization.\n"
                "D (-1): Union rep review is not a prerequisite."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "G03-06, Section VI-B-7; Section VII-A-6",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q20: Reviewing Supervisor Perimeter ---
        {
            "question_id": "g0306_q20",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Inner and Outer Perimeters",
            "content": (
                "The reviewing supervisor from the district of occurrence has arrived at a firearm "
                "discharge scene and is establishing perimeters."
            ),
            "question": "What is the purpose of the INNER perimeter versus the OUTER perimeter?",
            "options": [
                {"label": "A", "text": "Inner = where media can access; Outer = restricted to police only"},
                {"label": "B", "text": "Inner = where physical evidence is likely to be recovered; Outer = surrounding area for briefing and deploying personnel"},
                {"label": "C", "text": "Inner = for COPA investigators only; Outer = for CPD investigators"},
                {"label": "D", "text": "Inner = where the involved officer stands; Outer = where witnesses wait"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VI-C-5: (a) 'The inner perimeters are the areas "
                "at the scene of the incident where physical evidence is likely to be recovered.' (b) 'The "
                "outer perimeters are the areas surrounding and encompassing the inner perimeters where "
                "assigned personnel can be briefed and deployed.'\n\n"
                "STUDY TIP: Inner = evidence zone, Outer = staging zone. Access to the inner perimeter "
                "is strictly controlled per Crime Scene Protection and Processing directive.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Media access is governed by separate directives.\n"
                "C (-2): Both COPA and CPD access the inner perimeter.\n"
                "D (-1): Involved officers are separated, not positioned at the inner perimeter."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "easy",
            "reference": "G03-06, Section VI-C-5",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q21: Involved Member Separation ---
        {
            "question_id": "g0306_q21",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Post-Incident Separation of Members",
            "content": (
                "After a firearm discharge incident, two involved officers are sitting in the same "
                "squad car discussing what happened while waiting for the Street Deputy."
            ),
            "question": "What is the MOST appropriate action for the responding supervisor?",
            "options": [
                {"label": "A", "text": "Allow them to continue since they're both involved members"},
                {"label": "B", "text": "Immediately separate them and ensure they avoid contact or communication with each other until released by the Street Deputy, in coordination with COPA"},
                {"label": "C", "text": "Ask them to stop talking but let them remain in the same vehicle"},
                {"label": "D", "text": "Allow them to discuss it so they can align their accounts"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VII-A-2, involved members must 'remain separate "
                "from and avoid any contact or communication with any other involved members or witnesses "
                "until released by the Street Deputy/designated incident commander, in coordination with COPA.' "
                "Per Section VII-A-4, they must 'not discuss the facts of the incident with any other involved "
                "members or witnesses, until interviewed by COPA.'\n\n"
                "STUDY TIP: Separation is MANDATORY. Members must be physically separated AND prohibited "
                "from communicating. When feasible, they should be monitored by supervisory personnel of "
                "HIGHER RANK. They must also be transported SEPARATELY from the scene.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Allowing contact violates the directive.\n"
                "C (-1): They must be physically separated, not just told to stop talking.\n"
                "D (-2): Aligning accounts would compromise the investigation."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "easy",
            "reference": "G03-06, Section VII-A-2, VII-A-4",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q22: Communication Prohibition Duration ---
        {
            "question_id": "g0306_q22",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Communication Prohibition Duration",
            "content": (
                "It has been 45 days since a firearm discharge incident. The involved officer asks "
                "if he can now discuss the incident with a witness officer. COPA has not extended "
                "the communication prohibition."
            ),
            "question": "Can the involved officer discuss the incident with the witness officer?",
            "options": [
                {"label": "A", "text": "Yes, the prohibition only lasts 30 days"},
                {"label": "B", "text": "No, the prohibition lasts 60 days unless COPA extends it"},
                {"label": "C", "text": "Yes, once the officer has been interviewed by COPA the prohibition ends"},
                {"label": "D", "text": "No, the prohibition lasts until the case is fully adjudicated"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VII-A-4-a, the communication prohibition 'will "
                "not continue beyond 60 days from the date of the incident, unless COPA extends the "
                "prohibition.' COPA may extend for additional 60-day periods on an individual basis. Under "
                "no circumstances will it extend beyond the final disciplinary decision.\n\n"
                "STUDY TIP: The default prohibition is 60 DAYS. Exceptions to the prohibition: (1) officer/"
                "public safety communication, (2) as instructed by counsel, (3) wellness/stress management "
                "programs. COPA can extend in 60-day increments but never past final disciplinary decision.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): It's 60 days, not 30.\n"
                "C (-1): COPA interview doesn't end the prohibition.\n"
                "D (-1): It doesn't last until full adjudication — 60 days max unless extended."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "G03-06, Section VII-A-4-a through d",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q23: Exceptions to Communication Prohibition ---
        {
            "question_id": "g0306_q23",
            "type": "least_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Communication Prohibition Exceptions",
            "content": (
                "An officer involved in a firearm discharge incident wants to discuss the incident "
                "with someone before being interviewed by COPA."
            ),
            "question": "Which communication would be LEAST appropriate under G03-06?",
            "options": [
                {"label": "A", "text": "Discussing tactical information with other officers for public safety purposes"},
                {"label": "B", "text": "Discussing the incident details with a fellow involved officer to compare notes"},
                {"label": "C", "text": "Communicating with counsel regarding civil or criminal proceedings"},
                {"label": "D", "text": "Participating in a wellness or stress management program discussion"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B (LEAST appropriate). Per G03-06, Section VII-A-4 EXCEPTION, "
                "the communication prohibition does NOT restrict: (a) officer/public safety communication, "
                "(b) communication as instructed by counsel, (c) wellness/stress program participation. "
                "Comparing notes with another involved officer is NOT an exception and directly violates "
                "the prohibition.\n\n"
                "STUDY TIP: Memorize the three exceptions: Safety, Counsel, Wellness. Anything outside "
                "these three = violation. 'Comparing notes' is the exact behavior the prohibition is designed "
                "to prevent.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (+2): Public safety communication is a recognized exception.\n"
                "C (+2): Counsel communication is a recognized exception.\n"
                "D (+1): Wellness program participation is a recognized exception."
            ),
            "io_scores": {"A": 2, "B": -2, "C": 2, "D": 1},
            "difficulty": "medium",
            "reference": "G03-06, Section VII-A-4 EXCEPTION",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q24: TRR Narrative Exemption ---
        {
            "question_id": "g0306_q24",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "TRR Narrative for Firearm Discharge",
            "content": (
                "An officer involved in a firearm discharge is completing his Tactical Response "
                "Report (TRR). He asks his supervisor whether he needs to complete the Narrative section."
            ),
            "question": "What is the correct guidance regarding the TRR Narrative section?",
            "options": [
                {"label": "A", "text": "The member must complete the full Narrative section with all details of the incident"},
                {"label": "B", "text": "A member that has discharged a firearm WILL NOT be required to complete the Narrative section of the TRR for any firearms discharge incidents"},
                {"label": "C", "text": "The Narrative is only required if someone was injured"},
                {"label": "D", "text": "The member's attorney must write the Narrative section"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VII-A-7 NOTE, 'A member that has discharged "
                "a firearm WILL NOT be required to complete the \"Narrative\" section of the TRR for any "
                "firearms discharge incidents (with or without injury).'\n\n"
                "STUDY TIP: This is a frequently tested point. The TRR is still REQUIRED — just not the "
                "Narrative section. The member must still truthfully report the use of force on the TRR. "
                "This applies to ALL firearm discharges, whether or not anyone was injured.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Directly contradicts the exemption.\n"
                "C (-1): The exemption applies with or without injury.\n"
                "D (-1): There's no requirement for attorney involvement in TRR completion."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section VII-A-7 NOTE",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q25: Witness Member Definition ---
        {
            "question_id": "g0306_q25",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Witness Member Classification",
            "content": (
                "An off-duty officer was present during a firearm discharge incident. She did not "
                "fire her weapon and was not involved in the OID, but she observed the entire incident "
                "and was also fired upon by the suspect."
            ),
            "question": "How is this officer classified under G03-06?",
            "options": [
                {"label": "A", "text": "Civilian witness, since she was off duty"},
                {"label": "B", "text": "Involved member, since she was fired upon"},
                {"label": "C", "text": "Witness member — a member who did not discharge a firearm or participate in the OID but observed or was present or was fired upon"},
                {"label": "D", "text": "Bystander — no classification applies"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. Per G03-06, Section VII-B, a witness member is 'any member, "
                "whether on or off duty, who did not discharge a firearm nor was involved in an "
                "officer-involved death incident, but who observed or was present during the incident or "
                "who has been fired upon.' Witness members have specific responsibilities including "
                "remaining on scene, being separated from others, and completing reports.\n\n"
                "STUDY TIP: Know the distinction between involved member and witness member. Both "
                "must be separated, both cannot discuss facts until COPA interviews them, and both have "
                "the same 60-day communication prohibition. The classification applies regardless of "
                "on/off duty status.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): She's a Department member, not a civilian.\n"
                "B (-1): Being fired upon doesn't make you 'involved' — she didn't discharge.\n"
                "D (-2): A specific classification absolutely applies."
            ),
            "io_scores": {"A": -2, "B": -1, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section VII-B",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q26-50: Continuing pattern ---
        # --- Q26: Reviewing Supervisor CPIC Contact ---
        {
            "question_id": "g0306_q26",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Reviewing Supervisor CPIC Contact",
            "content": (
                "The reviewing supervisor has completed the public safety investigation and the "
                "scene is safe and secure."
            ),
            "question": "What is the reviewing supervisor's next notification responsibility?",
            "options": [
                {"label": "A", "text": "Promptly contact CPIC to confirm notifications have been made and provide updated incident information"},
                {"label": "B", "text": "Call the involved member's family to notify them"},
                {"label": "C", "text": "Issue a press release to the media"},
                {"label": "D", "text": "Contact the union representative for the involved member"}
            ],
            "correct_answer": "A",
            "explanation": (
                "CORRECT ANSWER: A. Per G03-06, Section VII-C-1, the reviewing supervisor will 'after "
                "the completion of the public safety investigation and the scene is safe and secure, "
                "promptly contact CPIC from the scene to confirm the notifications listed in Item V-C "
                "have been made and provide CPIC with additional relevant or updated incident information.'\n\n"
                "STUDY TIP: CPIC is the notification hub. The reviewing supervisor confirms that all required "
                "notifications went out and updates CPIC with any new info.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "B (-1): Family notification has separate procedures.\n"
                "C (-2): Media is handled by Communications Division, not the supervisor.\n"
                "D (0): Union notification is separate from scene responsibilities."
            ),
            "io_scores": {"A": 2, "B": -1, "C": -2, "D": 0},
            "difficulty": "medium",
            "reference": "G03-06, Section VII-C-1",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q27: Monitoring Involved Members ---
        {
            "question_id": "g0306_q27",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Monitoring Separated Members",
            "content": (
                "The reviewing supervisor is ensuring involved and witness members are kept "
                "separate after a firearm discharge incident."
            ),
            "question": "Per G03-06, who should monitor the separated members when feasible?",
            "options": [
                {"label": "A", "text": "Any available officer from the district"},
                {"label": "B", "text": "COPA investigators"},
                {"label": "C", "text": "Supervisory personnel of higher rank than the involved/witness member"},
                {"label": "D", "text": "The member's partner"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. Per G03-06, Section VII-C-2 NOTE, 'When feasible, involved and "
                "witness members will be monitored by supervisory personnel of higher rank.'\n\n"
                "STUDY TIP: Higher rank monitoring ensures the separation is maintained and adds a "
                "layer of authority and documentation. This also applies when the Street Deputy assigns "
                "supervisors to accompany involved members (Section VIII-A-6).\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Any officer won't suffice — supervisory rank required.\n"
                "B (-1): COPA has their own role; monitoring separation is CPD's duty.\n"
                "D (-2): Partners may themselves be witnesses and should be separated."
            ),
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section VII-C-2 NOTE",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q28: Injured Member Firearm ---
        {
            "question_id": "g0306_q28",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Injured Member Firearm Handling",
            "content": (
                "An officer involved in a firearm discharge has been shot and needs immediate "
                "medical treatment. The firearm needs to be secured before transport to the hospital."
            ),
            "question": "What is the correct procedure for handling the injured member's firearm?",
            "options": [
                {"label": "A", "text": "Leave the firearm at the scene for Forensic Services to collect later"},
                {"label": "B", "text": "Another Department member takes possession of the firearm AND duty belt, keeps the firearm holstered and secured, until the responding supervisor arrives"},
                {"label": "C", "text": "The paramedics should take custody of the firearm"},
                {"label": "D", "text": "Unload the firearm and place it in a separate evidence bag"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VI-B-5-a NOTE, 'If the involved member is "
                "injured and needs to be immediately relieved of his or her firearm prior to receiving "
                "medical treatment, another Department member will take possession of the firearm AND "
                "duty belt and ensure that the firearm remains holstered and secured, until the arrival of "
                "the responding supervisor.'\n\n"
                "STUDY TIP: Key details — take the ENTIRE duty belt (not just the gun), keep it HOLSTERED "
                "(don't remove the gun from the holster), and secure it until the supervisor arrives. The "
                "supervisor then holds it for FSD.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Cannot leave the firearm unsecured at the scene.\n"
                "C (-2): Non-police personnel should not handle firearms.\n"
                "D (-2): Do NOT unload — only FSD handles the firearm."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "G03-06, Section VI-B-5-a NOTE",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q29: Watch Ops Lieutenant U Number ---
        {
            "question_id": "g0306_q29",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Universal (U) Number from COPA",
            "content": (
                "A firearm discharge incident has occurred where a member discharged a firearm "
                "and another person was killed. The watch operations lieutenant is completing duties."
            ),
            "question": "In what circumstances must the watch operations lieutenant obtain a Universal (U) Number from COPA?",
            "options": [
                {"label": "A", "text": "For every firearm discharge regardless of outcome"},
                {"label": "B", "text": "Only when the State's Attorney requests it"},
                {"label": "C", "text": "When a member has discharged a firearm and another person is injured or killed, OR when a member has suffered a self-inflicted gunshot wound"},
                {"label": "D", "text": "Only when COPA opens a formal investigation"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. Per G03-06, Section VII-D-2, a U Number is obtained when a member "
                "has: (a) discharged a firearm (on or off duty) and another person is injured or killed by "
                "bullets fired by that member, or (b) suffered a self-inflicted gunshot wound.\n\n"
                "STUDY TIP: Not every discharge requires a U Number — only those resulting in injury/death "
                "to another person or self-inflicted gunshot wounds. The U Number is a COPA tracking number.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Not every discharge — only those with injury/death or self-inflicted.\n"
                "B (-2): SA request is not the trigger.\n"
                "D (-1): COPA investigation is separate from U Number requirement."
            ),
            "io_scores": {"A": -1, "B": -2, "C": 2, "D": -1},
            "difficulty": "hard",
            "reference": "G03-06, Section VII-D-2",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q30: Street Deputy Walk-Through ---
        {
            "question_id": "g0306_q30",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Street Deputy Walk-Through Interview",
            "content": (
                "The Street Deputy has arrived at the scene and conferred with the supervisor who "
                "conducted the public safety investigation. The Street Deputy wants to conduct a "
                "voluntary walk-through with the involved member."
            ),
            "question": "How should the walk-through and public safety interview be conducted?",
            "options": [
                {"label": "A", "text": "With all involved members present together to get a complete picture"},
                {"label": "B", "text": "With each involved member individually, without delay, outside the presence of any other individual"},
                {"label": "C", "text": "Only after COPA has completed their interview"},
                {"label": "D", "text": "With the member's attorney present and recorded on BWC"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VIII-A-4, the Street Deputy may 'conduct a "
                "voluntary walk through and a public safety interview with each of the involved Department "
                "member(s) without delay and outside the presence of any other individual.'\n\n"
                "STUDY TIP: Key words — VOLUNTARY, EACH member INDIVIDUALLY, WITHOUT DELAY, "
                "OUTSIDE the presence of ANY other individual. This is separate from the initial public "
                "safety investigation done by the reviewing supervisor.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Members must be interviewed separately, never together.\n"
                "C (-1): Doesn't need to wait for COPA — conducted without delay.\n"
                "D (0): Attorney presence is governed by collective bargaining, not this specific provision."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": 0},
            "difficulty": "medium",
            "reference": "G03-06, Section VIII-A-4",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q31: COPA Scene Access ---
        {
            "question_id": "g0306_q31",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "COPA Preliminary Assessment Access",
            "content": (
                "COPA investigators arrive at a firearm discharge scene. The scene is safe and secure."
            ),
            "question": "What access must be provided to COPA investigators at this point?",
            "options": [
                {"label": "A", "text": "Limited access to the outer perimeter only until the Department investigation is complete"},
                {"label": "B", "text": "COPA must be provided the opportunity to participate in the preliminary assessment to the same extent as any Department member or other law enforcement agency"},
                {"label": "C", "text": "COPA can only observe from a distance and cannot enter the crime scene"},
                {"label": "D", "text": "COPA access is at the discretion of the district commander"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VIII-B-1, the Street Deputy 'will ensure that as "
                "soon as the scene is safe and secure, COPA investigators will be provided the opportunity "
                "to participate in the preliminary assessment during the immediate aftermath to the SAME "
                "EXTENT as any Department member or any other law enforcement agency.'\n\n"
                "STUDY TIP: COPA gets EQUAL access, not secondary access. They participate in the "
                "preliminary assessment alongside CPD. The Street Deputy also provides COPA with a "
                "narrative, scene walk-through, public safety interview info, and all evidence/witnesses.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): COPA gets full access, not limited to outer perimeter.\n"
                "C (-2): COPA actively participates, not just observes.\n"
                "D (-1): Access is required by directive, not discretionary."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section VIII-B-1",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q32: Street Deputy Briefing COPA ---
        {
            "question_id": "g0306_q32",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Street Deputy Obligation to COPA",
            "content": (
                "COPA investigators have arrived at a firearm discharge scene. The Street Deputy "
                "needs to brief them."
            ),
            "question": "What information must the Street Deputy provide to COPA investigators?",
            "options": [
                {"label": "A", "text": "Only the basic incident type and location"},
                {"label": "B", "text": "A narrative of the incident, a walk through of the scene, public safety interview information, and disclosure of all evidence and witnesses identified"},
                {"label": "C", "text": "Only what COPA specifically requests in writing"},
                {"label": "D", "text": "A copy of the preliminary report only"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VIII-B-2, the Street Deputy will provide COPA "
                "with a narrative including: (a) walking through the incident scene, (b) providing information "
                "from the public safety interview, (c) disclosing any and all evidence and witnesses identified. "
                "Per Section VIII-B-3, there is an ONGOING obligation to keep COPA apprised of ALL relevant "
                "information or evidence.\n\n"
                "STUDY TIP: The obligation is BROAD and ONGOING. The Street Deputy must proactively share "
                "everything, not wait for COPA to ask. This includes approved reports and follow-up evidence.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Much more than basic info is required.\n"
                "C (-2): The obligation is proactive, not reactive.\n"
                "D (-1): More than just the report is required."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section VIII-B-2 and B-3",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q33: COPA and State's Attorney ---
        {
            "question_id": "g0306_q33",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Cook County State's Attorney Notification",
            "content": (
                "An officer-involved death investigation is underway. The State's Attorney's Office "
                "needs to be notified."
            ),
            "question": "Who is responsible for notifying the Cook County State's Attorney's Office Law Enforcement Accountability Division for the OID investigation?",
            "options": [
                {"label": "A", "text": "The Street Deputy"},
                {"label": "B", "text": "The Force Investigation Division"},
                {"label": "C", "text": "COPA personnel"},
                {"label": "D", "text": "The district commander"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. Per G03-06, Section VIII-C, 'COPA personnel will be responsible for "
                "notification and responding to the Cook County State's Attorney's Office Law Enforcement "
                "Accountability Division concerning the officer-involved death investigation.'\n\n"
                "STUDY TIP: Note the distinction — COPA notifies CCSAO's LAW ENFORCEMENT "
                "ACCOUNTABILITY Division (about the OID). The FID notifies CCSAO's FELONY REVIEW "
                "(about the underlying criminal case against the non-member). Two different divisions "
                "of the same office, notified by two different agencies.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Street Deputy oversees CPD side, not SA notification for OID.\n"
                "B (-1): FID contacts Felony Review for the criminal case, not LEAD for OID.\n"
                "D (-2): District commander does not make this notification."
            ),
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -2},
            "difficulty": "hard",
            "reference": "G03-06, Section VIII-C",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q34: Conflict Resolution ---
        {
            "question_id": "g0306_q34",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Conflict Between CPD and COPA at Scene",
            "content": (
                "At a firearm discharge scene, a CPD detective and a COPA investigator disagree "
                "about whether to move a piece of evidence."
            ),
            "question": "How should this conflict be resolved per G03-06?",
            "options": [
                {"label": "A", "text": "The CPD detective's decision prevails since it's a CPD scene"},
                {"label": "B", "text": "Report the conflict to the on-scene Street Deputy, who will confer with COPA to immediately resolve it; if unresolved, escalate up both chains of command"},
                {"label": "C", "text": "COPA's decision always takes precedence over CPD"},
                {"label": "D", "text": "Leave the evidence in place until a judge rules on it"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VIII-D, 'any conflict of opinion or procedure "
                "between Department members and COPA investigative personnel at the scene will be "
                "reported to the on-scene Street Deputy. The Street Deputy will confer with COPA to "
                "immediately resolve the conflict on-scene. If an immediate resolution is unavailable, "
                "the conflict will be reported up the respective chains of command for resolution.'\n\n"
                "STUDY TIP: The resolution process is: (1) Report to Street Deputy, (2) Street Deputy "
                "confers with COPA to resolve, (3) If unresolved → escalate up both chains. Neither agency "
                "unilaterally overrules the other.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): CPD doesn't automatically prevail.\n"
                "C (-1): COPA doesn't automatically prevail either.\n"
                "D (-2): Judicial involvement is not part of scene conflict resolution."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section VIII-D",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q35: FID Supervisor Scene Response ---
        {
            "question_id": "g0306_q35",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "FID Supervisor Scene Response",
            "content": (
                "A firearm discharge incident has occurred resulting in a suspect's death. The "
                "FID supervisor has been notified."
            ),
            "question": "What is the FID supervisor's first responsibility upon assignment?",
            "options": [
                {"label": "A", "text": "Begin reviewing available video footage remotely"},
                {"label": "B", "text": "Personally respond to the scene of the investigation"},
                {"label": "C", "text": "Send subordinate detectives and coordinate from the office"},
                {"label": "D", "text": "Contact COPA to request a joint investigation plan"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VIII-E-2-a, the FID supervisor will 'personally "
                "respond to the scene of the investigation.' Personal response is required — remote or "
                "delegated response is not sufficient.\n\n"
                "STUDY TIP: The FID supervisor has numerous scene responsibilities: personally respond, "
                "assume criminal investigation of non-members, preserve evidence, coordinate with COPA "
                "on evidence and witnesses, ensure video-recorded witness interviews, provide timely info "
                "to COPA, and ensure reports are completed.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Scene response comes before video review.\n"
                "C (-2): Personal response is required, not delegation.\n"
                "D (0): Coordination happens at the scene, not pre-arranged."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": 0},
            "difficulty": "easy",
            "reference": "G03-06, Section VIII-E-2-a",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q36: Witness Video Recording ---
        {
            "question_id": "g0306_q36",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Video Recording Witness Interviews",
            "content": (
                "FID detectives are interviewing a civilian witness to a firearm discharge incident "
                "at the Bureau of Detectives Area office."
            ),
            "question": "Should the witness interview be video-recorded?",
            "options": [
                {"label": "A", "text": "No, only suspect interviews are video-recorded"},
                {"label": "B", "text": "Yes, when possible, unless the witness declines or recording is prohibited by law"},
                {"label": "C", "text": "Only if COPA requests it"},
                {"label": "D", "text": "Only if the witness signs a consent form approved by the State's Attorney"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VIII-E-2-f, the FID supervisor will 'ensure that "
                "interviews of witnesses related to the criminal investigation are video-recorded, when "
                "possible, unless the witness declines to permit such recording or such recording is "
                "prohibited by law.'\n\n"
                "STUDY TIP: Default = video record. Exceptions: witness declines OR law prohibits. "
                "Also remember: ALL witnesses must be informed they have the opportunity to speak with "
                "COPA investigative personnel (Section VIII-E-2-g).\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Witness interviews should also be video-recorded.\n"
                "C (-1): Recording is a default, not COPA-initiated.\n"
                "D (-1): No SA-approved consent form is required."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section VIII-E-2-f",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q37: Witness Detention ---
        {
            "question_id": "g0306_q37",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Witness Detention Restrictions",
            "content": (
                "A civilian witness to a firearm discharge wants to leave the scene. COPA has not "
                "yet arrived to interview them."
            ),
            "question": "Can the witness be detained to wait for COPA?",
            "options": [
                {"label": "A", "text": "Yes, all witnesses must remain until both CPD and COPA complete their interviews"},
                {"label": "B", "text": "No, witnesses will not be held or detained against their will solely for the purpose of notifying COPA personnel"},
                {"label": "C", "text": "Yes, for up to 4 hours under the preliminary investigation rules"},
                {"label": "D", "text": "Only with a court order"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section IX-A and IX-C, 'Witnesses will not be held or "
                "detained against their will.' Furthermore, 'witnesses will not be held or detained against "
                "their will solely for the purpose of notifying COPA personnel.' Department personnel should "
                "notify COPA before a witness leaves, but cannot force them to stay.\n\n"
                "STUDY TIP: Witnesses are VOLUNTARY. You can encourage them to stay, transport them "
                "to the BofD Area for interviews, accommodate on-scene interviews, but you CANNOT detain "
                "them. Witnesses who refuse transport but agree to on-scene interviews should be accommodated.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Cannot force witnesses to remain.\n"
                "C (-2): No 4-hour detention rule exists for witnesses.\n"
                "D (-1): Court orders are not part of this process."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section IX-A, IX-C",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q38: Evidence Before COPA Arrival ---
        {
            "question_id": "g0306_q38",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Evidence Processing Before COPA Arrives",
            "content": (
                "Forensic Services Division personnel are at a firearm discharge scene. COPA has "
                "not yet arrived. It's starting to rain heavily and critical evidence may be destroyed."
            ),
            "question": "Can FSD mark, photograph, or collect evidence before COPA arrives?",
            "options": [
                {"label": "A", "text": "No, all evidence processing must wait for COPA under all circumstances"},
                {"label": "B", "text": "FSD may mark and photograph evidence before COPA arrives, but evidence will not be collected or processed until COPA arrives, unless exigent circumstances (like inclement weather) necessitate immediate collection"},
                {"label": "C", "text": "Yes, FSD has full authority to collect all evidence at any time"},
                {"label": "D", "text": "Only the Street Deputy can authorize evidence collection before COPA arrives"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section X-B-1, 'Department members assigned to the "
                "Forensic Services Division may mark and photograph evidence at the scene prior to the "
                "arrival of the COPA investigative personnel. Evidence will not be collected or processed "
                "until the arrival of COPA personnel, unless exigent circumstances necessitate immediate "
                "collection and processing (e.g., inclement weather resulting in the loss or destruction "
                "of evidence).'\n\n"
                "STUDY TIP: Two-step rule: (1) MARK and PHOTOGRAPH = OK before COPA. (2) COLLECT "
                "and PROCESS = WAIT for COPA, unless exigent circumstances. Rain destroying evidence "
                "= exigent circumstance.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Marking/photographing CAN happen before COPA; collection can in exigent cases.\n"
                "C (-1): Collection requires COPA presence except in exigent circumstances.\n"
                "D (-1): This is FSD's authority, not solely the Street Deputy's."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "G03-06, Section X-B-1",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q39: COPA Must Be Present For ---
        {
            "question_id": "g0306_q39",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "COPA Required Presence for Evidence",
            "content": (
                "Body worn camera footage from the firearm discharge incident is about to be viewed "
                "for the first time. A detective wants to watch it immediately."
            ),
            "question": "Per G03-06, a member of the COPA investigative team MUST be present for what activities?",
            "options": [
                {"label": "A", "text": "Only the initial interview of the involved member"},
                {"label": "B", "text": "The first viewing of available video/audio AND the collection of firearms recovered at the scene AND audio/video material obtained at or near the scene"},
                {"label": "C", "text": "All evidence processing at the Forensic Services lab"},
                {"label": "D", "text": "The autopsy of any deceased person"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section X-C, a COPA team member must be present for: "
                "(1) the first viewing of available video or audio, (2) the collection and preservation of "
                "firearms recovered at the scene, and (3) audio and video material obtained at or near "
                "the scene from the Department or third-party. Exception: public safety need when COPA "
                "has been notified but is unavailable.\n\n"
                "STUDY TIP: Three activities require COPA presence: FIRST VIDEO VIEWING, FIREARM "
                "COLLECTION, and AUDIO/VIDEO COLLECTION. The exception only applies when there's a "
                "public safety need AND COPA has been notified but is unavailable.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): COPA interviews are separate from evidence presence requirements.\n"
                "C (-1): Lab processing has its own procedures.\n"
                "D (-1): Autopsy attendance is not specified in this section."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "G03-06, Section X-C",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q40: FSD Scene Measurements ---
        {
            "question_id": "g0306_q40",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Forensic Services Division Scene Duties",
            "content": (
                "Forensic Services Division personnel are processing a firearm discharge scene."
            ),
            "question": "Which of the following is a required FSD scene duty under G03-06?",
            "options": [
                {"label": "A", "text": "Interviewing all civilian witnesses"},
                {"label": "B", "text": "Taking complete and accurate measurements to develop a detailed plat, numerous detailed photographs, and consulting with COPA on evidence collection"},
                {"label": "C", "text": "Determining whether the officer's use of force was justified"},
                {"label": "D", "text": "Briefing the media on forensic findings"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section X-D, FSD personnel will: (1) take complete "
                "and accurate measurements for a detailed plat, (2) take numerous detailed photographs "
                "from various angles and depths, (3) consult with COPA on evidence collection including "
                "at other locations like hospitals, (4) upon COPA request, take detailed photographs of "
                "involved/witness officers.\n\n"
                "STUDY TIP: FSD = measurements, photographs, evidence processing, trajectory analysis. "
                "They do NOT interview witnesses (that's detectives), determine justification (that's COPA), "
                "or brief media (that's Communications Division).\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Witness interviews are conducted by detectives and COPA.\n"
                "C (-2): Use of force justification is COPA's determination.\n"
                "D (-2): Media briefing is Communications Division's role."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -2},
            "difficulty": "easy",
            "reference": "G03-06, Section X-D",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q41: Deceased Removal ---
        {
            "question_id": "g0306_q41",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Immediate Removal of Decedent",
            "content": (
                "At an officer-involved death scene, a large hostile crowd is gathering and the "
                "highest ranking district supervisor determines officer and public safety is in jeopardy."
            ),
            "question": "Can the decedent be immediately removed from the scene?",
            "options": [
                {"label": "A", "text": "No, the decedent must remain until COPA and the Medical Examiner complete all processing"},
                {"label": "B", "text": "Yes, if the highest ranking on-scene district law enforcement supervisor determines safety of officers or public is in jeopardy, the supervisor may request immediate removal"},
                {"label": "C", "text": "Only with a court order"},
                {"label": "D", "text": "Only the Medical Examiner can authorize removal"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section X-E-1, 'if the highest ranking on-scene district "
                "law enforcement supervisor determines that the safety of officers or the public is in "
                "jeopardy, the supervisor may request the immediate removal of the decedent from the "
                "scene.' The removal must be done in a respectful and private manner, and the deceased "
                "must be pronounced consistent with the Processing and Transportation directive.\n\n"
                "STUDY TIP: Safety override exists for decedent removal. Also note: FSD should process "
                "evidence in a manner to ensure TIMELY removal from a public scene when applicable.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Safety override allows early removal.\n"
                "C (-2): No court order required.\n"
                "D (-1): The on-scene district supervisor makes this determination."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section X-E-1",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q42: Firearm Inspection Who ---
        {
            "question_id": "g0306_q42",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Firearm Inspection Personnel",
            "content": (
                "The firearm used in a discharge incident needs to be inspected to determine rounds "
                "expended and remaining."
            ),
            "question": "Who conducts the firearm inspection and who must be present?",
            "options": [
                {"label": "A", "text": "The involved member's sergeant, with COPA observing"},
                {"label": "B", "text": "Forensic Services Division personnel, in the presence of the Street Deputy, FID personnel, and COPA personnel (unless unavailable)"},
                {"label": "C", "text": "Any detective with firearm experience"},
                {"label": "D", "text": "Bureau of Internal Affairs investigators"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section XI-C-1, FSD personnel conduct the inspection "
                "'on-scene in the presence of the Street Deputy/designated incident commander, Force "
                "Investigation Division personnel, and COPA personnel, unless unavailable.' If safety or "
                "weather prevents on-scene inspection, the member remains with a higher-ranking supervisor "
                "until inspection occurs at the BofD Area.\n\n"
                "STUDY TIP: FSD inspects. Three entities present: Street Deputy, FID, COPA. Only FSD "
                "handles the weapon. Inspection determines: make, model, serial number, caliber, type, "
                "ammunition type, and rounds expended/remaining.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Sergeants do not inspect — only FSD.\n"
                "C (-2): Detectives do not conduct firearm inspections.\n"
                "D (-2): BIA does not conduct firearm inspections."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section XI-C-1",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q43: Firearm Inventory Required ---
        {
            "question_id": "g0306_q43",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Firearm Inventory Requirement",
            "content": (
                "A firearm discharge incident resulted in potential property damage only — a bullet "
                "may have struck a parked car but no one was injured."
            ),
            "question": "Must the involved member's firearm be inventoried in this case?",
            "options": [
                {"label": "A", "text": "No, inventory is only required when someone is injured or killed"},
                {"label": "B", "text": "Yes, firearms are inventoried when an individual is injured/killed, identifiable property damage occurred, OR potential property damage may have occurred"},
                {"label": "C", "text": "Only if COPA requests the inventory"},
                {"label": "D", "text": "Only if the member fired more than 3 rounds"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section XI-C-5, firearms will be inventoried when: "
                "(a) an individual has been injured or killed, (b) identifiable property damage has occurred, "
                "OR (c) potential property damage may have occurred. For case (c), the incident commander "
                "may authorize the member to retain the firearm for personal transport to FSD within 96 hours.\n\n"
                "STUDY TIP: Even POTENTIAL property damage triggers inventory. The 96-hour personal "
                "transport exception only applies to potential (not confirmed) property damage cases, and "
                "must be noted in the eTrack inventory application.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): Property damage and potential property damage also trigger inventory.\n"
                "C (-1): It's policy-driven, not COPA-request dependent.\n"
                "D (-2): Number of rounds is not the criterion."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-06, Section XI-C-5",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q44: Gunshot Residue Testing ---
        {
            "question_id": "g0306_q44",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Gunshot Residue Testing",
            "content": (
                "At a firearm discharge scene, evidence suggests a civilian may have also fired "
                "a weapon. A weapon is recovered near the civilian suspect."
            ),
            "question": "Under what conditions should gunshot residue (GSR) testing be conducted on the civilian?",
            "options": [
                {"label": "A", "text": "Automatically on all civilians at any firearm discharge scene"},
                {"label": "B", "text": "Upon request of COPA personnel in consultation with the Street Deputy, whenever a weapon is recovered on scene or any witness believes the subject possessed a weapon"},
                {"label": "C", "text": "Only if the civilian is deceased"},
                {"label": "D", "text": "Only if the civilian consents to the testing"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section XI-C-7, if additional weapons were discharged, "
                "upon request of COPA in consultation with the Street Deputy, GSR testing is conducted on: "
                "(a) any civilian involved when a weapon is recovered on scene or any witness believes the "
                "subject possessed a weapon, and (b) any Department member present, if requested by COPA.\n\n"
                "STUDY TIP: GSR testing requires TWO triggers: (1) COPA request + Street Deputy "
                "consultation, AND (2) weapon recovery or witness statement about a weapon. It's not "
                "automatic. COPA can also request GSR on Department members.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Not automatic — requires COPA request and weapon evidence.\n"
                "C (-2): Not limited to deceased civilians.\n"
                "D (-1): Civilian consent is not the determining factor."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "G03-06, Section XI-C-7",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q45: Media Information Release ---
        {
            "question_id": "g0306_q45",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "On-Scene Media Inquiries",
            "content": (
                "News media are at a firearm discharge scene asking for information about what happened."
            ),
            "question": "Who is responsible for addressing on-scene media inquiries on behalf of the Department?",
            "options": [
                {"label": "A", "text": "The reviewing supervisor from the district"},
                {"label": "B", "text": "The Director, Communications Division (or designee not involved in the investigation), in consultation with the FID Commander and Street Deputy"},
                {"label": "C", "text": "COPA spokesperson"},
                {"label": "D", "text": "Any officer with Public Information Officer training"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section XII-B, 'In consultation with the Commander, "
                "Force Investigation Division, and Street Deputy, the Director, Communications Division, "
                "(or a designee who is not directly involved in the investigation or investigative chain) is "
                "responsible for addressing on-scene media inquiries on behalf of the Department.'\n\n"
                "STUDY TIP: The designee CANNOT be directly involved in the investigation or investigative "
                "chain. Communications Division handles all media — on-scene, phone, email, electronic. "
                "For OID-specific media inquiries about the 50 ILCS 727 investigation, those are referred "
                "to COPA (Section XII-D).\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): District supervisor does not handle media.\n"
                "C (-1): COPA handles OID-specific media, not general scene media.\n"
                "D (-1): PIO training alone doesn't authorize scene media response."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section XII-B",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q46: Family Notification ---
        {
            "question_id": "g0306_q46",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Family Notification Responsibility",
            "content": (
                "A civilian has been killed during a firearm discharge incident. The family needs to be notified."
            ),
            "question": "Who is responsible for notifying the family of the deceased?",
            "options": [
                {"label": "A", "text": "COPA investigators"},
                {"label": "B", "text": "The district chaplain"},
                {"label": "C", "text": "The Force Investigation Division and Bureau of Detectives personnel"},
                {"label": "D", "text": "The Communications Division through a press release"}
            ],
            "correct_answer": "C",
            "explanation": (
                "CORRECT ANSWER: C. Per G03-06, Section XII-E, 'the Force Investigation Division and "
                "Bureau of Detectives personnel will be responsible for notifying the family of individuals "
                "who have been injured or the deceased during a firearm discharge or officer-involved "
                "death incident.'\n\n"
                "STUDY TIP: FID + BofD = family notification. Also remember from Section III-C: 'the "
                "actions of Department members will not unreasonably impede or delay access to "
                "information for the families.'\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): COPA investigates but doesn't handle family notification.\n"
                "B (-1): Chaplains may assist but are not the designated responsible party.\n"
                "D (-2): Press releases are not the mechanism for family notification."
            ),
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section XII-E",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q47: Conflict Provision ---
        {
            "question_id": "g0306_q47",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Conflict with Other Directives",
            "content": (
                "A supervisor discovers that a procedure in G03-06 conflicts with another Department directive."
            ),
            "question": "Which directive takes precedence?",
            "options": [
                {"label": "A", "text": "The most recently published directive always prevails"},
                {"label": "B", "text": "G03-06 takes precedence over any conflicting Department directive"},
                {"label": "C", "text": "The directive with the lower General Order number prevails"},
                {"label": "D", "text": "The supervisor must request a ruling from the Superintendent"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section XIII, 'If this directive conflicts with any other "
                "Department directive, this directive will take precedence.'\n\n"
                "STUDY TIP: G03-06 has a CONFLICT PROVISION that gives it priority over all other "
                "directives. This is unusual and signals the importance of these procedures. When in "
                "doubt, G03-06 wins.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Publication date doesn't determine precedence here.\n"
                "C (-1): GO number doesn't determine precedence.\n"
                "D (-2): No Superintendent ruling needed — the directive itself resolves conflicts."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "easy",
            "reference": "G03-06, Section XIII",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q48: Outside Agency OID ---
        {
            "question_id": "g0306_q48",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Outside Agency OID in Chicago",
            "content": (
                "An Illinois State Police officer is involved in a fatal shooting within the City of Chicago."
            ),
            "question": "Who conducts the investigative activities for this incident?",
            "options": [
                {"label": "A", "text": "Illinois State Police handles everything since it's their officer"},
                {"label": "B", "text": "The Chicago Police Department will conduct all investigative activities and perform duties required by the Police and Community Relations Improvement Act"},
                {"label": "C", "text": "A joint investigation between ISP and CPD with shared command"},
                {"label": "D", "text": "The FBI takes over all officer-involved deaths in major cities"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section IV-G, for any firearm discharge or OID within "
                "Chicago involving an officer from ANOTHER Illinois law enforcement agency, 'the Chicago "
                "Police Department will conduct all investigative activities related to the incident and "
                "when applicable, perform all of the duties required by the Police and Community Relations "
                "Improvement Act (50 ILCS 727).' NOTE: Federal agencies and out-of-state agencies are "
                "NOT governed by the Act and investigate under their own jurisdiction.\n\n"
                "STUDY TIP: If it's in Chicago + Illinois agency = CPD investigates. If it's federal or "
                "out-of-state = their jurisdiction, CPD assists as needed.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): CPD takes over for incidents within Chicago city limits.\n"
                "C (-1): CPD leads, not a joint command.\n"
                "D (-2): FBI does not automatically take over."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G03-06, Section IV-G",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q49: Traumatic Incident Stress ---
        {
            "question_id": "g0306_q49",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Traumatic Incident Stress Management",
            "content": (
                "After a firearm discharge resulting in a fatality, the Street Deputy is completing "
                "post-incident duties."
            ),
            "question": "What stress management obligation does the Street Deputy have under G03-06?",
            "options": [
                {"label": "A", "text": "No specific stress management obligations are mentioned in this directive"},
                {"label": "B", "text": "Determine if the incident should be classified as traumatic, notify the Professional Counseling Division, and notify the affected member of their responsibilities"},
                {"label": "C", "text": "Order the involved member to take 30 days off duty"},
                {"label": "D", "text": "Refer the member to an outside therapist of the member's choosing"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VIII-A-11, the Street Deputy will fulfill "
                "obligations outlined in the Traumatic Incident Stress Management Program, including: "
                "(a) determining whether the incident should be classified as traumatic, (b) notifying the "
                "Professional Counseling Division, (c) notifying the affected member of their responsibilities.\n\n"
                "STUDY TIP: The Department recognizes these incidents as traumatic (Section III-B). The "
                "Street Deputy has THREE specific stress management duties. The Professional Counseling "
                "Division is the designated notification point, not an outside provider.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-2): G03-06 explicitly addresses stress management.\n"
                "C (-1): No mandatory 30-day leave is specified in this directive.\n"
                "D (-1): Professional Counseling Division is the designated point, not outside providers."
            ),
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "G03-06, Section VIII-A-11",
            "exam_source": "2026 Part 2 Study Guide"
        },

        # --- Q50: Viewing Video with COPA ---
        {
            "question_id": "g0306_q50",
            "type": "most_appropriate",
            "category_id": "cat_g03_06_firearm_discharge",
            "category_name": "G03-06: Firearm Discharge & OID",
            "title": "Documenting Video Viewing",
            "content": (
                "Several Department members viewed body worn camera footage at the scene. "
                "The secondary case report is being prepared by Bureau of Detectives personnel."
            ),
            "question": "What must be documented in the secondary case report regarding video viewing?",
            "options": [
                {"label": "A", "text": "Only that video was available at the scene"},
                {"label": "B", "text": "Each Department member who viewed video or listened to audio at the scene, including whether COPA investigative personnel were present during the viewing"},
                {"label": "C", "text": "Only the total number of members who viewed footage"},
                {"label": "D", "text": "Video viewing does not need to be documented in the case report"}
            ],
            "correct_answer": "B",
            "explanation": (
                "CORRECT ANSWER: B. Per G03-06, Section VIII-E-3-b, the Bureau of Detectives secondary "
                "case report must 'document each Department member who viewed video evidence or "
                "listened to audio evidence at the scene, including whether the video was viewed or the "
                "audio was listened to with COPA investigative personnel present.' Section VIII-E-3-c also "
                "requires documenting the name and time of arrival of all COPA personnel on scene.\n\n"
                "STUDY TIP: Individual-level documentation is required — not just 'video was viewed.' "
                "Each member + whether COPA was present for each viewing. This ensures transparency "
                "and accountability in evidence handling.\n\n"
                "WHY OTHER ANSWERS ARE WRONG:\n"
                "A (-1): Much more specific documentation required.\n"
                "C (-1): Individual names required, not just a count.\n"
                "D (-2): Documentation is explicitly required."
            ),
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "G03-06, Section VIII-E-3-b, c",
            "exam_source": "2026 Part 2 Study Guide"
        },
    ]

    # ======== INSERT QUESTIONS ========
    count = 0
    for q in questions:
        q["created_at"] = now
        q["updated_at"] = now
        q["is_premium"] = True
        q["is_locked"] = True
        q["exam_source"] = "2026 Part 2 Study Guide"

        await db.questions.update_one(
            {"question_id": q["question_id"]},
            {"$set": q},
            upsert=True
        )
        count += 1

    print(f"✓ Seeded {count} G03-06 questions (2026 Part 2 Study Guide)")
    print(f"  Category: cat_g03_06_firearm_discharge")
    print(f"  Scoring: I/O Solutions format (+2/+1/0/-1/-2)")
    print(f"  Leaderboard: Enabled")
    print(f"  Types: most_appropriate, least_appropriate")


async def main():
    await seed_g03_06_questions()
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
