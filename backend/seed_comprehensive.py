import asyncio
import json
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Ensure store clerk receives medical assessment for shock or injuries from the armed encounter",
                        "Document clerk's physical and emotional condition upon arrival",
                        "Issue immediate flash message with suspect description: male, black ski mask, black semi-automatic handgun",
                        "Include suspect's direction of flight and dark-colored sedan description in flash message",
                        "Request K-9 unit for track if suspect fled on foot recently",
                        "Obtain preliminary statement from clerk once assessed as stable"
                    ],
                    "E": [
                        "Speak with responding officers and scene supervisor for initial briefing on arrival conditions",
                        "Establish inner perimeter around convenience store entrance, register area, and suspect's path",
                        "Establish outer perimeter covering parking lot and surrounding area where sedan was observed",
                        "Assign uniformed officers to secure all entry and exit points of the store",
                        "Identify and separate the parking lot witness from the clerk immediately",
                        "Establish detective command post at scene",
                        "Deploy additional units for area canvass along suspect's flight path"
                    ],
                    "A": [
                        "If suspect is apprehended, speak with apprehending officer and document suspect's condition",
                        "Photograph suspect upon apprehension and note any injuries or distinguishing marks",
                        "Advise Miranda prior to any custodial interrogation",
                        "Conduct electronically recorded interrogation if suspect agrees to speak",
                        "Document any spontaneous statements made by suspect during apprehension or transport",
                        "Prepare photo array using suspect description for witness identification if suspect is not immediately located"
                    ],
                    "C": [
                        "Obtain detailed statement from store clerk while memory is fresh, including suspect's exact words, mannerisms, and weapon details",
                        "Interview parking lot witness separately regarding sedan description, direction of travel, and any occupant details",
                        "Canvass nearby businesses for additional witnesses who may have seen suspect before or after robbery",
                        "Canvass parking lot and surrounding area for any other persons present at 2:15 AM",
                        "Obtain and preserve all security camera footage from the store",
                        "Canvass neighboring businesses for external surveillance cameras covering approach and flight routes",
                        "Instruct witnesses not to discuss the incident with each other to preserve independent recollection"
                    ],
                    "T": [
                        "Photograph entire crime scene from multiple angles before any evidence is moved",
                        "Document evidence locations including register area, suspect's path through store, and entry/exit points",
                        "Record all investigative actions in case report and Felony 101",
                        "Log all evidence into PCAD with detailed descriptions",
                        "Document clerk's injuries or visible distress with photographs",
                        "Preserve and document security camera footage with timestamps",
                        "Review and secure responding officers' body-worn camera footage",
                        "Update crime analysis with robbery pattern information"
                    ],
                    "I": [
                        "Obtain and preserve all surveillance video from store and nearby businesses",
                        "Process counter and register area for latent fingerprints",
                        "Preserve register for potential DNA evidence (touch DNA from suspect's hands)",
                        "Collect any physical evidence left by suspect along flight path",
                        "Review license plate reader data in surrounding area for dark-colored sedan",
                        "Request Forensic Services Division for complete scene processing",
                        "Maintain strict chain of custody documentation for all collected evidence"
                    ],
                    "O": [
                        "Coordinate with ASA on charges when suspect is identified",
                        "Prepare photo array if suspect identified through investigation",
                        "Conduct LEADS and CLEAR background checks on any persons of interest",
                        "Request search warrants for surveillance footage from businesses that do not voluntarily provide",
                        "Ensure 4th Amendment compliance with all search and seizure activities",
                        "Check NIBIN database if weapon is later recovered for ballistic matches"
                    ],
                    "N": [
                        "Analyze video with tech unit to enhance suspect and vehicle details",
                        "Enter suspect description in robbery pattern database and check for similar MO",
                        "Issue BOLO for dark-colored sedan with all available details",
                        "Check pawn databases for any activity matching stolen items",
                        "Review recent robbery arrests for similar MO and suspect description",
                        "Contact confidential informants regarding armed robbery activity",
                        "Monitor social media for suspect activity or bragging posts",
                        "Coordinate with robbery unit on known offenders matching description"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Secure scene and treat as homicide until determined otherwise",
                        "Request homicide detectives and crime scene unit immediately",
                        "Notify Medical Examiner for response — do NOT move body without ME approval",
                        "Assess and document victim's condition and apparent injuries (blunt force trauma to head)",
                        "Document husband's physical condition including visible scratches on forearms",
                        "Obtain preliminary information from responding officers about scene conditions upon arrival"
                    ],
                    "E": [
                        "Speak with responding officers for initial briefing on how scene was found",
                        "Establish inner perimeter around the body and immediate area of the residence",
                        "Establish outer perimeter around the entire property",
                        "Separate husband from the scene immediately — do NOT let him return to or contaminate evidence",
                        "Begin crime scene log documenting all persons present and times of entry/exit",
                        "Identify and separate all potential witnesses including neighbors who heard arguing",
                        "Assign officers to secure all entry and exit points of the residence"
                    ],
                    "A": [
                        "Husband is a person of interest and is not free to leave — invoke investigative detention",
                        "Obtain his voluntary statement before advising Miranda if encounter remains non-custodial",
                        "If probable cause develops based on evidence and statements, place under arrest and administer Miranda",
                        "Timeline his whereabouts — verify his claim of returning home from work",
                        "Document spontaneous statements made by husband at scene",
                        "Photograph husband's scratches on forearms and any other injuries or marks",
                        "Evaluate his claim that scratches are from playing with the dog"
                    ],
                    "C": [
                        "Interview neighbors who reported hearing loud argument and screaming separately and individually",
                        "Determine exact timeline of when neighbors heard the argument relative to when police were called",
                        "Interview family members, friends, and coworkers about the couple's relationship history",
                        "Pull all prior domestic violence calls to this address from CPD records",
                        "Check for any existing protective orders, pending divorce filings, or civil disputes",
                        "Review both parties' social media accounts for evidence of conflict or threats",
                        "Canvass additional neighbors for any other observations or security camera footage"
                    ],
                    "T": [
                        "Extensive photography of victim's body and all injuries from multiple angles",
                        "Document exact position of body, any signs of disturbance, and the surrounding area",
                        "Photograph husband's clothing, scratches on forearms, and any other marks",
                        "Document all signs of struggle throughout the residence",
                        "Photograph the dog and document any injuries to the dog to test husband's story",
                        "Record all actions in case report following domestic violence prosecution protocol",
                        "Document scene conditions including furniture positions, broken items, and blood evidence",
                        "Review and secure all responding officers' body-worn camera footage"
                    ],
                    "I": [
                        "Collect and preserve potential murder weapon(s) — identify objects consistent with blunt force trauma",
                        "Swab all blood evidence and document any blood spatter patterns",
                        "Process entire residence for fingerprints, focusing on areas of apparent struggle",
                        "Collect victim's fingernail scrapings for DNA evidence",
                        "Collect husband's clothing and swab his scratches for potential victim DNA transfer",
                        "Obtain DNA and fingernail scrapings from husband with warrant or consent",
                        "Request Forensic Services Division for complete scene processing",
                        "Preserve husband's and victim's cell phones for forensic examination"
                    ],
                    "O": [
                        "Notify ASA regarding homicide circumstances and developing probable cause",
                        "Consult ASA regarding search warrant for husband's person and property if consent is refused",
                        "Request search warrants for cell phone extraction and digital records",
                        "Conduct LEADS and CLEAR background checks on husband",
                        "Request Medical Examiner to determine cause and manner of death",
                        "Ensure 4th Amendment compliance with all searches",
                        "Ensure 5th and 6th Amendment protections if custodial interrogation occurs",
                        "Review prior domestic violence history for pattern evidence admissibility"
                    ],
                    "N": [
                        "Coordinate with ME on autopsy scheduling and attend autopsy",
                        "Verify husband's employment alibi — contact employer and check surveillance/badge records",
                        "Obtain husband's cell phone records to verify location during time of death window",
                        "Check for life insurance policies or financial motive",
                        "Prepare complete case file for felony review and charging decision",
                        "Notify victim's family through proper notification procedures",
                        "Coordinate with domestic violence advocacy resources",
                        "Refer media inquiries to Office of Communications"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Respond to the most recent burglary scene and ensure homeowner is assessed for any injuries or distress",
                        "Document homeowner's condition and secure the residence",
                        "Issue flash message with suspect descriptions: two males, one with distinctive sleeve tattoo, white work van",
                        "Request patrol units to conduct directed patrols in target area during daytime hours (10 AM - 3 PM)",
                        "Obtain preliminary statement from the homeowner regarding loss and any observations"
                    ],
                    "E": [
                        "Speak with responding officers and review all six burglary reports for common elements",
                        "Establish perimeter at the most recent scene including the alley where van was observed",
                        "Map all six burglary locations to identify geographic pattern and predict next target area",
                        "Coordinate with district commander to increase patrols during target timeframe",
                        "Establish command post for pattern investigation coordination",
                        "Deploy plainclothes officers and unmarked vehicles in target area for surveillance"
                    ],
                    "A": [
                        "If suspects are identified and located, coordinate tactical apprehension plan",
                        "Prepare photo arrays using suspect description (male with distinctive sleeve tattoo)",
                        "Run the white work van description through vehicle databases and registration records",
                        "Check for recent arrests of individuals matching descriptions with burglary history",
                        "Advise Miranda prior to any custodial interrogation of detained suspects",
                        "Document any spontaneous statements upon apprehension"
                    ],
                    "C": [
                        "Conduct detailed interview with the witness who observed the white work van and two males",
                        "Work with witness to develop composite description of suspect with sleeve tattoo",
                        "Re-interview all six burglary victims for any additional details or connections",
                        "Canvass all six neighborhoods for additional witnesses and doorbell/security camera footage",
                        "Contact nearby businesses along alley routes for surveillance footage of the white van",
                        "Check with delivery services and utility companies for any scheduled work vans in the areas",
                        "Instruct all witnesses to preserve independent recollection"
                    ],
                    "T": [
                        "Photograph the most recent burglary scene including point of entry (rear window)",
                        "Document entry methods at all six locations for MO comparison",
                        "Create detailed case report linking all six burglaries with common characteristics",
                        "Document pattern analysis: daytime hours, single-family homes, rear window entry, electronics/jewelry targets",
                        "Log all evidence from each scene into PCAD",
                        "Compile timeline showing dates, times, and locations of all six incidents",
                        "Review and collect body-worn camera footage from all responding officers across all six scenes"
                    ],
                    "I": [
                        "Process most recent scene for fingerprints at point of entry and areas where items were taken",
                        "Compare latent prints across all six scenes for matches",
                        "Collect tool mark evidence from rear windows at each location",
                        "Request Forensic Services Division for analysis and cross-comparison of evidence",
                        "Check for DNA evidence at entry/exit points (blood from broken glass, sweat, skin cells)",
                        "Preserve any tire track evidence from alley where van was parked",
                        "Maintain chain of custody documentation across all six linked cases"
                    ],
                    "O": [
                        "Consult ASA regarding linking cases for enhanced charges (pattern/organized crime)",
                        "Request search warrants for white work van when identified",
                        "Request warrants for surveillance footage from businesses that do not voluntarily cooperate",
                        "Conduct LEADS and CLEAR checks on any persons of interest",
                        "Run LEADS query on stolen electronics and jewelry serial numbers",
                        "Check pawn shop databases for recently sold items matching stolen property descriptions"
                    ],
                    "N": [
                        "Issue community alert for target neighborhoods about daytime burglary pattern",
                        "Distribute suspect and vehicle description to all district personnel",
                        "Coordinate with burglary unit and crime analysis for similar patterns in adjacent districts",
                        "Monitor pawn shops and online marketplaces for stolen electronics and jewelry",
                        "Set up surveillance operation in predicted target area during peak hours",
                        "Contact confidential informants regarding burglary crews using work vans",
                        "Prepare case file linking all six incidents for prosecution",
                        "Brief district commander on pattern status and resource needs"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Respond with sensitivity and ensure victim feels safe and supported throughout the process",
                        "Assess victim's physical and emotional condition — offer medical attention immediately",
                        "Arrange transportation to hospital for SANE (Sexual Assault Nurse Examiner) examination",
                        "Advise victim not to wash, change clothes, eat, drink, or use the restroom before exam if possible",
                        "Request SVU (Special Victims Unit) detective if not already assigned",
                        "Provide victim advocate contact information and offer their immediate presence",
                        "Reassure victim that the delayed report and showering do not prevent investigation"
                    ],
                    "E": [
                        "Identify and secure the off-campus party location as a potential crime scene",
                        "Establish perimeter around the bedroom where the assault allegedly occurred",
                        "Determine party host and attendee information to identify the location",
                        "Coordinate with campus police/security if party was on or near campus",
                        "Separate and identify potential witnesses who attended the party",
                        "Preserve the bedroom scene — do not allow cleaning or alteration"
                    ],
                    "A": [
                        "Identify 'Derek' through party attendees, host information, and social media",
                        "Once identified, determine whether to approach for voluntary interview or seek arrest warrant",
                        "If probable cause exists, arrest and advise Miranda prior to custodial interrogation",
                        "Conduct electronically recorded interrogation (required for sexual assault cases in Illinois)",
                        "Photograph suspect and document any injuries, scratches, or marks on his body",
                        "Document any spontaneous statements made by suspect"
                    ],
                    "C": [
                        "Obtain detailed statement from victim in private, comfortable setting using victim-centered approach",
                        "Use cognitive interview techniques to help victim recall details despite alcohol-impaired memory",
                        "Identify and interview party host about guest list, layout, and observations",
                        "Interview other party attendees who may have witnessed victim's condition or interactions with 'Derek'",
                        "Identify anyone who may have seen victim and suspect leave together or enter the bedroom",
                        "Check for any photos, videos, or social media posts from the party that night",
                        "Instruct all witnesses to preserve phones and not delete any photos or messages from that night"
                    ],
                    "T": [
                        "Photograph the party location and bedroom where assault occurred",
                        "Document victim's account in detail including timeline, alcohol consumption, and memory gaps",
                        "Document victim's emotional state and demeanor during interview",
                        "Record all investigative actions in case report following sexual assault protocol",
                        "Document SANE examination results and evidence collected",
                        "Preserve any text messages, social media communications, or digital evidence from victim's phone",
                        "Log all evidence into PCAD with detailed descriptions",
                        "Review and secure any body-worn camera footage from responding officers"
                    ],
                    "I": [
                        "Coordinate SANE examination at hospital — ensure kit is properly collected and preserved",
                        "Even though victim showered, DNA evidence may still be recoverable — proceed with exam",
                        "Collect victim's clothing worn during and after the assault (even if changed)",
                        "Collect bedsheets, pillowcases, and any materials from the bedroom where assault occurred",
                        "Process bedroom for DNA evidence, fingerprints, and other trace evidence",
                        "Preserve any cups, bottles, or containers the victim may have drunk from (test for date-rape drugs)",
                        "Request toxicology screen through SANE exam to detect any drugs",
                        "Submit sexual assault kit to crime lab within required timeframe",
                        "Maintain strict chain of custody for all evidence"
                    ],
                    "O": [
                        "Notify ASA regarding sexual assault investigation and evidence status",
                        "Consult ASA about charges including Criminal Sexual Assault under 720 ILCS 5/11-1.20",
                        "Request search warrant for the party location/bedroom if consent not given",
                        "Request search warrant for suspect's phone, social media, and digital communications",
                        "Conduct LEADS and CLEAR checks on suspect once identified",
                        "Ensure compliance with Illinois Sexual Assault Evidence Submission Act",
                        "Ensure 5th and 6th Amendment protections during interrogation"
                    ],
                    "N": [
                        "Connect victim with victim advocate services and sexual assault support resources",
                        "Develop safety plan for victim, especially if suspect is known on campus",
                        "Coordinate with campus Title IX office if applicable",
                        "Check if suspect has prior sexual assault complaints or arrests",
                        "Monitor suspect's social media for relevant posts or communications about the incident",
                        "Prepare complete case file for felony review",
                        "Follow up with victim regularly to maintain trust and provide case updates",
                        "Ensure SANE kit tracking through Illinois Rape Kit Tracking System"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Upon arriving at the apartment building for the shots fired call, ensure officer safety as top priority",
                        "Approach apartment 3B with backup and announce police presence",
                        "Assess the situation upon hearing yelling — determine if there is an immediate threat to life",
                        "Document the male's physical condition and demeanor when he answers the door",
                        "Note the smell of marijuana and observation of the handgun on the coffee table from the doorway"
                    ],
                    "E": [
                        "Evaluate whether exigent circumstances exist based on the shots fired call and yelling",
                        "The warrantless entry must be justified — shots fired call plus yelling may create exigent circumstances",
                        "If entry is justified, secure the scene and the firearm for officer safety",
                        "Limit the protective sweep to areas where a person could be hiding who poses a danger",
                        "Document the exact basis for exigent circumstances entry in detail",
                        "Recognize that the cocaine found during protective sweep may face suppression challenges"
                    ],
                    "A": [
                        "Analyze the legality of the warrantless entry — pushing past the resident requires justification",
                        "Exigent circumstances analysis: shots fired call + yelling may justify entry to check for injured persons",
                        "Plain view doctrine: the handgun visible from the doorway may be lawfully seized if officer is lawfully positioned",
                        "Miranda must be administered before any custodial interrogation of the arrested male",
                        "Document the sequence of events precisely — what was seen, heard, and done in order",
                        "The ammunition in the bedroom closet is most vulnerable to suppression — protective sweep must be justified"
                    ],
                    "C": [
                        "Interview responding officers about what they heard (shots, yelling) before entry",
                        "Canvass other apartment residents to corroborate shots fired call and any disturbance",
                        "Identify the original 911 caller and obtain their statement about shots fired",
                        "Interview building security or management about any prior incidents at apartment 3B",
                        "Separate any other persons found in the apartment and interview individually"
                    ],
                    "T": [
                        "Document the exact sequence: arrival, hearing yelling, knocking, door answered, observations from doorway",
                        "Record exact position from which handgun was observed (standing at threshold, visible on coffee table)",
                        "Document the marijuana odor and its detectability from the doorway",
                        "Photograph the interior from the doorway showing the coffee table and handgun placement",
                        "Document the protective sweep path and what was observed in each room",
                        "Record all actions in case report with precise timeline",
                        "Secure and review body-worn camera footage — this will be critical for suppression hearing"
                    ],
                    "I": [
                        "Secure the handgun from the coffee table under plain view doctrine",
                        "The cocaine found during protective sweep — document exact location and circumstances of discovery",
                        "The ammunition in the bedroom closet — document whether closet was open or required opening",
                        "Photograph all evidence in place before collection",
                        "Process evidence for fingerprints and DNA as appropriate",
                        "Maintain strict chain of custody for all seized items",
                        "Recognize that evidence beyond the plain view handgun may be challenged and suppressed"
                    ],
                    "O": [
                        "Consult ASA immediately regarding suppression issues with the evidence",
                        "Legal analysis: plain view seizure of the handgun is strongest if officer was lawfully at the doorway",
                        "Legal analysis: cocaine found during protective sweep depends on whether sweep was justified",
                        "Legal analysis: ammunition in bedroom closet is most vulnerable — was closet within scope of protective sweep?",
                        "Recommend obtaining a search warrant BEFORE expanding the search beyond the protective sweep",
                        "Should have frozen the scene and obtained a warrant after securing the handgun and any persons",
                        "Ensure 4th Amendment analysis is thoroughly documented for prosecution"
                    ],
                    "N": [
                        "Prepare for suppression hearing — body-worn camera footage will be critical",
                        "Brief ASA on the strength and weaknesses of each piece of evidence",
                        "Conduct LEADS and CLEAR checks on the apartment resident",
                        "Check firearm serial number through LEADS for stolen status",
                        "Submit narcotics for lab analysis",
                        "Document lessons learned: should have secured visible weapon, ensured safety, then obtained warrant for full search",
                        "Prepare case file noting which evidence is most likely admissible vs. at risk of suppression"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Ensure EMS/CFD respond to treat three gunshot victims — prioritize life-saving efforts",
                        "DOA victim: confirm deceased suspect is pronounced and the body is not moved without ME authorization",
                        "Critical victim: document condition, request trauma center transport, assign detective to hospital for dying declaration if applicable",
                        "Non-life-threatening victim: document injuries, obtain preliminary statement once medically stable",
                        "Request Medical Examiner response for DOA victim",
                        "Ensure officer safety upon arrival — multiple firearms involved, suspects may still be in area"
                    ],
                    "E": [
                        "Speak with responding officers and scene supervisor for initial briefing on arrival conditions",
                        "Establish wide inner perimeter around the shooting location — shell casings from multiple firearms indicate large scene",
                        "Establish outer perimeter covering the block and surrounding area where vehicle fled",
                        "Assign uniformed officers to secure all approach points to the corner",
                        "Deploy additional units and K-9 for area search for fleeing vehicle and possible additional suspects",
                        "Establish detective command post away from the crowd",
                        "Separate surviving victims from each other immediately — different hospitals if possible",
                        "Identify and document the gang territory and significance of the corner location"
                    ],
                    "A": [
                        "If fleeing vehicle or suspects are located, coordinate tactical apprehension with appropriate units",
                        "Surviving victims are both witnesses and potential suspects — assess involvement carefully",
                        "If victims are also offenders (mutual combat), advise Miranda prior to any custodial interrogation",
                        "Investigate whether victims were armed — recovered firearms may indicate mutual combat",
                        "Document any spontaneous statements by victims at scene or hospital",
                        "Photograph all victims' injuries, tattoos, and gang-related markings",
                        "Complete TRR documentation if any armed confrontation with police occurred"
                    ],
                    "C": [
                        "Recognize uncooperative witnesses are common in gang-related cases — do not be deterred",
                        "Identify persons who scattered when police arrived — area canvass for reluctant witnesses",
                        "Obtain the cell phone video posted to social media — preserve it immediately before account is deleted",
                        "Identify the anonymous social media account that posted the video through legal process",
                        "Conduct extensive neighborhood canvass including residences, businesses, and passing vehicles",
                        "Check for surveillance cameras on surrounding buildings, traffic cameras, and POD cameras",
                        "Interview surviving victims separately, even if claiming they saw nothing",
                        "Contact gang intelligence unit for information on ongoing disputes over this territory"
                    ],
                    "T": [
                        "Photograph entire scene from multiple angles before any evidence is moved",
                        "Document all shell casing locations with evidence markers and measurements",
                        "Document evidence indicating multiple shooters (different caliber casings, different locations)",
                        "Record all actions in case report and Felony 101",
                        "Log all evidence into PCAD with detailed descriptions",
                        "Preserve the social media video URL, screenshot with timestamps, and download the video",
                        "Document gang graffiti in the area and its significance to the territorial dispute",
                        "Review and secure all responding officers' body-worn camera footage",
                        "Document vehicle description and direction of flight"
                    ],
                    "I": [
                        "Collect and preserve all shell casings with precise location documentation",
                        "Recover and preserve any firearms found at the scene or on victims",
                        "Request Forensic Services Division for complete scene processing",
                        "Request ballistics comparison on all recovered casings and firearms through NIBIN",
                        "Request gunshot residue testing on all three victims and any suspects",
                        "Process the area for DNA evidence including blood evidence from each victim",
                        "Secure victims' cell phones for forensic extraction (call records, messages, location data)",
                        "Preserve the social media video as evidence — request legal hold from the platform",
                        "Maintain strict chain of custody for all evidence across this complex scene"
                    ],
                    "O": [
                        "Notify ASA regarding homicide and aggravated battery circumstances",
                        "Consult ASA regarding charges — assess potential mutual combatant situation",
                        "Request search warrants for victims' and suspects' cell phone data extraction",
                        "Request search warrant or legal process for social media platform to identify anonymous poster",
                        "Request subpoena for social media account records, IP addresses, and viewer data",
                        "Conduct LEADS and CLEAR background checks on all victims and persons of interest",
                        "Ensure 4th Amendment compliance with all digital evidence collection",
                        "Coordinate with COPA if any officer use of force occurred",
                        "Request Medical Examiner for autopsy of DOA victim"
                    ],
                    "N": [
                        "Issue flash message with fleeing vehicle description and any suspect information",
                        "Coordinate with gang intelligence unit on territory dispute and potential retaliation threats",
                        "Monitor for retaliatory violence — request increased patrols in affected areas",
                        "Cross-reference social media video viewers and commenters for potential witness identification",
                        "Monitor social media for additional posts, threats, or information about the shooting",
                        "Refer all media inquiries to Office of Communications",
                        "Avoid public disclosure that could compromise investigation or endanger witnesses",
                        "Prepare complete case file and coordinate follow-up investigation",
                        "Consider safety planning for any cooperative witnesses"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Respond with sensitivity appropriate for an 8-year-old child victim",
                        "Ensure Maria receives medical assessment for bruises on upper arms and back",
                        "Document Maria's visible injuries with photographs (with appropriate consent/procedures for a minor)",
                        "Assess whether Maria is in immediate danger if returned to her home",
                        "Coordinate with school nurse or medical professional for initial injury documentation",
                        "Ensure Maria's emotional well-being is prioritized throughout the investigation"
                    ],
                    "E": [
                        "Coordinate with DCFS investigator to establish parallel investigation protocols",
                        "Determine whether the home needs to be secured as a potential crime scene",
                        "Establish a safe, child-friendly interview environment at the school or CAC (Children's Advocacy Center)",
                        "Identify all individuals with access to Maria in the household: mother and mother's boyfriend",
                        "Review DCFS hotline history for prior reports on this family",
                        "Identify Maria's teacher as a mandated reporter and first disclosure witness"
                    ],
                    "A": [
                        "Identify the primary suspect — assess whether injuries are consistent with abuse by an adult",
                        "Interview mother's boyfriend separately regarding his interactions with Maria and explanation for injuries",
                        "Interview mother separately about her knowledge of the injuries and boyfriend's behavior",
                        "If probable cause develops for Aggravated Battery to a Child (720 ILCS 5/12-3.05), arrest and advise Miranda",
                        "Conduct electronically recorded interrogation of suspect",
                        "Document any spontaneous statements made by suspects",
                        "Photograph suspect's hands and body for evidence of striking"
                    ],
                    "C": [
                        "Conduct forensic interview of Maria at a Children's Advocacy Center with trained forensic interviewer",
                        "Do NOT conduct multiple interviews of Maria — one properly conducted forensic interview",
                        "Use age-appropriate, non-leading questions during the interview",
                        "Interview the teacher who reported the abuse — document exactly what Maria said and what was observed",
                        "Interview school counselor, other teachers, and staff about Maria's behavior changes and academic decline",
                        "Interview neighbors about the household dynamics and any observed or heard incidents",
                        "Interview mother about relationship with boyfriend, any prior violence, and Maria's daily care",
                        "Check with Maria's pediatrician for prior injury history"
                    ],
                    "T": [
                        "Photograph Maria's injuries with and without scale ruler (following CPD protocol for minor victims)",
                        "Document the inconsistency between injuries and the 'fell down stairs' explanation",
                        "Document Maria's behavioral indicators: flinching when touched, withdrawal, academic decline",
                        "Record all investigative actions in case report following child abuse investigation protocol",
                        "Document coordination with DCFS including case worker name, DCFS case number, and shared findings",
                        "Preserve all school records documenting attendance, behavior changes, and prior concerns",
                        "Document the forensic interview — video recording is standard at CACs"
                    ],
                    "I": [
                        "Arrange comprehensive medical examination by a child abuse specialist/pediatrician",
                        "Request full-body examination to identify any additional injuries including old/healing injuries",
                        "Medical imaging (X-rays) to check for prior fractures indicating pattern of abuse",
                        "Photograph and preserve any physical evidence from the home if a search is conducted",
                        "Collect and preserve Maria's medical records from the examination",
                        "Document any objects in the home consistent with causing the observed injuries",
                        "Maintain chain of custody for all evidence including medical records and photographs"
                    ],
                    "O": [
                        "Notify ASA regarding child abuse investigation and developing probable cause",
                        "Consult ASA on appropriate charges: Aggravated Battery to a Child, Domestic Battery, Child Endangerment",
                        "Coordinate with DCFS on safety plan and potential removal of Maria from the home",
                        "Request search warrant for the residence if consent is not given by the mother",
                        "Conduct LEADS and CLEAR checks on mother's boyfriend for prior violent offenses or child abuse history",
                        "Ensure compliance with mandated reporting requirements",
                        "Coordinate with juvenile court if DCFS seeks emergency custody"
                    ],
                    "N": [
                        "Coordinate with DCFS on immediate safety plan for Maria — determine if she can safely return home",
                        "If boyfriend is arrested, coordinate with DCFS on whether Maria remains with mother",
                        "Connect family with victim services and child protection resources",
                        "Prepare complete case file for felony review and charging decision",
                        "Follow up with school regarding ongoing monitoring of Maria's condition",
                        "Schedule follow-up medical examination to document healing pattern",
                        "Coordinate with ASA on court preparation and testimony of child witness",
                        "Document all interagency coordination for case file"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "This scenario focuses on legal analysis of the confession — not a crime scene response",
                        "Assess the circumstances of the arrest: eyewitness identification for home invasion",
                        "Document John's physical and mental condition upon arrival at the station",
                        "Ensure John is provided with basic necessities (food, water, restroom) during the interview process"
                    ],
                    "E": [
                        "Analyze the legal sufficiency of the Miranda advisement and waiver",
                        "Identify the critical legal issue: John's ambiguous statement 'maybe I should have a lawyer'",
                        "Under Davis v. United States, 'maybe I should have a lawyer' is an ambiguous invocation",
                        "However, best practice is to clarify the ambiguity rather than continue questioning",
                        "The detective's response encouraging John to talk without a lawyer is problematic"
                    ],
                    "A": [
                        "John's statement 'maybe I should have a lawyer' should have triggered clarification, not encouragement to waive",
                        "The detective's response 'we have strong evidence and this is your chance to tell your side' is coercive and suggestive",
                        "This response could be viewed as overcoming John's will and renders the waiver potentially involuntary",
                        "When John asked to stop ('I'm tired, can we do this tomorrow?'), this was an invocation of the right to silence",
                        "Under Michigan v. Mosley, once a suspect invokes the right to silence, questioning must cease",
                        "Continuing to question after the request to stop violates Miranda — 'we're almost done' is not sufficient",
                        "All statements obtained after the invocation of silence are likely inadmissible"
                    ],
                    "C": [
                        "No witness collection applies in this analysis scenario",
                        "However, document who was present during the interrogation",
                        "Identify the interrogating detective(s) and any observers",
                        "Obtain statements from all personnel present during the interview about the sequence of events"
                    ],
                    "T": [
                        "The 4-hour interview with only one bathroom break and no food raises voluntariness concerns",
                        "Document the exact timeline: when Miranda was read, when each statement was made",
                        "Document John's exact words regarding wanting a lawyer and wanting to stop",
                        "Document the detective's exact responses to John's requests",
                        "The interview should have been electronically recorded (required for home invasion cases in Illinois)",
                        "If recorded, the recording itself will demonstrate the Miranda issues",
                        "If not recorded, this is a separate violation under 725 ILCS 5/103-2.1"
                    ],
                    "I": [
                        "Preserve the interrogation recording as evidence",
                        "Document the physical conditions of the interview room",
                        "Preserve any written waiver forms signed by John",
                        "Document John's physical condition before and after the interview"
                    ],
                    "O": [
                        "Consult ASA regarding admissibility of the confession — it faces serious suppression challenges",
                        "Legal analysis: ambiguous invocation of counsel — confession after encouragement to waive is vulnerable",
                        "Legal analysis: invocation of right to silence — all statements after 'can we do this tomorrow?' are likely inadmissible",
                        "Legal analysis: voluntariness — 4 hours, minimal breaks, no food, detective overriding requests to stop",
                        "Even if the initial confession survives, the additional details after invoking silence will be suppressed",
                        "ASA should assess whether the case can proceed on the eyewitness identification alone",
                        "Ensure 5th and 6th Amendment protections are documented for suppression hearing",
                        "Recommend retraining on proper Miranda procedures and recognizing invocations"
                    ],
                    "N": [
                        "Prepare for suppression motion — defense will almost certainly challenge this confession",
                        "Document what evidence exists independent of the confession (eyewitness identification)",
                        "Determine if the case is viable without the confession",
                        "Brief supervisors on the Miranda issues and potential impact on prosecution",
                        "Use this case as a training example for proper interrogation procedures",
                        "Ensure future interrogations properly address ambiguous Miranda invocations",
                        "Prepare complete case file documenting the legal issues for the prosecution team"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Ensure the shot subject receives immediate medical attention — EMS/CFD response for life-saving measures",
                        "Confirm deceased subject is pronounced and request Medical Examiner response",
                        "Assess Officer Davis's physical and emotional condition — check for injuries",
                        "Ensure Officer Davis is removed from the immediate scene but do NOT release from duty",
                        "Provide Officer Davis access to FOP/PBA representative per CPD policy",
                        "Document Officer Davis's and Officer Kim's physical conditions including any injuries"
                    ],
                    "E": [
                        "Speak with scene supervisor for initial briefing on arrival conditions",
                        "Establish wide perimeter around the alley including the foot pursuit route",
                        "Secure the shooting scene — do NOT allow anyone to alter the location",
                        "Separate Officer Davis and Officer Kim immediately — do not let them discuss the incident",
                        "Remove the subject's family from the immediate scene but obtain contact information",
                        "Establish detective command post separate from the scene",
                        "Assign officers to secure the crowd and manage family members",
                        "Notify COPA immediately — COPA has jurisdiction over officer-involved shootings"
                    ],
                    "A": [
                        "Officer Davis is NOT a suspect at this stage but is a principal in the investigation",
                        "Officer Davis has the right to a 24-hour review period before giving a formal statement (per collective bargaining)",
                        "Do NOT interrogate Officer Davis on scene — obtain only public safety information initially",
                        "Advise Officer Davis of his Garrity rights if compelled statement is required",
                        "Document Officer Davis's spontaneous statements at the scene, if any",
                        "Do NOT force Officer Davis to surrender his weapon on scene — follow CPD protocol for turn-in",
                        "Complete TRR (Tactical Response Report) documentation"
                    ],
                    "C": [
                        "Locate and interview the civilian witness who claims she saw the shooting from her window",
                        "Conduct detailed interview: what exactly did she see, from what angle, distance, and lighting conditions",
                        "Interview Officer Kim separately about what he heard, saw, and his position during the incident",
                        "Canvass the alley and surrounding buildings for additional witnesses",
                        "Check for surveillance cameras covering the alley from nearby buildings or businesses",
                        "Obtain body-worn camera footage from both Officer Davis and Officer Kim",
                        "Canvass for any witnesses who observed the initial encounter or foot pursuit",
                        "Instruct all witnesses to preserve independent recollection and not discuss with others"
                    ],
                    "T": [
                        "Photograph entire alley scene from multiple angles before any evidence is moved",
                        "Document the exact location where the shooting occurred and where the subject fell",
                        "Document the distance between Officer Davis's position and the subject",
                        "Document Officer Kim's position (20 yards behind) relative to the shooting",
                        "Document the civilian witness's apartment window — line of sight, distance, angle, and lighting",
                        "Photograph the subject's body and hands (no gun recovered — document empty hands)",
                        "Document the foot pursuit path from origin to the shooting location",
                        "Record all actions in case report with precise timeline",
                        "Preserve and review all body-worn camera footage immediately"
                    ],
                    "I": [
                        "Conduct thorough search of the alley for any weapon — expand search area significantly",
                        "Check dumpsters, rooftops, behind objects, and along the foot pursuit route for a discarded weapon",
                        "Recover and preserve Officer Davis's firearm and count remaining ammunition",
                        "Collect and preserve all shell casings and projectiles",
                        "Request gunshot residue testing on the subject's hands",
                        "Request Forensic Services Division for complete scene processing",
                        "Request ballistics analysis on Officer Davis's weapon and recovered projectiles",
                        "Preserve the subject's clothing and personal effects",
                        "Preserve all digital evidence including body-worn camera footage and radio transmissions",
                        "Maintain strict chain of custody for all evidence"
                    ],
                    "O": [
                        "Notify COPA immediately — COPA investigates all officer-involved shooting deaths",
                        "Notify ASA regarding the homicide circumstances",
                        "Coordinate with COPA investigators who will conduct the independent investigation",
                        "Notify the department's Office of the Superintendent",
                        "Ensure Officer Davis has legal representation (FOP/PBA attorney)",
                        "Ensure 4th Amendment compliance with all searches of the alley and surrounding area",
                        "Request Medical Examiner for autopsy and cause/manner of death determination",
                        "Consult with department legal counsel regarding public statements and family notification"
                    ],
                    "N": [
                        "Prepare for significant public and media scrutiny — refer all inquiries to Office of Communications",
                        "Coordinate family notification through proper channels with chaplain services if available",
                        "Assign Officer Davis to administrative duty pending investigation",
                        "Monitor media coverage and social media for witness information or additional evidence",
                        "The missing gun is the critical issue — continue exhaustive search of the entire pursuit route",
                        "Consider whether the subject may have discarded a weapon during the foot pursuit",
                        "Cross-reference the subject's background for prior weapons offenses",
                        "Prepare complete case file for COPA, ASA, and department review",
                        "Coordinate with community affairs regarding public concerns"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Ensure officer safety during the traffic stop — maintain tactical positioning",
                        "Document the basis for the initial traffic stop: broken taillight (valid traffic violation)",
                        "Assess the driver's condition: extreme nervousness, sweating, shaking hands, avoiding eye contact",
                        "Document all observations of the driver's behavior and demeanor",
                        "Note the indicators observed in the vehicle: fast food wrappers, energy drinks, strong air freshener"
                    ],
                    "E": [
                        "Evaluate whether the totality of circumstances creates reasonable suspicion beyond the traffic violation",
                        "Nervousness alone does not establish reasonable suspicion (Illinois v. Wardlow considerations)",
                        "Multiple indicators together (nervousness, air freshener masking odor, long-distance travel, fast food suggesting non-stop driving) may support reasonable suspicion",
                        "Under Rodriguez v. United States (2015), a traffic stop cannot be extended beyond its purpose without reasonable suspicion",
                        "You CANNOT extend the stop 15 minutes solely to wait for K-9 without independent reasonable suspicion",
                        "Complete the traffic stop purpose (citation/warning for taillight) within a reasonable time"
                    ],
                    "A": [
                        "Determine whether you have reasonable suspicion of criminal activity beyond the traffic violation",
                        "If reasonable suspicion exists, you may briefly extend the stop for K-9 — but 15 minutes may exceed reasonable",
                        "If K-9 alerts, this provides probable cause for vehicle search under the automobile exception",
                        "Without K-9 alert, you need consent or probable cause to search the vehicle",
                        "You may ask for consent to search — driver can refuse without consequence",
                        "If consent is given, document the voluntary nature and scope of consent",
                        "If drugs are found, advise Miranda prior to any custodial interrogation"
                    ],
                    "C": [
                        "Ask the driver open-ended questions about his travel: where from, where going, purpose of trip",
                        "Note inconsistencies in the driver's story compared to observable evidence",
                        "Document the driver's answers and demeanor during questioning",
                        "If passengers are present, separate and interview individually",
                        "Verify the driver's stated travel route against GPS or phone data if search is lawful"
                    ],
                    "T": [
                        "Document all observations in detail: driver's behavior, vehicle interior observations, odors detected",
                        "Record the precise timeline of the stop from initiation to completion",
                        "Document the legal basis for any extension of the stop beyond the traffic violation",
                        "If K-9 is called, document the time of request, K-9 arrival time, and whether stop was complete before K-9",
                        "Body-worn camera footage is critical — ensure it captures all interactions and observations",
                        "Document the driver's valid license and clean record",
                        "Record all actions in case report with precise timeline showing stop duration"
                    ],
                    "I": [
                        "If K-9 alerts, search the vehicle pursuant to the automobile exception (Carroll doctrine)",
                        "If drugs are found, photograph and document the location and quantity before collection",
                        "Field test suspected narcotics using NIK kit or approved presumptive test",
                        "Weigh and document all narcotics for charging purposes",
                        "Preserve packaging for fingerprints and additional evidence",
                        "Check the vehicle for hidden compartments if drug trafficking is suspected",
                        "Maintain chain of custody for all seized evidence"
                    ],
                    "O": [
                        "Legal framework: Rodriguez v. United States — traffic stop cannot be extended without reasonable suspicion",
                        "Legal framework: Illinois v. Caballes — K-9 sniff during a lawful stop does not violate 4th Amendment",
                        "The key question: can you develop reasonable suspicion DURING the lawful stop to justify the K-9 call?",
                        "Consult ASA regarding sufficiency of reasonable suspicion if stop is extended",
                        "If drugs are found, request search warrant for cell phone extraction to establish trafficking network",
                        "Conduct LEADS check on driver and vehicle for prior drug-related activity",
                        "Ensure all 4th Amendment requirements are met for the stop, extension, and any search"
                    ],
                    "N": [
                        "If arrest is made, conduct a full vehicle inventory search per CPD policy",
                        "Coordinate with DEA or narcotics unit if large quantity suggests trafficking",
                        "Check for outstanding warrants or prior drug offenses in other jurisdictions",
                        "If driver is released without charges, document all observations for intelligence purposes",
                        "Prepare case file documenting the legal basis for every action taken during the stop",
                        "Brief narcotics unit on potential drug trafficking route if indicators are strong",
                        "Follow up on any leads developed from the stop"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Respond to the business owner and assess their safety — are the threats ongoing?",
                        "Document the business owner's account of the threats and the timeline of events",
                        "Assess whether there is an immediate threat to the owner's safety or life",
                        "Document the vandalism damage to the business with photographs",
                        "Provide the owner with safety planning resources and contact information for victim services"
                    ],
                    "E": [
                        "Establish the vandalism scene and process it for evidence",
                        "Document the timeline: when threats started, when they stopped, when vandalism occurred (2 days after)",
                        "Identify whether the vandalism is linked to the threats — the timeline strongly suggests connection",
                        "Determine the type of business and whether there is a motive (extortion: 'pay up or face consequences')",
                        "Secure and preserve the business's own security cameras for vandalism footage"
                    ],
                    "A": [
                        "Once the anonymous sender is identified through digital investigation, develop probable cause for arrest",
                        "Charges may include Intimidation (720 ILCS 5/12-6), Criminal Damage to Property, and possibly Extortion",
                        "Advise Miranda prior to any custodial interrogation of the suspect",
                        "Conduct electronically recorded interrogation",
                        "Document any spontaneous statements",
                        "Photograph suspect and note any connection to the business or owner"
                    ],
                    "C": [
                        "Obtain detailed statement from the business owner about the threats and any suspected persons",
                        "Ask the owner about any disputes, disgruntled employees, competitors, or personal conflicts",
                        "Interview employees about any observations, suspicious persons, or conflicts with customers",
                        "Canvass neighboring businesses for witnesses to the vandalism",
                        "Check neighboring businesses' surveillance cameras for footage of the vandalism suspect",
                        "Review the threatening messages for any identifying information, language patterns, or personal knowledge"
                    ],
                    "T": [
                        "Preserve the screenshots of threatening emails and social media messages provided by the owner",
                        "Document the exact content, timestamps, and sender information for each threatening message",
                        "Photograph the vandalism damage to the business from multiple angles",
                        "Record all digital evidence with proper documentation of how it was obtained",
                        "Document the fake name and profile photo used on the social media account",
                        "Document the generic Gmail address used for email threats",
                        "Record all investigative actions in case report with detailed digital evidence chain"
                    ],
                    "I": [
                        "Preserve original email headers from the threatening emails — these contain IP address and routing information",
                        "Do NOT rely only on screenshots — obtain the original emails with full headers",
                        "Preserve the social media messages with metadata including timestamps and account information",
                        "Process the vandalism scene for physical evidence: fingerprints, DNA, tool marks, surveillance footage",
                        "Secure any physical evidence from the vandalism that may link to the threat-maker",
                        "Document and preserve all digital evidence with proper chain of custody",
                        "Consider forensic analysis of the threatening messages for linguistic patterns"
                    ],
                    "O": [
                        "Request search warrant for Gmail to obtain subscriber information, IP logs, and email metadata",
                        "Request search warrant or legal process for social media platform to identify the fake account holder",
                        "Request subscriber information, IP addresses, login records, and account creation details from social media platform",
                        "Issue preservation letters to both Gmail and the social media platform to prevent data deletion",
                        "Subpoena ISP records to trace IP addresses to a physical location or subscriber",
                        "Consult ASA regarding charges: Intimidation, Criminal Damage, Extortion",
                        "Ensure compliance with the Stored Communications Act (18 U.S.C. § 2703) for digital evidence requests",
                        "Obtain search warrant for suspect's devices once identified"
                    ],
                    "N": [
                        "Monitor for any new threatening messages or escalation of threats",
                        "Coordinate with the business owner on safety measures while investigation is ongoing",
                        "Cross-reference IP address information with known persons connected to the business",
                        "Check for similar threat patterns against other businesses in the area",
                        "Coordinate with cyber crime unit for technical assistance with digital evidence",
                        "Prepare complete case file linking the digital threats to the physical vandalism",
                        "Follow up with tech companies on legal process responses",
                        "Brief the owner on the investigation progress and safety recommendations"
                    ]
                }
            }),
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
            "answer": json.dumps({
                "modelAnswer": {
                    "R": [
                        "Respond to the apartment and assess the scene for any signs of foul play",
                        "Document the condition of the apartment as found — no signs of forced entry or struggle",
                        "Note that Sarah's car, purse, and phone are all still at the apartment — this is highly concerning",
                        "Classify this as a high-risk missing person: unusual behavior, personal belongings left behind, recent relationship conflict",
                        "Enter Sarah into LEADS/NCIC immediately as a missing/endangered person",
                        "Request additional resources based on the high-risk indicators"
                    ],
                    "E": [
                        "Treat the apartment as a potential crime scene even without visible signs of struggle",
                        "Secure the apartment and limit access until determination is made",
                        "Obtain consent from the roommate to search the apartment thoroughly",
                        "Document the apartment layout, condition of Sarah's belongings, and any items that seem out of place",
                        "Establish a timeline of Sarah's last known activities based on the roommate's account",
                        "Coordinate with district commander for resource allocation"
                    ],
                    "A": [
                        "The ex-boyfriend is a primary person of interest given the recent breakup and angry text messages",
                        "Locate and interview the ex-boyfriend — determine his whereabouts during the disappearance window",
                        "Assess the content and tone of his angry text messages for threats or escalation",
                        "If probable cause develops for foul play, arrest and advise Miranda",
                        "At this stage, interview the boyfriend voluntarily — do NOT make him custodial prematurely",
                        "Document his demeanor, cooperation level, and alibi information"
                    ],
                    "C": [
                        "Obtain detailed statement from the roommate about Sarah's recent behavior, state of mind, and the breakup",
                        "Interview the roommate about the ex-boyfriend: history of the relationship, any violence or controlling behavior",
                        "Interview Sarah's family members about her mental state and any concerns",
                        "Interview Sarah's coworkers and supervisor about her behavior at work and any issues",
                        "Canvass the apartment building and neighbors for any observations of Sarah or unusual visitors",
                        "Contact Sarah's friends and social circle for any information about her plans or communications",
                        "Interview the gas station clerk and obtain surveillance footage from Sarah's last known credit card purchase at 8 PM"
                    ],
                    "T": [
                        "Photograph the apartment documenting Sarah's personal items (purse, phone, car keys) left behind",
                        "Document the roommate's timeline of when Sarah was last seen or heard from",
                        "Document Sarah's last known activity: credit card purchase at gas station at 8 PM two days ago",
                        "Create a detailed timeline of Sarah's last 72 hours based on all available information",
                        "Document the angry text messages from the ex-boyfriend (content, dates, times)",
                        "Record all investigative actions in case report",
                        "Photograph and document Sarah's vehicle still in the parking lot"
                    ],
                    "I": [
                        "Process Sarah's phone for recent calls, texts, app usage, and location history",
                        "Process Sarah's purse contents for any clues about planned activities",
                        "Check Sarah's computer/laptop for recent internet activity, emails, and social media",
                        "Obtain gas station surveillance footage from the time of the credit card purchase",
                        "Process Sarah's vehicle for any evidence (was she in the vehicle? did someone else drive it?)",
                        "Obtain Sarah's bank and credit card records for any activity after the last known purchase",
                        "Check cell tower data for Sarah's phone location history",
                        "Preserve the ex-boyfriend's threatening text messages as evidence"
                    ],
                    "O": [
                        "Consult ASA regarding the threshold for transitioning from missing person to criminal investigation",
                        "Request search warrant for Sarah's phone data and digital accounts if needed beyond consent",
                        "Request search warrant for ex-boyfriend's phone records and location data",
                        "Request preservation orders for Sarah's social media, email, and cloud storage accounts",
                        "Subpoena cell carrier records for both Sarah's and the ex-boyfriend's phones for location data",
                        "Conduct LEADS and CLEAR checks on the ex-boyfriend for prior domestic violence or stalking",
                        "Request search warrant for gas station surveillance footage if not voluntarily provided"
                    ],
                    "N": [
                        "Issue BOLO with Sarah's description, photo, and vehicle information",
                        "Distribute missing person flyer to all districts and neighboring jurisdictions",
                        "Check area hospitals and morgues for any unidentified persons matching Sarah's description",
                        "Monitor Sarah's financial accounts for any new activity",
                        "Monitor Sarah's social media accounts for any login activity or new posts",
                        "Coordinate with media for public appeal if family consents",
                        "Check ride-share apps (Uber, Lyft) for any trips from Sarah's location",
                        "Continue expanding the investigation as a potential criminal case given the high-risk indicators",
                        "Brief supervisors and request additional investigative resources as needed"
                    ]
                }
            }),
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
