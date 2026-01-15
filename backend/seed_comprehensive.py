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

async def clear_existing_data():
    """Clear existing questions and categories for fresh seed"""
    await db.questions.delete_many({})
    await db.categories.delete_many({})
    print("✓ Cleared existing data")

async def seed_categories():
    """Create categories for organizing questions"""
    categories = [
        {
            "category_id": "cat_general_orders",
            "name": "General Orders",
            "description": "Chicago PD General Orders and permanent policies",
            "order": 1
        },
        {
            "category_id": "cat_special_orders",
            "name": "Special Orders",
            "description": "Temporary modifications and clarifications",
            "order": 2
        },
        {
            "category_id": "cat_criminal_law",
            "name": "Illinois Criminal Law",
            "description": "Illinois Compiled Statutes - Criminal Offenses",
            "order": 3
        },
        {
            "category_id": "cat_procedures",
            "name": "Investigative Procedures",
            "description": "Detective procedures and protocols",
            "order": 4
        },
        {
            "category_id": "cat_evidence",
            "name": "Evidence Handling",
            "description": "Collection, preservation, and chain of custody",
            "order": 5
        },
        {
            "category_id": "cat_constitutional",
            "name": "Constitutional Law",
            "description": "4th, 5th, 6th Amendment rights and case law",
            "order": 6
        },
        {
            "category_id": "cat_interviews",
            "name": "Interviews & Interrogations",
            "description": "Witness and suspect interview techniques",
            "order": 7
        },
        {
            "category_id": "cat_reports",
            "name": "Reports & Documentation",
            "description": "Case reports, supplements, and documentation",
            "order": 8
        }
    ]
    
    for cat in categories:
        await db.categories.update_one(
            {"category_id": cat["category_id"]},
            {"$set": cat},
            upsert=True
        )
    print(f"✓ Seeded {len(categories)} categories")
    return categories

async def seed_flashcards():
    """Create comprehensive flashcard questions"""
    
    flashcards = [
        # ==================== GENERAL ORDERS (25 cards) ====================
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Use of Force - G03-02",
            "content": "According to CPD General Order G03-02, when is deadly force authorized?",
            "answer": "Deadly force is authorized when objectively reasonable and necessary to: (1) prevent death or great bodily harm to the officer or another person, or (2) prevent a forcible felony that threatens death/great bodily harm.",
            "explanation": "Officers must consider totality of circumstances. De-escalation required when safe and feasible. Based on Graham v. Connor and Tennessee v. Garner standards.",
            "difficulty": "medium",
            "reference": "General Order G03-02: Use of Force"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Force Options Model",
            "content": "What are the levels in CPD's Force Options Model from lowest to highest?",
            "answer": "1) Member presence, 2) Verbal direction/control, 3) Holding/restraint techniques, 4) Stunning, 5) Chemical agents, 6) Canine, 7) Taser, 8) Impact weapons, 9) Deadly force",
            "explanation": "Officers should use the minimum force necessary. The model is not a ladder - officers may enter at any level based on threat assessment.",
            "difficulty": "hard",
            "reference": "General Order G03-02-01: Force Options"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Duty to Intervene",
            "content": "What is a CPD member's duty to intervene according to G03-02?",
            "answer": "Members who observe another member using force that is clearly beyond what is objectively reasonable must intervene to prevent the use of unreasonable force if it is safe to do so.",
            "explanation": "Failure to intervene can result in discipline. Members must also report observed misconduct through proper channels.",
            "difficulty": "medium",
            "reference": "General Order G03-02: Use of Force"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Foot Pursuit Policy",
            "content": "What factors must an officer consider before initiating a foot pursuit?",
            "answer": "Consider: (1) Seriousness of offense, (2) Whether suspect is armed, (3) Risk to public safety, (4) Officer's physical condition, (5) Environmental hazards, (6) Availability of backup, (7) Whether suspect can be apprehended later.",
            "explanation": "Officers should not pursue if risks outweigh benefits. Must notify dispatcher immediately when pursuit begins.",
            "difficulty": "medium",
            "reference": "General Order G03-02-02: Foot Pursuits"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Vehicle Pursuit Policy",
            "content": "When may a CPD officer initiate a vehicle pursuit?",
            "answer": "Only when: (1) Officer has probable cause to believe occupant committed forcible felony, OR (2) Occupant poses immediate threat of death/great bodily harm to public. Traffic violations alone do NOT justify pursuit.",
            "explanation": "Supervisor must be notified immediately. Pursuit must be terminated if risks to public outweigh need for apprehension.",
            "difficulty": "hard",
            "reference": "General Order G03-03: Vehicle Pursuits"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Taser Deployment Restrictions",
            "content": "When is Taser deployment prohibited under CPD policy?",
            "answer": "Prohibited when: (1) Subject is handcuffed (unless extreme circumstances), (2) Subject is fleeing non-violent misdemeanor, (3) Near flammable substances, (4) Subject is in elevated position where fall could cause injury, (5) On subjects in water.",
            "explanation": "Multiple Taser cycles require justification. Medical attention required after deployment.",
            "difficulty": "hard",
            "reference": "General Order G03-02-04: Taser Use"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Body-Worn Camera Activation",
            "content": "When must a CPD officer activate their body-worn camera?",
            "answer": "Must activate for: (1) All law enforcement activities, (2) All investigative encounters, (3) Traffic stops, (4) Arrests, (5) Use of force, (6) Searches, (7) Statements from victims/witnesses, (8) Vehicle pursuits.",
            "explanation": "Camera should remain on until event concludes. Failure to activate may result in discipline and adverse inference in court.",
            "difficulty": "easy",
            "reference": "Special Order S03-14: Body-Worn Cameras"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Miranda Trigger",
            "content": "At what point must Miranda warnings be given?",
            "answer": "Miranda warnings must be given before custodial interrogation - when a person is (1) in custody (not free to leave) AND (2) being subjected to interrogation or its functional equivalent by law enforcement.",
            "explanation": "Both elements required. Voluntary statements without questioning don't require Miranda. Public safety exception allows limited questioning.",
            "difficulty": "medium",
            "reference": "General Order G06-01-02: Interviews and Interrogations"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Search Incident to Arrest",
            "content": "What is the scope of a search incident to arrest?",
            "answer": "Officers may search: (1) The arrestee's person, (2) Area within arrestee's immediate control (wingspan), (3) Vehicle passenger compartment if arrestee is unsecured and within reaching distance, or if reasonable to believe evidence of arrest crime is present.",
            "explanation": "Based on Chimel v. California and Arizona v. Gant. Purpose is officer safety and evidence preservation.",
            "difficulty": "medium",
            "reference": "General Order G06-01-03: Search and Seizure"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Terry Stop Requirements",
            "content": "What is required for a valid Terry stop (investigative detention)?",
            "answer": "Requires reasonable articulable suspicion that criminal activity is afoot. Officer must be able to point to specific, objective facts that justify the stop. Mere hunches or profiles are insufficient.",
            "explanation": "Terry v. Ohio (1968). Stop must be brief and limited in scope. Pat-down allowed only if reasonable belief subject is armed and dangerous.",
            "difficulty": "medium",
            "reference": "General Order G06-01: Field Interviews"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Protective Sweep",
            "content": "When can officers conduct a protective sweep of a residence?",
            "answer": "During arrest in home, officers may: (1) Look in closets and spaces immediately adjoining arrest location where attack could occur, (2) Conduct cursory sweep of entire premises if articulable facts support belief that dangerous individuals may be present.",
            "explanation": "Maryland v. Buie (1990). Limited to places where person could hide. Plain view doctrine applies to evidence observed.",
            "difficulty": "hard",
            "reference": "General Order G06-01-03: Search and Seizure"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Consent Search Requirements",
            "content": "What are the requirements for a valid consent search?",
            "answer": "Consent must be: (1) Voluntary - not coerced, (2) Given by person with authority over area, (3) Knowing - person aware they can refuse. Scope limited to what consent covers. Can be revoked at any time.",
            "explanation": "Document consent on Consent to Search form when possible. Third party can consent to common areas.",
            "difficulty": "medium",
            "reference": "General Order G06-01-03: Search and Seizure"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Inventory Search of Vehicle",
            "content": "What are the requirements for a valid inventory search of a vehicle?",
            "answer": "Must be: (1) Pursuant to department policy, (2) Conducted in good faith, (3) Not a pretext for investigation. Complete inventory form. All containers may be opened. Purpose is to protect owner's property, protect police from claims, and protect police from danger.",
            "explanation": "Colorado v. Bertine. Must follow standardized procedures. Cannot be used as excuse to search for evidence.",
            "difficulty": "medium",
            "reference": "General Order G06-01-05: Vehicle Inventory"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Plain View Doctrine",
            "content": "What are the requirements for a valid plain view seizure?",
            "answer": "Three requirements: (1) Officer lawfully present in location, (2) Item in plain view, (3) Incriminating nature of item immediately apparent. Officer cannot move objects to get better view.",
            "explanation": "Horton v. California. Discovery does not need to be inadvertent. Officer must have lawful right to access the item.",
            "difficulty": "medium",
            "reference": "General Order G06-01-03: Search and Seizure"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Exigent Circumstances",
            "content": "What circumstances allow warrantless entry into a home?",
            "answer": "Exigent circumstances include: (1) Hot pursuit of fleeing felon, (2) Imminent destruction of evidence, (3) Need to prevent suspect escape, (4) Risk of danger to police or others (emergency aid). Must have probable cause plus exigency.",
            "explanation": "Kentucky v. King - police cannot create exigency through unconstitutional conduct. Document circumstances thoroughly.",
            "difficulty": "hard",
            "reference": "General Order G06-01-03: Search and Seizure"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Strip Search Authority",
            "content": "When may a strip search be conducted under CPD policy?",
            "answer": "Only when: (1) Person arrested for felony or weapons offense, (2) Supervisor approves, (3) Reasonable belief person is concealing weapons, drugs, or evidence, (4) Same-sex officer conducts search, (5) Conducted in private.",
            "explanation": "Body cavity searches require search warrant. Document approval and circumstances. Ensure dignity of subject.",
            "difficulty": "hard",
            "reference": "General Order G06-01-06: Strip Searches"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Juvenile Processing",
            "content": "What are the time limits for processing a juvenile in custody?",
            "answer": "Juvenile must be: (1) Brought before juvenile court within 40 hours (excluding weekends/holidays), (2) Station adjustment or referral decision made within 6 hours of arrival at station. Parents must be notified immediately.",
            "explanation": "Juveniles have heightened protections. Cannot be housed with adults. Special interrogation rules apply under 705 ILCS 405.",
            "difficulty": "hard",
            "reference": "General Order G06-02: Juveniles"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Domestic Violence Response",
            "content": "What is mandatory when responding to domestic violence calls?",
            "answer": "Officers must: (1) Arrest if probable cause exists for DV battery, (2) Complete case report even if no arrest, (3) Provide victim with rights pamphlet, (4) Offer transportation to safe location, (5) Advise of protective order process, (6) Document all injuries with photos.",
            "explanation": "Illinois has mandatory arrest policy when probable cause exists. Dual arrests should be avoided - identify primary aggressor.",
            "difficulty": "medium",
            "reference": "General Order G04-04: Domestic Violence"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Crime Scene Protection",
            "content": "What are the first responding officer's duties at a crime scene?",
            "answer": "Officer must: (1) Render aid to injured, (2) Secure and protect scene, (3) Establish perimeter, (4) Start crime scene log, (5) Identify and separate witnesses, (6) Brief arriving detectives, (7) Remain until relieved.",
            "explanation": "First officer has critical role in preserving evidence. Note conditions, positions, and any changes made. Protect against weather and contamination.",
            "difficulty": "easy",
            "reference": "General Order G05-02: Crime Scene Protection"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Death Investigation Response",
            "content": "Who must be notified for a death investigation?",
            "answer": "Notify: (1) Detective Division, (2) Medical Examiner, (3) Crime lab if applicable, (4) Supervising sergeant, (5) Watch commander for unnatural deaths. Do not move body without ME authorization unless necessary for life-saving.",
            "explanation": "All unattended deaths require investigation. Medical examiner determines cause and manner of death. Preserve scene as potential homicide until determined otherwise.",
            "difficulty": "medium",
            "reference": "General Order G05-03: Death Investigations"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Sexual Assault Response",
            "content": "What are the critical steps when responding to a sexual assault?",
            "answer": "(1) Treat victim with sensitivity, (2) Secure crime scene, (3) Advise victim not to wash/change clothes, (4) Request SVU detective, (5) Arrange SANE exam, (6) Provide victim advocate information, (7) Preserve all physical evidence.",
            "explanation": "Victim-centered approach is critical. Never express doubt about victim's account. Evidence kit examination within 7 days preferred.",
            "difficulty": "medium",
            "reference": "Special Order S04-06: Sexual Assault Response"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Missing Persons Report",
            "content": "When must CPD accept a missing persons report?",
            "answer": "Must accept immediately - no waiting period required. High-risk missing: (1) Under 13, (2) Over 60, (3) Mental/physical disability, (4) Danger to self/others, (5) Unusual circumstances. AMBER Alert criteria for child abductions.",
            "explanation": "No jurisdictional restrictions - accept report regardless of where person was last seen. Enter into LEADS/NCIC immediately for high-risk.",
            "difficulty": "easy",
            "reference": "General Order G04-01: Missing Persons"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Off-Duty Action",
            "content": "What are the guidelines for off-duty police action?",
            "answer": "Off-duty officers should: (1) Be good witness and call 911, (2) Only take action for serious felonies when on-duty response is inadequate, (3) Identify self as police, (4) Not engage in vehicle pursuits, (5) Not carry weapon while consuming alcohol.",
            "explanation": "Safety first - wait for on-duty officers when possible. Must immediately notify on-duty officers of actions taken.",
            "difficulty": "medium",
            "reference": "General Order G03-01: Off-Duty Action"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Firearm Discharge Reporting",
            "content": "What must occur after any firearm discharge by an officer?",
            "answer": "(1) Notify supervisor immediately, (2) Render first aid, (3) Request medical assistance, (4) Protect scene, (5) Separate officers involved, (6) Complete TRR within 24 hours, (7) COPA notification for any shots at person, (8) Officer may have PBA/FOP rep present.",
            "explanation": "COPA investigates all officer-involved shootings. Officer has right to 24-hour review period before formal statement if requested.",
            "difficulty": "medium",
            "reference": "General Order G03-06: Firearm Discharge Incidents"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Report Writing Timeliness",
            "content": "What are the time requirements for completing case reports?",
            "answer": "Original case report: End of tour. Arrest report: Before end of tour. Progress reports: 10 days. Supplementary reports: 10 days. Administrative reports: Varies by type. Extension requires supervisor approval.",
            "explanation": "Timely reporting ensures accuracy and aids prosecution. Late reports should explain delay. All reports are legal documents.",
            "difficulty": "easy",
            "reference": "General Order G07-01: Case Reporting"
        },
        
        # ==================== ILLINOIS CRIMINAL LAW (35 cards) ====================
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Murder - First Degree",
            "content": "What are the elements of First Degree Murder in Illinois?",
            "answer": "A person commits first degree murder when: (1) Without lawful justification, kills an individual AND (2) Either intends to kill or do great bodily harm, OR knows acts create strong probability of death/GBH, OR is committing a forcible felony.",
            "explanation": "Class M felony. Sentence: 20-60 years, natural life for certain aggravating factors. Felony murder requires forcible felony.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/9-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Murder - Second Degree",
            "content": "What distinguishes Second Degree Murder from First Degree Murder?",
            "answer": "Second Degree Murder is First Degree Murder committed: (1) Under sudden and intense passion from serious provocation, OR (2) Under unreasonable belief that circumstances justified killing (imperfect self-defense).",
            "explanation": "Class 1 felony, 4-20 years. Defendant has burden to prove mitigating factors. Cannot be charged directly - it's a lesser included offense.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/9-2"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Involuntary Manslaughter",
            "content": "What are the elements of Involuntary Manslaughter?",
            "answer": "A person commits involuntary manslaughter when: (1) Unintentionally kills without lawful justification, AND (2) Acts are likely to cause death/GBH AND are performed recklessly, OR during commission of unlawful act.",
            "explanation": "Class 3 felony, 2-5 years. Recklessness requires conscious disregard of substantial risk. Distinguished from reckless homicide (vehicle related).",
            "difficulty": "medium",
            "reference": "720 ILCS 5/9-3"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Aggravated Battery",
            "content": "What elevates Battery to Aggravated Battery?",
            "answer": "Battery becomes aggravated when: (1) Great bodily harm/permanent disability, (2) Victim is protected person (police, teacher, elderly, disabled), (3) Use of deadly weapon, (4) On public property, (5) In certain locations (school, church).",
            "explanation": "Class 3 felony minimum, can be Class X with firearm. Multiple aggravating factors possible. Protected persons include correctional officers, firefighters.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/12-3.05"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Assault vs. Battery",
            "content": "What is the difference between Assault and Battery in Illinois?",
            "answer": "ASSAULT: Conduct placing another in reasonable apprehension of receiving a battery (no contact required). BATTERY: Causes bodily harm OR makes physical contact of insulting/provoking nature. Assault is the threat; Battery is the contact.",
            "explanation": "Simple assault is Class C misdemeanor. Simple battery is Class A misdemeanor. Both can be aggravated based on circumstances.",
            "difficulty": "easy",
            "reference": "720 ILCS 5/12-1, 5/12-3"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Robbery Elements",
            "content": "What are the elements of Robbery in Illinois?",
            "answer": "Robbery requires: (1) Knowingly taking property, (2) From the person or presence of another, (3) By use of force or by threatening imminent use of force. The force/threat distinguishes robbery from theft.",
            "explanation": "Class 2 felony, 3-7 years. Force must be to accomplish taking, not just to escape. Presence means victim's awareness.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/18-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Armed Robbery",
            "content": "What makes a robbery 'Armed Robbery'?",
            "answer": "Armed robbery occurs when during robbery, offender: (1) Carries or is armed with dangerous weapon, (2) Indicates verbally or by actions possession of weapon, OR (3) Discharges a firearm. Even a fake weapon qualifies if victim reasonably believes it's real.",
            "explanation": "Class X felony, 6-30 years (21-45 with firearm, 25-life if discharged). No probation eligible.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/18-2"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Burglary Elements",
            "content": "What are the elements of Burglary in Illinois?",
            "answer": "Burglary requires: (1) Without authority, (2) Knowingly entering or remaining in a building/vehicle/watercraft/aircraft, (3) With intent to commit a felony or theft therein. Intent must exist at time of entry.",
            "explanation": "Class 2 felony. Residential burglary is Class 1 (4-15 years). Actual completion of theft/felony not required.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/19-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Home Invasion",
            "content": "What distinguishes Home Invasion from Residential Burglary?",
            "answer": "Home Invasion requires: (1) Without authority enters dwelling, (2) Knows or has reason to know someone is present, AND (3) Uses or threatens force, OR is armed, OR intentionally injures someone. The human presence element is key.",
            "explanation": "Class X felony, 6-30 years. With firearm: 15-30 years. One of the most serious property crimes.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/19-6"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Theft Classifications",
            "content": "What are the theft classifications based on value in Illinois?",
            "answer": "Under $500: Class A misdemeanor. $500-$10,000: Class 3 felony. $10,000-$100,000: Class 2 felony. $100,000-$500,000: Class 1 felony. Over $500,000: Class X felony. Theft from person is Class 3 regardless of value.",
            "explanation": "Value can be aggregated for single scheme. Prior theft convictions can enhance classification. Retail theft has separate provisions.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/16-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Criminal Sexual Assault",
            "content": "What are the elements of Criminal Sexual Assault?",
            "answer": "CSA occurs when accused: (1) Commits act of sexual penetration, AND (2) Uses force/threat of force, OR knows victim cannot understand nature of act, OR knows victim cannot give knowing consent, OR victim is family member under 18.",
            "explanation": "Class 1 felony, 4-15 years. Aggravated CSA is Class X. No corroboration required. Consent is an affirmative defense.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/11-1.20"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Kidnapping Elements",
            "content": "What are the elements of Kidnapping in Illinois?",
            "answer": "Kidnapping requires: (1) Knowingly and secretly confining a person against their will, OR (2) By deceit/enticement inducing person to go from one place to another with intent to secretly confine. Must be without consent.",
            "explanation": "Class 2 felony. Aggravated kidnapping (with ransom, weapon, or GBH) is Class X. Child abduction has separate statute.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/10-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Unlawful Restraint",
            "content": "How does Unlawful Restraint differ from Kidnapping?",
            "answer": "Unlawful Restraint: Knowingly without legal authority detains another. Key difference: No secret confinement or movement required. Aggravated Unlawful Restraint: Using a deadly weapon.",
            "explanation": "Simple unlawful restraint is Class 4 felony. Aggravated is Class 3. Lesser included offense of kidnapping.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/10-3"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "UUW - Unlawful Use of Weapon",
            "content": "What constitutes Unlawful Use of Weapon (UUW)?",
            "answer": "UUW includes: (1) Carrying concealed firearm without valid CCL, (2) Carrying in prohibited location (school, government building), (3) Possession by felon, (4) Firearm with altered serial number, (5) Carrying while under influence.",
            "explanation": "Classifications vary: Class A misdemeanor to Class X felony. AUUW (Aggravated) includes prior convictions, body armor, or extended magazine.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/24-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Armed Habitual Criminal",
            "content": "What is Armed Habitual Criminal?",
            "answer": "Occurs when person possesses firearm after being convicted of 2+ qualifying felonies (murder, CSA, robbery, burglary, aggravated DUI causing death, etc.). Possession of firearm is the triggering offense.",
            "explanation": "Class X felony, 6-30 years, no probation. One of the most serious weapons charges. Prior convictions must be separate incidents.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/24-1.7"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Arson Elements",
            "content": "What are the elements of Arson?",
            "answer": "Arson: By means of fire or explosive, knowingly damages: (1) Real property of another without consent, OR (2) Any property with intent to defraud insurer, OR (3) Any property knowing persons are present.",
            "explanation": "Class 2 felony. Aggravated arson (injury to person/firefighter or property over $100K) is Class X. Residential arson is Class 1.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/20-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Criminal Damage to Property",
            "content": "What are the elements of Criminal Damage to Property?",
            "answer": "Knowingly damages property of another without consent by: (1) Using fire/explosive, (2) Tampering with property so as to endanger life, (3) Interfering with public utility, (4) Damaging property exceeding certain values.",
            "explanation": "Classification based on damage amount and type. Under $500: Class A misdemeanor. Over $10,000: Class 3 felony. Government property has enhanced penalties.",
            "difficulty": "easy",
            "reference": "720 ILCS 5/21-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Criminal Trespass to Land",
            "content": "When does entry on property become Criminal Trespass?",
            "answer": "Occurs when person: (1) Enters or remains on land after receiving notice that entry is forbidden, OR (2) Remains on land after being notified to depart. Notice can be verbal, written, or by posting/fencing.",
            "explanation": "Class B misdemeanor. Enhanced to Class A near school. Criminal trespass to residence is Class 4 felony.",
            "difficulty": "easy",
            "reference": "720 ILCS 5/21-3"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "DUI Per Se Limits",
            "content": "What are the per se BAC limits for DUI in Illinois?",
            "answer": "Adult drivers: 0.08 BAC. Commercial vehicle: 0.04 BAC. Drivers under 21: 0.00 BAC (zero tolerance). School bus driver: 0.00 BAC. Also illegal to drive with any amount of illegal drug in system.",
            "explanation": "Class A misdemeanor (1st/2nd offense). Aggravated DUI with death is Class 2 felony. Refusal to test results in automatic license suspension.",
            "difficulty": "easy",
            "reference": "625 ILCS 5/11-501"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Aggravated DUI",
            "content": "What factors make a DUI 'Aggravated DUI'?",
            "answer": "DUI becomes aggravated when: (1) Third or subsequent offense, (2) No valid license, (3) In school zone, (4) Caused accident with injury, (5) Child under 16 in vehicle, (6) Driving school bus with passengers.",
            "explanation": "Ranges from Class 4 felony to Class X for death. Mandatory prison for 4th+ offense. DUI causing death is minimum Class 4 felony.",
            "difficulty": "medium",
            "reference": "625 ILCS 5/11-501(d)"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Controlled Substance Act",
            "content": "What determines the classification of drug possession charges?",
            "answer": "Classification based on: (1) Drug schedule (I-V), (2) Amount possessed, (3) Intent (personal use vs. delivery), (4) Location (school zone enhancement), (5) Prior convictions. Schedule I includes heroin, LSD, ecstasy.",
            "explanation": "Cannabis has separate statute since legalization. Possession with intent has higher penalties than simple possession. Delivery to minor is enhanced.",
            "difficulty": "medium",
            "reference": "720 ILCS 570/Controlled Substances Act"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Possession with Intent",
            "content": "What factors indicate Possession with Intent to Deliver?",
            "answer": "Indicators include: (1) Quantity exceeding personal use, (2) Packaging materials, (3) Scales/measuring devices, (4) Large amounts of cash, (5) Multiple cellphones, (6) Customer lists, (7) Statements by defendant, (8) Location/patterns.",
            "explanation": "Intent can be proven circumstantially. Amount thresholds vary by drug type. Expert testimony often used to establish dealing indicators.",
            "difficulty": "medium",
            "reference": "720 ILCS 570/401"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "FOID Card Requirements",
            "content": "Who may NOT possess a FOID card in Illinois?",
            "answer": "Prohibited: (1) Convicted felon, (2) Adjudicated mentally disabled, (3) Under order of protection, (4) Convicted of misdemeanor DV, (5) Under 21 without guardian consent, (6) Drug addict, (7) Intellectually disabled.",
            "explanation": "FOID required to possess firearms/ammunition in Illinois. Valid for 10 years. ISP administers program. Violations are Class A misdemeanor minimum.",
            "difficulty": "medium",
            "reference": "430 ILCS 65/FOID Card Act"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Order of Protection Violations",
            "content": "What constitutes Violation of Order of Protection?",
            "answer": "Violation occurs when: (1) Person has been served with/has knowledge of OP, AND (2) Commits act prohibited by order (contact, proximity, harassment, removal of child, entering residence). First violation: Class A misdemeanor.",
            "explanation": "Second violation or with prior DV conviction is Class 4 felony. Mandatory arrest when probable cause exists. No bond until court hearing.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/12-3.4"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Stalking Elements",
            "content": "What are the elements of Stalking in Illinois?",
            "answer": "Stalking requires: (1) On at least 2 separate occasions, (2) Knowingly follows/monitors/surveils/threatens person, AND (3) Transmits threat OR places person in reasonable apprehension of bodily harm, confinement, or restraint.",
            "explanation": "Class 4 felony. Aggravated stalking (with weapon, violation of OP, or prior conviction) is Class 3. Cyberstalking is separate offense.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/12-7.3"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Disorderly Conduct",
            "content": "What constitutes Disorderly Conduct?",
            "answer": "A person commits disorderly conduct when they knowingly: (1) Do an act in unreasonable manner to alarm/disturb another and provoke breach of peace, (2) Make false 911 call, (3) File false police report, (4) Make bomb threat.",
            "explanation": "Class C misdemeanor for general DC. False police report is Class 4 felony. False 911 call can be Class 3 felony.",
            "difficulty": "easy",
            "reference": "720 ILCS 5/26-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Mob Action",
            "content": "What constitutes Mob Action in Illinois?",
            "answer": "Mob Action: (1) Use of force by 2+ persons acting together to compel action, OR (2) Assembly of 2+ to do unlawful act, OR (3) Assembly of 2+ without authority of law to do violence to person/property.",
            "explanation": "Class C misdemeanor general, Class 4 felony if using force, Class 3 if causes injury. Does not require actual violence if assembly has violent purpose.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/25-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Resisting/Obstructing",
            "content": "What are the elements of Resisting or Obstructing a Peace Officer?",
            "answer": "Occurs when person knowingly: (1) Resists or obstructs performance of authorized act, (2) By peace officer, firefighter, or correctional employee. Must be performing official duties. Physical resistance not required - fleeing sufficient.",
            "explanation": "Class A misdemeanor. Aggravated (injury to officer) is Class 4 felony. Officer must be acting lawfully. Verbal objection alone insufficient.",
            "difficulty": "easy",
            "reference": "720 ILCS 5/31-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Identity Theft",
            "content": "What are the elements of Identity Theft?",
            "answer": "Occurs when person knowingly uses another's personal identifying information or document to: (1) Fraudulently obtain credit/property/services, (2) Commit any felony. Includes social security numbers, financial account numbers, passwords.",
            "explanation": "Class 3 felony ($300+), Class 2 if elderly victim or prior conviction. Aggravated identity theft is Class 1 or X based on amount.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/16-30"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Attempt",
            "content": "What are the elements of Criminal Attempt?",
            "answer": "Attempt requires: (1) Intent to commit specific offense, AND (2) Substantial step toward commission beyond mere preparation. Impossibility is not a defense if crime would have occurred but for circumstances unknown to defendant.",
            "explanation": "Sentenced one class lower than target offense (attempted murder is still Class X). Must identify specific target crime.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/8-4"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Conspiracy",
            "content": "What are the elements of Conspiracy?",
            "answer": "Conspiracy requires: (1) Agreement between 2+ persons, (2) Intent that offense be committed, (3) An act in furtherance of agreement by any party. Cannot conspire with undercover officer alone (must be 2+ actual conspirators).",
            "explanation": "Same class as target offense. Each conspirator liable for acts of others in furtherance. Withdrawal possible before completion.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/8-2"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Accountability",
            "content": "When is a person legally accountable for another's conduct?",
            "answer": "Person is accountable when: (1) Before or during offense, (2) With intent to promote or facilitate commission, (3) Solicits, aids, abets, agrees to aid, or attempts to aid. Mere presence at scene is insufficient.",
            "explanation": "Accountable person is chargeable with same offense as principal. Must have knowledge and intent. Flight after crime can show accountability.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/5-2"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Self-Defense",
            "content": "When is use of force justified in self-defense?",
            "answer": "Self-defense justified when person: (1) Reasonably believes force is necessary, (2) To defend against imminent unlawful force, (3) Force used is proportional to threat. Duty to retreat may apply (not in one's dwelling). Cannot be initial aggressor.",
            "explanation": "Deadly force only to prevent death/GBH or forcible felony. Castle doctrine allows defense of home without retreat. Defense applies to defense of others too.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/7-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Affirmative Defenses",
            "content": "What are common affirmative defenses in Illinois?",
            "answer": "Affirmative defenses include: (1) Self-defense/Defense of others, (2) Insanity, (3) Duress, (4) Entrapment, (5) Necessity, (6) Intoxication (specific intent crimes only), (7) Compulsion. Defendant has burden of production.",
            "explanation": "Once raised, prosecution must disprove beyond reasonable doubt. Insanity requires mental disease such that defendant didn't appreciate criminality.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/6, 5/7"
        },
        
        # ==================== EVIDENCE HANDLING (15 cards) ====================
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Chain of Custody",
            "content": "What are the essential elements of maintaining chain of custody?",
            "answer": "Must document: (1) Who collected evidence, (2) Date/time/location of collection, (3) Every person who handled item, (4) Date/time of each transfer, (5) Storage conditions, (6) Any changes to item's condition. Unbroken chain from scene to court.",
            "explanation": "Any gap can result in evidence being excluded. Use evidence bags with tamper-evident seals. Minimize handlers.",
            "difficulty": "medium",
            "reference": "General Order G05-02: Evidence and Property"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "DNA Evidence Collection",
            "content": "What are the proper procedures for collecting DNA evidence?",
            "answer": "Procedures: (1) Wear fresh gloves for each sample, (2) Use sterile swabs, (3) Allow samples to air dry before packaging, (4) Package in paper (not plastic), (5) Avoid contamination from own DNA, (6) Maintain temperature control. Never package wet evidence.",
            "explanation": "DNA can degrade rapidly if not properly handled. Reference samples needed from victim and suspects for comparison. Submit to crime lab ASAP.",
            "difficulty": "hard",
            "reference": "Crime Lab Evidence Submission Guide"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Fingerprint Evidence",
            "content": "What are the types of fingerprint evidence and how are they collected?",
            "answer": "Types: (1) Patent - visible prints in blood/ink (photograph), (2) Latent - invisible prints (powder/chemical processing), (3) Plastic - 3D impressions (photograph/cast). Collection depends on surface: porous vs. non-porous materials require different techniques.",
            "explanation": "Latent prints most common. Document location before collection. Superglue fuming for non-porous surfaces. AFIS for comparison searches.",
            "difficulty": "medium",
            "reference": "Crime Lab Evidence Submission Guide"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Firearm Evidence Handling",
            "content": "What are the safety and collection procedures for firearm evidence?",
            "answer": "Safety first: (1) Point in safe direction, (2) Check if loaded with chamber, (3) Make safe without destroying evidence, (4) Do NOT fire test or insert objects in barrel. Documentation: Serial numbers, make/model, loaded status. Package separately from ammo.",
            "explanation": "Ballistics can match bullet to weapon. Document position at scene. Preserve fired cartridge cases. Submit for NIBIN entry.",
            "difficulty": "medium",
            "reference": "Crime Lab Evidence Submission Guide"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Digital Evidence",
            "content": "What are the key principles for handling digital evidence?",
            "answer": "Principles: (1) Don't turn on if off, don't turn off if on, (2) Photograph screen state, (3) Document all connections, (4) Use write-blockers for imaging, (5) Hash values for integrity, (6) Maintain isolation from networks. Prevent any changes to data.",
            "explanation": "Volatile data (RAM) can be lost if powered off. Cell phones should be placed in Faraday bag. Get search warrant for content.",
            "difficulty": "hard",
            "reference": "Special Order S06-06: Digital Evidence"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Blood Evidence",
            "content": "How should blood evidence be collected and preserved?",
            "answer": "Wet blood: Absorb on sterile swab, air dry completely, package in paper. Dry blood: Scrape into paper bindle, or cut out stained material. Liquid blood: Collect in purple-top tube (EDTA). Never use plastic bags - promotes bacterial growth.",
            "explanation": "Blood spatter patterns should be photographed before collection. Reference standards needed from known individuals. Refrigerate liquid samples.",
            "difficulty": "medium",
            "reference": "Crime Lab Evidence Submission Guide"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Trace Evidence",
            "content": "What is trace evidence and how is it collected?",
            "answer": "Trace evidence: Hair, fibers, glass, soil, paint, gunshot residue. Collection: (1) Pick with forceps, (2) Tape lifting, (3) Vacuuming with filtered vacuum. Package each sample separately. Document exact location of recovery.",
            "explanation": "Locard's Exchange Principle: Every contact leaves a trace. Hair can provide DNA (if root attached). GSR on hands degrades after ~6 hours.",
            "difficulty": "medium",
            "reference": "Crime Lab Evidence Submission Guide"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Evidence Packaging",
            "content": "What are the proper packaging methods for different evidence types?",
            "answer": "Paper bags: Biologicals, drugs. Plastic bags: Dry non-biological items. Paper bindles: Trace evidence, powders. Evidence cans: Arson samples. Rigid containers: Fragile items. General rule: Paper for biologicals, seal all openings, label completely.",
            "explanation": "Packaging protects evidence from contamination and degradation. Include case number, item number, date, collector's name on each package.",
            "difficulty": "easy",
            "reference": "General Order G05-02: Evidence and Property"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Search Warrant Execution",
            "content": "What are the time and manner restrictions for executing search warrants?",
            "answer": "Illinois requirements: (1) Execute within 96 hours of issuance, (2) Generally between 6am-10pm unless nighttime authorized, (3) Knock and announce presence unless no-knock authorized, (4) Use reasonable force to enter if denied. Return warrant within 48 hours.",
            "explanation": "Nighttime warrants require showing evidence destruction likely or officer safety concern. No-knock requires specific articulable danger.",
            "difficulty": "medium",
            "reference": "725 ILCS 5/108-8"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Crime Scene Photography",
            "content": "What are the essential photographs at a crime scene?",
            "answer": "Required shots: (1) Overall/establishing shots, (2) Mid-range showing relationship of evidence to scene, (3) Close-ups with and without scale, (4) Evidence in place before collection, (5) All points of entry/exit. Take from multiple angles. Include identifiers.",
            "explanation": "Photographs are most important documentation. Use proper lighting. Video can supplement but not replace still photos. Log all shots taken.",
            "difficulty": "easy",
            "reference": "General Order G05-02: Crime Scene Processing"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Crime Scene Sketching",
            "content": "What should be included in a crime scene sketch?",
            "answer": "Include: (1) Case identifiers, (2) Direction of north, (3) Scale used, (4) Legend explaining symbols, (5) Accurate measurements to fixed reference points, (6) Location of evidence, (7) Bodies/victims, (8) Furniture/obstacles, (9) Sketcher's name/date.",
            "explanation": "Rough sketch done at scene, final sketch prepared later. Triangulation or baseline methods for measurements. Software like SketchUp can be used for final.",
            "difficulty": "medium",
            "reference": "General Order G05-02: Crime Scene Processing"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Vehicle Evidence",
            "content": "What procedures apply to processing a vehicle as evidence?",
            "answer": "Procedures: (1) Impound and secure, (2) Obtain warrant before search (unless exception applies), (3) Document VIN, plates, damage, (4) Process exterior before interior, (5) Note and preserve anything in plain view. Inventory forms required.",
            "explanation": "Carroll doctrine allows warrantless search with PC due to mobility. Impounded vehicles require inventory search per policy.",
            "difficulty": "medium",
            "reference": "General Order G05-02: Vehicle Evidence"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Drug Evidence Field Testing",
            "content": "What are the requirements for field testing suspected drugs?",
            "answer": "Requirements: (1) Use NIK or approved presumptive test kit, (2) Follow kit instructions exactly, (3) Document color change reaction, (4) Field test is presumptive only - lab confirmation required, (5) Weigh evidence for charging purposes.",
            "explanation": "False positives possible with field tests. Lab analysis required for court. Always retain sample for defense testing. Document total quantity and packaging.",
            "difficulty": "easy",
            "reference": "General Order G05-02: Drug Evidence"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Sexual Assault Kit",
            "content": "What are the critical procedures for sexual assault evidence kits?",
            "answer": "Procedures: (1) SANE nurse collects kit at hospital, (2) Kit must be submitted to crime lab within 10 days, (3) Chain of custody documented continuously, (4) Keep refrigerated if delay, (5) Victim clothing collected separately. Illinois Rape Kit Tracking System tracks all kits.",
            "explanation": "Victim has right to have kit collected regardless of prosecution decision. Backlog elimination mandate in Illinois. DNA profile entered in CODIS.",
            "difficulty": "medium",
            "reference": "725 ILCS 202/Sexual Assault Evidence Submission Act"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Evidence Inventory Requirements",
            "content": "What documentation is required for evidence inventory at CPD?",
            "answer": "Required: (1) Inventory Sheet with complete item descriptions, (2) Property Case Report, (3) Evidence technician worksheet if processed, (4) Lab submission forms if applicable, (5) Owner information for recovered property. Use evidence tracking system.",
            "explanation": "All evidence must be inventoried before end of tour. Currency counted by two officers. Narcotics require supervisor verification of weight.",
            "difficulty": "easy",
            "reference": "General Order G05-02: Evidence and Property Management"
        },
        
        # ==================== INTERVIEWS & INTERROGATIONS (15 cards) ====================
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Interview vs. Interrogation",
            "content": "What is the difference between an interview and an interrogation?",
            "answer": "INTERVIEW: Non-accusatory, information gathering from witnesses/victims, rapport-based, open-ended questions. INTERROGATION: Accusatory, questioning suspect believed to be involved, designed to elicit admission/confession. Miranda required for custodial interrogation.",
            "explanation": "Interview can transition to interrogation if reasonable suspicion develops. Document when transition occurs. Consider voluntariness throughout.",
            "difficulty": "easy",
            "reference": "General Order G06-01-02: Interviews"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Cognitive Interview",
            "content": "What are the components of the Cognitive Interview technique?",
            "answer": "Four techniques: (1) Mental reinstatement - recreate context/emotions, (2) Report everything - even partial/seemingly irrelevant info, (3) Recall from different perspectives, (4) Recall in different orders. Non-leading, open-ended questions throughout.",
            "explanation": "Research shows 25-35% more accurate information than standard interview. Best for cooperative witnesses. Requires uninterrupted narrative.",
            "difficulty": "medium",
            "reference": "Detective Training: Cognitive Interview"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Reid Technique",
            "content": "What are the phases of the Reid interrogation technique?",
            "answer": "Two phases: (1) Behavior Analysis Interview (BAI) - structured interview to assess veracity, (2) Nine Steps of Interrogation - positive confrontation, theme development, handling denials, overcoming objections, keeping attention, passive mood, alternatives, bringing into conversation, converting admission to written confession.",
            "explanation": "Controversial technique - risk of false confessions. CPD emphasizes ethical approach and voluntary confessions. Document entire process.",
            "difficulty": "hard",
            "reference": "Detective Training: Interrogation"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Confession Voluntariness",
            "content": "What factors determine if a confession is voluntary?",
            "answer": "Courts consider: (1) Duration of interrogation, (2) Whether suspect was given food/water/breaks, (3) Physical or psychological coercion, (4) Suspect's age/education/mental state, (5) Whether Miranda given, (6) Promises or threats made, (7) Deception used.",
            "explanation": "Totality of circumstances test. Even true confessions can be suppressed if involuntary. Document everything to prove voluntariness.",
            "difficulty": "hard",
            "reference": "General Order G06-01-02: Interrogations"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Juvenile Interrogation Rules",
            "content": "What special rules apply when interrogating juveniles?",
            "answer": "Illinois requirements: (1) Parent/guardian notified immediately, (2) Youth have right to counsel before questioning, (3) Miranda in age-appropriate language, (4) Electronic recording required, (5) Simplified waiver determination. Under 15: presumption of inadmissibility without attorney present.",
            "explanation": "J.D.B. v. North Carolina - age must be considered in custody determination. Greater scrutiny on voluntariness. Limit duration.",
            "difficulty": "hard",
            "reference": "705 ILCS 405/5-401.5"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Electronic Recording",
            "content": "When must interrogations be electronically recorded in Illinois?",
            "answer": "Recording required for: (1) Homicide cases, (2) Sexual assault, (3) Predatory criminal sexual assault of child, (4) Aggravated arson. Must record entire interrogation in its entirety. Failure may render statement inadmissible.",
            "explanation": "720 ILCS 5/103-2.1. Recording must include Miranda, waiver, and all questioning. Video preferred over audio only.",
            "difficulty": "medium",
            "reference": "725 ILCS 5/103-2.1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Miranda Invocation",
            "content": "What must occur when a suspect invokes Miranda rights?",
            "answer": "If RIGHT TO SILENCE invoked: Questioning must cease. Can re-approach after significant time if fresh warnings given. If RIGHT TO COUNSEL invoked: All questioning must cease until attorney present. Cannot reinitiate - must wait for suspect to reinitiate.",
            "explanation": "Edwards v. Arizona - counsel invocation is stronger protection. Invocation must be unambiguous. 'Maybe I should get a lawyer' is not clear invocation (Davis v. U.S.).",
            "difficulty": "hard",
            "reference": "General Order G06-01-02: Miranda"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Public Safety Exception",
            "content": "When does the public safety exception to Miranda apply?",
            "answer": "Applies when: (1) Immediate threat to public safety, (2) Questions reasonably prompted by safety concern (e.g., 'Where's the gun?'). Limited to addressing imminent danger. Normal Miranda rules apply once threat neutralized.",
            "explanation": "New York v. Quarles. Exception is narrow - must be genuine emergency. Document circumstances justifying exception. Statements may still be challenged.",
            "difficulty": "hard",
            "reference": "General Order G06-01-02: Miranda Exceptions"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Witness Statement Documentation",
            "content": "What are best practices for documenting witness statements?",
            "answer": "Best practices: (1) Use witness's own words, (2) Include date/time/location, (3) Have witness read and sign, (4) Note any corrections made by witness, (5) Document demeanor observations, (6) Record if possible with consent, (7) Note who was present.",
            "explanation": "Witness statements may be used to refresh memory at trial or impeach contradictory testimony. Preserve original notes even after report written.",
            "difficulty": "easy",
            "reference": "General Order G06-01-01: Witness Statements"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Rapport Building",
            "content": "What are effective rapport building techniques for interviews?",
            "answer": "Techniques: (1) Use person's name, (2) Find common ground, (3) Active listening, (4) Open body language, (5) Appropriate eye contact, (6) Express empathy, (7) Non-judgmental tone, (8) Let them tell their story. Build trust before asking difficult questions.",
            "explanation": "Good rapport increases cooperation and information quality. Mirror body language subtly. Avoid interrogation-style from start.",
            "difficulty": "easy",
            "reference": "Detective Training: Interview Techniques"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Leading Questions",
            "content": "When should leading questions be avoided in interviews?",
            "answer": "Avoid leading questions when: (1) Gathering initial narrative, (2) With child witnesses, (3) Witness is suggestible, (4) Establishing facts for first time. Leading acceptable for: (1) Clarifying specific details, (2) Testing consistency, (3) Confronting with evidence.",
            "explanation": "Leading questions suggest the answer. Can contaminate witness memory. Defense will challenge at trial. Open-ended questions produce more reliable information.",
            "difficulty": "medium",
            "reference": "Detective Training: Interview Techniques"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Child Witness Interviews",
            "content": "What special considerations apply when interviewing child witnesses?",
            "answer": "Considerations: (1) Use age-appropriate language, (2) Avoid leading questions, (3) Establish understanding of truth vs. lie, (4) Use open-ended questions, (5) Allow support person if needed, (6) Keep interview short, (7) Minimize number of interviews, (8) Record interview.",
            "explanation": "Child Advocacy Centers preferred setting. Forensic interviewers are specially trained. Child's memory is more susceptible to suggestion.",
            "difficulty": "medium",
            "reference": "Special Order S04-06: Child Victims"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Eyewitness Identification Factors",
            "content": "What factors affect reliability of eyewitness identification?",
            "answer": "System variables (controllable): Lineup composition, instructions, administrator blindness, recording confidence. Estimator variables (uncontrollable): Lighting, distance, duration of exposure, stress level, weapon focus, cross-race identification.",
            "explanation": "Eyewitness misidentification is leading cause of wrongful convictions. Document all factors present. Use double-blind lineup procedures.",
            "difficulty": "medium",
            "reference": "General Order G03-06: Eyewitness Identification"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Lineup Procedures",
            "content": "What are the CPD requirements for conducting lineups?",
            "answer": "Requirements: (1) Blind or blinded administration, (2) 6+ fillers of similar appearance, (3) Pre-lineup instructions (may not be present), (4) One suspect per lineup, (5) Record witness confidence at time of ID, (6) Document entire procedure, (7) Video record when possible.",
            "explanation": "Sequential presentation reduces misidentification. Fillers must match witness description. Same procedures for photo and live lineups.",
            "difficulty": "medium",
            "reference": "General Order G03-06: Eyewitness Identification"
        },
        {
            "type": "flashcard",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "title": "Interpreter Requirements",
            "content": "When must an interpreter be used in interviews?",
            "answer": "Interpreter required when: (1) Witness/suspect not proficient in English, (2) Hearing impaired individual, (3) Limited English proficiency. Use certified interpreters when available. Document language barriers. Avoid using family members as interpreters.",
            "explanation": "Due process requires understanding of rights and questions. ASL interpreter for deaf individuals. Document qualifications of interpreter used.",
            "difficulty": "easy",
            "reference": "General Order G06-01: Interpreter Services"
        },
        
        # ==================== REPORTS & DOCUMENTATION (10 cards) ====================
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "Case Report Requirements",
            "content": "What essential elements must be included in every case report?",
            "answer": "Elements: (1) Date/time/location of incident, (2) Victim/witness/offender information, (3) Narrative describing what happened (who, what, when, where, why, how), (4) Evidence collected, (5) Actions taken, (6) Disposition/status. Must be factual, objective, and complete.",
            "explanation": "Reports are legal documents used in court. Write in first person, past tense. Avoid opinions unless expert. Spell check and proofread.",
            "difficulty": "easy",
            "reference": "General Order G07-01: Case Reporting"
        },
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "Arrest Report Elements",
            "content": "What must be documented in an arrest report?",
            "answer": "Must include: (1) Probable cause for arrest, (2) All charges with statute citations, (3) How arrestee was located, (4) Arresting officers, (5) Miranda if given, (6) Statements made, (7) Property inventory, (8) Bond information, (9) Processing station, (10) Court date.",
            "explanation": "Arrest report must establish probable cause for each charge. ASA may use to approve charges. Defense will scrutinize for inconsistencies.",
            "difficulty": "medium",
            "reference": "General Order G07-01: Arrest Reports"
        },
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "TRR - Tactical Response Report",
            "content": "When is a Tactical Response Report required?",
            "answer": "TRR required when: (1) Member uses force (any level above presence/verbal), (2) Force used against member, (3) Firearm discharged (including accidental), (4) Taser deployed, (5) OC spray used, (6) Impact weapon used. Must be completed within 24 hours.",
            "explanation": "TRR documents force used and justification. Subject to COPA/BIA review. Multiple officers may need to complete if multiple involved. Supervisory review required.",
            "difficulty": "medium",
            "reference": "General Order G03-02-02: Response Reports"
        },
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "Supplementary Reports",
            "content": "When should supplementary reports be completed?",
            "answer": "Supplements required for: (1) Follow-up investigation results, (2) Additional witness statements, (3) Evidence submissions, (4) Lab results received, (5) Case status changes, (6) Additional offender information, (7) Arrest information. Due within 10 days of activity.",
            "explanation": "Each supplement should be complete standing alone. Reference original report. Use for significant developments, not minor updates.",
            "difficulty": "easy",
            "reference": "General Order G07-01: Supplementary Reports"
        },
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "ISR - Investigative Stop Report",
            "content": "What must be documented on an Investigative Stop Report?",
            "answer": "Required: (1) Reason for stop (articulable suspicion), (2) Location/date/time, (3) Subject demographics, (4) Whether frisk conducted and basis, (5) Results of stop, (6) Duration, (7) Whether enforcement action taken. Contact receipt given to subject.",
            "explanation": "ISR required for Terry stops. ACLU consent decree requires enhanced documentation. Subject has right to receipt with officer info.",
            "difficulty": "medium",
            "reference": "Special Order S04-13-09: Investigative Stop Reports"
        },
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "Court Documentation",
            "content": "What documentation should be prepared for court testimony?",
            "answer": "Prepare: (1) Original reports and supplements, (2) Evidence inventory sheets, (3) Lab reports, (4) Photographs, (5) Video evidence, (6) Personal notes (may be discoverable), (7) Witness lists. Review all materials before testimony. Organize chronologically.",
            "explanation": "Reports can be used to refresh memory on stand. Defense entitled to any notes used. Retain all notes as evidence. Coordinate with ASA pre-trial.",
            "difficulty": "medium",
            "reference": "General Order G07-03: Court Preparation"
        },
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "Narrative Writing",
            "content": "What are the principles of effective report narrative writing?",
            "answer": "Principles: (1) Chronological order, (2) First person active voice, (3) Objective facts (not opinions), (4) Specific details (exact words, measurements), (5) Clear and concise sentences, (6) Proper grammar/spelling, (7) Include all relevant information, (8) Explain police terminology.",
            "explanation": "Reports are read by ASAs, judges, juries, defense. Avoid jargon. Quote statements exactly. Re-read for clarity before submission.",
            "difficulty": "easy",
            "reference": "Detective Training: Report Writing"
        },
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "Vehicle Crash Reports",
            "content": "When is an official crash report required?",
            "answer": "Report required when: (1) Injury or death, (2) Property damage over $1,500, (3) Hit and run, (4) DUI involved, (5) Hazardous materials involved, (6) Commercial vehicle involved, (7) City vehicle involved. SR-1 form for reportable crashes.",
            "explanation": "Minor property damage (under $1,500) may only need exchange of information. Document scene thoroughly. Interview all parties/witnesses.",
            "difficulty": "easy",
            "reference": "General Order G04-02: Traffic Crash Reporting"
        },
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "Evidence Documentation",
            "content": "What information must be recorded when documenting evidence?",
            "answer": "Document: (1) Item description, (2) Exact location found, (3) Date/time of recovery, (4) Who recovered it, (5) Condition when found, (6) Unique identifying marks/serial numbers, (7) Photographs taken, (8) Inventory number assigned, (9) Lab submissions.",
            "explanation": "Complete evidence documentation supports chain of custody. Be specific - 'on floor' vs 'on bedroom floor, 3 feet from north wall'. Use evidence markers.",
            "difficulty": "medium",
            "reference": "General Order G05-02: Evidence Documentation"
        },
        {
            "type": "flashcard",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "title": "Detective Case File",
            "content": "What components should be in a complete detective case file?",
            "answer": "Components: (1) Case report and supplements, (2) All witness statements, (3) Evidence inventory, (4) Lab reports, (5) Photos/videos, (6) Canvass results, (7) Telephone records, (8) Surveillance results, (9) Criminal histories, (10) Court documents, (11) Correspondence, (12) Detective notes.",
            "explanation": "Organized file aids prosecution and case review. Keep original documents, copy for prosecutor. Index major items. Prepare case summary.",
            "difficulty": "medium",
            "reference": "General Order G07-01: Detective Case Management"
        }
    ]
    
    now = datetime.now(timezone.utc)
    count = 0
    
    for q in flashcards:
        q["question_id"] = f"fc_{uuid.uuid4().hex[:12]}"
        q["created_at"] = now
        q["updated_at"] = now
        
        await db.questions.update_one(
            {"question_id": q["question_id"]},
            {"$set": q},
            upsert=True
        )
        count += 1
    
    print(f"✓ Seeded {count} flashcards")
    return count

async def seed_scenarios():
    """Create comprehensive scenario questions"""
    
    scenarios = [
        # Scenario 1: Armed Robbery
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Armed Robbery Investigation",
            "content": """You are assigned to investigate an armed robbery at a convenience store. The store clerk reports that at 2:15 AM, a male offender wearing a black ski mask entered the store, displayed what appeared to be a black semi-automatic handgun, and demanded cash from the register. The offender fled on foot with approximately $450 in cash.

Security cameras captured the incident. A witness in the parking lot observed a dark-colored sedan speed away from the area shortly after the robbery. The clerk is shaken but cooperative.

As the lead detective, outline your investigative plan for the first 48 hours. What are your immediate priorities? What evidence will you collect? How will you identify and apprehend the suspect?""",
            "answer": """IMMEDIATE ACTIONS (First 2 Hours):
1. Secure crime scene, establish perimeter
2. Ensure victim receives any needed medical attention
3. Obtain detailed statement from clerk while memory fresh
4. Canvas for additional witnesses in parking lot and nearby businesses
5. Issue flash message with suspect and vehicle description
6. Request K-9 track if suspect fled on foot recently
7. Check for similar pattern robberies in area

EVIDENCE COLLECTION:
1. Obtain all surveillance video (store and nearby businesses)
2. Process counter/register area for fingerprints
3. Preserve register for potential DNA evidence
4. Photograph scene from multiple angles
5. Collect any physical evidence left by suspect
6. Document victim's injuries or distress

FOLLOW-UP INVESTIGATION (24-48 Hours):
1. Analyze video with tech unit for suspect/vehicle details
2. Enter suspect description in robbery pattern database
3. Check pawn databases for any activity
4. Review recent robbery arrests for similar MO
5. Contact confidential informants
6. Issue BOLO for vehicle description
7. Monitor social media for suspect activity
8. Coordinate with robbery unit on known offenders
9. Check for NIBIN hits if weapon later recovered
10. Review license plate readers in area

CASE DOCUMENTATION:
1. Complete comprehensive case report
2. Update crime analysis with pattern information
3. Prepare photo array if suspect identified
4. Coordinate with ASA on charges when appropriate""",
            "explanation": "Tests knowledge of robbery investigation procedures, evidence preservation, witness management, and resource coordination.",
            "difficulty": "hard",
            "reference": "General Order G05-03: Robbery Investigation"
        },
        
        # Scenario 2: Domestic Violence Homicide
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Domestic Violence Death Investigation",
            "content": """You respond to a call of a person down at a residence. Upon arrival, you find a 34-year-old female victim deceased with apparent blunt force trauma to the head. Her husband, present at the scene, states he found her this way when he returned home from work. However, neighbors report hearing a loud argument and screaming approximately two hours before police were called.

The husband has visible scratches on his forearms. He claims these are from playing with their dog. The couple has a history of domestic disturbances, including two prior police responses in the past year, though no arrests were made.

How do you proceed with this investigation? What evidence will you collect? How do you handle the husband?""",
            "answer": """IMMEDIATE SCENE ACTIONS:
1. Secure scene as homicide until determined otherwise
2. Separate husband from scene - do NOT let him contaminate evidence
3. Request homicide detectives and crime scene unit
4. Notify Medical Examiner immediately
5. Begin crime scene log - document all persons present
6. Do NOT move body without ME approval
7. Identify and separate all potential witnesses

HUSBAND HANDLING:
1. He is not free to leave - invoke investigative detention
2. Document his clothing, injuries (photograph scratches)
3. Obtain his voluntary statement before advising Miranda if non-custodial
4. If probable cause develops, arrest and then Miranda
5. Collect clothing as evidence (get search warrant if necessary)
6. Obtain DNA/fingernail scrapings with warrant or consent
7. Check hands for defensive injuries
8. Timeline his whereabouts - verify alibi

EVIDENCE COLLECTION:
1. Extensive photography of victim and entire scene
2. Document position of body, any disturbance
3. Collect potential murder weapon(s)
4. Swab blood evidence, document spatter patterns
5. Process for fingerprints throughout
6. Collect victim's fingernail scrapings for DNA
7. Document signs of struggle
8. Collect husband's clothing and swab scratches for victim DNA
9. Seize all electronic devices (cell phones, computers) - warrant required
10. Photograph dog, document any dog injuries

BACKGROUND INVESTIGATION:
1. Pull all prior domestic calls to address
2. Interview neighbors who heard argument
3. Interview family, friends about relationship history
4. Subpoena phone records for both parties
5. Check for protective orders or pending divorce
6. Review social media accounts
7. Check for life insurance policies
8. Investigate financial situation

COORDINATION:
1. Work with ME on autopsy findings
2. Request expedited DNA analysis
3. Coordinate with State's Attorney on charging
4. Document everything for domestic violence prosecution protocol""",
            "explanation": "Tests homicide investigation procedures, domestic violence awareness, evidence collection, and suspect handling while building case.",
            "difficulty": "hard",
            "reference": "General Order G05-03: Death Investigation, G04-04: Domestic Violence"
        },
        
        # Scenario 3: Burglary Pattern
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Residential Burglary Pattern",
            "content": """Over the past three weeks, there have been six residential burglaries in your district with similar characteristics: All occurred during daytime hours (10 AM - 3 PM), all targeted single-family homes, entry was made through rear windows, and electronics and jewelry were primary targets.

A witness at the most recent burglary saw a white work van in the alley behind the targeted home about 30 minutes before the homeowner discovered the break-in. The witness could not provide a plate number but described seeing two males, one with a distinctive sleeve tattoo.

As the detective assigned to this pattern, how would you approach connecting these cases and identifying the suspects?""",
            "answer": """PATTERN ANALYSIS:
1. Create detailed matrix of all six burglaries
2. Map locations - identify geographic cluster
3. Analyze exact entry methods, tools used
4. Compare items taken - specific preferences
5. Review MO details for unique signatures
6. Check for any forensic evidence connections
7. Timeline analysis - day of week, time patterns
8. Identify why these homes were selected (vacant, routine)

SUSPECT IDENTIFICATION:
1. Canvas all six neighborhoods for van sightings
2. Check traffic cameras for white work vans in area during burglary times
3. Review license plate readers for patterns
4. Check pawn shops for stolen items
5. Alert informants about pattern and tattoo description
6. Search databases for burglars with similar MO
7. Check probation/parole records for residential burglars
8. Query CLEAR for tattoo description
9. Review recent burglary arrests in surrounding districts

ENHANCED SURVEILLANCE:
1. Identify potential target area based on pattern
2. Request plainclothes surveillance during peak hours
3. Coordinate with district tactical teams
4. Alert patrol to watch for white vans in residential areas
5. Consider bait house operation if approved

EVIDENCE COORDINATION:
1. Ensure all fingerprints from six scenes processed for comparison
2. Check for tool mark matches between scenes
3. Any DNA evidence cross-referenced
4. Review surveillance footage from all scenes
5. Create comprehensive photo array when suspect identified

PREVENTION:
1. Alert neighborhood watch groups
2. Issue community notification via social media
3. Provide prevention tips (lock windows, timers for lights)
4. Request increased patrol visibility during peak hours""",
            "explanation": "Tests pattern analysis, investigative coordination across multiple cases, and proactive investigation techniques.",
            "difficulty": "medium",
            "reference": "General Order G05-03: Property Crimes Investigation"
        },
        
        # Scenario 4: Sexual Assault Investigation
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Sexual Assault Investigation",
            "content": """A 22-year-old female college student reports that she was sexually assaulted last night at an off-campus party. She states she was drinking at the party, became very intoxicated, and the next thing she remembers is waking up partially undressed in an unfamiliar bedroom. She believes she was assaulted by a male she met at the party but only knows his first name, "Derek."

She delayed reporting for 12 hours because she was ashamed and unsure if anyone would believe her. She has since showered and changed clothes. She is visibly upset and considering not pursuing charges because she "can't prove anything."

How do you handle this sensitive investigation? What evidence can still be collected? How do you support the victim while building the case?""",
            "answer": """IMMEDIATE VICTIM SUPPORT:
1. Express belief and empathy - no judgment
2. Explain that showering doesn't eliminate all evidence
3. Explain she has options - evidence collection doesn't require prosecution decision
4. Connect with victim advocate immediately
5. Let her make informed choices, respect autonomy
6. Provide written information on resources/rights
7. Reassure that intoxication does not equal consent

EVIDENCE COLLECTION:
1. SANE exam - still valuable even after shower
   - DNA may persist in body cavities up to 5-7 days
   - Document any injuries, even minor
   - Toxicology for drug-facilitated assault
2. Collect clothing worn to party (even if different from now)
3. Photograph any visible injuries
4. Document her emotional state and demeanor
5. Obtain her detailed statement when ready

INVESTIGATION:
1. Identify party location and attendees
2. Locate "Derek" - check with party host, social media
3. Canvas for witnesses who saw them together
4. Identify whose house/room she woke in
5. Obtain video/photos from party (phones, social media)
6. Secure any digital communications
7. Check for surveillance cameras near party location
8. Interview witnesses about victim's level of intoxication
9. Interview suspect - document any admissions about intoxication level

LEGAL ELEMENTS:
1. Document evidence of inability to consent due to intoxication
2. Determine if drugs may have been used (toxicology)
3. Witness statements about victim's condition
4. Any statements by suspect about victim's state
5. Medical evidence of assault

VICTIM-CENTERED APPROACH:
1. Keep victim informed of investigation progress
2. Let her set pace when possible
3. Coordinate with SVU and victim services
4. Prepare her for what to expect in process
5. Document her wishes regarding prosecution
6. Provide safety planning if suspect may have contact

SUSPECT INTERVIEW STRATEGY:
1. Approach without revealing full case
2. Establish timeline and opportunity
3. Let him describe events before revealing details
4. Document any admissions about her intoxication
5. If interview reveals probable cause, arrest and Miranda""",
            "explanation": "Tests victim-centered approach, sexual assault investigation protocols, evidence collection after delay, and building case without traditional evidence.",
            "difficulty": "hard",
            "reference": "Special Order S04-06: Sexual Assault Response"
        },
        
        # Scenario 5: Fourth Amendment Search Issue
        {
            "type": "scenario",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "title": "Search and Seizure Challenge",
            "content": """You respond to a shots fired call and arrive at an apartment building. You hear yelling from apartment 3B. You knock, and a male answers. You smell marijuana and see, through the doorway, what appears to be a handgun on the coffee table. The male says, "You're not coming in without a warrant."

You push past him, secure the gun, and during a protective sweep find cocaine on the kitchen counter and ammunition in a bedroom closet. The male is arrested for weapons and drug offenses.

Analyze the legality of your entry and search. What, if any, evidence will be suppressed? What should you have done differently?""",
            "answer": """FOURTH AMENDMENT ANALYSIS:

INITIAL ENTRY - PROBLEMATIC:
The warrantless entry into a home is presumptively unconstitutional. Exceptions must apply.

EXIGENT CIRCUMSTANCES ANALYSIS:
For entry to be valid, need probable cause + exigency:

ARGUED EXIGENCIES:
1. Shots fired call - provides reason to investigate, but you arrived at scene, didn't observe active shooting
2. Yelling heard - suggests disturbance but not necessarily emergency
3. Cannabis smell - in Illinois post-legalization, cannabis odor alone is NOT an exigent circumstance
4. Gun in plain view - gun alone (without threat) does not create emergency
5. Subject at door - no one in apparent danger

LIKELY SUPPRESSION:
✗ Gun on coffee table - seized during unlawful entry
✗ Cocaine in kitchen - fruit of unlawful entry
✗ Ammunition in closet - exceeded any protective sweep authority

WHAT SHOULD HAVE BEEN DONE:

OPTION 1 - SECURE AND GET WARRANT:
1. Subject denies entry but is not threatening
2. You can secure the scene (prevent destruction of evidence)
3. Station officer at door to ensure no one leaves
4. Call supervisor and ASA
5. Apply for search warrant based on observations:
   - Shots fired call response
   - Yelling heard
   - Gun observed in plain view
6. Execute warrant once obtained
7. All evidence admissible

OPTION 2 - ARTICULATE TRUE EXIGENCY:
If genuine emergency exists (e.g., you hear someone inside screaming for help, sounds of struggle), document:
- Specific facts showing imminent danger
- Why entry was immediately necessary
- What threat existed to persons
- Why waiting for warrant was not feasible

EXCEPTION NOT APPLICABLE HERE:
- Hot pursuit: No - suspect at door, not fleeing
- Emergency aid: No - no one in apparent distress
- Imminent evidence destruction: Weak - subject wasn't destroying anything
- Prevent escape: No - subject was conversing at door

CONSEQUENCE OF CURRENT ACTIONS:
- All evidence likely suppressed
- Case dismissed
- Potential civil rights lawsuit
- Violation of CPD policy
- COPA review likely

LESSON:
When time permits, ALWAYS get a warrant for home entry. The home receives highest Fourth Amendment protection. "I saw contraband" is not an emergency. Secure scene and seek judicial authorization.""",
            "explanation": "Tests Fourth Amendment knowledge, warrantless entry exceptions, and proper procedure when observing evidence in home.",
            "difficulty": "hard",
            "reference": "4th Amendment, Kentucky v. King, General Order G06-01-03"
        },
        
        # Scenario 6: Gang-Related Shooting
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Gang-Related Shooting Investigation",
            "content": """Three males are shot at 11 PM on a street corner known for gang activity. One victim is DOA, one is critical, and one has non-life-threatening injuries. Witnesses scatter immediately upon police arrival. Shell casings from multiple firearms are on the ground, and a vehicle was seen speeding from the scene.

No one is talking. The surviving victims claim they "didn't see anything." Cell phone video posted to social media 30 minutes later shows part of the incident from across the street, but the account is anonymous. Gang graffiti in the area suggests this corner is disputed territory.

How do you approach this complex investigation where witnesses are uncooperative and gang dynamics are at play?""",
            "answer": """IMMEDIATE SCENE ACTIONS:
1. Establish expanded perimeter - evidence likely spread
2. Request crime scene unit and additional detectives
3. Document all persons in area before they leave
4. Medical examiner notification for DOA
5. Assign officers to hospitals with surviving victims
6. Recover all shell casings with proper documentation
7. Request ShotSpotter data for exact shot timing/locations
8. Canvass for surveillance cameras (business, residential, city)
9. Document gang graffiti and territorial markers

WITNESS STRATEGY:
1. Understand reluctance is fear-based, not hostile
2. Separate potential witnesses for individual contact
3. Provide business cards - may cooperate later
4. Look for witnesses from windows, parked cars
5. Identify anonymous caller who reported shots
6. Check if anyone sought medical attention who left scene
7. Use Crime Stoppers for anonymous tips

SOCIAL MEDIA INVESTIGATION:
1. Preserve the anonymous video immediately (screenshot, screen record)
2. Issue preservation letter to platform
3. Work with tech unit to identify account owner
4. Search for additional posts about incident
5. Monitor gang members' social media for admissions
6. Look for rival gang taunting or claiming credit

VICTIM APPROACH:
1. Hospital bedside interviews when medically cleared
2. Have victim advocate present
3. Explain safety resources available
4. Offer to relocate family if cooperation given
5. Non-fatal victims may become cooperative later
6. Document any spontaneous statements to medical staff

GANG INTELLIGENCE:
1. Coordinate with gang intelligence unit
2. Identify which gangs claim this territory
3. Check for recent gang conflicts or retaliations
4. Review recent arrests of gang members
5. Identify any ongoing feuds
6. Check for social media "beefs" between groups

FORENSIC INVESTIGATION:
1. Match shell casings to prior shooting cases (NIBIN)
2. Compare bullets recovered from victims
3. Check if vehicle identified through surveillance
4. Process scene for DNA, fingerprints despite low probability
5. Analyze ShotSpotter for number of shooters

LONG-TERM STRATEGY:
1. This investigation may take months
2. Cultivate confidential informants
3. Monitor for retaliation incidents
4. Build case through circumstantial evidence
5. Consider federal prosecution for gang conspiracy
6. Coordinate with U.S. Attorney if appropriate

DOCUMENTATION:
1. Comprehensive evidence preservation
2. Document all tips regardless of source
3. Create timeline with all evidence
4. Maintain informant confidentiality""",
            "explanation": "Tests gang-related investigation strategies, witness reluctance handling, social media evidence, and multi-victim scene management.",
            "difficulty": "hard",
            "reference": "General Order G05-03: Homicide Investigation, Gang Intelligence Protocols"
        },
        
        # Scenario 7: Child Abuse Investigation
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Child Abuse Investigation",
            "content": """A teacher reports that an 8-year-old student, Maria, came to school with bruises on her upper arms and back. When asked, Maria said she "fell down stairs." The teacher noticed Maria flinch when touched and observed that she has been withdrawn and struggling academically recently. Maria lives with her mother and mother's boyfriend.

DCFS has been notified and is conducting a parallel investigation. You are assigned to conduct the criminal investigation.

How do you approach this sensitive investigation involving a child victim? What evidence do you need? How do you coordinate with DCFS while building a criminal case?""",
            "answer": """IMMEDIATE COORDINATION:
1. Contact DCFS investigator - coordinate, don't duplicate
2. Determine if child is in immediate danger
3. If danger present, protective custody may be needed
4. Establish information sharing protocol with DCFS
5. Joint investigation preferred when possible

FORENSIC INTERVIEW:
1. Refer to Child Advocacy Center for forensic interview
2. DO NOT conduct your own detailed interview first - one interview protects child and case
3. Observe forensic interview behind glass
4. Forensic interviewer is trained for child witnesses
5. Interview will be recorded for court use
6. Avoid leading questions, multiple interviews

MEDICAL EVIDENCE:
1. Refer for medical examination by child abuse specialist
2. Document all injuries with photographs
3. Medical opinion on whether injuries consistent with explanation
4. Determine age of injuries - are there healing injuries?
5. Full body examination for hidden injuries
6. Growth chart review for malnutrition signs

INVESTIGATION:
1. Interview teacher and school personnel
2. Obtain school records - attendance, behavior changes
3. Interview mother separately from boyfriend
4. Interview boyfriend separately
5. Background checks on all adults in home
6. Check for prior DCFS history
7. Check for prior police calls to address
8. Interview neighbors about household
9. Obtain medical records for child's prior injuries
10. Interview child's other contacts (relatives, friends' parents)

SUSPECT INTERVIEWS:
1. Non-custodial interview preferred initially
2. Let suspect explain injuries before revealing evidence
3. Document inconsistencies in explanations
4. Be aware of who has access to child
5. Determine primary caregiver
6. If probable cause, arrest and continue with Miranda

EVIDENCE COLLECTION:
1. Photograph all injuries with scale
2. Document home conditions
3. Seize any implements that may have caused injuries
4. Preserve child's clothing if relevant
5. Document sleeping arrangements
6. Note cleanliness, food availability

ONGOING PROTECTION:
1. Ensure safety plan in place with DCFS
2. If arrest made, seek no-contact order
3. Monitor for witness intimidation
4. Keep child informed in age-appropriate way
5. Connect family with victim services

PROSECUTION:
1. Work closely with ASA specializing in child abuse
2. Prepare child for court process
3. Consider use of recorded forensic interview at trial
4. Address hearsay exceptions for child statements
5. Expert testimony on abuse indicators""",
            "explanation": "Tests child abuse investigation protocols, multi-agency coordination, forensic interview principles, and child-sensitive approaches.",
            "difficulty": "hard",
            "reference": "Special Order S04-06: Child Abuse Investigation, DCFS Protocols"
        },
        
        # Scenario 8: Miranda Application
        {
            "type": "scenario",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "title": "Miranda and Confession Issues",
            "content": """You arrest John for a home invasion based on eyewitness identification. At the station, you read him Miranda rights, and he says, "I want to talk to you, but maybe I should have a lawyer." You respond, "That's up to you, but we have strong evidence and this is your chance to tell your side." John then says, "Okay, I'll talk," and confesses to the crime.

During the interview, which lasts 4 hours with one bathroom break and no food, John asks to stop at one point, saying, "I'm tired, can we do this tomorrow?" You say, "We're almost done, just a few more questions," and continue. He then provides additional details about how he selected the victim's home.

Analyze the legal issues with this confession. Will it be admissible?""",
            "answer": """MIRANDA INVOCATION ANALYSIS:

ISSUE 1: AMBIGUOUS INVOCATION OF COUNSEL
Statement: "maybe I should have a lawyer"

ANALYSIS:
- Under Davis v. United States, invocation must be unambiguous
- "Maybe I should have a lawyer" is ambiguous
- Police may seek clarification
- Your response "that's up to you" is permissible
- Subsequent clear waiver "I'll talk" is valid
- THIS PORTION LIKELY SURVIVES

ISSUE 2: VOLUNTARINESS CONCERNS

FACTORS AGAINST VOLUNTARINESS:
1. Four-hour interrogation - lengthy but not per se unconstitutional
2. Only one bathroom break - concerning
3. No food provided - concerning
4. Request to stop: "Can we do this tomorrow?" - THIS IS PROBLEMATIC
5. Response "we're almost done" could be considered coercive

INVOCATION OF RIGHT TO SILENCE:
- "Can we do this tomorrow?" is ambiguous
- Not a clear invocation of right to silence
- BUT combined with stated fatigue, shows duress
- Statements after this point MORE vulnerable to suppression

TOTALITY OF CIRCUMSTANCES:
- Duration + lack of food/breaks + tired request = coercive environment
- Even if valid waiver initially, voluntariness can erode
- Statements made under fatigue/duress may be excluded

LIKELY OUTCOME:
1. Initial confession (before "tired" statement) - likely ADMISSIBLE
   - Ambiguous counsel reference properly handled
   - Clear subsequent waiver

2. Statements after "I'm tired, can we do this tomorrow?" - VULNERABLE
   - Could be found involuntary
   - "We're almost done" could be seen as coercive
   - Additional details may be suppressed

WHAT YOU SHOULD HAVE DONE:

WHEN HE MENTIONED ATTORNEY:
- Clarification appropriate: "Are you asking for an attorney or do you want to talk to me?"
- Get clear answer before proceeding
- Your approach was acceptable

DURING INTERVIEW:
1. Provide food and water
2. Regular breaks (every 1-2 hours)
3. Document all breaks given
4. When he asked to stop due to fatigue:
   - STOP QUESTIONING
   - Let him rest or resume another day
   - Continuing undermines voluntariness

WHEN HE SAID HE WAS TIRED:
- Proper response: "We can stop now and continue tomorrow"
- His request was not unambiguous, but prudent to honor
- Continuing risks entire confession

BEST PRACTICE:
- Shorter, focused interviews
- Document all comfort provided
- Take "I'm tired" seriously
- Record everything to prove voluntariness
- When in doubt, stop and resume later""",
            "explanation": "Tests Miranda invocation standards, confession voluntariness factors, and proper interrogation procedures.",
            "difficulty": "hard",
            "reference": "5th Amendment, Davis v. United States, General Order G06-01-02"
        },
        
        # Scenario 9: Officer-Involved Shooting
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Officer-Involved Shooting Investigation",
            "content": """You are a detective called to the scene of an officer-involved shooting. Officer Davis shot and killed a male subject in an alley after a foot pursuit. Officer Davis says the subject pointed a gun at him. No gun has been recovered at the scene. Officer Davis's partner, Officer Kim, was 20 yards behind and did not witness the actual shooting but heard Officer Davis yell "gun" before shots were fired.

A civilian witness in a nearby apartment says she saw the shooting from her window and claims the subject's hands were empty and raised when he was shot. The subject's family, who arrived at the scene, is demanding answers.

How do you handle this sensitive and complex investigation?""",
            "answer": """IMMEDIATE SCENE MANAGEMENT:
1. Ensure all life-saving measures provided to subject
2. Separate Officer Davis from scene immediately
3. DO NOT interview Officer Davis - he has right to representation and 24-hour review period
4. Officer Kim also separated but can be briefly interviewed
5. Notify COPA immediately - they have primary jurisdiction on OIS
6. Notify command staff through chain
7. Request crime scene unit
8. Establish expanded perimeter - alley and surrounding area

EVIDENCE COLLECTION:
1. Comprehensive search for weapon - expand search area
2. Officer Davis's weapon recovered and inventoried
3. Document exact position of body
4. Document distance from Officer Davis's position
5. Shell casing locations
6. Body-worn camera footage - preserve immediately
7. Search subject's body and clothing
8. Canvas entire area for surveillance cameras
9. ShotSpotter data if available
10. Photograph and document everything

WITNESS MANAGEMENT:
1. Civilian witness - detailed statement immediately
2. Document her vantage point - what she could actually see
3. Officer Kim statement on what he observed (not opinions)
4. Canvas for additional witnesses
5. Keep witnesses separated
6. Obtain contact information from all

FAMILY HANDLING:
1. Compassion is paramount
2. Do not provide details of investigation
3. Connect with victim services
4. Document any statements they make (spontaneous)
5. Do not allow access to scene

INVESTIGATION PROTOCOLS:
1. COPA will conduct independent investigation
2. Detective Division conducts criminal investigation in parallel
3. Officer Davis entitled to:
   - Union representation
   - 24-hour review period before statement (if invoked)
   - Access to BWC before statement
4. Administrative investigation separate from criminal

THE MISSING GUN ISSUE:
1. Expand search extensively - weapons can be thrown
2. Check dumpsters, bushes, under vehicles
3. Did subject have accomplices who may have retrieved weapon?
4. Interview subject's associates about weapon possession
5. Check subject's criminal history for weapons offenses
6. Social media may show prior weapon possession
7. Absence of gun doesn't mean it wasn't there - continue searching

CREDIBILITY ASSESSMENT:
1. Civilian witness distance and lighting conditions
2. What was her actual view - obstructions?
3. Officer Kim's corroboration of "gun" statement
4. Body-worn camera footage is critical evidence
5. Forensic evidence of subject's hand position (GSR)
6. Look for corroborating or contradicting evidence

DOCUMENTATION:
1. Complete and comprehensive reports
2. All evidence properly inventoried
3. Video evidence preserved with chain of custody
4. Witness statements in their own words
5. Scene diagrams and measurements
6. All notifications documented with times

COMMUNITY RELATIONS:
1. PIO should handle media inquiries
2. Department policy on releasing BWC
3. Community meetings may be necessary
4. Transparency builds trust
5. Investigation integrity is priority""",
            "explanation": "Tests OIS investigation protocols, officer rights, evidence collection, community relations, and multi-agency coordination.",
            "difficulty": "hard",
            "reference": "General Order G03-06: Firearm Discharge, COPA Protocols"
        },
        
        # Scenario 10: Vehicle Stop Drug Investigation
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Traffic Stop Drug Investigation",
            "content": """During a traffic stop for a broken taillight, you notice the driver appears extremely nervous - sweating profusely, avoiding eye contact, and his hands are shaking. When you ask for his license and registration, he fumbles excessively. You observe fast food wrappers, energy drinks, and a strong air freshener smell in the vehicle. The driver says he is traveling from California to New York to visit family.

Your K-9 unit is 15 minutes away. The driver has a valid license and clean driving record.

Can you extend the stop to wait for the K-9? What are your options? What legal standards apply?""",
            "answer": """LEGAL FRAMEWORK:

RODRIGUEZ v. UNITED STATES (2015):
- A traffic stop cannot be extended beyond time needed to complete the stop's mission
- K-9 sniff that prolongs stop beyond ordinary time = unconstitutional unless you have reasonable suspicion of drug activity
- Nervous behavior alone may not be sufficient

CURRENT SITUATION ANALYSIS:

OBSERVATIONS SUPPORTING SUSPICION:
+ Extreme nervousness (sweating, shaking, no eye contact)
+ Cross-country travel (drug courier indicator)
+ Strong air freshener (masking odor indicator)
+ Energy drinks/fast food (non-stop travel indicator)

OBSERVATIONS AGAINST:
- Valid license and registration
- Clean driving record
- Lawful explanation for travel
- Nervousness normal during police contact

CAN YOU EXTEND THE STOP?

OPTION 1: DEVELOP RS DURING NORMAL STOP
- While processing license/writing citation, you can:
  - Ask questions about travel (origin, destination, purpose)
  - Look for inconsistencies in story
  - Observe vehicle contents in plain view
  - Note if story makes sense
- This does NOT extend the stop

OPTION 2: K-9 DURING NORMAL PROCESSING TIME
- If K-9 arrives while you are still completing normal tasks, sniff is permissible
- 15 minutes likely exceeds normal stop time for taillight
- Cannot artificially slow down to wait

OPTION 3: REASONABLE SUSPICION DETERMINATION
If you can articulate reasonable suspicion based on:
- Nervousness + travel pattern + indicators of drug activity
- You MAY briefly extend stop for K-9
- Document specific facts supporting RS
- Totality of circumstances analysis

WHAT YOU SHOULD DO:

DURING NORMAL STOP TIME:
1. Process license and registration normally
2. Ask conversational questions about trip
3. Note responses and any inconsistencies
4. Observe anything in plain view
5. If story has inconsistencies, document them

DECISION POINT:
If you find additional indicators (inconsistent story, visible contraband, admission):
- RS exists, extend for K-9 justified

If just nervousness and travel pattern:
- Risky to extend - these factors common in innocent travelers
- Issue warning/citation and release
- Document observations for future reference if same vehicle
- Consider alerting agencies in travel direction

IF CONSENT REQUESTED:
- You may ask for consent to search
- Must be voluntary, not coerced
- If granted, document clearly
- If refused, cannot use refusal as RS

BEST PRACTICE:
Without stronger indicators than nervousness and travel, complete stop and release. Document observations in case vehicle encountered again. Weak RS leads to suppressed evidence and civil liability.""",
            "explanation": "Tests Rodriguez v. U.S. application, reasonable suspicion development, and Fourth Amendment traffic stop standards.",
            "difficulty": "hard",
            "reference": "Rodriguez v. United States, 4th Amendment, General Order G06-01"
        },
        
        # Scenario 11: Digital Evidence Investigation  
        {
            "type": "scenario",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Digital Evidence and Social Media",
            "content": """You are investigating a series of threatening messages sent to a local business owner. The threats arrived via email and social media, warning the owner to "pay up or face consequences." The business was vandalized two days after the threats stopped.

The business owner provides you with screenshots of the messages. The email came from a generic Gmail address. The social media messages came from an account with a fake name and profile photo.

How do you investigate this digital evidence case? What legal process is required? How do you identify the anonymous sender?""",
            "answer": """EVIDENCE PRESERVATION:

IMMEDIATE ACTIONS:
1. Do NOT rely solely on screenshots - get originals
2. Preserve original emails with full headers
3. Document social media profile before it's deleted
4. Screenshot all posts, followers, following
5. Check if accounts still active
6. Note exact URLs and usernames
7. Document timeline of threats and vandalism

LEGAL PROCESS FOR RECORDS:

GMAIL RECORDS:
1. Send preservation letter to Google immediately
2. This preserves records for 90 days (extendable)
3. Search warrant required for content of emails
4. Warrant application needs:
   - Probable cause linking account to crime
   - Specific records sought
   - Account identifiers
5. Google may provide: subscriber info, IP logs, account activity, email content

SOCIAL MEDIA (Facebook/Instagram/Twitter):
1. Preservation letter to platform
2. Search warrant for content
3. May get: account info, IP addresses, login history, messages, posts
4. Platforms have law enforcement portals
5. Subpoena may get basic subscriber info (varies by platform)

IP ADDRESS ANALYSIS:
1. IP addresses from email headers
2. IP logs from social media logins
3. Subpoena to ISP for subscriber info
4. Be aware of:
   - VPN usage masks real IP
   - Public WiFi complicates identification
   - Dynamic IPs require exact time stamp

INVESTIGATION:

VICTIMOLOGY:
1. Who would threaten this business?
2. Any disputes with employees, competitors, customers?
3. Prior complaints or conflicts?
4. Financial issues that might relate to "pay up"?

CONNECTING VANDALISM:
1. Surveillance from business
2. Any evidence left at vandalism scene
3. Method of vandalism match threats?
4. Timeline supports same actor

LINGUISTIC ANALYSIS:
1. Compare threat language to known communications
2. Spelling/grammar patterns
3. Phrase usage that might identify writer
4. Time of day messages sent

PARALLEL INVESTIGATION:
1. While awaiting records, investigate traditionally
2. Interview employees, former employees
3. Business competitors
4. Anyone with access who might know vulnerabilities
5. Check for similar threats to other businesses

ONCE SUSPECT IDENTIFIED:
1. Search warrant for suspect's devices
2. Compare writing samples
3. Check for saved threatening messages
4. Browser history showing accounts
5. Interview with confrontation of evidence

CHARGES:
1. Intimidation (720 ILCS 5/12-6)
2. Criminal damage to property
3. Computer tampering if applicable
4. Possibly extortion if "pay up" demand

DOCUMENTATION:
1. Screenshot/preserve everything at each step
2. Hash values for digital evidence integrity
3. Maintain chain of custody for all records
4. Expert may be needed to explain at trial""",
            "explanation": "Tests digital evidence investigation, legal process for electronic records, and anonymous suspect identification.",
            "difficulty": "medium",
            "reference": "Special Order S06-06: Digital Evidence, 18 USC 2703"
        },
        
        # Scenario 12: Missing Person to Homicide
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures", 
            "title": "Missing Person Investigation",
            "content": """A 25-year-old woman, Sarah, was reported missing by her roommate 48 hours ago. Sarah failed to show up for work and hasn't responded to calls or texts, which is extremely unusual behavior. Her car is still in the apartment parking lot. Her purse and phone were found in the apartment. The roommate says Sarah had recently broken up with her boyfriend of 2 years, who did not take it well and had been sending angry text messages.

There are no signs of forced entry or struggle in the apartment. Sarah's last known activity was a credit card purchase at a nearby gas station at 8 PM two days ago.

How do you approach this missing person investigation? At what point does this become a criminal investigation?""",
            "answer": """INITIAL CLASSIFICATION:

HIGH-RISK INDICATORS PRESENT:
✓ Purse and phone left behind - out of character
✓ Car still at residence
✓ No contact with anyone
✓ Failed to appear at work (unusual)
✓ Recent relationship conflict
✓ Angry communications from ex-boyfriend

CLASSIFICATION: HIGH-RISK MISSING PERSON
Treat as potential foul play from outset

IMMEDIATE ACTIONS:
1. Enter into LEADS/NCIC immediately
2. Issue BOLO with photo
3. Notify command - potential criminal case
4. Request additional investigative resources
5. Check hospitals and morgue
6. Check jail systems

APARTMENT INVESTIGATION:
1. Treat as potential crime scene
2. Process for evidence - fingerprints, DNA, blood
3. Luminol test for cleaned blood
4. Examine all electronics left behind
5. Check for any diary, notes, calendar
6. Interview roommate thoroughly
7. Document condition of apartment
8. Check if any items missing that she would take

GAS STATION:
1. Obtain surveillance video immediately
2. Was she alone? Any other vehicles?
3. Did she appear distressed?
4. Direction of travel after?
5. Witnesses at gas station

EX-BOYFRIEND INVESTIGATION:
1. This is your primary person of interest
2. Interview immediately - where was he at 8 PM that night?
3. Obtain his phone for angry messages
4. Check his car and residence (consent or warrant)
5. Verify alibi completely
6. Check his GPS/phone location data
7. Social media monitoring
8. Prior DV history?

DIGITAL INVESTIGATION:
1. Search warrant for Sarah's phone records
2. Text messages with ex-boyfriend
3. Last location data from phone
4. Social media account activity
5. Email accounts
6. Dating apps (was she meeting someone new?)
7. Bank/credit card records for activity after gas station

EXPANDED INVESTIGATION:
1. Canvas entire apartment complex
2. Interview all friends and family
3. Interview coworkers
4. Check surveillance along route from gas station to home
5. K-9 search if evidence of foul play develops
6. Check sex offender registry in area
7. Any similar missing persons in region?

MEDIA/FAMILY:
1. Coordinate with PIO on media release
2. Photo and description to media
3. Family may help with social media sharing
4. Keep family informed but don't compromise investigation
5. Consider tip line

TRANSITION TO CRIMINAL CASE:
Case becomes criminal investigation when:
1. Evidence of foul play discovered
2. Probable cause to believe crime occurred
3. Body discovered
4. Witness reports abduction
5. Suspect provides incriminating evidence

CURRENT STATUS:
Based on circumstances, this should be investigated as probable foul play:
- Ex-boyfriend angry and threatening
- Personal items left behind
- No voluntary indicators
- Completely out of character

DOCUMENTATION:
1. Timeline of last known activities
2. All interviews documented
3. Evidence properly preserved
4. Chain of custody maintained
5. Regular updates to command""",
            "explanation": "Tests missing person protocols, criminal investigation transition, suspect development, and multi-faceted investigation approach.",
            "difficulty": "hard",
            "reference": "General Order G04-01: Missing Persons, G05-03: Homicide Investigation"
        }
    ]
    
    now = datetime.now(timezone.utc)
    count = 0
    
    for q in scenarios:
        q["question_id"] = f"sc_{uuid.uuid4().hex[:12]}"
        q["created_at"] = now
        q["updated_at"] = now
        
        await db.questions.update_one(
            {"question_id": q["question_id"]},
            {"$set": q},
            upsert=True
        )
        count += 1
    
    print(f"✓ Seeded {count} scenarios")
    return count

async def main():
    print("🌱 Starting comprehensive database seeding...")
    print("=" * 50)
    
    await clear_existing_data()
    await seed_categories()
    fc_count = await seed_flashcards()
    sc_count = await seed_scenarios()
    
    print("=" * 50)
    print(f"✅ Seeding complete!")
    print(f"   📚 Flashcards: {fc_count}")
    print(f"   📝 Scenarios: {sc_count}")
    print(f"   📁 Total: {fc_count + sc_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
