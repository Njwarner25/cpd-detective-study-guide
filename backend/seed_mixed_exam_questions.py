import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


async def seed_mixed_exam(ext_db=None):
    """Seed I/O-style mixed-method detective exam questions.

    Question types:
      - most_appropriate: Pick the BEST action (+2 correct, weighted penalties)
      - least_appropriate: Pick the WORST action (+2 correct, weighted penalties)
      - legal_trap: Tricky legal/constitutional questions (+2 correct, -2 wrong)
      - digital_evidence: Digital evidence scenario MCQs
      - mini_scenario: Short written scenarios graded by AI (R.E.A.C.T.I.O.N.)

    Args:
        ext_db: Optional external database connection. If provided, uses it
                instead of the module-level db.
    """
    global db
    if ext_db is not None:
        db = ext_db

    now = datetime.now(timezone.utc)

    # ======== CATEGORIES ========
    categories = [
        {"category_id": "cat_most_appropriate", "name": "Most Appropriate", "description": "Select the MOST appropriate action for the scenario.", "order": 21},
        {"category_id": "cat_least_appropriate", "name": "Least Appropriate", "description": "Select the LEAST appropriate action for the scenario.", "order": 22},
        {"category_id": "cat_legal_trap", "name": "Legal Trap", "description": "Tricky legal and constitutional questions designed to test your knowledge under pressure.", "order": 23},
        {"category_id": "cat_digital_evidence", "name": "Digital Evidence", "description": "Digital evidence handling and preservation scenarios.", "order": 24},
        {"category_id": "cat_mini_scenario", "name": "Mini Scenarios", "description": "Short written scenarios graded by AI using the R.E.A.C.T.I.O.N. framework.", "order": 25},
    ]

    for cat in categories:
        await db.categories.update_one(
            {"category_id": cat["category_id"]},
            {"$set": cat},
            upsert=True
        )

    # ================================================================
    # SECTION 1: MOST APPROPRIATE (10 questions)
    # ================================================================
    most_appropriate = [
        {
            "title": "Ambiguous Invocation of Counsel",
            "content": "During interrogation, the suspect states:\n\"Maybe I should talk to someone.\"",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Continue questioning"},
                {"label": "B", "text": "Stop interrogation immediately"},
                {"label": "C", "text": "Clarify whether suspect is invoking counsel"},
                {"label": "D", "text": "Tell suspect a lawyer is unnecessary"}
            ],
            "correct_answer": "C",
            "explanation": "An ambiguous or equivocal reference to an attorney does NOT require cessation of questioning. Under Davis v. United States (1994), officers should clarify the suspect's intent. Continuing without clarification (A) risks suppression. Stopping immediately (B) is overly cautious for an ambiguous statement. Telling the suspect a lawyer is unnecessary (D) is coercive and improper.",
            "io_scores": {"A": -1, "B": 1, "C": 2, "D": -2},
            "difficulty": "hard",
            "reference": "Davis v. United States, 512 U.S. 452 (1994); 5th Amendment"
        },
        {
            "title": "Witness Contamination Before Interview",
            "content": "You arrive at an aggravated assault scene. Two witnesses are arguing about the suspect's description before you speak to them.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Interview them together to resolve the disagreement"},
                {"label": "B", "text": "Document the potential contamination and separate them immediately"},
                {"label": "C", "text": "Disregard both statements since they are contaminated"},
                {"label": "D", "text": "Tell them to agree on one description"}
            ],
            "correct_answer": "B",
            "explanation": "Document what you observed (the argument/contamination) and immediately separate the witnesses. Their statements can still be valuable — the contamination goes to weight, not admissibility. Interviewing together (A) compounds the problem. Disregarding both (C) loses valuable evidence. Telling them to agree (D) is witness tampering.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Witness Management"
        },
        {
            "title": "Suspect Provides Spontaneous Statement",
            "content": "While being transported to the station (no questions asked), the suspect blurts out: \"I didn't mean to shoot him, it just happened.\"",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Immediately read Miranda and begin formal questioning"},
                {"label": "B", "text": "Document the spontaneous statement verbatim and continue transport without questioning"},
                {"label": "C", "text": "Ask follow-up questions about what happened"},
                {"label": "D", "text": "Ignore the statement since Miranda was not given"}
            ],
            "correct_answer": "B",
            "explanation": "Spontaneous statements are admissible without Miranda because they are not the product of interrogation (Rhode Island v. Innis). Document the exact words, time, and circumstances. Do NOT follow up with questions (C) — that converts it to interrogation requiring Miranda. Do not ignore it (D) — it's valuable evidence. Reading Miranda and questioning immediately (A) may be premature and could taint the spontaneous statement.",
            "io_scores": {"A": 0, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "Rhode Island v. Innis, 446 U.S. 291 (1980); 5th Amendment"
        },
        {
            "title": "Victim Refuses Medical Treatment",
            "content": "You arrive at a battery scene. The victim has a visible laceration on the forehead and is bleeding. The victim refuses medical treatment and wants to give a statement immediately.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Respect the victim's wishes and take the statement immediately"},
                {"label": "B", "text": "Document the victim's refusal of medical treatment, photograph injuries, then take the statement"},
                {"label": "C", "text": "Force the victim to accept medical treatment before taking any statement"},
                {"label": "D", "text": "Ignore the injuries and focus only on getting the statement"}
            ],
            "correct_answer": "B",
            "explanation": "Document the refusal of medical treatment (CYA), photograph injuries while they are fresh and visible, and then proceed with the statement. You cannot force medical treatment on a conscious, competent adult (C). Ignoring injuries (D) fails to document critical evidence. Just taking the statement (A) misses the opportunity to document injuries and the refusal.",
            "io_scores": {"A": 0, "B": 2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Victim Rights"
        },
        {
            "title": "Off-Duty Witness is a Police Officer",
            "content": "At a homicide scene, one of the witnesses identifies himself as an off-duty CPD officer who observed the shooting while jogging.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Let the officer assist with the investigation since he is trained"},
                {"label": "B", "text": "Treat the officer as any other witness — separate, identify, and interview individually"},
                {"label": "C", "text": "Give the officer's statement more weight than civilian witnesses"},
                {"label": "D", "text": "Have the officer write his own supplemental report instead of being interviewed"}
            ],
            "correct_answer": "B",
            "explanation": "An off-duty officer who is a witness must be treated as a witness, not an investigator. Separate them from other witnesses, obtain identification, and conduct an individual interview. Allowing them to assist (A) compromises their witness role. Giving extra weight (C) introduces bias. A supplemental report (D) does not replace a proper witness interview.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": 0},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Witness Procedures"
        },
        {
            "title": "Supervisor Orders Premature Entry",
            "content": "Your supervisor orders you to enter an apartment to search for evidence of a narcotics offense. You have probable cause but no search warrant, no consent, and no exigent circumstances.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Follow the supervisor's order and enter the apartment"},
                {"label": "B", "text": "Respectfully inform the supervisor that a warrant is needed and document the conversation"},
                {"label": "C", "text": "Enter but do not seize anything until a warrant is obtained"},
                {"label": "D", "text": "Refuse the order publicly in front of other officers"}
            ],
            "correct_answer": "B",
            "explanation": "An unlawful order should not be followed. Respectfully inform the supervisor that without a warrant, consent, or exigent circumstances, the entry violates the 4th Amendment and any evidence will likely be suppressed. Document the conversation. Entering without a warrant (A, C) is unconstitutional. Public refusal (D) is unnecessarily confrontational.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": 0},
            "difficulty": "hard",
            "reference": "4th Amendment; Mapp v. Ohio; CPD General Order"
        },
        {
            "title": "Co-Defendant Wants to Cooperate",
            "content": "During a gang-related shooting investigation, one of two arrested co-defendants says to you: \"I want to tell you everything but I need a deal first.\"",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Promise leniency in exchange for information"},
                {"label": "B", "text": "Stop the conversation and contact the ASA to discuss potential cooperation"},
                {"label": "C", "text": "Continue questioning and worry about deals later"},
                {"label": "D", "text": "Tell the co-defendant that deals are not your responsibility"}
            ],
            "correct_answer": "B",
            "explanation": "Cooperation agreements must go through the ASA. You cannot promise leniency (A) — only prosecutors can authorize deals. Contact the ASA to discuss cooperation options. Continuing to question (C) without addressing the request may result in the defendant clamming up or an attorney challenge. Dismissing the request (D) loses a potentially valuable cooperating witness.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": 0},
            "difficulty": "hard",
            "reference": "CPD General Order; Felony Review Procedures"
        },
        {
            "title": "Child Witness at Violent Crime Scene",
            "content": "At a domestic homicide, an 8-year-old child witnessed the father kill the mother. The child is in shock and a responding officer wants to interview the child immediately to get the account while it's fresh.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Interview the child immediately while the memory is fresh"},
                {"label": "B", "text": "Secure the child with a trained advocate, notify DCFS, and arrange a forensic interview"},
                {"label": "C", "text": "Have the responding officer conduct a brief preliminary interview"},
                {"label": "D", "text": "Wait until the child is an adult to take a statement"}
            ],
            "correct_answer": "B",
            "explanation": "Child witnesses in traumatic situations require specialized handling. Secure the child with a trained victim advocate, notify DCFS as mandated, and arrange a forensic interview by a trained child interviewer at a Children's Advocacy Center. Immediate interrogation (A, C) by untrained officers can traumatize the child and produce unreliable testimony. Waiting until adulthood (D) is absurd and loses critical evidence.",
            "io_scores": {"A": -1, "B": 2, "C": 0, "D": -2},
            "difficulty": "hard",
            "reference": "CPD Special Order S07-01; DCFS Notification Requirements"
        },
        {
            "title": "Anonymous Tip About Firearm in Vehicle",
            "content": "You receive an anonymous tip that a specific vehicle parked on the street contains a firearm. The vehicle is unoccupied and legally parked.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Immediately search the vehicle based on the anonymous tip"},
                {"label": "B", "text": "Corroborate the tip through investigation, then seek a warrant if probable cause develops"},
                {"label": "C", "text": "Tow the vehicle to the station for a full inventory search"},
                {"label": "D", "text": "Ignore the tip since it is anonymous and uncorroborated"}
            ],
            "correct_answer": "B",
            "explanation": "An anonymous tip alone does not provide probable cause for a warrantless search (Florida v. J.L.). You must corroborate the tip through independent investigation. If corroborated, seek a warrant. Searching immediately (A) violates the 4th Amendment. Towing for inventory (C) is a pretextual seizure. Ignoring (D) fails your investigative duty.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "Florida v. J.L., 529 U.S. 266 (2000); 4th Amendment"
        },
        {
            "title": "Victim Wants to Recant Statement",
            "content": "Two days after a domestic battery arrest, the victim calls you and says she wants to \"drop the charges\" and take back her statement because she has reconciled with the offender.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Accommodate the victim's request and close the case"},
                {"label": "B", "text": "Document the recantation, inform the ASA, and continue the investigation with available evidence"},
                {"label": "C", "text": "Warn the victim that recanting is a crime"},
                {"label": "D", "text": "Pressure the victim to maintain the original statement"}
            ],
            "correct_answer": "B",
            "explanation": "Victim recantation is common in domestic violence cases. Document the recantation attempt, inform the ASA, and continue the investigation — the State may proceed without victim cooperation using other evidence (photographs, 911 calls, witness statements, excited utterances). You cannot close a case just because the victim wants to (A). Recanting is not inherently criminal (C). Pressuring the victim (D) is improper.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G06-04; Domestic Violence Procedures"
        },
    ]

    # ================================================================
    # SECTION 2: LEAST APPROPRIATE (10 questions)
    # ================================================================
    least_appropriate = [
        {
            "title": "Media at High-Profile Homicide",
            "content": "You are the lead detective at a high-profile homicide scene. Media crews are requesting comment.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Refer media to the Office of Communications"},
                {"label": "B", "text": "Protect investigative details from disclosure"},
                {"label": "C", "text": "Confirm an uncharged suspect's identity publicly"},
                {"label": "D", "text": "Coordinate with the ASA on public statements"}
            ],
            "correct_answer": "C",
            "explanation": "Publicly confirming an uncharged suspect's identity is the LEAST appropriate action. It can compromise the investigation, taint witness identifications, alert the suspect to flee, create civil liability, and violate the suspect's rights. All other options (A, B, D) are proper and expected actions.",
            "io_scores": {"A": -2, "B": -2, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G09-01; Media Relations"
        },
        {
            "title": "Evidence Moved Before Photography",
            "content": "A responding officer accidentally moved a firearm at the crime scene before photographs were taken.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Re-photograph the firearm and document the movement in the report"},
                {"label": "B", "text": "Ignore the movement because the firearm is now secured"},
                {"label": "C", "text": "Note the chain of custody disruption"},
                {"label": "D", "text": "Include the officer's action in the case report"}
            ],
            "correct_answer": "B",
            "explanation": "Ignoring the movement is the LEAST appropriate action. Failing to document the disruption creates a chain of custody gap that defense attorneys will exploit. You MUST document the movement, re-photograph, note the disruption, and include everything in the report — transparency protects the case.",
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-02; Evidence Handling"
        },
        {
            "title": "Suspect Requests Attorney During Interrogation",
            "content": "During custodial interrogation of a robbery suspect, the suspect clearly states: \"I want a lawyer.\"",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Immediately cease all questioning"},
                {"label": "B", "text": "Document the invocation and time"},
                {"label": "C", "text": "Ask \"Are you sure? We can clear this up right now.\""},
                {"label": "D", "text": "Contact the Public Defender's office"}
            ],
            "correct_answer": "C",
            "explanation": "Attempting to persuade the suspect to waive their invocation is the LEAST appropriate action. Once a suspect unambiguously invokes the right to counsel, ALL questioning must stop (Edwards v. Arizona). Trying to talk them out of it is coercive and will result in suppression of any subsequent statements.",
            "io_scores": {"A": -2, "B": -2, "C": 2, "D": -1},
            "difficulty": "hard",
            "reference": "Edwards v. Arizona, 451 U.S. 477 (1981); 5th & 6th Amendment"
        },
        {
            "title": "Crime Scene Contamination by Supervisor",
            "content": "Your watch commander arrives at a homicide scene and begins walking through the inner perimeter without booties or gloves, touching surfaces.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Politely inform the commander that the inner perimeter is restricted"},
                {"label": "B", "text": "Document the commander's entry in the crime scene log"},
                {"label": "C", "text": "Obtain the commander's DNA/fingerprint elimination samples"},
                {"label": "D", "text": "Say nothing because the commander outranks you"}
            ],
            "correct_answer": "D",
            "explanation": "Saying nothing because of rank is the LEAST appropriate action. Scene integrity trumps rank. You must protect the crime scene from ALL unauthorized contamination, document any contamination that occurs, and obtain elimination samples. Allowing contamination to go undocumented can destroy the case.",
            "io_scores": {"A": -2, "B": -2, "C": -2, "D": 2},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Crime Scene Integrity"
        },
        {
            "title": "Witness Identification Procedure",
            "content": "A robbery victim says they can identify the suspect. You have a suspect in custody matching the description.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Conduct a properly administered photo array or lineup"},
                {"label": "B", "text": "Show the victim a single photograph of the suspect and ask \"Is this the guy?\""},
                {"label": "C", "text": "Document the identification procedure with witnesses present"},
                {"label": "D", "text": "Have an independent administrator conduct the lineup"}
            ],
            "correct_answer": "B",
            "explanation": "Showing a single photograph is the LEAST appropriate action — it is an impermissibly suggestive identification procedure that will be challenged and likely suppressed (Manson v. Brathwaite). Proper procedure requires a photo array with fillers, or a lineup, preferably administered by someone not involved in the investigation.",
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "Manson v. Brathwaite, 432 U.S. 98 (1977); CPD Special Order S04-16"
        },
        {
            "title": "Processing Juvenile After Arrest",
            "content": "You arrest a 14-year-old for aggravated battery. The juvenile's parents cannot be located.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Continue attempting to contact parents/guardians through all available means"},
                {"label": "B", "text": "Proceed with custodial interrogation since parents are unavailable"},
                {"label": "C", "text": "Transport to the Youth Investigation section for processing"},
                {"label": "D", "text": "Document all efforts to contact parents in the report"}
            ],
            "correct_answer": "B",
            "explanation": "Proceeding with custodial interrogation of a juvenile without parental notification is the LEAST appropriate action. Illinois law requires that a juvenile's parent, guardian, or responsible adult be notified before any interrogation. You must continue attempts to locate them while processing the juvenile through Youth Investigation.",
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -2},
            "difficulty": "medium",
            "reference": "705 ILCS 405/5-405; CPD Special Order S07-01"
        },
        {
            "title": "Handling Confidential Informant Information",
            "content": "A confidential informant provides you with specific details about an upcoming gang retaliation shooting, including the target's name and location.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Document the information and share with your supervisor and intelligence unit"},
                {"label": "B", "text": "Warn the potential target about the threat"},
                {"label": "C", "text": "Post the informant's tip on social media to alert the public"},
                {"label": "D", "text": "Coordinate with tactical teams for an appropriate response"}
            ],
            "correct_answer": "C",
            "explanation": "Posting confidential informant information on social media is the LEAST appropriate action — it compromises the CI's identity and safety, destroys the investigation, alerts the offenders, and violates CI handling protocols. You should document, notify supervisors, warn the target through proper channels, and coordinate tactical response.",
            "io_scores": {"A": -2, "B": -1, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "CPD Special Order S09-07; Confidential Informant Procedures"
        },
        {
            "title": "Exigent Circumstances Assessment",
            "content": "You respond to a 911 call reporting screams from inside an apartment. Upon arrival, the apartment is quiet. No one answers the door. A neighbor says the screaming stopped 15 minutes ago.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Force entry based on exigent circumstances — potential victim inside"},
                {"label": "B", "text": "Continue knocking and announcing while listening for sounds of distress"},
                {"label": "C", "text": "Leave the scene since the screaming has stopped"},
                {"label": "D", "text": "Contact a supervisor and request guidance on forced entry"}
            ],
            "correct_answer": "C",
            "explanation": "Leaving the scene is the LEAST appropriate action. A 911 call reporting screams creates a reasonable belief that someone may be injured or in danger. The fact that screaming stopped does NOT mean the emergency is over — the victim could be incapacitated. Officers have a duty to investigate and ensure welfare.",
            "io_scores": {"A": -1, "B": -2, "C": 2, "D": -2},
            "difficulty": "hard",
            "reference": "CPD General Order; Community Caretaking Doctrine; Brigham City v. Stuart"
        },
        {
            "title": "Body-Worn Camera at Critical Incident",
            "content": "You arrive at a use-of-force incident. Multiple officers are present. You notice one officer's body-worn camera appears to be deactivated.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Document that the camera appeared deactivated in your report"},
                {"label": "B", "text": "Inform the officer's supervisor about the deactivated camera"},
                {"label": "C", "text": "Delete the observation from your notes to protect the officer"},
                {"label": "D", "text": "Ensure your own camera is recording and note the time"}
            ],
            "correct_answer": "C",
            "explanation": "Deleting observations to protect another officer is the LEAST appropriate action — it constitutes falsification of records and obstruction. You must document what you observe accurately, inform the supervisor, and ensure your own camera captures the scene. Truthful documentation protects everyone.",
            "io_scores": {"A": -2, "B": -2, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "CPD Special Order S03-14; Body-Worn Camera Policy"
        },
        {
            "title": "Search Warrant Scope Exceeded",
            "content": "While executing a search warrant for narcotics in the living room, you notice what appears to be child pornography on a computer screen in the bedroom (not covered by the warrant).",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Note the plain view observation and apply for an additional warrant for the computer"},
                {"label": "B", "text": "Seize the computer and begin searching its contents immediately"},
                {"label": "C", "text": "Document the observation and secure the room until a warrant is obtained"},
                {"label": "D", "text": "Contact the ASA about expanding the search warrant scope"}
            ],
            "correct_answer": "B",
            "explanation": "Seizing the computer and searching its contents exceeds the warrant scope and is the LEAST appropriate action. While the plain view doctrine allows you to note contraband in plain sight, searching digital contents requires a separate warrant. Secure the room, document the observation, and get a new warrant.",
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "Riley v. California, 573 U.S. 373 (2014); 4th Amendment; Plain View Doctrine"
        },
    ]

    # ================================================================
    # SECTION 3: LEGAL TRAP (10 questions)
    # ================================================================
    legal_trap = [
        {
            "title": "Invocation of Right to Silence",
            "content": "During custodial interrogation, the suspect says:\n\"I don't want to talk anymore.\"",
            "question": "What MUST you do?",
            "options": [
                {"label": "A", "text": "Ask one more clarifying question"},
                {"label": "B", "text": "Continue discussing unrelated topics"},
                {"label": "C", "text": "Cease interrogation immediately"},
                {"label": "D", "text": "Threaten additional charges"}
            ],
            "correct_answer": "C",
            "explanation": "When a suspect unambiguously invokes the right to silence, ALL questioning must cease immediately (Miranda v. Arizona; Michigan v. Mosley). There are no exceptions for \"one more question\" (A), unrelated topics (B), or threats (D). Any statements obtained after invocation will be suppressed.",
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -2},
            "difficulty": "hard",
            "reference": "Miranda v. Arizona, 384 U.S. 436 (1966); Michigan v. Mosley"
        },
        {
            "title": "Automobile Exception to Warrant Requirement",
            "content": "During a traffic stop for a broken taillight, you smell burnt cannabis coming from the vehicle. The driver denies having any cannabis.",
            "question": "Can you search the vehicle without a warrant?",
            "options": [
                {"label": "A", "text": "No — the smell of cannabis alone is insufficient since legalization"},
                {"label": "B", "text": "Yes — the odor of burnt cannabis provides probable cause under the automobile exception"},
                {"label": "C", "text": "Only if you arrest the driver first"},
                {"label": "D", "text": "Only with the driver's written consent"}
            ],
            "correct_answer": "B",
            "explanation": "Under the automobile exception (Carroll v. United States), the odor of burnt cannabis provides probable cause to search the vehicle. While Illinois legalized recreational cannabis possession, the odor of BURNT cannabis in a vehicle still provides probable cause because operating a vehicle while impaired is illegal and the officer has reason to believe the driver may have been using while driving.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": 0},
            "difficulty": "hard",
            "reference": "Carroll v. United States; People v. Molina (IL); 625 ILCS 5/11-502.1"
        },
        {
            "title": "Fruit of the Poisonous Tree",
            "content": "An officer conducts an illegal stop and finds a firearm on the suspect. While processing, the suspect's fingerprints match an unrelated cold-case homicide.",
            "question": "What is the likely outcome regarding the homicide fingerprint evidence?",
            "options": [
                {"label": "A", "text": "The homicide evidence is admissible because it relates to a different crime"},
                {"label": "B", "text": "The homicide evidence is likely inadmissible as fruit of the poisonous tree"},
                {"label": "C", "text": "The homicide evidence is automatically admissible under the good faith exception"},
                {"label": "D", "text": "Only the firearm is suppressed; fingerprints are always admissible"}
            ],
            "correct_answer": "B",
            "explanation": "Under the fruit of the poisonous tree doctrine (Wong Sun v. United States), evidence derived from an illegal stop is tainted and generally inadmissible — even if it relates to a different crime. The fingerprints were obtained as a direct result of the illegal stop. There may be exceptions (independent source, inevitable discovery, attenuation), but the evidence is likely suppressed.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "Wong Sun v. United States, 371 U.S. 471 (1963); Exclusionary Rule"
        },
        {
            "title": "Terry Stop Duration",
            "content": "You conduct a Terry stop on a suspicious individual. The person provides identification and answers your questions. After 5 minutes, you have not developed probable cause but have a \"gut feeling\" something is wrong.",
            "question": "What must you do?",
            "options": [
                {"label": "A", "text": "Continue detaining the person until you satisfy your suspicion"},
                {"label": "B", "text": "Release the person — a Terry stop cannot be prolonged without developing probable cause"},
                {"label": "C", "text": "Transport the person to the station for further investigation"},
                {"label": "D", "text": "Conduct a full search based on your gut feeling"}
            ],
            "correct_answer": "B",
            "explanation": "A Terry stop must be brief and limited in scope. If after reasonable investigation you cannot develop probable cause, you must release the person. A \"gut feeling\" is not reasonable suspicion or probable cause. Prolonging the detention (A), transporting (C), or searching (D) without legal justification violates the 4th Amendment.",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -2},
            "difficulty": "medium",
            "reference": "Terry v. Ohio, 392 U.S. 1 (1968); Illinois v. Wardlow"
        },
        {
            "title": "Public Safety Exception to Miranda",
            "content": "Officers respond to a shooting in a mall. The suspect is apprehended. Before Miranda is given, an officer asks: \"Where did you put the gun?\"",
            "question": "Is the suspect's answer admissible?",
            "options": [
                {"label": "A", "text": "No — Miranda is always required before any custodial questioning"},
                {"label": "B", "text": "Yes — the public safety exception allows limited pre-Miranda questioning about imminent danger"},
                {"label": "C", "text": "Only if the suspect was not formally arrested"},
                {"label": "D", "text": "Only if the suspect was read an abbreviated Miranda warning"}
            ],
            "correct_answer": "B",
            "explanation": "Under New York v. Quarles (1984), the public safety exception allows officers to ask questions necessary to protect public safety before reading Miranda. A gun loose in a public mall poses an imminent threat. The question is narrowly tailored to locate the weapon. The answer is admissible.",
            "io_scores": {"A": -1, "B": 2, "C": 0, "D": -1},
            "difficulty": "hard",
            "reference": "New York v. Quarles, 467 U.S. 649 (1984); Public Safety Exception"
        },
        {
            "title": "Consent Search After Arrest",
            "content": "After arresting a suspect for narcotics possession outside his apartment, you ask the suspect: \"Mind if we check inside your place?\" The suspect, in handcuffs, says: \"Sure, go ahead.\"",
            "question": "Is this consent likely valid?",
            "options": [
                {"label": "A", "text": "Yes — the suspect verbally consented"},
                {"label": "B", "text": "The consent is vulnerable to challenge because it was given while in custody under coercive circumstances"},
                {"label": "C", "text": "Yes — consent after arrest is automatically valid"},
                {"label": "D", "text": "No — arrested persons can never consent to searches"}
            ],
            "correct_answer": "B",
            "explanation": "While consent searches after arrest are not automatically invalid (D is wrong), consent given while in handcuffs/custody is subject to heightened scrutiny. Courts examine the totality of circumstances — custody is a significant factor suggesting coercion. The consent is vulnerable to challenge. A warrant is the safer approach.",
            "io_scores": {"A": 0, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "Schneckloth v. Bustamonte, 412 U.S. 218 (1973); Voluntariness Standard"
        },
        {
            "title": "Knock-and-Announce Requirement",
            "content": "You have a search warrant for a residence. Based on intelligence, the occupant is a convicted felon with prior weapons charges but there is no current information about weapons inside.",
            "question": "Are you required to knock and announce before entry?",
            "options": [
                {"label": "A", "text": "No — a felon's prior weapons charges automatically justify a no-knock entry"},
                {"label": "B", "text": "Yes — knock-and-announce is required unless you have specific, current information justifying a no-knock warrant"},
                {"label": "C", "text": "No — all narcotics warrants are no-knock by default"},
                {"label": "D", "text": "Only if the judge specifically orders knock-and-announce on the warrant"}
            ],
            "correct_answer": "B",
            "explanation": "The knock-and-announce rule is a constitutional requirement (Wilson v. Arkansas). Exceptions require specific, articulable reasons related to the CURRENT situation — not just a prior record. Prior weapons charges alone do not justify no-knock entry. You need current intelligence suggesting a specific threat.",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "Wilson v. Arkansas, 514 U.S. 927 (1995); Richards v. Wisconsin"
        },
        {
            "title": "Dual Sovereignty and Double Jeopardy",
            "content": "A suspect is acquitted of a gang-related murder in Cook County court. Federal prosecutors want to charge the same suspect for the same killing under federal RICO statutes.",
            "question": "Can the federal government proceed?",
            "options": [
                {"label": "A", "text": "No — double jeopardy prohibits any re-prosecution after acquittal"},
                {"label": "B", "text": "Yes — under the dual sovereignty doctrine, federal charges are not barred by state acquittal"},
                {"label": "C", "text": "Only if new evidence emerges after the state trial"},
                {"label": "D", "text": "Only with the state prosecutor's written consent"}
            ],
            "correct_answer": "B",
            "explanation": "Under the dual sovereignty doctrine (Gamble v. United States, 2019), the same conduct can be prosecuted by different sovereigns (state and federal) without violating double jeopardy. The state and federal governments are separate sovereigns. Federal RICO prosecution can proceed regardless of the state outcome.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": 0},
            "difficulty": "hard",
            "reference": "Gamble v. United States, 587 U.S. ___ (2019); Dual Sovereignty Doctrine"
        },
        {
            "title": "Protective Sweep After In-Home Arrest",
            "content": "You have an arrest warrant for a suspect in his apartment. After arresting the suspect in the living room, you want to check the rest of the apartment for other occupants.",
            "question": "What is the legal standard for this protective sweep?",
            "options": [
                {"label": "A", "text": "You need probable cause to believe other criminals are present"},
                {"label": "B", "text": "Reasonable suspicion that the area harbors a person posing a danger is sufficient for a protective sweep"},
                {"label": "C", "text": "No legal standard — you can search the entire apartment after any arrest"},
                {"label": "D", "text": "A separate search warrant is always required"}
            ],
            "correct_answer": "B",
            "explanation": "Under Maryland v. Buie (1990), a protective sweep incident to an in-home arrest requires only reasonable, articulable suspicion that the area to be swept harbors an individual posing a danger. The sweep is limited to a cursory visual inspection of spaces where a person could be hiding. It is not a full search.",
            "io_scores": {"A": 0, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "Maryland v. Buie, 494 U.S. 325 (1990); Protective Sweep Doctrine"
        },
        {
            "title": "Electronic Recording Requirement",
            "content": "You are about to begin a custodial interrogation for a Class 1 felony. The electronic recording equipment in the interview room is malfunctioning.",
            "question": "What must you do?",
            "options": [
                {"label": "A", "text": "Proceed with the interrogation — recording is preferred but not legally required"},
                {"label": "B", "text": "Use any available alternative recording method (phone, body camera) and document the equipment failure"},
                {"label": "C", "text": "Cancel the interrogation entirely until equipment is fixed"},
                {"label": "D", "text": "Have the suspect sign a waiver agreeing to unrecorded interrogation"}
            ],
            "correct_answer": "B",
            "explanation": "Illinois law (725 ILCS 5/103-2.1) requires electronic recording of custodial interrogations for certain felonies. If the primary equipment fails, use any available alternative and document the failure. A waiver (D) does not satisfy the statutory requirement. Proceeding without any recording (A) risks suppression. Canceling entirely (C) is unnecessary if alternatives exist.",
            "io_scores": {"A": -2, "B": 2, "C": 0, "D": -1},
            "difficulty": "hard",
            "reference": "725 ILCS 5/103-2.1; Illinois Electronic Recording Act"
        },
    ]

    # ================================================================
    # SECTION 4: DIGITAL EVIDENCE (10 questions)
    # ================================================================
    digital_evidence = [
        {
            "title": "Live-Streamed Robbery — Phone Recovery",
            "content": "A suspect live-streamed a robbery on social media. The suspect's phone is recovered at arrest.",
            "question": "What is the MOST appropriate next step?",
            "options": [
                {"label": "A", "text": "Scroll through the phone contents immediately to find the video"},
                {"label": "B", "text": "Secure the phone in a Faraday bag and seek a search warrant"},
                {"label": "C", "text": "Have the victim unlock the phone to verify the video"},
                {"label": "D", "text": "Return the phone to the suspect's personal property"}
            ],
            "correct_answer": "B",
            "explanation": "Riley v. California (2014) requires a warrant to search cell phone contents, even incident to arrest. Secure the phone in a Faraday bag to prevent remote wiping, then obtain a warrant. Scrolling through (A) violates the 4th Amendment. The victim has no authority to unlock the suspect's phone (C). Returning it (D) loses critical evidence.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "Riley v. California, 573 U.S. 373 (2014)"
        },
        {
            "title": "Social Media Witnesses Identifying Suspect",
            "content": "You learn that social media viewers are identifying the robbery suspect in comments on the live-stream video.",
            "question": "What should you do FIRST?",
            "options": [
                {"label": "A", "text": "Publicly respond in the comments to confirm the investigation"},
                {"label": "B", "text": "Preserve the link and request a legal hold from the platform"},
                {"label": "C", "text": "Ignore the comments since social media is unreliable"},
                {"label": "D", "text": "Share screenshots of the comments with media outlets"}
            ],
            "correct_answer": "B",
            "explanation": "Preserve the evidence immediately — social media content can be deleted at any time. Request a legal hold/preservation letter to the platform. Public comments (A) compromise the investigation. Ignoring (C) loses potential leads and witnesses. Sharing with media (D) could taint identifications and compromise the case.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "18 U.S.C. 2703(f); Stored Communications Act; Evidence Preservation"
        },
        {
            "title": "Suspect's Computer at Crime Scene",
            "content": "While executing a search warrant for fraud, you find a laptop with the screen open showing financial records. The warrant covers paper records and financial documents.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Photograph what is visible on screen (plain view) and apply for a separate warrant for the computer"},
                {"label": "B", "text": "Seize the computer and perform a full forensic search under the existing warrant"},
                {"label": "C", "text": "Close the laptop to preserve evidence and search it at the station"},
                {"label": "D", "text": "Have the suspect log off to protect his privacy rights"}
            ],
            "correct_answer": "A",
            "explanation": "Under the plain view doctrine, you can photograph what is visible on the screen. However, a computer search requires a specific warrant (Riley v. California extended to computers). You cannot search beyond what is in plain view under a paper records warrant. Closing the laptop (C) may destroy volatile data. Having the suspect interact with evidence (D) compromises the chain of custody.",
            "io_scores": {"A": 2, "B": -2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "Riley v. California; United States v. Ganias; Plain View Doctrine"
        },
        {
            "title": "Cloud Storage and Jurisdiction",
            "content": "During a homicide investigation, you discover the suspect uses an encrypted cloud storage service hosted on servers in another state. You need the contents for evidence.",
            "question": "What is the correct approach?",
            "options": [
                {"label": "A", "text": "Hack into the cloud account using the suspect's credentials found at the scene"},
                {"label": "B", "text": "Obtain a search warrant and serve it on the cloud provider with a preservation request"},
                {"label": "C", "text": "Ask the suspect to voluntarily provide the password"},
                {"label": "D", "text": "Subpoena the cloud provider for all account contents without a warrant"}
            ],
            "correct_answer": "B",
            "explanation": "Cloud storage has a reasonable expectation of privacy requiring a warrant (Carpenter v. United States framework). Obtain a warrant and serve it on the provider along with a preservation request (18 U.S.C. 2703(f)). Hacking (A) is illegal (CFAA). Voluntary password request (C) may work but is less reliable. A subpoena (D) typically only yields subscriber info, not contents.",
            "io_scores": {"A": -2, "B": 2, "C": 0, "D": -1},
            "difficulty": "hard",
            "reference": "Carpenter v. United States, 585 U.S. ___ (2018); 18 U.S.C. 2703"
        },
        {
            "title": "Body-Worn Camera Footage as Evidence",
            "content": "An officer's body-worn camera captured a suspect making incriminating statements during a Terry stop. The suspect was not in custody and Miranda was not given.",
            "question": "Is the BWC footage admissible?",
            "options": [
                {"label": "A", "text": "No — Miranda was not given before the statements"},
                {"label": "B", "text": "Yes — Miranda is only required for custodial interrogation, and a Terry stop is not custody"},
                {"label": "C", "text": "Only if the suspect consented to being recorded"},
                {"label": "D", "text": "Only if the camera was activated before contact"}
            ],
            "correct_answer": "B",
            "explanation": "Miranda applies only to custodial interrogation. A Terry stop is a temporary detention, not custody, so Miranda warnings are not required. Statements made during a consensual encounter or Terry stop are admissible. Illinois is a one-party consent state for recordings, and BWC policies authorize recording.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": 0},
            "difficulty": "medium",
            "reference": "Berkemer v. McCarty, 468 U.S. 420 (1984); CPD BWC Policy"
        },
        {
            "title": "GPS Tracking Device",
            "content": "You want to place a GPS tracking device on a suspect's vehicle to monitor movements during a narcotics investigation.",
            "question": "What legal authorization do you need?",
            "options": [
                {"label": "A", "text": "No authorization needed — vehicles on public roads have no expectation of privacy"},
                {"label": "B", "text": "A search warrant is required to attach a GPS tracker to a vehicle"},
                {"label": "C", "text": "Only a supervisor's approval is needed"},
                {"label": "D", "text": "A grand jury subpoena is sufficient"}
            ],
            "correct_answer": "B",
            "explanation": "United States v. Jones (2012) held that physically attaching a GPS device to a vehicle constitutes a search under the 4th Amendment, requiring a warrant. The trespassory installation plus monitoring of movements triggers warrant protection. Supervisor approval (C) and subpoenas (D) are insufficient.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "United States v. Jones, 565 U.S. 400 (2012)"
        },
        {
            "title": "Geofence Warrant",
            "content": "A bombing occurred in a commercial district. You want to identify all cell phones that were in the area during the incident using location data from Google.",
            "question": "What is the proper legal process?",
            "options": [
                {"label": "A", "text": "Submit a records request to Google — no warrant needed for business records"},
                {"label": "B", "text": "Obtain a geofence warrant specifying the geographic area, time frame, and limiting data to relevant devices"},
                {"label": "C", "text": "Request all cell tower data from every carrier in the area without a warrant"},
                {"label": "D", "text": "Use a cell site simulator (Stingray) without authorization"}
            ],
            "correct_answer": "B",
            "explanation": "A geofence warrant (reverse location warrant) requires judicial authorization specifying the area, time frame, and step-down protocols to minimize privacy intrusion. Carpenter v. United States established that cell phone location data is protected by the 4th Amendment. Warrantless requests (A, C) and unauthorized Stingray use (D) violate constitutional protections.",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "Carpenter v. United States; Geofence Warrant Best Practices"
        },
        {
            "title": "Drone Surveillance",
            "content": "You want to use a CPD drone to conduct aerial surveillance of a suspect's fenced backyard during an investigation.",
            "question": "What is required?",
            "options": [
                {"label": "A", "text": "Nothing — aerial surveillance from any altitude is legal under the open fields doctrine"},
                {"label": "B", "text": "A search warrant, since the fenced backyard has a reasonable expectation of privacy (curtilage)"},
                {"label": "C", "text": "Only FAA flight approval is needed"},
                {"label": "D", "text": "Written consent from the suspect's neighbors"}
            ],
            "correct_answer": "B",
            "explanation": "A fenced backyard is curtilage — an area with a reasonable expectation of privacy (Florida v. Riley framework). While some aerial surveillance from public airspace may be lawful, drone technology capable of detailed surveillance likely requires a warrant under Kyllo v. United States principles. A warrant is the safest legal approach.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": 0},
            "difficulty": "hard",
            "reference": "Florida v. Riley; Kyllo v. United States; FAA Part 107"
        },
        {
            "title": "Suspect's Ring Doorbell Camera",
            "content": "During a neighborhood canvass for a shooting, a resident's Ring doorbell camera likely captured the incident. The resident is not home.",
            "question": "How do you obtain the footage?",
            "options": [
                {"label": "A", "text": "Log into the Ring app using the resident's WiFi network"},
                {"label": "B", "text": "Contact Ring/Amazon directly with an emergency disclosure request and simultaneously seek a warrant"},
                {"label": "C", "text": "Remove the doorbell camera and download footage at the station"},
                {"label": "D", "text": "Wait until the resident returns — there is no urgency"}
            ],
            "correct_answer": "B",
            "explanation": "Under 18 U.S.C. 2702(c)(4), providers may disclose records in emergency situations involving danger of death or serious injury. Contact Ring with an emergency disclosure request while simultaneously seeking a warrant. Unauthorized access (A), theft of the camera (C), and unnecessary delay (D) are all improper.",
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "18 U.S.C. 2702(c)(4); Emergency Disclosure; Stored Communications Act"
        },
        {
            "title": "Encrypted Messaging App Evidence",
            "content": "A gang member uses an encrypted messaging app (Signal) to coordinate drug transactions. You have a warrant for the phone but the app uses end-to-end encryption.",
            "question": "What is the MOST effective legal approach?",
            "options": [
                {"label": "A", "text": "Compel Signal to decrypt the messages with a court order"},
                {"label": "B", "text": "Extract what is available from the physical device via forensic tools — messages may be stored locally even if encrypted in transit"},
                {"label": "C", "text": "Abandon the digital evidence since encryption makes it impossible"},
                {"label": "D", "text": "Install spyware on the suspect's phone without a warrant"}
            ],
            "correct_answer": "B",
            "explanation": "End-to-end encryption means the provider (Signal) cannot decrypt messages — they don't hold the keys. However, messages are stored in decrypted form on the device itself. Forensic extraction tools (Cellebrite, GrayKey) may be able to access local storage. Signal cannot be compelled to decrypt (A). Abandoning (C) gives up prematurely. Unauthorized spyware (D) is illegal.",
            "io_scores": {"A": 0, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "All Writs Act; Forensic Extraction Procedures"
        },
    ]

    # ================================================================
    # SECTION 5: MINI SCENARIOS (10 questions)
    # ================================================================
    mini_scenarios = [
        {
            "title": "Robbery with Armed Store Owner",
            "content": "You arrive at a robbery scene. The store owner shot one suspect (deceased). A second suspect fled on foot eastbound. The store owner appears to be in shock and is still holding the firearm. The store has surveillance video. Multiple witnesses are present outside. Outline your investigative steps in 8-12 bullet points using proper prioritization.",
            "answer": '{"modelAnswer":{"R":["Ensure officer safety — the store owner is armed and in shock, approach cautiously with verbal commands","Request CFD/EMS for the deceased suspect (pronouncement) and assess store owner for injuries","Secure the firearm from the store owner safely — do NOT let a shocked armed person remain holding a weapon","Request Medical Examiner for the deceased suspect"],"E":["Broadcast flash message/BOLO with second suspect description and direction of flight","Establish inner/outer perimeter around the store","Assign officers to protect the scene and control entry/exit","Separate the store owner from the shooting scene"],"A":["Determine if the store owner needs to be detained or is cooperative witness/victim","Document the store owner position and the deceased suspect position","Advise the store owner of his rights if custodial situation develops","Note any spontaneous statements"],"C":["Separate and identify all witnesses before they leave","Obtain preliminary statements from each witness individually","Identify witnesses who saw the second suspect flee","Canvass for additional witnesses in nearby businesses"],"T":["Photograph the entire scene before anything is moved","Document the firearm location, shell casings, blood evidence","Secure body-worn camera footage from all responding officers","Sketch the scene with measurements"],"I":["Recover and inventory the store owner firearm with proper chain of custody","Request Evidence Technicians for the full scene","Collect shell casings, blood evidence, trace evidence","Preserve the surveillance video immediately — do not let it be overwritten"],"O":["Notify ASA for Felony Review regarding the shooting circumstances","Determine if self-defense/justifiable use of force","Request search warrant if needed for store records","Conduct LEADS/CLEAR check on deceased suspect"],"N":["Issue supplemental BOLO as more suspect information develops","Notify Area Detective Division supervisor","Prepare case file for Felony Review","Coordinate with COPA if any officer use of force involved"]}}',
            "difficulty": "hard",
            "time_limit": 600,
            "reference": "CPD General Order G06-01-01; Use of Force by Civilians"
        },
        {
            "title": "Aggravated DUI with Pedestrian Fatality",
            "content": "You respond to a fatal traffic crash. A vehicle struck a pedestrian in a crosswalk. The driver remained on scene and appears intoxicated — slurred speech, unsteady gait, strong odor of alcohol. The pedestrian is deceased. Multiple witnesses stopped. The driver states: \"I only had two beers.\" Outline your investigative steps in 8-12 bullet points.",
            "answer": '{"modelAnswer":{"R":["Confirm pedestrian is deceased, request Medical Examiner","Assess driver for injuries, request EMS evaluation","Ensure scene safety — activate emergency lights, request traffic control"],"E":["Close the intersection and establish a perimeter","Request Major Accident Investigation Unit (MAIU)","Assign officers to secure scene and divert traffic","Protect tire marks, debris, and point of impact"],"A":["Administer standardized field sobriety tests (SFST)","Request blood/breath alcohol testing — time-critical evidence","Document the driver spontaneous statement verbatim (excited utterance)","Place driver under arrest for Aggravated DUI causing death if tests support"],"C":["Identify and separate all witnesses","Obtain witness statements about vehicle speed, traffic signals, pedestrian position","Canvass for additional witnesses who may have left","Identify any dash-cam or ride-share footage from other vehicles"],"T":["Photograph entire scene including skid marks, final rest positions, debris field","Document weather, lighting, road conditions, traffic signals","Video record the scene and driver demeanor/behavior","Record precise measurements for crash reconstruction"],"I":["Preserve blood/breath alcohol evidence with proper chain of custody","Impound the vehicle for inspection — do not release","Request ECM/black box data download from vehicle","Collect driver clothing for trace evidence"],"O":["Contact ASA for Felony Review — Aggravated DUI causing death is a Class 2 felony","Request search warrant for driver blood draw if refused","Check driver record through LEADS for prior DUI history","Ensure 625 ILCS 5/11-501 compliance"],"N":["Notify deceased pedestrian next of kin through proper channels","Complete full crash report and supplement with detective case report","Coordinate with MAIU for crash reconstruction","Prepare case for Felony Review and court"]}}',
            "difficulty": "hard",
            "time_limit": 600,
            "reference": "625 ILCS 5/11-501; CPD General Order G06-03"
        },
        {
            "title": "Carjacking with GPS Tracking",
            "content": "A victim reports her vehicle was just carjacked at gunpoint 10 minutes ago. She has a GPS tracking app showing the vehicle is moving southbound on the expressway. She can describe the offender. The victim is uninjured but shaken. Outline your investigative steps in 8-12 bullet points.",
            "answer": '{"modelAnswer":{"R":["Assess victim for injuries and emotional state, offer victim services","Ensure victim is in a safe location away from the scene"],"E":["Broadcast emergency flash message with suspect description, vehicle description, and current GPS location","Coordinate with OEMC for real-time GPS tracking and pursuit coordination","Request helicopter/aviation unit if available","Notify expressway units and surrounding districts"],"A":["If suspect is located — conduct felony vehicle stop with tactical approach","Arrest offender for vehicular hijacking (Class 1 felony)","Administer Miranda before custodial interrogation","Photograph suspect and document any injuries/identifying marks"],"C":["Obtain detailed victim statement including suspect description, weapon description, exact sequence of events","Canvas the carjacking location for witnesses","Check POD cameras at the scene","Instruct victim to preserve independent recollection"],"T":["Photograph the carjacking scene","Document the GPS tracking data as evidence (screenshots, timestamps)","Secure body-worn camera footage","Document timeline from report to recovery"],"I":["When vehicle is recovered — process for fingerprints, DNA, trace evidence","Recover and inventory the weapon if found","Do not return vehicle to victim until fully processed","Check for suspect personal items left in vehicle"],"O":["Contact ASA for Felony Review — vehicular hijacking with firearm","Request search warrant for suspect phone if recovered","Run suspect through LEADS/CLEAR for prior history","Check for pattern — link to other carjackings in area"],"N":["Issue BOLO updates as situation develops","Notify Area Detective supervisor","Connect victim with victim services and court advocacy","Prepare complete case package for prosecution"]}}',
            "difficulty": "hard",
            "time_limit": 600,
            "reference": "720 ILCS 5/18-3; Vehicular Hijacking Procedures"
        },
        {
            "title": "Home Invasion with Elderly Victim",
            "content": "An 82-year-old woman calls 911 reporting two men just forced their way into her home, tied her up, and ransacked the house. They left approximately 20 minutes ago in a dark SUV. The victim is physically uninjured but extremely frightened. She can provide partial descriptions. Outline your investigative steps in 8-12 bullet points.",
            "answer": '{"modelAnswer":{"R":["Request EMS to evaluate the elderly victim despite no visible injuries","Ensure victim comfort and safety — assign a female officer if victim prefers","Check for signs of elder abuse beyond the home invasion","Document victim emotional and physical state"],"E":["Broadcast BOLO with suspect descriptions, vehicle description, and direction of travel","Secure the residence as a crime scene","Establish perimeter to prevent evidence loss","Check for forced entry points and document"],"A":["Canvass neighborhood for suspect vehicle — check POD cameras, traffic cameras","Run suspect descriptions through databases and local intelligence","Check for similar home invasion patterns in the area","Coordinate with patrol for area saturation"],"C":["Obtain detailed victim statement when she is calm enough","Ask specific questions about items taken (for tracking/pawn alerts)","Canvass neighbors — someone may have seen the SUV or suspects","Check for Ring/Nest doorbell cameras on the block"],"T":["Photograph all entry points, ransacked areas, and ligature marks on victim","Document timeline based on victim account","Secure body-worn camera footage","Create crime scene sketch"],"I":["Request Evidence Technicians for fingerprints at entry points and touched surfaces","Collect ligature material as evidence","Process for DNA — suspects may have touched victim","Check for shoe prints and tool marks at entry"],"O":["Contact ASA — Home Invasion is a Class X felony","Alert pawn shops and online marketplaces for stolen items","Run LEADS check on any suspect information","Coordinate with Area detective resources"],"N":["Connect victim with elder services and victim advocacy","Arrange for victim safety — can she stay with family? Does she need relocation?","Issue crime alert for the neighborhood","Follow up on forensic results and surveillance leads"]}}',
            "difficulty": "medium",
            "time_limit": 600,
            "reference": "720 ILCS 5/19-6; CPD Home Invasion Response"
        },
        {
            "title": "Officer-Involved Shooting — You Are First Detective",
            "content": "An officer-involved shooting has just occurred. The offender is deceased. The involved officer is physically uninjured but visibly shaken. Another officer on scene administered first aid to the offender before he died. You are the first detective on scene. Outline your investigative steps in 8-12 bullet points.",
            "answer": '{"modelAnswer":{"R":["Confirm offender is deceased, request Medical Examiner","Assess involved officer for injuries — include psychological welfare check","Request EMS to evaluate the involved officer even if no visible injuries","Ensure all officers on scene are accounted for and safe"],"E":["Secure the entire scene with expanded perimeter — this is a critical incident","Separate the involved officer from the scene immediately","Do NOT allow the involved officer to discuss the incident with anyone","Assign officers to protect all evidence including shell casings, weapon positions"],"A":["Do NOT take a formal statement from the involved officer — COPA handles the investigation","Document the involved officer position, weapon status, and general condition","Note any spontaneous statements made before separation","Ensure all officers weapons are accounted for"],"C":["Identify and separate ALL witnesses — civilian and officer","Obtain witness statements from civilian witnesses","Identify officers who witnessed the event for COPA","Canvas for additional witnesses and surveillance"],"T":["Photograph the entire scene before anything is moved","Document offender weapon location, officer position, evidence locations","Secure all body-worn camera footage — place administrative hold","Document exact time of your arrival and all subsequent actions"],"I":["Preserve ALL physical evidence — shell casings, weapons, clothing","Request Evidence Technicians for full crime scene processing","Collect the offender weapon with proper chain of custody","Do NOT collect the involved officer weapon — COPA/firearms unit handles this"],"O":["Notify COPA (Civilian Office of Police Accountability) immediately — mandatory","Notify the Area Deputy Chief and Detective Division Chief","Contact the ASA for Felony Review of the shooting circumstances","Request FOP representation for the involved officer before any formal interview"],"N":["Prepare the scene for COPA investigators arrival","Ensure media is kept outside the perimeter","Notify Office of Communications for media management","Complete initial case report documenting the scene and evidence — NOT the officer statement"]}}',
            "difficulty": "hard",
            "time_limit": 600,
            "reference": "CPD General Order G03-06; Special Order S08-01; COPA Notification"
        },
        {
            "title": "Sexual Assault at University",
            "content": "Campus police request CPD assistance with a sexual assault reported at a university dorm room. The victim (20-year-old female) reports being assaulted by a male student she knows. The assault occurred approximately 4 hours ago. The victim has not showered but has changed clothing. The suspect is believed to be in his dorm room in another building. Outline your investigative steps in 8-12 bullet points.",
            "answer": '{"modelAnswer":{"R":["Assign a same-gender officer if possible, provide privacy and victim-centered care","Assess victim emotional and physical state","Contact victim advocate/SANE coordinator","Do NOT ask the victim to repeat the account multiple times at this stage"],"E":["Secure the dorm room where the assault occurred — seal as crime scene","Secure the changed clothing as evidence — do not discard","Coordinate jurisdiction with campus police — CPD has primary for felony investigation","Notify SVU (Special Victims Unit) to assign the case"],"A":["Do NOT rush to arrest the suspect — build the case first","Identify suspect location (other dorm building) and ensure he does not flee","Consider whether to seek warrant or make contact","Preserve suspects clothing and physical evidence if contact is made"],"C":["Transport victim to hospital for SAFE exam (forensic evidence kit)","Obtain victim statement when ready, with SVU guidance","Identify potential witnesses — roommates, hallway residents, party attendees","Check for surveillance cameras in dorm hallways and entry points"],"T":["Photograph the crime scene dorm room","Document the victim account with exact timeline","Secure any electronic communications between victim and suspect","Preserve campus security footage"],"I":["SAFE exam is priority for DNA and physical evidence collection","Collect the changed clothing as evidence","Process the dorm room for DNA, fingerprints, biological evidence","Preserve any alcohol/drug evidence if intoxication involved"],"O":["Contact ASA for Felony Review — Criminal Sexual Assault","Determine if a search warrant is needed for suspects dorm room","Review Title IX implications with university","Check suspect background through LEADS/CLEAR"],"N":["Connect victim with university victim services and advocacy","Advise victim of order of protection options","Coordinate with SVU for follow-up investigation","Prepare case package for prosecution"]}}',
            "difficulty": "hard",
            "time_limit": 600,
            "reference": "CPD Special Order S04-03; Sexual Assault Response; SVU Procedures"
        },
        {
            "title": "Active Shooter Aftermath — Mass Casualty",
            "content": "An active shooter event at a shopping mall has been neutralized. The offender is in custody (wounded). There are 6 victims with varying injuries — 2 critical, 3 moderate, 1 deceased. Dozens of witnesses are present. Multiple agencies are on scene. You are assigned as lead detective. Outline your investigative steps in 8-12 bullet points.",
            "answer": '{"modelAnswer":{"R":["Coordinate triage — ensure all victims are receiving appropriate medical care based on severity","Request additional EMS resources for mass casualty","Assign officers to accompany critical victims to hospitals for evidence and statements","Request Medical Examiner for the deceased victim"],"E":["Establish a unified command post with all agencies","Designate separate areas: crime scene, witness staging, media, family reunification","Expand the perimeter to encompass all potential evidence areas","Request SWAT/tactical clearance confirmation that no additional threats exist"],"A":["Secure the wounded offender with medical guard — separate from victims","Preserve all offender evidence — clothing, weapon, electronics","Do NOT interrogate the offender until medically cleared and Miranda given","Document offender injuries and weapons for later prosecution"],"C":["Establish a witness registration point — document everyone before they leave","Prioritize witnesses who were closest to the shooter","Assign multiple detectives to conduct simultaneous interviews","Coordinate with FBI Victim Assistance for family reunification"],"T":["Photograph the entire mall scene systematically zone by zone","Secure ALL surveillance footage from mall cameras","Collect body-worn camera footage from all responding officers","Document the offender path and each shooting location"],"I":["Process the offender weapon and all ammunition evidence","Request Evidence Technicians for the entire scene","Collect ballistic evidence from each shooting location","Preserve digital evidence — offender phone, social media, manifesto"],"O":["Contact ASA for multiple felony charges","Coordinate with FBI for federal charges if applicable","Seek search warrants for offender residence, vehicle, digital accounts","Notify COPA if any officer use of force occurred"],"N":["Activate CPD Critical Incident Response","Coordinate media messaging through Office of Communications","Prepare for extended investigation — assign detective teams to each victim","Brief command staff and prepare for press conference"]}}',
            "difficulty": "hard",
            "time_limit": 600,
            "reference": "CPD Active Shooter Response; Mass Casualty Protocol; Multi-Agency Coordination"
        },
        {
            "title": "Narcotics Overdose Death Investigation",
            "content": "You are called to a residence where a 25-year-old male has been found deceased by his roommate. Drug paraphernalia is visible — a syringe, a small bag of white powder, and tin foil. The roommate states the deceased was using heroin and fentanyl. The roommate appears nervous and evasive. Outline your investigative steps in 8-12 bullet points.",
            "answer": '{"modelAnswer":{"R":["Confirm death and note physical indicators (rigor, lividity)","Request Medical Examiner for death investigation","Ensure scene safety — test for airborne fentanyl exposure risk, use PPE"],"E":["Secure the residence as a crime scene","Do NOT assume this is a simple overdose — investigate as potential homicide until ruled otherwise","Protect all drug paraphernalia and evidence in place","Restrict access to the scene"],"A":["Interview the roommate in detail — timeline, who supplied drugs, who was present","Assess whether the roommate may be a suspect (drug-induced homicide)","Advise the roommate of rights if custodial situation develops","Investigate the drug source — potential drug-induced homicide charges under 720 ILCS 5/9-3.3"],"C":["Identify who else was present before and during the incident","Canvass neighbors for additional information","Check deceased phone for recent contacts and messages","Identify the drug supplier through investigation"],"T":["Photograph the scene, body position, drug paraphernalia, all rooms","Document the syringe, powder, foil locations precisely","Secure the deceased phone as evidence","Video record the overall scene"],"I":["Collect all drug paraphernalia for lab testing — fentanyl confirmation","Request Evidence Technicians for processing","Collect the white powder for forensic analysis","Preserve any packaging materials for fingerprints"],"O":["Contact ASA regarding potential drug-induced homicide charges","Request search warrant for deceased phone records","Request toxicology expedite from Medical Examiner","Run LEADS/CLEAR on all involved persons"],"N":["Notify deceased next of kin through proper channels","Coordinate with Narcotics Division for source investigation","Prepare case file for potential prosecution","Monitor Medical Examiner findings for cause and manner of death"]}}',
            "difficulty": "hard",
            "time_limit": 600,
            "reference": "720 ILCS 5/9-3.3; Drug-Induced Homicide; Death Investigation Procedures"
        },
        {
            "title": "Armed Robbery Pattern — Third Incident",
            "content": "This is the third armed robbery in your beat this week with the same MO: male offender, dark hoodie, silver revolver, targeting food delivery drivers at night. Tonight's victim was pistol-whipped and had his phone, cash, and vehicle stolen. The victim is at the hospital with a head laceration. Outline your investigative steps in 8-12 bullet points.",
            "answer": '{"modelAnswer":{"R":["Ensure victim is receiving medical treatment at hospital","Send detective to hospital for victim statement and evidence collection","Photograph victim injuries at hospital","Request victim clothing for trace evidence"],"E":["Broadcast flash message with updated pattern information","Request evidence technicians for the robbery scene","Secure the scene where the robbery and assault occurred","Check for POD cameras and surveillance in the area"],"A":["Alert all patrol units of the escalating pattern — armed and violent","Coordinate with tactical teams for targeted patrol in the beat","Check stolen vehicle through LEADS and LoJack/GPS tracking","Issue BOLO for the stolen vehicle with armed suspect warning"],"C":["Interview victim in detail — exact sequence, weapon details, unique identifiers","Compare this victims description with previous two robbery victims","Canvass for witnesses in the area","Check delivery app records for ride/route data"],"T":["Document this robbery in connection with the pattern — link all three cases","Create a comprehensive pattern analysis with timelines, locations, MO details","Review all available surveillance from all three incidents","Build composite suspect description from all victims"],"I":["Process scene for DNA, fingerprints, shoe impressions","Cross-reference evidence from all three scenes","Request NIBIN if any ballistic evidence from pistol-whipping","Preserve victim phone records for delivery app data"],"O":["Contact ASA for pattern prosecution strategy","Coordinate with Area intelligence for suspect identification","Request search warrant for delivery app records","Consider federal charges if pattern crosses jurisdictions"],"N":["Issue community alert to delivery drivers and delivery companies","Coordinate media release to warn potential targets","Assign dedicated team to pattern investigation","Brief command staff on escalating violence — pistol-whipping is escalation"]}}',
            "difficulty": "hard",
            "time_limit": 600,
            "reference": "CPD Pattern Crime Response; Aggravated Robbery Procedures"
        },
        {
            "title": "Arson Investigation at Occupied Building",
            "content": "CFD has just extinguished a fire at a two-story apartment building. Two residents suffered smoke inhalation. A CFD investigator believes the fire was intentionally set — accelerant odor detected at the rear entry point. One resident tells you she saw a man pour liquid on the back door and light it. She can describe him. Outline your investigative steps in 8-12 bullet points.",
            "answer": '{"modelAnswer":{"R":["Ensure all residents are accounted for and receiving medical attention","Coordinate with CFD for building safety assessment before entry","Document injuries of smoke inhalation victims","Assess if building is structurally safe for investigation"],"E":["Secure the building as a crime scene — no re-entry by residents until processed","Establish perimeter around the building, especially the rear entry point","Broadcast BOLO with suspect description from the eyewitness","Coordinate with CFD Fire Investigation for joint investigation"],"A":["This is attempted murder/aggravated arson — occupied building","Canvass area for suspect immediately — he may be watching","Check surveillance cameras for suspect approach and departure","Run suspect description through databases and intelligence"],"C":["Interview the eyewitness in detail — full description, exact actions observed","Interview all residents about suspicious activity, threats, disputes","Canvas neighborhood for additional witnesses","Check for prior complaints or disputes involving the building"],"T":["Photograph the fire origin point and accelerant pour patterns","Document the rear entry point with measurements","Secure body-worn camera footage","Create detailed timeline from witness accounts and CFD logs"],"I":["Collect accelerant samples from the rear entry for lab analysis","Request Evidence Technicians for the scene","Preserve the point of origin evidence — do NOT contaminate with water","Coordinate with CFD for fire debris collection"],"O":["Contact ASA — Aggravated Arson of occupied building is Class X felony","If suspect identified, seek arrest warrant","Request search warrant for suspect residence and vehicle","Check suspect for prior arson or fire-related offenses"],"N":["Coordinate with Building Department for resident relocation","Connect victims with Red Cross and victim services","Issue community alert if suspect is at large","Prepare joint CFD/CPD investigation report"]}}',
            "difficulty": "hard",
            "time_limit": 600,
            "reference": "720 ILCS 5/20-1.1; Aggravated Arson; Joint CPD/CFD Investigation"
        },
    ]

    # ======== INSERT ALL QUESTIONS ========
    total_inserted = 0

    for q_data in most_appropriate:
        q = {
            "question_id": f"mexam_{uuid.uuid4().hex[:12]}",
            "type": "most_appropriate",
            "category_id": "cat_most_appropriate",
            "category_name": "Most Appropriate",
            "title": q_data["title"],
            "content": q_data["content"],
            "question": q_data["question"],
            "options": q_data["options"],
            "correct_answer": q_data["correct_answer"],
            "explanation": q_data["explanation"],
            "io_scores": q_data["io_scores"],
            "difficulty": q_data["difficulty"],
            "reference": q_data.get("reference", ""),
            "is_premium": True,
            "created_at": now,
            "updated_at": now
        }
        result = await db.questions.update_one(
            {"title": q["title"], "type": q["type"]},
            {"$set": q}, upsert=True
        )
        if result.upserted_id or result.modified_count:
            total_inserted += 1

    for q_data in least_appropriate:
        q = {
            "question_id": f"lexam_{uuid.uuid4().hex[:12]}",
            "type": "least_appropriate",
            "category_id": "cat_least_appropriate",
            "category_name": "Least Appropriate",
            "title": q_data["title"],
            "content": q_data["content"],
            "question": q_data["question"],
            "options": q_data["options"],
            "correct_answer": q_data["correct_answer"],
            "explanation": q_data["explanation"],
            "io_scores": q_data["io_scores"],
            "difficulty": q_data["difficulty"],
            "reference": q_data.get("reference", ""),
            "is_premium": True,
            "created_at": now,
            "updated_at": now
        }
        result = await db.questions.update_one(
            {"title": q["title"], "type": q["type"]},
            {"$set": q}, upsert=True
        )
        if result.upserted_id or result.modified_count:
            total_inserted += 1

    for q_data in legal_trap:
        q = {
            "question_id": f"ltrap_{uuid.uuid4().hex[:12]}",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "category_name": "Legal Trap",
            "title": q_data["title"],
            "content": q_data["content"],
            "question": q_data["question"],
            "options": q_data["options"],
            "correct_answer": q_data["correct_answer"],
            "explanation": q_data["explanation"],
            "io_scores": q_data["io_scores"],
            "difficulty": q_data["difficulty"],
            "reference": q_data.get("reference", ""),
            "is_premium": True,
            "created_at": now,
            "updated_at": now
        }
        result = await db.questions.update_one(
            {"title": q["title"], "type": q["type"]},
            {"$set": q}, upsert=True
        )
        if result.upserted_id or result.modified_count:
            total_inserted += 1

    for q_data in digital_evidence:
        q = {
            "question_id": f"digi_{uuid.uuid4().hex[:12]}",
            "type": "digital_evidence",
            "category_id": "cat_digital_evidence",
            "category_name": "Digital Evidence",
            "title": q_data["title"],
            "content": q_data["content"],
            "question": q_data["question"],
            "options": q_data["options"],
            "correct_answer": q_data["correct_answer"],
            "explanation": q_data["explanation"],
            "io_scores": q_data["io_scores"],
            "difficulty": q_data["difficulty"],
            "reference": q_data.get("reference", ""),
            "is_premium": True,
            "created_at": now,
            "updated_at": now
        }
        result = await db.questions.update_one(
            {"title": q["title"], "type": q["type"]},
            {"$set": q}, upsert=True
        )
        if result.upserted_id or result.modified_count:
            total_inserted += 1

    for q_data in mini_scenarios:
        q = {
            "question_id": f"mini_{uuid.uuid4().hex[:12]}",
            "type": "mini_scenario",
            "category_id": "cat_mini_scenario",
            "category_name": "Mini Scenarios",
            "title": q_data["title"],
            "content": q_data["content"],
            "answer": q_data["answer"],
            "difficulty": q_data["difficulty"],
            "time_limit": q_data.get("time_limit", 600),
            "reference": q_data.get("reference", ""),
            "is_premium": True,
            "created_at": now,
            "updated_at": now
        }
        result = await db.questions.update_one(
            {"title": q["title"], "type": q["type"]},
            {"$set": q}, upsert=True
        )
        if result.upserted_id or result.modified_count:
            total_inserted += 1

    print(f"Seeded {total_inserted} mixed exam questions")
    print(f"  Most Appropriate: {await db.questions.count_documents({'type': 'most_appropriate'})}")
    print(f"  Least Appropriate: {await db.questions.count_documents({'type': 'least_appropriate'})}")
    print(f"  Legal Trap: {await db.questions.count_documents({'type': 'legal_trap'})}")
    print(f"  Digital Evidence: {await db.questions.count_documents({'type': 'digital_evidence'})}")
    print(f"  Mini Scenarios: {await db.questions.count_documents({'type': 'mini_scenario'})}")


if __name__ == "__main__":
    asyncio.run(seed_mixed_exam())
