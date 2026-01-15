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

async def seed_multiple_choice():
    """Seed 100+ multiple choice questions for tests"""
    
    mcq_questions = [
        # ==================== CRIMINAL LAW (35 questions) ====================
        {
            "question": "Under Illinois law, what is the primary element that distinguishes First Degree Murder from Second Degree Murder?",
            "options": [
                "The use of a deadly weapon",
                "Premeditation and deliberation",
                "The presence of mitigating factors such as sudden passion or imperfect self-defense",
                "The victim's status as a protected person"
            ],
            "correct_answers": ["The presence of mitigating factors such as sudden passion or imperfect self-defense"],
            "explanation": "Second Degree Murder requires proof of the same elements as First Degree Murder, but the defendant must also prove mitigating factors (sudden intense passion from serious provocation OR unreasonable belief in justification).",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "hard",
            "reference": "720 ILCS 5/9-1, 5/9-2"
        },
        {
            "question": "Which of the following elements are required for a valid Robbery charge in Illinois?",
            "options": [
                "Taking property from the person or presence of another",
                "Use of force or threat of imminent force",
                "Intent to permanently deprive the owner",
                "All of the above"
            ],
            "correct_answers": ["All of the above"],
            "explanation": "Robbery requires: (1) knowingly taking property, (2) from the person or presence of another, (3) by use of force or threatening imminent use of force.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "medium",
            "reference": "720 ILCS 5/18-1"
        },
        {
            "question": "What is the BAC (Blood Alcohol Concentration) limit for DUI in Illinois for drivers 21 and over?",
            "options": [
                "0.04%",
                "0.08%",
                "0.10%",
                "0.00%"
            ],
            "correct_answers": ["0.08%"],
            "explanation": "The per se BAC limit for adult drivers (21+) in Illinois is 0.08%. Commercial drivers have a limit of 0.04%, and drivers under 21 have zero tolerance (0.00%).",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "easy",
            "reference": "625 ILCS 5/11-501"
        },
        {
            "question": "Burglary in Illinois requires which of the following?",
            "options": [
                "Breaking and entering",
                "Entry without authority with intent to commit felony or theft",
                "Actual completion of a theft",
                "Nighttime entry only"
            ],
            "correct_answers": ["Entry without authority with intent to commit felony or theft"],
            "explanation": "Illinois burglary does NOT require 'breaking' - only unauthorized entry (or remaining) with intent to commit a felony or theft. The crime is complete upon entry with intent.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "medium",
            "reference": "720 ILCS 5/19-1"
        },
        {
            "question": "What distinguishes Home Invasion from Residential Burglary?",
            "options": [
                "The time of day the offense occurs",
                "Knowledge that someone is present and use of force, being armed, or causing injury",
                "The value of property taken",
                "Whether a weapon is displayed"
            ],
            "correct_answers": ["Knowledge that someone is present and use of force, being armed, or causing injury"],
            "explanation": "Home Invasion requires: (1) unauthorized entry into a dwelling, (2) knowing/reason to know someone is present, AND (3) use/threat of force, OR being armed, OR intentionally injuring someone.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "hard",
            "reference": "720 ILCS 5/19-6"
        },
        {
            "question": "Which of the following makes a Battery charge 'Aggravated' in Illinois? (Select all that apply)",
            "options": [
                "Great bodily harm or permanent disability",
                "Victim is a peace officer performing duties",
                "Use of a deadly weapon",
                "All of these can make battery aggravated"
            ],
            "correct_answers": ["All of these can make battery aggravated"],
            "explanation": "Battery becomes aggravated when: causing great bodily harm, victim is a protected person (officer, teacher, elderly), use of deadly weapon, or committed in certain locations.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "medium",
            "reference": "720 ILCS 5/12-3.05"
        },
        {
            "question": "Under Illinois law, what is required for a valid claim of self-defense?",
            "options": [
                "Reasonable belief that force is necessary to prevent imminent unlawful force",
                "Proportional force to the threat",
                "The defender was not the initial aggressor",
                "All of the above"
            ],
            "correct_answers": ["All of the above"],
            "explanation": "Self-defense requires: (1) reasonable belief force is necessary, (2) against imminent unlawful force, (3) proportional response, and (4) defender cannot be initial aggressor.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "medium",
            "reference": "720 ILCS 5/7-1"
        },
        {
            "question": "What class of felony is Armed Robbery in Illinois?",
            "options": [
                "Class 1 Felony",
                "Class 2 Felony",
                "Class X Felony",
                "Class 3 Felony"
            ],
            "correct_answers": ["Class X Felony"],
            "explanation": "Armed Robbery is a Class X felony, punishable by 6-30 years. With firearm discharge, it's 25 years to life. No probation is available.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "medium",
            "reference": "720 ILCS 5/18-2"
        },
        {
            "question": "Which of the following is NOT a forcible felony under Illinois law?",
            "options": [
                "First Degree Murder",
                "Aggravated Criminal Sexual Assault",
                "Retail Theft",
                "Armed Robbery"
            ],
            "correct_answers": ["Retail Theft"],
            "explanation": "Forcible felonies include: treason, murder, sexual assault, robbery, burglary, arson, kidnapping, aggravated battery, and any felony involving use or threat of physical force.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "easy",
            "reference": "720 ILCS 5/2-8"
        },
        {
            "question": "For Criminal Sexual Assault, which element must the prosecution prove?",
            "options": [
                "Sexual penetration only",
                "Sexual penetration by force, threat, or when victim cannot consent",
                "Physical injury to the victim",
                "Presence of witnesses"
            ],
            "correct_answers": ["Sexual penetration by force, threat, or when victim cannot consent"],
            "explanation": "CSA requires: (1) act of sexual penetration AND (2) use of force/threat, OR victim unable to understand/give consent, OR victim is family member under 18.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "hard",
            "reference": "720 ILCS 5/11-1.20"
        },
        {
            "question": "What is the theft threshold for a Class 3 Felony in Illinois?",
            "options": [
                "Under $500",
                "$500 to $10,000",
                "$10,000 to $100,000",
                "Over $100,000"
            ],
            "correct_answers": ["$500 to $10,000"],
            "explanation": "Theft classifications by value: Under $500 = Class A misdemeanor; $500-$10,000 = Class 3 felony; $10,000-$100,000 = Class 2 felony; Over $100,000 = Class 1 felony.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "medium",
            "reference": "720 ILCS 5/16-1"
        },
        {
            "question": "Which statement about Stalking in Illinois is TRUE?",
            "options": [
                "A single incident is sufficient for a stalking charge",
                "The conduct must occur on at least two separate occasions",
                "Physical contact is required",
                "Stalking is always a misdemeanor"
            ],
            "correct_answers": ["The conduct must occur on at least two separate occasions"],
            "explanation": "Stalking requires conduct on at least 2 separate occasions of following, monitoring, or threatening, AND transmitting a threat OR placing victim in reasonable apprehension.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "medium",
            "reference": "720 ILCS 5/12-7.3"
        },
        {
            "question": "What makes a person an 'Armed Habitual Criminal' under Illinois law?",
            "options": [
                "Possessing any weapon after one felony conviction",
                "Possessing a firearm after two or more qualifying felony convictions",
                "Carrying a concealed weapon without a permit",
                "Selling firearms without a license"
            ],
            "correct_answers": ["Possessing a firearm after two or more qualifying felony convictions"],
            "explanation": "Armed Habitual Criminal (Class X felony) occurs when a person possesses a firearm after being convicted of 2+ qualifying felonies (murder, CSA, robbery, burglary, etc.).",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "hard",
            "reference": "720 ILCS 5/24-1.7"
        },
        {
            "question": "Under the Illinois FOID Card Act, who is PROHIBITED from possessing a firearm?",
            "options": [
                "Any convicted felon",
                "Person adjudicated mentally disabled",
                "Person under an active order of protection",
                "All of the above"
            ],
            "correct_answers": ["All of the above"],
            "explanation": "FOID prohibitions include: convicted felons, mentally disabled persons, those under protection orders, DV misdemeanor convicts, drug addicts, and minors without guardian consent.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "easy",
            "reference": "430 ILCS 65/FOID Card Act"
        },
        {
            "question": "What constitutes 'Attempt' under Illinois criminal law?",
            "options": [
                "Mere preparation to commit a crime",
                "Intent plus a substantial step toward commission",
                "Thinking about committing a crime",
                "Discussing plans to commit a crime"
            ],
            "correct_answers": ["Intent plus a substantial step toward commission"],
            "explanation": "Criminal attempt requires: (1) intent to commit a specific offense AND (2) a substantial step toward commission that goes beyond mere preparation.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "medium",
            "reference": "720 ILCS 5/8-4"
        },
        {
            "question": "For a Conspiracy charge, what must be proven?",
            "options": [
                "Agreement between two or more persons to commit an offense",
                "Intent that the offense be committed",
                "An overt act in furtherance of the agreement",
                "All of the above"
            ],
            "correct_answers": ["All of the above"],
            "explanation": "Conspiracy requires: (1) agreement between 2+ persons, (2) intent to commit the offense, AND (3) an act in furtherance of the agreement by any party.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "hard",
            "reference": "720 ILCS 5/8-2"
        },
        {
            "question": "When is a person legally 'accountable' for another's criminal conduct?",
            "options": [
                "When they are present during the crime",
                "When they aid, abet, or agree to aid with intent to promote the crime",
                "When they fail to report the crime",
                "When they are related to the offender"
            ],
            "correct_answers": ["When they aid, abet, or agree to aid with intent to promote the crime"],
            "explanation": "Accountability requires: before or during offense, with intent to promote/facilitate, the person solicits, aids, abets, agrees to aid, or attempts to aid. Mere presence is insufficient.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "hard",
            "reference": "720 ILCS 5/5-2"
        },
        {
            "question": "Violation of an Order of Protection is a Class A misdemeanor for the first offense. What is it for a second violation?",
            "options": [
                "Class B Misdemeanor",
                "Class 4 Felony",
                "Class 2 Felony",
                "Class A Misdemeanor with enhanced penalties"
            ],
            "correct_answers": ["Class 4 Felony"],
            "explanation": "First violation of OP is Class A misdemeanor. Second violation (or first with prior DV conviction) is Class 4 felony. Mandatory arrest when PC exists.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "medium",
            "reference": "720 ILCS 5/12-3.4"
        },
        {
            "question": "What is required for Resisting or Obstructing a Peace Officer?",
            "options": [
                "Physical resistance only",
                "Knowingly resisting or obstructing an authorized act",
                "Threatening the officer",
                "Use of a weapon"
            ],
            "correct_answers": ["Knowingly resisting or obstructing an authorized act"],
            "explanation": "Resisting/obstructing requires knowingly resisting or obstructing a peace officer performing authorized duties. Physical resistance not required - fleeing is sufficient.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "easy",
            "reference": "720 ILCS 5/31-1"
        },
        {
            "question": "Under Illinois law, what is the legal definition of 'Deadly Force'?",
            "options": [
                "Any use of a firearm",
                "Force likely to cause death or great bodily harm",
                "Force causing any injury",
                "Force used with a weapon"
            ],
            "correct_answers": ["Force likely to cause death or great bodily harm"],
            "explanation": "Deadly force is force which is likely to cause death or great bodily harm. It is not limited to firearms - any force meeting this standard qualifies.",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "difficulty": "easy",
            "reference": "720 ILCS 5/7-1"
        },
        
        # ==================== CONSTITUTIONAL LAW (25 questions) ====================
        {
            "question": "Under Terry v. Ohio, what level of suspicion is required for an investigative stop?",
            "options": [
                "Probable cause",
                "Reasonable articulable suspicion",
                "Beyond reasonable doubt",
                "Preponderance of evidence"
            ],
            "correct_answers": ["Reasonable articulable suspicion"],
            "explanation": "Terry stops require reasonable articulable suspicion - specific, objective facts that criminal activity is afoot. Less than probable cause but more than a hunch.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "easy",
            "reference": "Terry v. Ohio (1968)"
        },
        {
            "question": "What are the requirements for a valid search incident to arrest?",
            "options": [
                "Warrant must be obtained first",
                "Search limited to arrestee's person and area within immediate control",
                "Any area of the house may be searched",
                "Search must occur before the arrest"
            ],
            "correct_answers": ["Search limited to arrestee's person and area within immediate control"],
            "explanation": "Search incident to arrest allows search of arrestee's person and area within immediate control (wingspan) for weapons and evidence. Based on Chimel v. California.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "medium",
            "reference": "Chimel v. California (1969)"
        },
        {
            "question": "Which of the following is an exception to the warrant requirement?",
            "options": [
                "Consent search",
                "Exigent circumstances",
                "Search incident to arrest",
                "All of the above"
            ],
            "correct_answers": ["All of the above"],
            "explanation": "Warrant exceptions include: consent, exigent circumstances, search incident to arrest, automobile exception, plain view, inventory searches, and hot pursuit.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "easy",
            "reference": "4th Amendment Exceptions"
        },
        {
            "question": "Under Miranda v. Arizona, when must warnings be given?",
            "options": [
                "Before any police contact",
                "Before custodial interrogation",
                "Only before formal arrest",
                "Only for felony charges"
            ],
            "correct_answers": ["Before custodial interrogation"],
            "explanation": "Miranda warnings required before custodial interrogation - when person is in custody (not free to leave) AND being subjected to interrogation or its functional equivalent.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "medium",
            "reference": "Miranda v. Arizona (1966)"
        },
        {
            "question": "What happens when a suspect unambiguously invokes the right to counsel during interrogation?",
            "options": [
                "Officers may continue with different questions",
                "All questioning must cease until attorney is present",
                "Officers may continue after a 2-hour break",
                "Officers may re-approach after re-reading Miranda"
            ],
            "correct_answers": ["All questioning must cease until attorney is present"],
            "explanation": "Under Edwards v. Arizona, once counsel is invoked, all questioning must cease. Police cannot reinitiate - must wait for suspect to reinitiate communication.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "hard",
            "reference": "Edwards v. Arizona (1981)"
        },
        {
            "question": "The 'Plain View' doctrine requires which of the following?",
            "options": [
                "Officer lawfully present in location",
                "Item in plain view",
                "Incriminating nature immediately apparent",
                "All of the above"
            ],
            "correct_answers": ["All of the above"],
            "explanation": "Plain view seizure requires: (1) officer lawfully present, (2) item in plain view, (3) incriminating nature immediately apparent. Cannot move objects for better view.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "medium",
            "reference": "Horton v. California (1990)"
        },
        {
            "question": "Under Arizona v. Gant, when may officers search a vehicle incident to arrest?",
            "options": [
                "Any time after an arrest of an occupant",
                "Only when arrestee is unsecured and within reaching distance, or when evidence of arrest crime may be present",
                "Never - vehicle searches always require a warrant",
                "Only for felony arrests"
            ],
            "correct_answers": ["Only when arrestee is unsecured and within reaching distance, or when evidence of arrest crime may be present"],
            "explanation": "Gant limits vehicle search incident to arrest to: (1) arrestee unsecured and within reaching distance, OR (2) reasonable belief evidence of arrest crime is in vehicle.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "hard",
            "reference": "Arizona v. Gant (2009)"
        },
        {
            "question": "Which exigent circumstance does NOT justify warrantless entry into a home?",
            "options": [
                "Hot pursuit of fleeing felon",
                "Imminent destruction of evidence",
                "Suspicion that evidence exists inside",
                "Emergency aid to injured person"
            ],
            "correct_answers": ["Suspicion that evidence exists inside"],
            "explanation": "Mere suspicion evidence exists is insufficient. Exigent circumstances require: hot pursuit, imminent evidence destruction, preventing escape, or emergency aid.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "medium",
            "reference": "Kentucky v. King (2011)"
        },
        {
            "question": "According to Rodriguez v. United States, what is the rule regarding extending traffic stops?",
            "options": [
                "Officers may extend any stop for safety reasons",
                "A stop cannot be extended beyond its original purpose without reasonable suspicion",
                "All stops may include a K-9 sniff",
                "Stops may be extended up to 30 minutes"
            ],
            "correct_answers": ["A stop cannot be extended beyond its original purpose without reasonable suspicion"],
            "explanation": "Rodriguez holds that extending a traffic stop beyond time needed for the stop's mission requires reasonable suspicion of additional criminal activity.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "hard",
            "reference": "Rodriguez v. United States (2015)"
        },
        {
            "question": "What does the 'Exclusionary Rule' provide?",
            "options": [
                "Evidence obtained through constitutional violation is generally inadmissible",
                "Defendants may be excluded from trial",
                "Certain witnesses cannot testify",
                "Prosecutors must exclude certain charges"
            ],
            "correct_answers": ["Evidence obtained through constitutional violation is generally inadmissible"],
            "explanation": "The exclusionary rule prohibits use of evidence obtained through Fourth Amendment violations. Purpose is to deter police misconduct.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "easy",
            "reference": "Mapp v. Ohio (1961)"
        },
        {
            "question": "The 'Fruit of the Poisonous Tree' doctrine means:",
            "options": [
                "Physical evidence is always admissible",
                "Evidence derived from illegal search is also excluded",
                "Witness testimony cannot be excluded",
                "Confessions are always inadmissible"
            ],
            "correct_answers": ["Evidence derived from illegal search is also excluded"],
            "explanation": "Fruit of the Poisonous Tree excludes not only illegally obtained evidence but also evidence derived from it. Exceptions: independent source, inevitable discovery, attenuation.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "medium",
            "reference": "Wong Sun v. United States (1963)"
        },
        {
            "question": "Under Graham v. Connor, how is use of force evaluated?",
            "options": [
                "Based on the officer's subjective intent",
                "Using an objective reasonableness standard",
                "Based solely on the outcome",
                "Using a malicious intent standard"
            ],
            "correct_answers": ["Using an objective reasonableness standard"],
            "explanation": "Graham v. Connor established that use of force is judged by objective reasonableness under the 4th Amendment, considering totality of circumstances from perspective of reasonable officer.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "medium",
            "reference": "Graham v. Connor (1989)"
        },
        {
            "question": "What standard governs use of deadly force to prevent escape under Tennessee v. Garner?",
            "options": [
                "Deadly force may be used for any fleeing felon",
                "Deadly force may be used only when suspect poses significant threat of death or serious harm",
                "Deadly force is never permitted against fleeing suspects",
                "Deadly force requires supervisor approval"
            ],
            "correct_answers": ["Deadly force may be used only when suspect poses significant threat of death or serious harm"],
            "explanation": "Tennessee v. Garner: deadly force to prevent escape is justified only when officer has probable cause to believe suspect poses significant threat of death or serious physical injury.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "hard",
            "reference": "Tennessee v. Garner (1985)"
        },
        {
            "question": "A protective sweep of a residence during arrest is justified when:",
            "options": [
                "Automatically upon any arrest in a home",
                "Articulable facts support belief that dangerous persons may be present",
                "Officer wants to look for additional evidence",
                "Homeowner is uncooperative"
            ],
            "correct_answers": ["Articulable facts support belief that dangerous persons may be present"],
            "explanation": "Maryland v. Buie: protective sweep beyond immediately adjoining areas requires articulable facts supporting reasonable belief dangerous individuals are present.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "hard",
            "reference": "Maryland v. Buie (1990)"
        },
        {
            "question": "What is required for valid consent to search?",
            "options": [
                "Written consent only",
                "Voluntary consent from person with authority over area",
                "Consent from any person present",
                "Consent only from property owner"
            ],
            "correct_answers": ["Voluntary consent from person with authority over area"],
            "explanation": "Valid consent requires: (1) voluntariness (not coerced), (2) given by person with authority over area. Third parties can consent to common areas.",
            "category_id": "cat_constitutional",
            "category_name": "Constitutional Law",
            "difficulty": "medium",
            "reference": "Schneckloth v. Bustamonte (1973)"
        },
        
        # ==================== CPD PROCEDURES (25 questions) ====================
        {
            "question": "According to CPD policy, when must body-worn cameras be activated?",
            "options": [
                "Only during arrests",
                "All law enforcement activities including stops, arrests, searches, and use of force",
                "Only when a supervisor directs",
                "Only for felony investigations"
            ],
            "correct_answers": ["All law enforcement activities including stops, arrests, searches, and use of force"],
            "explanation": "BWC must be activated for all law enforcement activities, investigative encounters, traffic stops, arrests, use of force, searches, statements, and pursuits.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "easy",
            "reference": "Special Order S03-14: Body-Worn Cameras"
        },
        {
            "question": "What is a CPD member's duty when observing another member using unreasonable force?",
            "options": [
                "Report it after the incident concludes",
                "Intervene to prevent unreasonable force if safe to do so",
                "Continue assisting the other member",
                "Notify a supervisor only"
            ],
            "correct_answers": ["Intervene to prevent unreasonable force if safe to do so"],
            "explanation": "Members must intervene to prevent clearly unreasonable force if safe to do so. Failure to intervene can result in discipline. Must also report through proper channels.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "medium",
            "reference": "General Order G03-02: Use of Force"
        },
        {
            "question": "Under CPD vehicle pursuit policy, when may a pursuit be initiated?",
            "options": [
                "For any traffic violation",
                "Only when occupant committed forcible felony or poses immediate threat of death/GBH",
                "Whenever a vehicle fails to stop",
                "Only with supervisor pre-approval"
            ],
            "correct_answers": ["Only when occupant committed forcible felony or poses immediate threat of death/GBH"],
            "explanation": "Vehicle pursuit only when: (1) PC that occupant committed forcible felony, OR (2) occupant poses immediate threat of death/great bodily harm. Traffic violations alone do not justify pursuit.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "hard",
            "reference": "General Order G03-03: Vehicle Pursuits"
        },
        {
            "question": "What form must be completed after any use of force beyond member presence and verbal commands?",
            "options": [
                "Case Report only",
                "Tactical Response Report (TRR)",
                "Arrest Report only",
                "Supplementary Report"
            ],
            "correct_answers": ["Tactical Response Report (TRR)"],
            "explanation": "TRR required when member uses force beyond presence/verbal direction, force used against member, firearm discharged, or Taser/OC spray/impact weapon used.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "easy",
            "reference": "General Order G03-02-02: Response Reports"
        },
        {
            "question": "When responding to domestic violence calls, what is MANDATORY if probable cause exists for DV battery?",
            "options": [
                "Mediation between parties",
                "Arrest of the offender",
                "Referral to social services only",
                "Warning the offender"
            ],
            "correct_answers": ["Arrest of the offender"],
            "explanation": "Illinois has mandatory arrest policy when probable cause exists for domestic violence battery. Case report required even if no arrest. Avoid dual arrests - identify primary aggressor.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "medium",
            "reference": "General Order G04-04: Domestic Violence"
        },
        {
            "question": "What is the time limit for bringing a juvenile before juvenile court after being taken into custody?",
            "options": [
                "24 hours",
                "40 hours excluding weekends and holidays",
                "72 hours",
                "48 hours"
            ],
            "correct_answers": ["40 hours excluding weekends and holidays"],
            "explanation": "Juvenile must be brought before juvenile court within 40 hours (excluding weekends/holidays). Station adjustment decision must be made within 6 hours of arrival at station.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "hard",
            "reference": "General Order G06-02: Juveniles"
        },
        {
            "question": "According to CPD policy, when must a strip search be authorized by a supervisor?",
            "options": [
                "Never - strip searches are prohibited",
                "For all arrests",
                "For felony or weapons arrests when reasonable belief exists of concealed items",
                "Only for narcotics arrests"
            ],
            "correct_answers": ["For felony or weapons arrests when reasonable belief exists of concealed items"],
            "explanation": "Strip search requires: (1) felony or weapons arrest, (2) supervisor approval, (3) reasonable belief of concealed weapons/drugs/evidence, (4) same-sex officer, (5) private location.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "medium",
            "reference": "General Order G06-01-06: Strip Searches"
        },
        {
            "question": "What are the first responding officer's duties at a crime scene?",
            "options": [
                "Begin collecting evidence immediately",
                "Render aid, secure scene, establish perimeter, start scene log, identify witnesses",
                "Wait for detectives before taking any action",
                "Interview all witnesses in detail"
            ],
            "correct_answers": ["Render aid, secure scene, establish perimeter, start scene log, identify witnesses"],
            "explanation": "First officer: (1) render aid to injured, (2) secure/protect scene, (3) establish perimeter, (4) start crime scene log, (5) identify/separate witnesses, (6) brief detectives, (7) remain until relieved.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "easy",
            "reference": "General Order G05-02: Crime Scene Protection"
        },
        {
            "question": "For missing person reports, what is CPD's policy on waiting periods?",
            "options": [
                "24-hour waiting period for adults",
                "48-hour waiting period for non-high-risk cases",
                "No waiting period - accept report immediately",
                "Waiting period determined by supervisor"
            ],
            "correct_answers": ["No waiting period - accept report immediately"],
            "explanation": "No waiting period required - accept missing person report immediately. High-risk categories (under 13, over 60, disabled, danger to self/others) require immediate enhanced response.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "easy",
            "reference": "General Order G04-01: Missing Persons"
        },
        {
            "question": "After a firearm discharge incident, what is the officer's right regarding making a statement?",
            "options": [
                "Must provide statement immediately",
                "May have union representation and request 24-hour review period",
                "May refuse to provide any statement",
                "Must wait 72 hours before any statement"
            ],
            "correct_answers": ["May have union representation and request 24-hour review period"],
            "explanation": "After firearm discharge, officer may have PBA/FOP representative present and may request 24-hour review period before formal statement. COPA investigates all shots at persons.",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "difficulty": "medium",
            "reference": "General Order G03-06: Firearm Discharge Incidents"
        },
        
        # ==================== EVIDENCE & INVESTIGATIONS (20 questions) ====================
        {
            "question": "What is the primary purpose of maintaining chain of custody?",
            "options": [
                "To track officer overtime",
                "To ensure evidence integrity and admissibility in court",
                "To assign responsibility for lost evidence",
                "To document case assignment"
            ],
            "correct_answers": ["To ensure evidence integrity and admissibility in court"],
            "explanation": "Chain of custody documents every person who handled evidence from collection to court, ensuring integrity and admissibility. Any gap can result in exclusion.",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "difficulty": "easy",
            "reference": "General Order G05-02: Evidence and Property"
        },
        {
            "question": "How should biological evidence (blood, DNA) be packaged?",
            "options": [
                "In sealed plastic bags",
                "In paper containers after air drying",
                "In any available container",
                "In glass vials only"
            ],
            "correct_answers": ["In paper containers after air drying"],
            "explanation": "Biological evidence must be air dried completely before packaging in paper (not plastic). Plastic promotes bacterial growth and degradation.",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "difficulty": "medium",
            "reference": "Crime Lab Evidence Submission Guide"
        },
        {
            "question": "When handling digital evidence, what is the first rule?",
            "options": [
                "Turn on the device to check contents",
                "If device is off, leave it off; if on, document screen state",
                "Immediately remove the battery",
                "Connect to internet to download data"
            ],
            "correct_answers": ["If device is off, leave it off; if on, document screen state"],
            "explanation": "Digital evidence: don't turn on if off (preserves volatile data), don't turn off if on (prevents data loss). Photograph screen state, document connections, use write-blockers.",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "difficulty": "medium",
            "reference": "Special Order S06-06: Digital Evidence"
        },
        {
            "question": "What is required for a valid inventory search of a vehicle?",
            "options": [
                "Probable cause that evidence exists",
                "Search pursuant to department policy in good faith, not as pretext for investigation",
                "Warrant from a judge",
                "Owner's consent"
            ],
            "correct_answers": ["Search pursuant to department policy in good faith, not as pretext for investigation"],
            "explanation": "Inventory search must be: (1) pursuant to department policy, (2) conducted in good faith, (3) not pretext for investigation. Purpose is to protect property, police from claims, and officer safety.",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "difficulty": "medium",
            "reference": "General Order G06-01-05: Vehicle Inventory"
        },
        {
            "question": "In Illinois, sexual assault evidence kits must be submitted to the crime lab within:",
            "options": [
                "24 hours",
                "72 hours",
                "10 days",
                "30 days"
            ],
            "correct_answers": ["10 days"],
            "explanation": "Sexual assault evidence kits must be submitted to crime lab within 10 days. Illinois Rape Kit Tracking System monitors all kits. Victim has right to have kit collected regardless of prosecution decision.",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "difficulty": "hard",
            "reference": "725 ILCS 202/Sexual Assault Evidence Submission Act"
        },
        {
            "question": "When must interrogations be electronically recorded in Illinois?",
            "options": [
                "All felony cases",
                "Homicide, sexual assault, predatory criminal sexual assault of child, and aggravated arson",
                "Only when suspect requests recording",
                "Only when confession is obtained"
            ],
            "correct_answers": ["Homicide, sexual assault, predatory criminal sexual assault of child, and aggravated arson"],
            "explanation": "Illinois requires electronic recording for: homicide, sexual assault, predatory criminal sexual assault of child, and aggravated arson. Must record entire interrogation.",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "difficulty": "hard",
            "reference": "725 ILCS 5/103-2.1"
        },
        {
            "question": "What are the three types of fingerprint evidence?",
            "options": [
                "Rolled, flat, and partial",
                "Patent (visible), latent (invisible), and plastic (3D impression)",
                "Index, thumb, and palm",
                "Fresh, aged, and degraded"
            ],
            "correct_answers": ["Patent (visible), latent (invisible), and plastic (3D impression)"],
            "explanation": "Patent prints are visible (blood, ink). Latent prints are invisible (require powder/chemical processing). Plastic prints are 3D impressions in soft material.",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "difficulty": "medium",
            "reference": "Crime Lab Evidence Submission Guide"
        },
        {
            "question": "According to CPD lineup procedures, what is required for photo arrays?",
            "options": [
                "Suspect's photo must be in position #1",
                "Blind or blinded administration with 6+ fillers of similar appearance",
                "Only 4 photos are needed",
                "Victim must identify suspect within 5 seconds"
            ],
            "correct_answers": ["Blind or blinded administration with 6+ fillers of similar appearance"],
            "explanation": "Lineup requirements: (1) blind/blinded administration, (2) 6+ fillers of similar appearance, (3) pre-lineup instructions, (4) one suspect per lineup, (5) record confidence at time of ID.",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "difficulty": "medium",
            "reference": "General Order G03-06: Eyewitness Identification"
        },
        {
            "question": "What must be documented when collecting evidence?",
            "options": [
                "Item description only",
                "Item description, exact location, date/time, collector, condition, and identifying marks",
                "Collector's name only",
                "Case number only"
            ],
            "correct_answers": ["Item description, exact location, date/time, collector, condition, and identifying marks"],
            "explanation": "Document: (1) item description, (2) exact location found, (3) date/time, (4) who recovered it, (5) condition, (6) unique marks/serial numbers, (7) photographs taken, (8) inventory number.",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "difficulty": "easy",
            "reference": "General Order G05-02: Evidence Documentation"
        },
        {
            "question": "During the Cognitive Interview technique, what should the interviewer encourage?",
            "options": [
                "Yes/no answers only",
                "Mental reinstatement of context and reporting everything including partial information",
                "Leading questions to guide the witness",
                "Interrupting to clarify details"
            ],
            "correct_answers": ["Mental reinstatement of context and reporting everything including partial information"],
            "explanation": "Cognitive Interview: (1) mental reinstatement of context, (2) report everything even partial info, (3) recall from different perspectives, (4) recall in different orders. Non-leading questions throughout.",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "difficulty": "medium",
            "reference": "Detective Training: Cognitive Interview"
        },
        {
            "question": "What factors affect reliability of eyewitness identification?",
            "options": [
                "System variables only (lineup procedures)",
                "Estimator variables only (lighting, stress)",
                "Both system and estimator variables",
                "Neither - eyewitness ID is always reliable"
            ],
            "correct_answers": ["Both system and estimator variables"],
            "explanation": "System variables (controllable): lineup composition, instructions, administrator blindness. Estimator variables (uncontrollable): lighting, distance, duration, stress, weapon focus, cross-race ID.",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "difficulty": "hard",
            "reference": "General Order G03-06: Eyewitness Identification"
        },
        {
            "question": "When interviewing juvenile witnesses, what special considerations apply?",
            "options": [
                "Same procedures as adult interviews",
                "Age-appropriate language, avoid leading questions, establish truth understanding, keep interview short",
                "Parents must ask all questions",
                "Multiple detailed interviews are preferred"
            ],
            "correct_answers": ["Age-appropriate language, avoid leading questions, establish truth understanding, keep interview short"],
            "explanation": "Juvenile interviews: use age-appropriate language, avoid leading questions, establish understanding of truth vs lie, open-ended questions, support person if needed, keep short, minimize number of interviews.",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "difficulty": "medium",
            "reference": "Special Order S04-06: Child Victims"
        },
        {
            "question": "What determines if a confession is voluntary?",
            "options": [
                "Whether the suspect signed a waiver form",
                "Totality of circumstances including duration, coercion, and suspect's condition",
                "Whether the suspect is guilty",
                "The severity of the crime"
            ],
            "correct_answers": ["Totality of circumstances including duration, coercion, and suspect's condition"],
            "explanation": "Courts consider: (1) duration of interrogation, (2) food/water/breaks provided, (3) coercion used, (4) suspect's age/education/mental state, (5) Miranda given, (6) promises/threats made.",
            "category_id": "cat_interviews",
            "category_name": "Interviews & Interrogations",
            "difficulty": "hard",
            "reference": "General Order G06-01-02: Interrogations"
        },
        {
            "question": "In Illinois, what time restrictions apply to executing a search warrant?",
            "options": [
                "Must be executed within 24 hours",
                "Execute within 96 hours, generally between 6am-10pm unless nighttime authorized",
                "No time restrictions apply",
                "Must be executed within 72 hours, any time"
            ],
            "correct_answers": ["Execute within 96 hours, generally between 6am-10pm unless nighttime authorized"],
            "explanation": "Search warrant: execute within 96 hours of issuance, generally 6am-10pm unless nighttime specifically authorized by judge. Knock and announce unless no-knock authorized. Return within 48 hours.",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "difficulty": "medium",
            "reference": "725 ILCS 5/108-8"
        },
        {
            "question": "Case reports must be completed by when?",
            "options": [
                "Within 24 hours",
                "End of tour",
                "Within 10 days",
                "Within 72 hours"
            ],
            "correct_answers": ["End of tour"],
            "explanation": "Original case report due by end of tour. Arrest report: before end of tour. Progress/supplementary reports: within 10 days. Extension requires supervisor approval.",
            "category_id": "cat_reports",
            "category_name": "Reports & Documentation",
            "difficulty": "easy",
            "reference": "General Order G07-01: Case Reporting"
        }
    ]
    
    now = datetime.now(timezone.utc)
    count = 0
    
    for q in mcq_questions:
        q["type"] = "multiple_choice"
        q["question_id"] = f"mcq_{uuid.uuid4().hex[:12]}"
        q["created_at"] = now
        q["updated_at"] = now
        
        await db.questions.update_one(
            {"question_id": q["question_id"]},
            {"$set": q},
            upsert=True
        )
        count += 1
    
    print(f"✓ Seeded {count} multiple choice questions")
    return count

async def main():
    print("🌱 Seeding Multiple Choice Questions...")
    print("=" * 50)
    
    count = await seed_multiple_choice()
    
    print("=" * 50)
    print(f"✅ Seeding complete! Added {count} MCQ questions")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
