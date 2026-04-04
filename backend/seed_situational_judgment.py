import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ.get('MONGO_URL', os.environ.get('MONGODB_URI', ''))
db_name = os.environ.get('DB_NAME', 'cpd_detective')
if mongo_url:
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
else:
    db = None


async def seed_situational_judgment(ext_db=None):
    """Seed Part 2 Situational Judgment scenarios with paired Most/Least Effective questions.

    10 scenarios, each with a 'most effective' and 'least effective' question = 20 questions total.
    Also includes 7 case management & prioritization cases and an investigative case summary exercise.

    These are PREMIUM content — requires paid access.
    """
    global db
    if ext_db is not None:
        db = ext_db

    now = datetime.now(timezone.utc)

    # ======== CATEGORY ========
    categories = [
        {
            "category_id": "cat_situational_judgment",
            "name": "Situational Judgment",
            "description": "Paired Most Effective / Least Effective scenario questions — mirrors the actual CPD Part 2 exam format.",
            "order": 30,
        },
        {
            "category_id": "cat_case_management",
            "name": "Case Management & Prioritization",
            "description": "Assign priority levels (High/Medium/Low) to detective cases and justify your reasoning.",
            "order": 31,
        },
        {
            "category_id": "cat_investigative_summary",
            "name": "Investigative Case Summary",
            "description": "Review case reports and write a concise factual summary for a supervisor.",
            "order": 32,
        },
    ]

    for cat in categories:
        await db.categories.update_one(
            {"category_id": cat["category_id"]},
            {"$set": cat},
            upsert=True,
        )
    print(f"  Seeded {len(categories)} SJ categories")

    # ================================================================
    # SITUATIONAL JUDGMENT — 10 SCENARIOS, 20 QUESTIONS
    # Each scenario has a 'most_effective' and 'least_effective' question
    # ================================================================

    sj_questions = [
        # ---- SCENARIO 1: Child Removal / Caregiver ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 1a — Child Welfare: Most Effective",
            "scenario_group": "sj_scenario_1",
            "content": "Officers remove a young child from a residence following a violent domestic incident and report that no safe caregiver is present. Shortly after, a person claiming to be a relative arrives and demands to take the child immediately, saying they can bring the child home \"right now.\" This individual cannot provide any proof of identity or demonstrate their relationship to the child. The child is visibly upset and refuses to leave with anyone. As the lead detective, you must determine your next steps in accordance with Department guidelines.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Adhere to the Department's child-welfare protocol: confirm caregiver credentials, finish all mandatory notifications and paperwork, and turn the child over to the first adult who establishes a family connection, prioritizing the child's emotional well-being."},
                {"label": "B", "text": "Adhere to the Department's child-welfare protocol: confirm caregiver credentials, finish all mandatory notifications and paperwork, and have the child remain with an officer in the station's family area until the next shift, then reevaluate placement options."},
                {"label": "C", "text": "Adhere to the Department's child-welfare protocol: confirm caregiver credentials, finish all mandatory notifications and paperwork, and coordinate with the appropriate child protective placement services."},
                {"label": "D", "text": "Tell the relative to take the child to a family member's home and \"call us later once everything settles down\" so names and identities can be confirmed afterward."},
            ],
            "correct_answer": "C",
            "explanation": "Option C guarantees caregiver verification, child safety, required notifications/placement, and proper documentation. Option A prioritizes family placement before completing required verification steps. Option B delays safeguards by holding the child without pursuing proper placement. Option D is the least effective — releasing a child informally without verification is unsafe and non-compliant.",
            "io_scores": {"A": 0, "B": -1, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "CPD Directive S06-04-05",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 1b — Child Welfare: Least Effective",
            "scenario_group": "sj_scenario_1",
            "content": "Officers remove a young child from a residence following a violent domestic incident and report that no safe caregiver is present. Shortly after, a person claiming to be a relative arrives and demands to take the child immediately, saying they can bring the child home \"right now.\" This individual cannot provide any proof of identity or demonstrate their relationship to the child. The child is visibly upset and refuses to leave with anyone. As the lead detective, you must determine your next steps in accordance with Department guidelines.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Adhere to the Department's child-welfare protocol: confirm caregiver credentials, finish all mandatory notifications and paperwork, and turn the child over to the first adult who establishes a family connection, prioritizing the child's emotional well-being."},
                {"label": "B", "text": "Adhere to the Department's child-welfare protocol: confirm caregiver credentials, finish all mandatory notifications and paperwork, and have the child remain with an officer in the station's family area until the next shift, then reevaluate placement options."},
                {"label": "C", "text": "Adhere to the Department's child-welfare protocol: confirm caregiver credentials, finish all mandatory notifications and paperwork, and coordinate with the appropriate child protective placement services."},
                {"label": "D", "text": "Tell the relative to take the child to a family member's home and \"call us later once everything settles down\" so names and identities can be confirmed afterward."},
            ],
            "correct_answer": "D",
            "explanation": "Informal release without verifying identity or completing documentation is unsafe and non-compliant with Department child-welfare procedures.",
            "io_scores": {"A": 0, "B": -1, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "CPD Directive S06-04-05",
            "created_at": now,
        },

        # ---- SCENARIO 2: Welcoming City / Witness Fear of Deportation ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 2a — Welcoming City Witness: Most Effective",
            "scenario_group": "sj_scenario_2",
            "content": "During a neighborhood canvass for a shooting investigation, you encounter a resident who indicates they witnessed the shooter but is visibly afraid that cooperating with police will result in deportation. The witness will not provide a formal written statement or even share their name. You need to obtain critical information for your case while adhering to the Department's Welcoming City policies and safeguarding the witness's confidence.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Inform the witness that their immigration status is outside the scope of your investigation, clarify the Department's policy, and request a statement."},
                {"label": "B", "text": "Warn the witness that you will contact federal immigration authorities and insist on a signed statement along with identification documents."},
                {"label": "C", "text": "Assure the witness that you will disregard their status only if the information they provide directly leads to an arrest tonight."},
                {"label": "D", "text": "Describe the policy clearly, take a verbal account as an initial step, and acknowledge the witness's concerns throughout."},
            ],
            "correct_answer": "A",
            "explanation": "Option A provides a truthful, policy-consistent explanation, reduces the witness's fear, and directly encourages voluntary cooperation. Option D is a sound fallback approach but less direct. Option C misrepresents the policy as conditional. Option B violates the Welcoming City Ordinance and destroys trust.",
            "io_scores": {"A": 2, "B": -2, "C": -1, "D": 1},
            "difficulty": "medium",
            "reference": "General Order G02-01-01 (Welcoming City Ordinance)",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 2b — Welcoming City Witness: Least Effective",
            "scenario_group": "sj_scenario_2",
            "content": "During a neighborhood canvass for a shooting investigation, you encounter a resident who indicates they witnessed the shooter but is visibly afraid that cooperating with police will result in deportation. The witness will not provide a formal written statement or even share their name. You need to obtain critical information for your case while adhering to the Department's Welcoming City policies and safeguarding the witness's confidence.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Inform the witness that their immigration status is outside the scope of your investigation, clarify the Department's policy, and request a statement."},
                {"label": "B", "text": "Warn the witness that you will contact federal immigration authorities and insist on a signed statement along with identification documents."},
                {"label": "C", "text": "Assure the witness that you will disregard their status only if the information they provide directly leads to an arrest tonight."},
                {"label": "D", "text": "Describe the policy clearly, take a verbal account as an initial step, and acknowledge the witness's concerns throughout."},
            ],
            "correct_answer": "B",
            "explanation": "Threatening immigration enforcement violates the Welcoming City Ordinance (G02-01-01) and immediately destroys the witness's trust, making cooperation impossible.",
            "io_scores": {"A": 2, "B": -2, "C": -1, "D": 1},
            "difficulty": "medium",
            "reference": "General Order G02-01-01 (Welcoming City Ordinance)",
            "created_at": now,
        },

        # ---- SCENARIO 3: Burglary ID Procedure ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 3a — Burglary Identification: Most Effective",
            "scenario_group": "sj_scenario_3",
            "content": "You have been assigned to investigate a home burglary. Several days later, the victim forwards you a social media screenshot and states, \"this is the person who broke into my house.\" The victim concedes they only glimpsed the burglar for a few seconds and insists the screenshot confirms their suspicion. Meanwhile, a second witness tells you they can recognize the offender's voice but did not see the person's face. You must prevent witness contamination and carry out a legally sound identification procedure.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Treat the screenshot as a confirmed identification and proceed toward filing charges, given that the victim feels certain and is eager to cooperate."},
                {"label": "B", "text": "Arrange a formal, structured lineup following proper procedural guidelines with full documentation, keeping witnesses apart and not reinforcing any social media imagery during the process."},
                {"label": "C", "text": "Arrange a formal, structured lineup following proper procedural guidelines with full documentation, and present a single booking photograph to verify the victim's belief, then evaluate whether charges are supported."},
                {"label": "D", "text": "Have both witnesses meet privately to compare their observations, and once their accounts are consistent, conduct a photo array."},
            ],
            "correct_answer": "B",
            "explanation": "Option B employs controlled, documented procedures that prevent contamination before it can occur. Option C is weakened by showing a single suggestive photo. Option D contaminates memory through joint witness discussion. Option A — treating a social media screenshot as a confirmed ID — is unreliable, suggestive, and the weakest approach.",
            "io_scores": {"A": -2, "B": 2, "C": 0, "D": -1},
            "difficulty": "hard",
            "reference": "CPD Directive S06-02",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 3b — Burglary Identification: Least Effective",
            "scenario_group": "sj_scenario_3",
            "content": "You have been assigned to investigate a home burglary. Several days later, the victim forwards you a social media screenshot and states, \"this is the person who broke into my house.\" The victim concedes they only glimpsed the burglar for a few seconds and insists the screenshot confirms their suspicion. Meanwhile, a second witness tells you they can recognize the offender's voice but did not see the person's face. You must prevent witness contamination and carry out a legally sound identification procedure.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Treat the screenshot as a confirmed identification and proceed toward filing charges, given that the victim feels certain and is eager to cooperate."},
                {"label": "B", "text": "Arrange a formal, structured lineup following proper procedural guidelines with full documentation, keeping witnesses apart and not reinforcing any social media imagery during the process."},
                {"label": "C", "text": "Arrange a formal, structured lineup following proper procedural guidelines with full documentation, and present a single booking photograph to verify the victim's belief, then evaluate whether charges are supported."},
                {"label": "D", "text": "Have both witnesses meet privately to compare their observations, and once their accounts are consistent, conduct a photo array."},
            ],
            "correct_answer": "A",
            "explanation": "Social media images are unreliable and suggestive; treating a screenshot as a positive ID and rushing to charge is the weakest and most legally vulnerable option.",
            "io_scores": {"A": -2, "B": 2, "C": 0, "D": -1},
            "difficulty": "hard",
            "reference": "CPD Directive S06-02",
            "created_at": now,
        },

        # ---- SCENARIO 4: Two Witnesses / Staggered ID ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 4a — Witness ID Scheduling: Most Effective",
            "scenario_group": "sj_scenario_4",
            "content": "Two individuals witnessed a robbery: one saw the suspect's face directly, while the other only observed the suspect's profile. A suspect has been developed through video analysis and database inquiries. One witness is available immediately; the other cannot come in for two days. As the assigned detective, you must schedule identification procedures that protect reliability and avoid contamination.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Have both witnesses come in at the same time whenever both are free, and present the photo lineup to them together."},
                {"label": "B", "text": "Bring both witnesses in together, let them view the video evidence jointly, and then conduct separate identification procedures."},
                {"label": "C", "text": "Administer a properly structured identification procedure for each witness individually, with full instructions and documentation, preventing any cross-contamination or exchange of information."},
                {"label": "D", "text": "Wait until both witnesses are available on the same day, because running the process at different times produces an inconsistent, staggered approach. Once both are present, conduct a properly administered identification procedure for each witness separately with full instructions and documentation."},
            ],
            "correct_answer": "C",
            "explanation": "Option C maintains witness independence, minimizes contamination, and produces defensible identifications. Option D delays unnecessarily, risking memory decay. Option B contaminates through joint video review. Option A — showing a lineup to both witnesses simultaneously — violates procedure and is the worst approach.",
            "io_scores": {"A": -2, "B": -1, "C": 2, "D": 0},
            "difficulty": "hard",
            "reference": "CPD Directive S06-02",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 4b — Witness ID Scheduling: Least Effective",
            "scenario_group": "sj_scenario_4",
            "content": "Two individuals witnessed a robbery: one saw the suspect's face directly, while the other only observed the suspect's profile. A suspect has been developed through video analysis and database inquiries. One witness is available immediately; the other cannot come in for two days. As the assigned detective, you must schedule identification procedures that protect reliability and avoid contamination.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Have both witnesses come in at the same time whenever both are free, and present the photo lineup to them together."},
                {"label": "B", "text": "Bring both witnesses in together, let them view the video evidence jointly, and then conduct separate identification procedures."},
                {"label": "C", "text": "Administer a properly structured identification procedure for each witness individually, with full instructions and documentation, preventing any cross-contamination or exchange of information."},
                {"label": "D", "text": "Wait until both witnesses are available on the same day, because running the process at different times produces an inconsistent, staggered approach. Once both are present, conduct a properly administered identification procedure for each witness separately with full instructions and documentation."},
            ],
            "correct_answer": "A",
            "explanation": "Showing a lineup to both witnesses simultaneously violates identification procedure and puts the entire case in legal jeopardy.",
            "io_scores": {"A": -2, "B": -1, "C": 2, "D": 0},
            "difficulty": "hard",
            "reference": "CPD Directive S06-02",
            "created_at": now,
        },

        # ---- SCENARIO 5: Crime Scene at Private Property ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 5a — Private Property Crime Scene: Most Effective",
            "scenario_group": "sj_scenario_5",
            "content": "You are leading a homicide investigation at a privately owned tourist venue. The facility's private security managers are pressuring you to reopen portions of the scene right away, citing heavy foot traffic and business losses. They argue that because the property is privately held, they have the authority to make access decisions. As the detective responsible for preserving evidence, you understand the need to protect scene integrity while recognizing the commercial impact.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Let security handle initial crowd management and permit some visitors to enter, given that the property is privately owned."},
                {"label": "B", "text": "Leave the area temporarily to prevent a confrontation and plan to come back later."},
                {"label": "C", "text": "Allow a partial reopening without documenting the decision or establishing any conditions."},
                {"label": "D", "text": "Retain control of the scene and firmly establish your investigative authority regardless of property ownership."},
            ],
            "correct_answer": "D",
            "explanation": "G04-02 vests investigative authority in the detective regardless of property ownership. Maintaining scene control preserves evidence integrity and defensibility. Ceding control (A) invites contamination. Withdrawing (B) delays the investigation. Reopening without documentation (C) undermines chain of custody.",
            "io_scores": {"A": -2, "B": -1, "C": -1, "D": 2},
            "difficulty": "medium",
            "reference": "CPD Directive G04-02 Crime Scene Protection and Processing",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 5b — Private Property Crime Scene: Least Effective",
            "scenario_group": "sj_scenario_5",
            "content": "You are leading a homicide investigation at a privately owned tourist venue. The facility's private security managers are pressuring you to reopen portions of the scene right away, citing heavy foot traffic and business losses. They argue that because the property is privately held, they have the authority to make access decisions. As the detective responsible for preserving evidence, you understand the need to protect scene integrity while recognizing the commercial impact.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Let security handle initial crowd management and permit some visitors to enter, given that the property is privately owned."},
                {"label": "B", "text": "Leave the area temporarily to prevent a confrontation and plan to come back later."},
                {"label": "C", "text": "Allow a partial reopening without documenting the decision or establishing any conditions."},
                {"label": "D", "text": "Retain control of the scene and firmly establish your investigative authority regardless of property ownership."},
            ],
            "correct_answer": "A",
            "explanation": "Private ownership does not override CPD authority at a crime scene. Ceding control invites evidence contamination and violates scene-protection requirements under G04-02.",
            "io_scores": {"A": -2, "B": -1, "C": -1, "D": 2},
            "difficulty": "medium",
            "reference": "CPD Directive G04-02 Crime Scene Protection and Processing",
            "created_at": now,
        },

        # ---- SCENARIO 6: Bias Crime Info Leak ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 6a — Bias Crime Info Leak: Most Effective",
            "scenario_group": "sj_scenario_6",
            "content": "You are the lead detective on a widely publicized bias-motivated aggravated battery. The victim has voiced concerns about retaliation and has specifically asked that identifying details remain tightly controlled.\n\nDuring the investigation, you discover that sensitive case information — including details about the victim's background and preliminary suspect data — was shared informally among Department personnel who are not assigned to the case. You also learn that portions of this information may have reached people outside the Department.\n\nThe case is attracting significant community and media scrutiny. You understand that unauthorized leaks in bias-related investigations can undermine the victim's trust, weaken the prosecution's strategy, and heighten tensions in the community.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Concentrate solely on moving the investigation forward and take no steps regarding the informal disclosures unless someone files a formal complaint."},
                {"label": "B", "text": "Release a broad public clarification and apology to address the misinformation and assure the community that the case is being handled properly."},
                {"label": "C", "text": "Record the unauthorized disclosure, retain all related communications, and alert the appropriate Department oversight channels for review and corrective measures."},
                {"label": "D", "text": "Approach the person you believe is responsible for the leak directly and caution them to be more discreet going forward, without formally escalating the issue."},
            ],
            "correct_answer": "C",
            "explanation": "Documenting the leak, preserving relevant communications, and notifying Department oversight aligns with G04-06 (hate/bias crime protections), G02-01 standards, and confidentiality provisions. This maintains accountability and protects victim privacy without overstepping the detective's role.",
            "io_scores": {"A": -1, "B": -2, "C": 2, "D": 0},
            "difficulty": "hard",
            "reference": "G04-06 Hate Crimes; G02-01 Protection of Human Rights; CPD Confidentiality Provisions",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 6b — Bias Crime Info Leak: Least Effective",
            "scenario_group": "sj_scenario_6",
            "content": "You are the lead detective on a widely publicized bias-motivated aggravated battery. The victim has voiced concerns about retaliation and has specifically asked that identifying details remain tightly controlled.\n\nDuring the investigation, you discover that sensitive case information — including details about the victim's background and preliminary suspect data — was shared informally among Department personnel who are not assigned to the case. You also learn that portions of this information may have reached people outside the Department.\n\nThe case is attracting significant community and media scrutiny. You understand that unauthorized leaks in bias-related investigations can undermine the victim's trust, weaken the prosecution's strategy, and heighten tensions in the community.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Concentrate solely on moving the investigation forward and take no steps regarding the informal disclosures unless someone files a formal complaint."},
                {"label": "B", "text": "Release a broad public clarification and apology to address the misinformation and assure the community that the case is being handled properly."},
                {"label": "C", "text": "Record the unauthorized disclosure, retain all related communications, and alert the appropriate Department oversight channels for review and corrective measures."},
                {"label": "D", "text": "Approach the person you believe is responsible for the leak directly and caution them to be more discreet going forward, without formally escalating the issue."},
            ],
            "correct_answer": "B",
            "explanation": "Releasing a broad public clarification and apology risks further spreading sensitive details and could unintentionally confirm compromised information. Public messaging decisions fall outside a detective's authority and may worsen the situation.",
            "io_scores": {"A": -1, "B": -2, "C": 2, "D": 0},
            "difficulty": "hard",
            "reference": "G04-06 Hate Crimes; G02-01 Protection of Human Rights; CPD Confidentiality Provisions",
            "created_at": now,
        },

        # ---- SCENARIO 7: Unlawful Detention ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 7a — Unlawful Detention Review: Most Effective",
            "scenario_group": "sj_scenario_7",
            "content": "While conducting a follow-up review on a felony arrest, you find that the arrestee has been held in Department custody for several hours beyond the initial processing stage. The original probable cause was based on preliminary witness testimony, but subsequent investigative steps did not produce supporting evidence.\n\nYou verify that no additional charges have been approved and no new facts have emerged to bolster the grounds for continued detention. The holdup appears to stem from stalled paperwork and coordination breakdowns during shift changes.\n\nThe arrestee has not objected, but you recognize that holding someone without adequate legal justification raises serious constitutional issues and could compromise any future prosecution.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Act promptly to resolve the delay and ensure the arrestee is either formally processed through lawful channels or released without further hold."},
                {"label": "B", "text": "Continue the investigation hoping that new evidence surfaces before you need to address the custody question."},
                {"label": "C", "text": "Leave things as they are unless the arrestee files a formal objection or retains an attorney."},
                {"label": "D", "text": "Arrange for a different unit to take over custodial responsibility so the detention decision falls outside your case."},
            ],
            "correct_answer": "A",
            "explanation": "Detectives are responsible for ensuring continued detention is legally supported. When probable cause no longer holds, prompt corrective action — lawful processing or release — upholds constitutional standards and protects case integrity under G06-01-01.",
            "io_scores": {"A": 2, "B": -1, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G06-01-01 Field Arrest Procedures; Constitutional Custodial Standards",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 7b — Unlawful Detention Review: Least Effective",
            "scenario_group": "sj_scenario_7",
            "content": "While conducting a follow-up review on a felony arrest, you find that the arrestee has been held in Department custody for several hours beyond the initial processing stage. The original probable cause was based on preliminary witness testimony, but subsequent investigative steps did not produce supporting evidence.\n\nYou verify that no additional charges have been approved and no new facts have emerged to bolster the grounds for continued detention. The holdup appears to stem from stalled paperwork and coordination breakdowns during shift changes.\n\nThe arrestee has not objected, but you recognize that holding someone without adequate legal justification raises serious constitutional issues and could compromise any future prosecution.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Act promptly to resolve the delay and ensure the arrestee is either formally processed through lawful channels or released without further hold."},
                {"label": "B", "text": "Continue the investigation hoping that new evidence surfaces before you need to address the custody question."},
                {"label": "C", "text": "Leave things as they are unless the arrestee files a formal objection or retains an attorney."},
                {"label": "D", "text": "Arrange for a different unit to take over custodial responsibility so the detention decision falls outside your case."},
            ],
            "correct_answer": "D",
            "explanation": "Passing custodial responsibility to another unit to avoid the constitutional problem does not fix unlawful detention. Delegation reflects avoidance rather than corrective action.",
            "io_scores": {"A": 2, "B": -1, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G06-01-01 Field Arrest Procedures; Constitutional Custodial Standards",
            "created_at": now,
        },

        # ---- SCENARIO 8: Emergency Vehicle Misuse ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 8a — Emergency Vehicle Misuse: Most Effective",
            "scenario_group": "sj_scenario_8",
            "content": "While driving between assignments, you see a fellow officer activate emergency lights and siren and speed through traffic at a high rate. You are unaware of any dispatched emergency, and your radio shows no priority calls in the vicinity.\n\nThe officer's driving is causing other vehicles to brake suddenly and creating a clear hazard for motorists and pedestrians along a busy commercial stretch. As a detective, you understand that reckless emergency vehicle operation exposes the Department to significant civil liability and erodes community confidence. At the same time, you are not the officer's supervisor and must act within the boundaries of your role.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Disregard the behavior and proceed with your own assignment, since the officer may possess information you are not aware of."},
                {"label": "B", "text": "Immediately confront the officer over the radio to demand they stop the dangerous driving."},
                {"label": "C", "text": "Note the details of the observed conduct and report it through the proper Department channels for supervisory review, confirming there is no imminent threat that warrants your direct intervention."},
                {"label": "D", "text": "Speed up and activate your own emergency equipment to keep pace with the officer and stay aware of the situation."},
            ],
            "correct_answer": "C",
            "explanation": "Documenting the conduct and notifying proper channels aligns with G03-03 (emergency vehicle operations). This preserves accountability, avoids compounding risk, and stays within the detective's appropriate authority.",
            "io_scores": {"A": -1, "B": 0, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "G03-03 Emergency Use of Department Vehicles",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 8b — Emergency Vehicle Misuse: Least Effective",
            "scenario_group": "sj_scenario_8",
            "content": "While driving between assignments, you see a fellow officer activate emergency lights and siren and speed through traffic at a high rate. You are unaware of any dispatched emergency, and your radio shows no priority calls in the vicinity.\n\nThe officer's driving is causing other vehicles to brake suddenly and creating a clear hazard for motorists and pedestrians along a busy commercial stretch. As a detective, you understand that reckless emergency vehicle operation exposes the Department to significant civil liability and erodes community confidence. At the same time, you are not the officer's supervisor and must act within the boundaries of your role.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Disregard the behavior and proceed with your own assignment, since the officer may possess information you are not aware of."},
                {"label": "B", "text": "Immediately confront the officer over the radio to demand they stop the dangerous driving."},
                {"label": "C", "text": "Note the details of the observed conduct and report it through the proper Department channels for supervisory review, confirming there is no imminent threat that warrants your direct intervention."},
                {"label": "D", "text": "Speed up and activate your own emergency equipment to keep pace with the officer and stay aware of the situation."},
            ],
            "correct_answer": "D",
            "explanation": "Matching the unsafe behavior compounds the danger to the public and exposes both the detective and the Department to additional liability. Activating emergency equipment without justification directly violates policy and escalates the hazard.",
            "io_scores": {"A": -1, "B": 0, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "G03-03 Emergency Use of Department Vehicles",
            "created_at": now,
        },

        # ---- SCENARIO 9: Incomplete Custodial Documentation ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 9a — Custodial Documentation: Most Effective",
            "scenario_group": "sj_scenario_9",
            "content": "You are assembling a felony case package for submission to the State's Attorney's Office. As you review the arrest and interview reports, you notice that an arrestee requested to speak with a lawyer during custodial questioning. The narrative states the request was acknowledged and the interview stopped; however, the documentation does not clearly establish when the request was made relative to the officer's response, nor does it confirm whether questioning resumed only after counsel was consulted.\n\nThe case depends on incriminating custodial statements. You realize that incomplete records regarding the invocation of counsel could lead to suppression motions and damage the case's credibility.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Submit the file as-is, noting that the report indicates counsel contact occurred, and plan to fix the documentation later."},
                {"label": "B", "text": "Correct the documentation so it precisely reflects the request, the Department's response, and the sequence of events before sending the case forward."},
                {"label": "C", "text": "Overlook the documentation gap unless defense counsel raises the issue down the line."},
                {"label": "D", "text": "Add your own informal notes to your personal case file without requiring the original report to be amended."},
            ],
            "correct_answer": "B",
            "explanation": "Ensuring the report accurately captures the attorney request, the Department's response, and the precise timeline preserves constitutional compliance under G06-01-04 and safeguards the admissibility of statements.",
            "io_scores": {"A": 0, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "G06-01-04 Arrestee-and-In-Custody Communications; Constitutional Custodial Standards",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 9b — Custodial Documentation: Least Effective",
            "scenario_group": "sj_scenario_9",
            "content": "You are assembling a felony case package for submission to the State's Attorney's Office. As you review the arrest and interview reports, you notice that an arrestee requested to speak with a lawyer during custodial questioning. The narrative states the request was acknowledged and the interview stopped; however, the documentation does not clearly establish when the request was made relative to the officer's response, nor does it confirm whether questioning resumed only after counsel was consulted.\n\nThe case depends on incriminating custodial statements. You realize that incomplete records regarding the invocation of counsel could lead to suppression motions and damage the case's credibility.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Submit the file as-is, noting that the report indicates counsel contact occurred, and plan to fix the documentation later."},
                {"label": "B", "text": "Correct the documentation so it precisely reflects the request, the Department's response, and the sequence of events before sending the case forward."},
                {"label": "C", "text": "Overlook the documentation gap unless defense counsel raises the issue down the line."},
                {"label": "D", "text": "Add your own informal notes to your personal case file without requiring the original report to be amended."},
            ],
            "correct_answer": "C",
            "explanation": "Ignoring the documentation gap invites suppression of critical statements and undermines prosecutorial viability. Constitutional compliance cannot depend on whether defense counsel notices the deficiency.",
            "io_scores": {"A": 0, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "G06-01-04 Arrestee-and-In-Custody Communications; Constitutional Custodial Standards",
            "created_at": now,
        },

        # ---- SCENARIO 10: Victim Privacy in Multi-Agency Case ----
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 10a — Victim Privacy Disclosure: Most Effective",
            "scenario_group": "sj_scenario_10",
            "content": "You are the lead detective on a complex aggravated criminal sexual assault investigation that involves coordination with several law enforcement agencies and a victim-services organization. The victim has expressed deep fear of retaliation and has explicitly asked that personal identifying information not be disclosed beyond what the law requires.\n\nThe investigation demands sharing certain information with outside agencies, including details that could indirectly reveal the victim's identity. You understand that both over-sharing and unnecessarily withholding information can harm the case — either by breaching privacy protections or by stalling investigative progress.",
            "question": "What is the MOST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Disclose only the information that is legally authorized and necessary for investigative purposes, and log every disclosure that is made."},
                {"label": "B", "text": "Provide all relevant case data to partner agencies without restriction to ensure seamless coordination and efficiency."},
                {"label": "C", "text": "Withhold all identifying details entirely, even when required disclosures are necessary for the investigation to move forward."},
                {"label": "D", "text": "Delegate the disclosure decisions to another detective or a supervisor so the responsibility does not fall on you."},
            ],
            "correct_answer": "A",
            "explanation": "Balancing lawful investigative disclosure with victim privacy obligations aligns with G02-01 protections. Sharing only what is authorized and necessary preserves victim trust while supporting investigative progress. Documenting all disclosures ensures accountability.",
            "io_scores": {"A": 2, "B": -1, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G02-01 Protection of Human Rights; Victim Privacy and Confidentiality Provisions",
            "created_at": now,
        },
        {
            "question_id": f"sj_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_situational_judgment",
            "category_name": "Situational Judgment",
            "title": "SJ 10b — Victim Privacy Disclosure: Least Effective",
            "scenario_group": "sj_scenario_10",
            "content": "You are the lead detective on a complex aggravated criminal sexual assault investigation that involves coordination with several law enforcement agencies and a victim-services organization. The victim has expressed deep fear of retaliation and has explicitly asked that personal identifying information not be disclosed beyond what the law requires.\n\nThe investigation demands sharing certain information with outside agencies, including details that could indirectly reveal the victim's identity. You understand that both over-sharing and unnecessarily withholding information can harm the case — either by breaching privacy protections or by stalling investigative progress.",
            "question": "What is the LEAST effective response to this scenario?",
            "options": [
                {"label": "A", "text": "Disclose only the information that is legally authorized and necessary for investigative purposes, and log every disclosure that is made."},
                {"label": "B", "text": "Provide all relevant case data to partner agencies without restriction to ensure seamless coordination and efficiency."},
                {"label": "C", "text": "Withhold all identifying details entirely, even when required disclosures are necessary for the investigation to move forward."},
                {"label": "D", "text": "Delegate the disclosure decisions to another detective or a supervisor so the responsibility does not fall on you."},
            ],
            "correct_answer": "D",
            "explanation": "Handing off disclosure decisions to avoid making them reflects avoidance rather than investigative ownership. As the assigned detective, you are responsible for ensuring disclosures are lawful, necessary, and properly documented.",
            "io_scores": {"A": 2, "B": -1, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "G02-01 Protection of Human Rights; Victim Privacy and Confidentiality Provisions",
            "created_at": now,
        },
    ]

    # Insert all SJ questions
    for q in sj_questions:
        q.setdefault("created_at", now)
        q.setdefault("updated_at", now)
        await db.questions.update_one(
            {"title": q["title"], "category_id": q["category_id"]},
            {"$set": q},
            upsert=True,
        )
    print(f"  Seeded {len(sj_questions)} Situational Judgment questions")

    # ================================================================
    # CASE MANAGEMENT & PRIORITIZATION — 7 CASES (mini_scenario type)
    # These are written-response questions graded by AI
    # ================================================================
    case_mgmt_questions = [
        {
            "question_id": f"cm_{uuid.uuid4().hex[:12]}",
            "type": "mini_scenario",
            "category_id": "cat_case_management",
            "category_name": "Case Management & Prioritization",
            "title": "Case A — Armed Vehicular Hijacking Pattern",
            "content": "Three vehicular hijackings have taken place over the past six days within the same district. In every incident, a single offender brandished a handgun, confronted drivers who had just parked, and escaped in the stolen vehicle. All three events occurred during evening hours in busy commercial areas. Partial plate information was recovered from a witness who observed a possible support vehicle. Two victims described the offender as wearing dark clothing and a hooded sweatshirt, though neither could give a detailed facial description. The incident locations fall within a relatively compact geographic zone and may reflect a recognizable pattern. A crime bulletin has been prepared, but no detective follow-up on the potential support vehicle has occurred yet.",
            "question": "Assign this case a priority level (High, Medium, or Low) and explain your reasoning.",
            "model_answer": "HIGH PRIORITY. Armed pattern crime with escalating frequency (3 incidents in 6 days). Handgun used in each — imminent public safety threat. Geographic clustering suggests a serial offender likely to strike again. Perishable lead (partial plate on support vehicle) requires immediate follow-up before it goes cold. Evening hours in commercial areas maximize potential victims. The pattern nature elevates this above a single incident.",
            "difficulty": "medium",
            "reference": "Case prioritization principles; pattern crime response",
            "created_at": now,
        },
        {
            "question_id": f"cm_{uuid.uuid4().hex[:12]}",
            "type": "mini_scenario",
            "category_id": "cat_case_management",
            "category_name": "Case Management & Prioritization",
            "title": "Case B — Missing Elderly Person",
            "content": "An 81-year-old man with early-stage dementia left his home at roughly 11:00 a.m. and has not come back. His family says this behavior is unusual and notes that he does not have a cell phone. He was last observed wearing a light jacket despite cold weather. A neighbor saw him walking toward a nearby shopping corridor, but no one has confirmed seeing him since then. Family members have searched local stores and the homes of relatives without success. The man requires daily medication and can become disoriented when he is outside familiar surroundings. Patrol completed an initial missing person report and logged the information, but detectives have just been assigned for follow-up.",
            "question": "Assign this case a priority level (High, Medium, or Low) and explain your reasoning.",
            "model_answer": "HIGH PRIORITY. Vulnerable missing person — elderly with dementia, medication-dependent, inadequately dressed for cold weather. Time-sensitive: every hour increases risk of medical emergency, exposure, or disorientation leading to danger. No cell phone means no way to track or contact him. Last seen heading toward a commercial area where he could wander into traffic or become further lost. The combination of cognitive impairment, medical needs, and environmental exposure creates an imminent life-safety concern requiring immediate investigative resources.",
            "difficulty": "medium",
            "reference": "Missing person protocols; vulnerable adult procedures",
            "created_at": now,
        },
        {
            "question_id": f"cm_{uuid.uuid4().hex[:12]}",
            "type": "mini_scenario",
            "category_id": "cat_case_management",
            "category_name": "Case Management & Prioritization",
            "title": "Case C — Felony Retail Theft Follow-Up",
            "content": "A department store filed a delayed report for a theft that happened four days ago. The estimated loss is $3,800. Store security has clear video footage of the offender as well as a vehicle plate that has not yet been investigated. The suspect reportedly chose high-value merchandise and left through a side exit without paying. Security staff believe the same individual may have visited the store the day before the theft, but that earlier footage has not been preserved yet. The plate was recorded by an exterior camera, and the images are said to be of sufficient quality for identification. No arrest, suspect interview, or database inquiry has been documented since the patrol response.",
            "question": "Assign this case a priority level (High, Medium, or Low) and explain your reasoning.",
            "model_answer": "MEDIUM PRIORITY. Property crime with no violence or immediate public safety threat. However, strong investigative leads exist (clear video, vehicle plate) that could go cold if not pursued — especially the prior-day footage that hasn't been preserved. The $3,800 loss meets felony threshold. No urgency comparable to violent crimes, but the available evidence warrants timely follow-up before leads deteriorate. Plate run and video preservation should happen within days, not weeks.",
            "difficulty": "medium",
            "reference": "Property crime investigation; evidence preservation timelines",
            "created_at": now,
        },
        {
            "question_id": f"cm_{uuid.uuid4().hex[:12]}",
            "type": "mini_scenario",
            "category_id": "cat_case_management",
            "category_name": "Case Management & Prioritization",
            "title": "Case D — Recent Sexual Assault Report",
            "content": "A 24-year-old victim reported a sexual assault that occurred earlier that morning involving someone she knows. The victim is willing to cooperate and says there may be relevant text messages and location history. Patrol documentation reflects that initial notifications were made, but detective follow-up is now required. The victim indicated that the acquaintance continued contacting her after the incident, and some of those messages remain on her phone. The reported location is known, and nearby businesses may have surveillance footage. The victim has identified the suspect by name and provided basic background information. No indication has been given that a full detective interview has taken place yet.",
            "question": "Assign this case a priority level (High, Medium, or Low) and explain your reasoning.",
            "model_answer": "HIGH PRIORITY. Violent person crime — sexual assault with a cooperative victim and identified suspect. Time-sensitive evidence: text messages could be deleted, surveillance footage is typically overwritten within 24-72 hours, and the victim's account is freshest now. Ongoing suspect contact with the victim raises safety concerns and potential witness intimidation. The victim's willingness to cooperate is a perishable asset — delays can lead to recantation or disengagement. Named suspect allows for immediate investigation. This requires same-day detective response.",
            "difficulty": "medium",
            "reference": "Sexual assault investigation protocols; victim cooperation; evidence preservation",
            "created_at": now,
        },
        {
            "question_id": f"cm_{uuid.uuid4().hex[:12]}",
            "type": "mini_scenario",
            "category_id": "cat_case_management",
            "category_name": "Case Management & Prioritization",
            "title": "Case E — Residential Burglary With Named Suspect",
            "content": "A burglary from two days ago resulted in the loss of approximately $6,500 in electronics and jewelry. The victim suspects a cousin may be involved because only family members knew the victim would be away. No forced entry was observed, and there is no indication that detectives have spoken with the named suspect yet. The victim also reported that a spare key went missing several weeks before the burglary but never filed a report about it at the time. Neighbors did not notice anything suspicious, although one recalled seeing an unfamiliar vehicle parked near the house. Several stolen items have serial numbers on file. Patrol photographs were taken, but no follow-up with pawn databases or direct contact with the named suspect has been documented.",
            "question": "Assign this case a priority level (High, Medium, or Low) and explain your reasoning.",
            "model_answer": "MEDIUM PRIORITY. Property crime with no violence or immediate danger. However, a named suspect and serial numbers for stolen items provide actionable leads. The missing spare key and no forced entry support the family-member theory. Pawn database checks should be initiated promptly since stolen electronics are often resold quickly. The suspect interview can be scheduled within a reasonable timeframe. Not as urgent as violent crimes or pattern offenses, but the available leads justify active follow-up rather than a low-priority shelf.",
            "difficulty": "medium",
            "reference": "Property crime investigation; suspect interview protocols",
            "created_at": now,
        },
        {
            "question_id": f"cm_{uuid.uuid4().hex[:12]}",
            "type": "mini_scenario",
            "category_id": "cat_case_management",
            "category_name": "Case Management & Prioritization",
            "title": "Case F — Domestic Violence Strangulation Report",
            "content": "Patrol responded late last night to a domestic violence call in which the victim reported being strangled by her partner during an argument. The suspect departed before officers arrived but is thought to still be nearby and has reportedly tried to call the victim multiple times since the incident. Patrol completed the initial report and advised that follow-up for victim safety planning and warrant review is necessary. The victim reported visible redness and soreness in the neck area at the time of the patrol response. A child was present in the home during part of the incident, though no injury to the child was reported. The victim stated this was the first physical incident but that it was the first time police were contacted. No detective contact with the victim or suspect has been documented since the initial patrol response.",
            "question": "Assign this case a priority level (High, Medium, or Low) and explain your reasoning.",
            "model_answer": "HIGH PRIORITY. Strangulation is one of the strongest predictors of future lethal domestic violence — elevates this above a typical DV case. Suspect is unapprehended and attempting ongoing contact, indicating continued risk to the victim. Visible injuries (neck redness) corroborate the account and support felony charges. Child present during the incident adds urgency for safety planning. Warrant review is needed immediately to prevent further contact/harm. The combination of strangulation, at-large suspect, ongoing contact attempts, and a child in the home demands same-day detective response.",
            "difficulty": "medium",
            "reference": "S04-19 Domestic Violence procedures; strangulation lethality research",
            "created_at": now,
        },
        {
            "question_id": f"cm_{uuid.uuid4().hex[:12]}",
            "type": "mini_scenario",
            "category_id": "cat_case_management",
            "category_name": "Case Management & Prioritization",
            "title": "Case G — Fraud Complaint with Identified Account",
            "content": "A bank customer reported unauthorized withdrawals totaling $2,200 over the past three weeks. The bank has frozen the compromised account and provided transaction records showing where the funds were transferred. No suspect has been identified, and there is no indication of immediate physical danger to the victim. The customer stated that several online banking alerts were initially overlooked because they resembled routine account notifications. A bank representative confirmed the transactions were routed through multiple accounts before the freeze was placed. The customer has access to account statements and is willing to provide all relevant financial documentation. There is also information suggesting that additional fraudulent activity occurred after the initial freeze was implemented.",
            "question": "Assign this case a priority level (High, Medium, or Low) and explain your reasoning.",
            "model_answer": "LOW-to-MEDIUM PRIORITY. Financial crime with no physical danger to the victim. The account is already frozen, limiting further immediate loss. No identified suspect yet — investigation will require financial record analysis and subpoenas, which are time-consuming but not time-critical in the same way as violent crimes. The post-freeze fraudulent activity is concerning and should be documented, but the bank's cooperation and preserved records mean evidence is not at risk of being lost. This case can be worked methodically without the urgency demanded by violent or pattern crimes.",
            "difficulty": "medium",
            "reference": "Financial crimes investigation; fraud case management",
            "created_at": now,
        },
    ]

    for q in case_mgmt_questions:
        q.setdefault("created_at", now)
        q.setdefault("updated_at", now)
        await db.questions.update_one(
            {"title": q["title"], "category_id": q["category_id"]},
            {"$set": q},
            upsert=True,
        )
    print(f"  Seeded {len(case_mgmt_questions)} Case Management questions")

    total = len(sj_questions) + len(case_mgmt_questions)
    print(f"  Total Situational Judgment content seeded: {total} questions")
    return total


if __name__ == "__main__":
    asyncio.run(seed_situational_judgment())
