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


async def seed_ranking_questions():
    """Seed 20 ranking questions based on CPD General Orders and I/O Solutions format.

    Each question presents a scenario and 6 actions (A-F) that must be ranked
    in the correct priority order. Graded using I/O differential weighting:
      Correct position = +2
      Off by 1 = +1
      Off by 2 = 0
      Off by 3 = -1
      Off by 4+ = -2
    """

    # Ensure the ranking category exists
    await db.categories.update_one(
        {"category_id": "cat_ranking"},
        {"$set": {
            "category_id": "cat_ranking",
            "name": "Ranking Questions",
            "description": "Priority-ordering questions graded using I/O Solutions differential weighting. Rank actions in the correct sequence.",
            "order": 20
        }},
        upsert=True
    )

    now = datetime.now(timezone.utc)

    ranking_questions = [
        # 1 - Scene Priority: Shooting with Victim Down
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Shooting with Victim Down — Scene Priority",
            "content": "You are the first detective to arrive at a reported shooting on the 2400 block of S. Michigan Ave. A male victim is lying on the sidewalk with apparent gunshot wounds to the torso. Several bystanders are gathered nearby. Beat officers have just arrived. A witness is yelling that the shooter ran eastbound. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Broadcast a flash message with the offender description and direction of flight"},
                {"label": "B", "text": "Ensure the victim is receiving medical attention and request CFD/EMS"},
                {"label": "C", "text": "Establish an inner perimeter and secure the crime scene with tape"},
                {"label": "D", "text": "Separate and identify all witnesses before they leave"},
                {"label": "E", "text": "Begin collecting shell casings and physical evidence"},
                {"label": "F", "text": "Canvass the area for POD cameras and private surveillance"}
            ],
            "correct_order": [1, 0, 2, 3, 5, 4],
            "explanation": "Life safety (B) is always the top priority — ensure the victim gets medical aid. Next, broadcast the offender description (A) while the information is fresh to aid apprehension. Secure the scene (C) to preserve evidence and control access. Separate witnesses (D) before they contaminate each other's accounts. Canvass for cameras (F) before evidence is overwritten. Evidence collection (E) comes last — after ET/forensics arrive and the scene is properly documented.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD General Order G06-01-01; Special Order S04-04",
            "created_at": now,
            "updated_at": now
        },
        # 2 - Domestic Battery with Child Present
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Domestic Battery with Child Present — Response Priority",
            "content": "You respond to a domestic battery call at a residence. Upon arrival, you find a female victim with visible injuries to her face. A 4-year-old child is crying in the next room. The male offender is still on scene and agitated. Responding officers have not yet secured the offender. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Photograph the victim's injuries and document the scene"},
                {"label": "B", "text": "Ensure officer safety and secure/detain the offender"},
                {"label": "C", "text": "Request EMS for the victim and assess the child's welfare"},
                {"label": "D", "text": "Obtain a detailed statement from the victim"},
                {"label": "E", "text": "Contact DCFS regarding the child's exposure to domestic violence"},
                {"label": "F", "text": "Complete an Illinois Domestic Violence report and seek an Order of Protection"}
            ],
            "correct_order": [1, 2, 0, 3, 4, 5],
            "explanation": "Officer safety and securing the offender (B) is always first when a threat is present. Render aid to the victim and check on the child (C) immediately after. Photograph injuries (A) while they are fresh and visible. Obtain the victim's statement (D) once the scene is safe and calm. Contact DCFS (E) as mandated when a child witnesses domestic violence. Complete reports and seek protective orders (F) as the final administrative step.",
            "difficulty": "medium",
            "is_premium": True,
            "reference": "CPD General Order G06-04; Special Order S04-04-01",
            "created_at": now,
            "updated_at": now
        },
        # 3 - Evidence Handling: Firearm Recovery
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Firearm Recovery at Crime Scene — Evidence Priority",
            "content": "During a homicide investigation, a firearm believed to be the murder weapon is located under a vehicle near the scene. The area is not yet fully secured. Several officers and witnesses are in the vicinity. Rank the following actions in the correct priority order for handling this evidence.",
            "items": [
                {"label": "A", "text": "Pick up the firearm, make it safe, and place it in an evidence bag"},
                {"label": "B", "text": "Secure the immediate area around the firearm and restrict access"},
                {"label": "C", "text": "Photograph the firearm in place with measurement markers from multiple angles"},
                {"label": "D", "text": "Request Evidence Technicians (ET) to process the firearm for prints, DNA, and trace evidence"},
                {"label": "E", "text": "Document the exact location, time of discovery, and who found it in your notes"},
                {"label": "F", "text": "Run the firearm serial number through LEADS/NCIC for stolen status"}
            ],
            "correct_order": [1, 4, 2, 3, 5, 0],
            "explanation": "Secure the area first (B) to prevent contamination or tampering. Document the discovery details (E) while memory is fresh. Photograph in place (C) before anything is moved — this preserves the evidentiary context. Request ET (D) for proper forensic processing. Run the serial number (F) for investigative leads. Never pick up a firearm at a crime scene yourself (A) — ET should handle recovery to preserve forensic evidence.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD General Order G06-01-02; Evidence and Recovered Property",
            "created_at": now,
            "updated_at": now
        },
        # 4 - Witness Management: Multiple Witnesses
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Multiple Witnesses at Aggravated Assault — Management Priority",
            "content": "You arrive at an aggravated assault scene where the victim was stabbed. Three witnesses are present: one who saw the attack, one who heard screaming and came outside, and one who claims to know the offender. The witnesses are talking to each other. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Interview all three witnesses together to get a complete picture quickly"},
                {"label": "B", "text": "Immediately separate all witnesses to prevent cross-contamination of statements"},
                {"label": "C", "text": "Prioritize the eyewitness who saw the attack for the first detailed interview"},
                {"label": "D", "text": "Obtain written statements from each witness individually"},
                {"label": "E", "text": "Ask the witness who knows the offender for identifying information and possible location"},
                {"label": "F", "text": "Release witnesses who did not see the actual attack since their statements are less important"}
            ],
            "correct_order": [1, 2, 4, 3, 0, 5],
            "explanation": "Separate witnesses immediately (B) — this is critical to preserve independent recollections. Interview the eyewitness first (C) as they have the most valuable information. Get offender identification from the witness who knows them (E) to aid apprehension. Obtain written statements from each (D) to lock in their accounts. Never interview witnesses together (A) — it contaminates testimony. Never release witnesses prematurely (F) — all witnesses may have relevant information.",
            "difficulty": "medium",
            "is_premium": True,
            "reference": "CPD General Order G06-01-01; Witness Management Procedures",
            "created_at": now,
            "updated_at": now
        },
        # 5 - Arrest and Interrogation Sequence
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Felony Arrest and Interrogation — Procedural Sequence",
            "content": "You have probable cause to arrest a suspect in an armed robbery. The suspect is located at his residence and agrees to come to the station. You need to conduct a custodial interrogation. Rank the following actions in the correct procedural order.",
            "items": [
                {"label": "A", "text": "Begin questioning the suspect about the robbery details"},
                {"label": "B", "text": "Administer Miranda warnings and obtain a knowing, voluntary waiver"},
                {"label": "C", "text": "Transport the suspect to the Area and place in an interview room"},
                {"label": "D", "text": "Activate the electronic recording equipment before any questioning begins"},
                {"label": "E", "text": "Conduct a thorough pat-down search and inventory personal property"},
                {"label": "F", "text": "Contact the ASA for Felony Review and present the case facts"}
            ],
            "correct_order": [4, 2, 1, 3, 0, 5],
            "explanation": "Pat-down for officer safety (E) must happen before transport. Transport to the Area (C) for a controlled interview environment. Administer Miranda (B) before any custodial interrogation — failure invalidates statements. Activate recording equipment (D) as required by Illinois law (725 ILCS 5/103-2.1) before questioning begins. Only then begin questioning (A). Contact the ASA (F) after you have developed the case through interrogation.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD General Order G06-01-03; 725 ILCS 5/103-2.1",
            "created_at": now,
            "updated_at": now
        },
        # 6 - Digital Evidence Priority
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Digital Evidence Recovery — Priority Order",
            "content": "During a narcotics trafficking investigation, you execute a search warrant at a suspect's apartment. You find a smartphone, a laptop, a tablet, external hard drives, and drug ledger notes. The suspect's phone is unlocked and showing recent messages. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Scroll through the unlocked phone to read messages and photograph the screen"},
                {"label": "B", "text": "Place the phone in airplane mode or a Faraday bag to prevent remote wiping"},
                {"label": "C", "text": "Power off all devices to preserve their current state"},
                {"label": "D", "text": "Photograph all devices in their found locations before moving them"},
                {"label": "E", "text": "Request a digital forensics examiner to conduct proper extraction"},
                {"label": "F", "text": "Begin searching the laptop files for evidence of trafficking"}
            ],
            "correct_order": [1, 3, 4, 0, 2, 5],
            "explanation": "Prevent remote wiping (B) is the most urgent — the phone could be wiped at any moment. Photograph devices in place (D) before moving anything. Request digital forensics (E) for proper chain of custody extraction. If the phone is unlocked, photograph visible evidence (A) as it may lock. Avoid powering off devices unnecessarily (C) — forensic examiners may need the current state. Never search a laptop without forensic tools (F) — you could alter metadata and compromise evidence.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD Special Order S09-06; Digital Evidence Recovery",
            "created_at": now,
            "updated_at": now
        },
        # 7 - Media Response at Major Crime Scene
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Media Response at Homicide Scene — Communication Priority",
            "content": "You are the lead detective at a high-profile homicide scene in a busy commercial area. Multiple media crews have arrived with cameras. Community members are posting on social media. A reporter approaches you directly asking for details. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Provide the reporter with basic confirmed facts to maintain public trust"},
                {"label": "B", "text": "Establish a media staging area outside the crime scene perimeter"},
                {"label": "C", "text": "Notify your supervisor and request CPD Office of Communications be dispatched"},
                {"label": "D", "text": "Decline to comment and refer all media to the Office of Communications"},
                {"label": "E", "text": "Monitor social media posts to identify potential witnesses or evidence"},
                {"label": "F", "text": "Brief the community liaison officer for neighborhood outreach"}
            ],
            "correct_order": [2, 1, 3, 4, 5, 0],
            "explanation": "Notify your supervisor and request Communications (C) immediately — media management is their responsibility. Establish a media staging area (B) to keep press away from the active scene. Decline personal comment and refer to Communications (D) — detectives should not make public statements. Monitor social media (E) as an investigative tool. Brief community liaison (F) for neighborhood relations. Never provide details to reporters directly (A) — even 'basic facts' could compromise the investigation.",
            "difficulty": "medium",
            "is_premium": True,
            "reference": "CPD General Order G09-01; Office of Communications Protocol",
            "created_at": now,
            "updated_at": now
        },
        # 8 - Constitutional Protections Order
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Constitutional Protections During Search — Compliance Order",
            "content": "You receive information that a burglary suspect is inside an apartment with stolen property. You arrive at the location with other officers. The suspect's girlfriend answers the door and says he is inside. You want to enter and search the apartment. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Enter the apartment under exigent circumstances since the suspect may destroy evidence"},
                {"label": "B", "text": "Ask the girlfriend for consent to enter and search, documenting her consent in writing"},
                {"label": "C", "text": "Secure the apartment perimeter to prevent the suspect from leaving or destroying evidence"},
                {"label": "D", "text": "Contact the ASA and apply for a search warrant based on probable cause"},
                {"label": "E", "text": "Order the suspect to come outside and detain him while obtaining a warrant"},
                {"label": "F", "text": "Search incident to arrest after the suspect exits"}
            ],
            "correct_order": [2, 4, 3, 1, 5, 0],
            "explanation": "Secure the perimeter (C) first to prevent flight or destruction while you work within the law. Order the suspect out and detain (E) using lawful authority. Apply for a search warrant (D) — the gold standard for 4th Amendment compliance. Consent search (B) is an alternative but less reliable than a warrant. Search incident to arrest (F) is limited in scope. Entering on exigent circumstances (A) without more is the weakest legal basis and most likely to be challenged.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "4th Amendment; CPD General Order G06-01-03; Illinois v. Gates",
            "created_at": now,
            "updated_at": now
        },
        # 9 - Notification Chain of Command
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Officer-Involved Shooting — Notification Chain",
            "content": "An officer-involved shooting has just occurred on your watch. The offender is down with gunshot wounds and the involved officer is physically uninjured but shaken. EMS is en route. As the first detective supervisor on scene, rank the following notification and response actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Notify COPA (Civilian Office of Police Accountability) of the incident"},
                {"label": "B", "text": "Ensure the involved officer is separated from the scene and not discussing the incident"},
                {"label": "C", "text": "Notify your Area Deputy Chief and the Detective Division Chief"},
                {"label": "D", "text": "Secure the scene and ensure all weapons and evidence are preserved in place"},
                {"label": "E", "text": "Request FOP representation for the involved officer"},
                {"label": "F", "text": "Begin taking statements from the involved officer about what happened"}
            ],
            "correct_order": [3, 1, 2, 0, 4, 5],
            "explanation": "Secure the scene and preserve evidence (D) is the immediate priority. Separate the involved officer (B) to preserve their independent account — do not let them discuss it with others. Notify the chain of command (C) immediately as required. Notify COPA (A) as mandated by law for all officer-involved shootings. Request FOP representation (E) before any formal interview. Never take statements from the involved officer immediately (F) — they have the right to representation and COPA conducts the formal investigation.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD General Order G03-06; Special Order S08-01; COPA Notification Requirements",
            "created_at": now,
            "updated_at": now
        },
        # 10 - Use of Force Response Priority
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Subject Resisting Arrest — Use of Force Response",
            "content": "You and your partner are attempting to arrest a suspect wanted for aggravated battery. The suspect begins actively resisting — pushing officers away and attempting to flee. He is unarmed but significantly larger than both officers. Rank the following response actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Deploy your Taser to gain compliance"},
                {"label": "B", "text": "Issue clear verbal commands to stop resisting and comply"},
                {"label": "C", "text": "Request backup units to assist with the arrest"},
                {"label": "D", "text": "Use control techniques and joint locks to gain physical control"},
                {"label": "E", "text": "Document the use of force in a Tactical Response Report (TRR)"},
                {"label": "F", "text": "Use OC spray to disorient the subject"}
            ],
            "correct_order": [1, 2, 3, 0, 5, 4],
            "explanation": "Verbal commands (B) must always be attempted first — this is the lowest level of force. Request backup (C) to achieve numerical advantage, which often resolves resistance without force. Control techniques (D) are appropriate for active resistance before escalating to weapons. Taser deployment (A) is justified for active resistance but only after lesser means are considered. OC spray (F) is an alternative less-lethal option. Document everything (E) in a TRR as the final required step after the incident is resolved.",
            "difficulty": "medium",
            "is_premium": True,
            "reference": "CPD General Order G03-02; Use of Force Model",
            "created_at": now,
            "updated_at": now
        },
        # 11 - Crime Scene Processing Order
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Burglary Scene Processing — Systematic Order",
            "content": "You are assigned to investigate a commercial burglary at a jewelry store. The front glass door was shattered for entry. Display cases are broken. The alarm company reports the alarm triggered at 0300 hours. The store owner has arrived. Rank the following scene processing actions in the correct order.",
            "items": [
                {"label": "A", "text": "Allow the store owner to walk through and identify what was taken"},
                {"label": "B", "text": "Conduct a walk-through to assess the scene and develop a processing plan"},
                {"label": "C", "text": "Request Evidence Technicians to process for fingerprints, DNA, and tool marks"},
                {"label": "D", "text": "Photograph the overall scene, points of entry, and damaged areas before anything is touched"},
                {"label": "E", "text": "Collect glass fragments, tool mark evidence, and any items left by the offender"},
                {"label": "F", "text": "Review alarm company records and request surveillance footage from the store and neighbors"}
            ],
            "correct_order": [1, 3, 2, 5, 4, 0],
            "explanation": "Walk-through assessment (B) first to understand the scope without disturbing evidence. Photograph everything (D) before any processing begins. Request ET (C) for professional forensic work. Review alarm records and surveillance (F) for timeline and suspect identification. Collect physical evidence (E) only after documentation and ET processing. Never let the owner walk through (A) before processing — they will contaminate the scene.",
            "difficulty": "medium",
            "is_premium": True,
            "reference": "CPD General Order G06-01-01; Crime Scene Processing",
            "created_at": now,
            "updated_at": now
        },
        # 12 - Missing Child Response
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Missing Child Report — Response Priority",
            "content": "A frantic mother reports her 6-year-old daughter has been missing for approximately 2 hours from a public park. The child was last seen near the playground. Other parents at the park report seeing an unfamiliar man talking to children earlier. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Broadcast an emergency BOLO with the child's description, photo, and last known location"},
                {"label": "B", "text": "Conduct a thorough search of the park, surrounding buildings, and nearby vehicles"},
                {"label": "C", "text": "Interview the mother for detailed physical description, clothing, and recent photos"},
                {"label": "D", "text": "Canvass for surveillance cameras in the park and surrounding businesses"},
                {"label": "E", "text": "Issue an AMBER Alert through the state notification system"},
                {"label": "F", "text": "Interview other parents about the unfamiliar man and obtain his description"}
            ],
            "correct_order": [2, 0, 1, 5, 3, 4],
            "explanation": "Get the child's description from the mother (C) first — you need this information to broadcast effectively. Issue the BOLO immediately (A) with that description. Conduct a thorough local search (B) as the child may be nearby. Interview witnesses about the suspicious man (F) for potential suspect information. Canvass for surveillance (D) to track movements. AMBER Alert (E) has specific criteria that must be met and requires supervisor approval — it's not the first step.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD Special Order S06-01-01; Missing/Abducted Children Procedures",
            "created_at": now,
            "updated_at": now
        },
        # 13 - Death Investigation Initial Response
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Unattended Death Investigation — Initial Response",
            "content": "You are called to an apartment where a 72-year-old man has been found deceased by his neighbor. The neighbor used a spare key to enter when newspapers piled up. The body is in the bedroom. There are no obvious signs of trauma. Prescription medications are on the nightstand. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Contact the Medical Examiner's office to respond and make the official death determination"},
                {"label": "B", "text": "Confirm the individual is deceased and note obvious signs (rigor, lividity, temperature)"},
                {"label": "C", "text": "Secure the apartment and treat it as a potential crime scene until ruled otherwise"},
                {"label": "D", "text": "Interview the neighbor about the deceased's health, last contact, and any suspicious circumstances"},
                {"label": "E", "text": "Photograph the scene, body position, medications, and surroundings"},
                {"label": "F", "text": "Search the apartment for identification, next-of-kin information, and a will or DNR"}
            ],
            "correct_order": [1, 2, 4, 3, 0, 5],
            "explanation": "Confirm death (B) and note physical indicators — this is always first. Secure the scene (C) and treat as potential crime scene until manner of death is determined. Photograph everything (E) before the scene is disturbed. Interview the neighbor (D) for background and circumstances. Contact the Medical Examiner (A) for official determination and body removal. Search for identification/NOK (F) only after the scene is documented and in coordination with ME.",
            "difficulty": "medium",
            "is_premium": True,
            "reference": "CPD General Order G06-01-01; Death Investigation Procedures",
            "created_at": now,
            "updated_at": now
        },
        # 14 - Traffic Fatality Investigation
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Fatal Hit-and-Run — Investigation Priority",
            "content": "A pedestrian has been struck and killed by a vehicle that fled the scene. The incident occurred at a busy intersection during evening rush hour. Several motorists stopped. Debris and vehicle parts are scattered across the roadway. Traffic is backed up in all directions. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Collect vehicle debris and parts for identification of the suspect vehicle make/model"},
                {"label": "B", "text": "Close the intersection and establish traffic rerouting with assistance from traffic control"},
                {"label": "C", "text": "Broadcast a flash message with available suspect vehicle description and direction of travel"},
                {"label": "D", "text": "Identify and separate witnesses before they leave the congested area"},
                {"label": "E", "text": "Request the Major Accident Investigation Unit (MAIU) to respond"},
                {"label": "F", "text": "Document the scene with measurements, photographs, and skid mark analysis"}
            ],
            "correct_order": [2, 1, 3, 4, 5, 0],
            "explanation": "Broadcast the suspect vehicle description (C) immediately — every second counts in a hit-and-run. Close the intersection (B) to preserve the scene and prevent additional accidents. Identify and separate witnesses (D) before they drive away in traffic. Request MAIU (E) as they are the specialized unit for fatal traffic investigations. Document the scene thoroughly (F) with their guidance. Collect debris (A) last, as part of the systematic evidence processing by MAIU.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD General Order G06-03; Traffic Crash Investigation",
            "created_at": now,
            "updated_at": now
        },
        # 15 - Sexual Assault Response Priority
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Sexual Assault Report — Response Priority",
            "content": "A 24-year-old female walks into the district station and reports she was sexually assaulted approximately 3 hours ago at a party. She is visibly distressed, has torn clothing, and has not showered. She can identify the offender by name. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Transport the victim to a hospital for a forensic sexual assault evidence kit (SAFE exam)"},
                {"label": "B", "text": "Obtain a detailed written statement from the victim about the assault"},
                {"label": "C", "text": "Assign a same-gender officer if possible, provide privacy, and ensure the victim's immediate comfort"},
                {"label": "D", "text": "Send officers to the party location to secure it as a crime scene"},
                {"label": "E", "text": "Contact SVU (Special Victims Unit) to assign the case"},
                {"label": "F", "text": "Locate and arrest the named offender as soon as possible"}
            ],
            "correct_order": [2, 0, 4, 3, 1, 5],
            "explanation": "Victim comfort and dignity (C) comes first — a trauma-informed approach is essential. Transport for SAFE exam (A) immediately — evidence degrades rapidly and the victim has not showered. Contact SVU (E) as they are the specialized unit for sexual assault cases. Secure the party location (D) to preserve physical evidence. Obtain a detailed statement (B) only when the victim is ready, ideally with SVU guidance. Locating the offender (F) is important but not at the expense of evidence collection and victim care.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD Special Order S04-03; Sexual Assault Response Protocol",
            "created_at": now,
            "updated_at": now
        },
        # 16 - Gang-Related Shooting Investigation
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Gang-Related Shooting — Investigation Priority",
            "content": "A drive-by shooting occurs in a known gang territory. Two male victims are wounded and transported to the hospital. Multiple shell casings are in the street. Residents are present but reluctant to speak with police. A vehicle matching the suspect description was spotted by a POD camera two blocks away. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Pull POD camera footage and attempt to identify the suspect vehicle and occupants"},
                {"label": "B", "text": "Secure the scene and document all shell casing locations before collection"},
                {"label": "C", "text": "Send detectives to the hospital to interview victims and collect clothing as evidence"},
                {"label": "D", "text": "Conduct a canvass with bilingual officers and community mediators to encourage cooperation"},
                {"label": "E", "text": "Run NIBIN (ballistic comparison) on recovered casings to link to other shootings"},
                {"label": "F", "text": "Check gang intelligence databases for recent conflicts and potential suspects"}
            ],
            "correct_order": [1, 2, 0, 5, 3, 4],
            "explanation": "Secure the scene and document evidence (B) is the foundation. Send detectives to the hospital (C) to get victim statements while they're willing and collect clothing with possible GSR/DNA. Pull POD footage (A) while it's still available — some systems overwrite quickly. Check gang intelligence (F) to develop suspect leads and understand the motive. Community canvass (D) using culturally competent approaches to overcome reluctance. NIBIN comparison (E) is valuable but takes longer to process.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD Special Order S09-05; Gang Investigation Procedures",
            "created_at": now,
            "updated_at": now
        },
        # 17 - Robbery Pattern Response
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Commercial Robbery Pattern — Strategic Response",
            "content": "Intelligence analysis reveals a pattern of armed robberies targeting convenience stores in your Area over the past two weeks. Six robberies have occurred with a similar MO: lone male offender, black ski mask, silver handgun, striking between 2200-0100 hours. You are tasked with developing the response. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Deploy plainclothes surveillance teams near likely target stores during the pattern hours"},
                {"label": "B", "text": "Analyze all six cases for commonalities, routes of approach/escape, and geographic patterns"},
                {"label": "C", "text": "Distribute a community alert to convenience store owners with the offender description and safety tips"},
                {"label": "D", "text": "Request additional patrol units for high-visibility presence in the target area"},
                {"label": "E", "text": "Review surveillance footage from all six locations to develop a composite description"},
                {"label": "F", "text": "Cross-reference the MO with parolees and known robbery offenders in the area"}
            ],
            "correct_order": [1, 4, 5, 2, 0, 3],
            "explanation": "Analyze all cases first (B) to identify true patterns and predict the next target. Review surveillance from all locations (E) to build the best possible suspect description. Cross-reference with known offenders (F) to develop suspect leads. Distribute community alerts (C) to help potential targets protect themselves. Deploy surveillance teams (A) based on pattern analysis. Request additional patrol (D) for general deterrence, but this is less targeted than the above measures.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD Special Order S09-01; Pattern Crime Response",
            "created_at": now,
            "updated_at": now
        },
        # 18 - Narcotics Search Warrant Execution
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Narcotics Search Warrant Execution — Procedural Order",
            "content": "You have obtained a search warrant for an apartment suspected of being a drug stash location. Intelligence suggests the occupant may be armed. The tactical team is ready for entry. Rank the following actions in the correct procedural order.",
            "items": [
                {"label": "A", "text": "Begin a systematic search of the apartment, documenting every room and item found"},
                {"label": "B", "text": "Announce police presence, serve the warrant, and make tactical entry"},
                {"label": "C", "text": "Conduct a pre-raid briefing covering layout, roles, suspect information, and contingencies"},
                {"label": "D", "text": "Secure all occupants, pat-down for weapons, and move them to a controlled area"},
                {"label": "E", "text": "Inventory and photograph all narcotics, currency, weapons, and other evidence in place"},
                {"label": "F", "text": "Complete the search warrant return, listing all seized items, and file with the court"}
            ],
            "correct_order": [2, 1, 3, 4, 0, 5],
            "explanation": "Pre-raid briefing (C) is essential — every team member must know the plan before entry. Announce and make entry (B) per the knock-and-announce requirement. Secure all occupants (D) immediately for officer safety. Inventory and photograph evidence in place (E) before moving anything. Systematic search (A) following documentation protocols. Complete the warrant return (F) as the final legal requirement — all items must be filed with the court.",
            "difficulty": "medium",
            "is_premium": True,
            "reference": "CPD Special Order S09-03; Search Warrant Procedures",
            "created_at": now,
            "updated_at": now
        },
        # 19 - Juvenile Offender Processing
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Juvenile Offender Arrest — Processing Priority",
            "content": "A 15-year-old is arrested for aggravated battery after a fight at school where the victim suffered a broken jaw. The juvenile is cooperative but his parents have not yet been contacted. The school principal wants to give a statement. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Question the juvenile about the incident to get his version of events"},
                {"label": "B", "text": "Contact the juvenile's parents or legal guardian and inform them of the arrest"},
                {"label": "C", "text": "Interview the school principal and obtain witness statements from other students"},
                {"label": "D", "text": "Complete station adjustments and determine whether to refer to juvenile court"},
                {"label": "E", "text": "Transport the juvenile to the Youth Investigation section for processing"},
                {"label": "F", "text": "Photograph the victim's injuries and obtain a medical report from the hospital"}
            ],
            "correct_order": [1, 4, 5, 2, 0, 3],
            "explanation": "Contact parents (B) immediately — this is legally required for juveniles before any processing. Transport to Youth Investigation (E) for proper juvenile processing. Document the victim's injuries (F) as this is critical evidence for the aggravated battery charge. Interview the principal and witnesses (C) while events are fresh. Any questioning of the juvenile (A) requires parental/guardian presence for minors. Station adjustment determination (D) comes after the full investigation is complete.",
            "difficulty": "medium",
            "is_premium": True,
            "reference": "CPD Special Order S07-01; Juvenile Arrest Procedures; 705 ILCS 405/5-405",
            "created_at": now,
            "updated_at": now
        },
        # 20 - Multi-Vehicle Accident with Hazmat
        {
            "question_id": f"rank_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": "Multi-Vehicle Crash with Hazmat Spill — Response Priority",
            "content": "A multi-vehicle accident on the expressway involves a commercial tanker truck that is leaking an unknown chemical. Multiple motorists are injured. Traffic is completely stopped. You are the first CPD unit on scene. The chemical odor is strong and some motorists are complaining of difficulty breathing. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Begin directing traffic around the accident scene to relieve congestion"},
                {"label": "B", "text": "Establish an upwind perimeter at a safe distance from the chemical spill"},
                {"label": "C", "text": "Request CFD Hazmat team, multiple EMS units, and OEMC notification"},
                {"label": "D", "text": "Attempt to identify the chemical using the tanker's placard or shipping documents"},
                {"label": "E", "text": "Begin evacuating motorists from vehicles nearest to the spill to a safe staging area"},
                {"label": "F", "text": "Render first aid to injured motorists trapped in their vehicles near the tanker"}
            ],
            "correct_order": [2, 1, 4, 3, 0, 5],
            "explanation": "Request Hazmat and EMS (C) immediately — you need specialized resources for an unknown chemical. Establish an upwind perimeter (B) to protect yourself and others from fumes. Evacuate motorists away from the spill (E) — move people to safety before treating. Attempt to identify the chemical (D) using placards or the ERG guide to inform responders. Direct traffic (A) only after life safety is addressed. Do NOT enter the hazmat zone to render first aid (F) without proper protective equipment — you could become a casualty.",
            "difficulty": "hard",
            "is_premium": True,
            "reference": "CPD General Order G05-02; Hazardous Materials Response; Emergency Response Guidebook",
            "created_at": now,
            "updated_at": now
        },
    ]

    # Insert all questions
    inserted = 0
    for q in ranking_questions:
        result = await db.questions.update_one(
            {"title": q["title"], "type": "ranking"},
            {"$set": q},
            upsert=True
        )
        if result.upserted_id or result.modified_count:
            inserted += 1

    print(f"Seeded {inserted} ranking questions in 'cat_ranking' category")
    print(f"Total ranking questions in DB: {await db.questions.count_documents({'type': 'ranking'})}")


if __name__ == "__main__":
    asyncio.run(seed_ranking_questions())
