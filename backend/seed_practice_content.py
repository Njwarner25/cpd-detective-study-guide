"""
Seed script for adding 100 Practice Test MCQs and 5 Gold Scenarios
Based on previous practice materials from the testing company (Bernstein & Associates)
"""

from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timezone
import os
import uuid
import json

load_dotenv('.env')

client = MongoClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

# Create Practice Test category if not exists
practice_category = {
    "category_id": "cat_practice_test",
    "name": "Practice Test",
    "description": "Questions based on previous practice from the testing company",
    "order": 9
}

existing = db.categories.find_one({"category_id": "cat_practice_test"})
if not existing:
    db.categories.insert_one(practice_category)
    print("Created Practice Test category")

# Create Gold Scenarios category if not exists
gold_category = {
    "category_id": "cat_gold_scenarios",
    "name": "Gold Scenarios",
    "description": "Premium scenarios based on previous practice from the testing company",
    "order": 10
}

existing = db.categories.find_one({"category_id": "cat_gold_scenarios"})
if not existing:
    db.categories.insert_one(gold_category)
    print("Created Gold Scenarios category")

now = datetime.now(timezone.utc)

# ============================================================================
# 100 PRACTICE TEST MCQs - Based on previous practice from the testing company
# ============================================================================

practice_mcqs = [
    # LINEUPS (Questions 1-10) - Critical lineup procedures
    {
        "question": "When conducting a live lineup, what is the minimum number of fillers required?",
        "options": ["Two (2)", "Three (3)", "Four (4)", "Five (5)"],
        "correct_answers": ["Three (3)"],
        "explanation": "Per CPD directive S06-02, a live lineup should consist of at least six individuals (one suspect and five fillers), but in no event shall there be less than three (3) fillers.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "medium"
    },
    {
        "question": "The photo lineup will consist of a minimum of how many photographs?",
        "options": ["Four (4)", "Five (5)", "Six (6)", "Eight (8)"],
        "correct_answers": ["Six (6)"],
        "explanation": "Per CPD directive S06-02, a photo lineup will consist of a minimum of six (6) photographs, using a minimum of five (5) filler photos together with one (1) suspect.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "medium"
    },
    {
        "question": "Who should conduct a lineup per CPD policy?",
        "options": [
            "The arresting officer",
            "The lead detective on the case",
            "An independent administrator not involved in the investigation",
            "The district supervisor"
        ],
        "correct_answers": ["An independent administrator not involved in the investigation"],
        "explanation": "Per S06-02, lineups must be conducted by an 'independent administrator' - someone not participating in the investigation and unaware of the suspect's identity, unless impractical.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "medium"
    },
    {
        "question": "When may a showup identification procedure be used?",
        "options": [
            "At any time during an investigation",
            "Only when the suspect is detained within a short time frame, generally within one hour of the offense",
            "Only after obtaining supervisory approval",
            "Only when the victim cannot travel to view a lineup"
        ],
        "correct_answers": ["Only when the suspect is detained within a short time frame, generally within one hour of the offense"],
        "explanation": "Showups should only be used when the suspect is detained within a short time frame following the commission of the offense, generally within one hour.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "medium"
    },
    {
        "question": "Whether or not a positive identification is made, all photographs used in a photo spread will be:",
        "options": [
            "Discarded when the case is closed",
            "Printed in a black and white format",
            "Stored at one designated detective area",
            "Inventoried"
        ],
        "correct_answers": ["Inventoried"],
        "explanation": "All photographs used in a photo spread must be inventoried regardless of whether a positive identification was made.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "easy"
    },
    {
        "question": "During a showup, officers should:",
        "options": [
            "Transport the suspect to the witness's residence",
            "Transport the witness to the location of the suspect when practical",
            "Allow witnesses to confer before the identification",
            "Present the suspect to multiple witnesses at the same time"
        ],
        "correct_answers": ["Transport the witness to the location of the suspect when practical"],
        "explanation": "During a showup, transport the witness to the location of the suspect whenever practical. Do NOT transport the suspect to the witness's residence unless it is the scene of the crime.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "medium"
    },
    {
        "question": "What form must be presented to each witness before conducting a live or photo lineup?",
        "options": [
            "Miranda Rights Form",
            "Photo/Live Lineup Advisory Form (CPD-11.900)",
            "Witness Statement Form",
            "Chain of Custody Form"
        ],
        "correct_answers": ["Photo/Live Lineup Advisory Form (CPD-11.900)"],
        "explanation": "The Photo/Live Lineup Advisory Form (CPD-11.900) must be presented to each witness individually before the lineup, and the witness must understand and sign the 'instructions to witness' section.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "medium"
    },
    {
        "question": "In no case will a live lineup or photo lineup be conducted without what document being completed?",
        "options": [
            "A General Offense Case Report",
            "A Miranda Rights Form",
            "A Supplementary Report",
            "An Arrest Report"
        ],
        "correct_answers": ["A Supplementary Report"],
        "explanation": "A Supplementary Report (CPD-11.411-A or B) must be completed for every live or photo lineup, documenting all details of the procedure.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "medium"
    },
    {
        "question": "When conducting a lineup, can the same suspect be presented to the same witness more than once?",
        "options": [
            "Yes, if the witness requests it",
            "Yes, if a supervisor approves",
            "No, avoid multiple identification procedures where the same witness views the same suspect",
            "Only during photo lineups"
        ],
        "correct_answers": ["No, avoid multiple identification procedures where the same witness views the same suspect"],
        "explanation": "Per S06-02, avoid multiple identification procedures where the same witness views the same suspect more than once, as this can taint the identification process.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "medium"
    },
    {
        "question": "At what point does a suspect have the right to have counsel present during a lineup?",
        "options": [
            "At all times",
            "Never",
            "After adversarial criminal proceedings have begun (after appearing before a judge/magistrate)",
            "Only if the suspect requests it"
        ],
        "correct_answers": ["After adversarial criminal proceedings have begun (after appearing before a judge/magistrate)"],
        "explanation": "Per Kirby v. Illinois, suspects are not entitled to counsel prior to adversarial criminal proceedings. If the 6th Amendment right has attached, counsel must be notified and given an opportunity to observe.",
        "reference": "S06-02 Live Lineups, Photo Lineups, and Showups",
        "difficulty": "hard"
    },
    
    # USE OF FORCE (Questions 11-20)
    {
        "question": "Department members may only use force that is:",
        "options": [
            "Minimal and non-lethal",
            "Objectively reasonable, necessary, and proportional under the totality of circumstances",
            "Authorized by a supervisor",
            "Documented in advance"
        ],
        "correct_answers": ["Objectively reasonable, necessary, and proportional under the totality of circumstances"],
        "explanation": "Per G03-02, members may only use force that is objectively reasonable, necessary, and proportional, under the totality of the circumstances.",
        "reference": "G03-02 De-escalation, Response to Resistance, and Use of Force",
        "difficulty": "medium"
    },
    {
        "question": "Which of the following is the only authorized option in potential use of force situations for persons who are fully cooperative?",
        "options": ["Police Presence", "Compliance Techniques", "Control Instruments", "LRAD"],
        "correct_answers": ["Police Presence"],
        "explanation": "For fully cooperative individuals, police presence is the only authorized option. Force options escalate based on the subject's level of resistance.",
        "reference": "G03-02-01 Response to Resistance and Force Options",
        "difficulty": "medium"
    },
    {
        "question": "Discharge of a firearm is a Level ___ reportable use of force:",
        "options": ["Level 1", "Level 2", "Level 3", "Level 4"],
        "correct_answers": ["Level 3"],
        "explanation": "Discharge of a firearm is classified as a Level 3 (highest level) reportable use of force, requiring the most extensive documentation and review.",
        "reference": "G03-02-01 Response to Resistance and Force Options",
        "difficulty": "medium"
    },
    {
        "question": "A sworn member may use deadly force only when necessary to prevent:",
        "options": [
            "Personal assault",
            "Death or great bodily harm from an imminent threat posed to the sworn member or to another person",
            "The subject from harming others",
            "Danger to others and control the subject"
        ],
        "correct_answers": ["Death or great bodily harm from an imminent threat posed to the sworn member or to another person"],
        "explanation": "Deadly force may only be used as a last resort when necessary to protect against an imminent threat to life or to prevent great bodily harm.",
        "reference": "G03-02 De-escalation, Response to Resistance, and Use of Force",
        "difficulty": "medium"
    },
    {
        "question": "Firing at or into a moving vehicle when the vehicle is the only force used against a sworn member is:",
        "options": [
            "Authorized with supervisor approval",
            "Authorized as a first response",
            "Prohibited unless such force is a last resort and necessary to protect against an imminent threat to life",
            "Always prohibited"
        ],
        "correct_answers": ["Prohibited unless such force is a last resort and necessary to protect against an imminent threat to life"],
        "explanation": "Firing at moving vehicles is generally prohibited unless it is a last resort necessary to protect against an imminent threat to life or great bodily harm.",
        "reference": "G03-02-01 Response to Resistance and Force Options",
        "difficulty": "hard"
    },
    {
        "question": "Department members are required to use ___ techniques to prevent or reduce the need for force:",
        "options": ["Verbal commands", "De-escalation", "Control", "Physical"],
        "correct_answers": ["De-escalation"],
        "explanation": "Members are required to use de-escalation techniques to prevent or reduce the need for force, unless doing so would place a person at immediate risk of harm.",
        "reference": "G03-02 De-escalation, Response to Resistance, and Use of Force",
        "difficulty": "easy"
    },
    {
        "question": "Which of the following require completion of a TRR (Tactical Response Report)?",
        "options": [
            "The use of a firm grip hold which does not result in injury",
            "Control hold utilized in conjunction with handcuffing which does not result in injury",
            "Discharge of OC spray which does not result in injury",
            "The use of escort holds not in response to active resistance that do not result in an injury"
        ],
        "correct_answers": ["Discharge of OC spray which does not result in injury"],
        "explanation": "Discharge of OC spray requires a TRR regardless of whether it results in injury. Simple control holds during handcuffing and escort holds without injury do not require a TRR.",
        "reference": "G03-02 De-escalation, Response to Resistance, and Use of Force",
        "difficulty": "hard"
    },
    {
        "question": "According to Taser Use Incidents directive, whenever possible, members should deploy the taser to the subject's:",
        "options": [
            "Front - upper center mass",
            "Back - below the neck area",
            "Back - above the shoulders",
            "Front - center mass"
        ],
        "correct_answers": ["Back - below the neck area"],
        "explanation": "Per G03-02-04, it is recommended that whenever possible, members deploy the taser to the subject's back - below the neck area.",
        "reference": "G03-02-04 Taser Use Incidents",
        "difficulty": "medium"
    },
    {
        "question": "When it is safe and feasible, members will provide a ___ prior to the use of physical force:",
        "options": ["Written notice", "Verbal warning", "Radio notification", "Video recording"],
        "correct_answers": ["Verbal warning"],
        "explanation": "When safe and feasible, members will provide a verbal warning prior to the use of physical force to give the subject an opportunity to comply.",
        "reference": "G03-02 De-escalation, Response to Resistance, and Use of Force",
        "difficulty": "easy"
    },
    {
        "question": "What type of force is force by any means that is likely to cause death or great bodily harm?",
        "options": ["Excessive force", "Deadly force", "Lethal force", "Maximum force"],
        "correct_answers": ["Deadly force"],
        "explanation": "Deadly force includes firing a firearm at a person, striking a subject's head/neck with an impact weapon, and other actions likely to cause death or great bodily harm.",
        "reference": "G03-02 De-escalation, Response to Resistance, and Use of Force",
        "difficulty": "easy"
    },
    
    # CRIME SCENE & EVIDENCE (Questions 21-30)
    {
        "question": "Which is the FIRST step a detective must take when arriving at a crime scene?",
        "options": [
            "Access the boundaries of the inner perimeter",
            "Report to the Bureau of Patrol Supervisor",
            "Consult with the evidence technician",
            "Document all observations"
        ],
        "correct_answers": ["Report to the Bureau of Patrol Supervisor"],
        "explanation": "The first step upon arrival is to report to the Bureau of Patrol supervisor on scene to receive a briefing and coordinate the investigation.",
        "reference": "G04-02 Crime Scene Protection and Processing",
        "difficulty": "medium"
    },
    {
        "question": "A detective assigned to investigate a crime scene will inform the Bureau of ___ when the crime scene processing and investigation are completed:",
        "options": ["Detectives Supervisor", "Forensic Services", "Patrol Supervisor", "Patrol Chief"],
        "correct_answers": ["Patrol Supervisor"],
        "explanation": "The detective will inform the Bureau of Patrol supervisor when crime scene processing and investigation are completed and crime scene protection can be terminated.",
        "reference": "G04-02 Crime Scene Protection and Processing",
        "difficulty": "medium"
    },
    {
        "question": "If during the course of an investigation an officer determines that a computer or electronic device may have evidentiary value, it will be:",
        "options": [
            "Categorized as intellectual property",
            "Considered hearsay evidence",
            "Documented on a supplemental report",
            "Processed as evidence"
        ],
        "correct_answers": ["Processed as evidence"],
        "explanation": "Any computer or electronic device with potential evidentiary value will be processed as evidence following proper procedures.",
        "reference": "G04-02 Crime Scene Protection and Processing",
        "difficulty": "easy"
    },
    {
        "question": "Which Bureau of Detectives unit is responsible for advising officers on how to recover computer related evidence?",
        "options": [
            "Forensic Services Technical Group",
            "Trap and Trace Technical Group",
            "Bureau of Detectives Crime Analysis Technical Group",
            "Support Services"
        ],
        "correct_answers": ["Bureau of Detectives Crime Analysis Technical Group"],
        "explanation": "The Bureau of Detectives Crime Analysis Technical Group is responsible for advising officers on how to recover computer related evidence and determining what evidence will be analyzed.",
        "reference": "Computer Evidence Recovery Directive",
        "difficulty": "medium"
    },
    {
        "question": "Notifications or requests for the assignment of a detective or forensic services will not be made from a ___ located within a crime scene:",
        "options": ["Telephone", "Radio", "Computer terminal", "Cell phone"],
        "correct_answers": ["Telephone"],
        "explanation": "To preserve the crime scene integrity, notifications should not be made using equipment within the crime scene area.",
        "reference": "G04-02 Crime Scene Protection and Processing",
        "difficulty": "medium"
    },
    {
        "question": "When feasible, a ___ detective will respond to the scene and determine if Forensic Services Division personnel are required:",
        "options": ["General assignment", "Property crimes", "Violent crimes", "Area"],
        "correct_answers": ["Area"],
        "explanation": "When feasible, an Area detective will respond to determine the need for Forensic Services personnel based on the nature of the crime.",
        "reference": "G04-02 Crime Scene Protection and Processing",
        "difficulty": "easy"
    },
    {
        "question": "Firearms and/or property directly related to a firearm that require fingerprint or DNA processing will not be touched, handled, or removed by any members other than:",
        "options": [
            "The arresting officer",
            "Forensic Services Division personnel",
            "The detective assigned",
            "The watch commander"
        ],
        "correct_answers": ["Forensic Services Division personnel"],
        "explanation": "Unless exigent circumstances exist, only Forensic Services Division personnel should handle firearms requiring fingerprint or DNA processing to preserve evidence.",
        "reference": "S07-01-04 Firearms Taken Into Custody or Turned In",
        "difficulty": "medium"
    },
    {
        "question": "All images captured by the PODS (Police Observation Devices) will be recorded over after a ___ hour period for non-wireless cameras:",
        "options": ["24", "48", "72", "96"],
        "correct_answers": ["72"],
        "explanation": "POD images are recorded over after 72 hours for non-wireless cameras and after 30 days for wireless cameras unless specifically retained.",
        "reference": "S02-04-01 Police Observation Device (POD) Program",
        "difficulty": "medium"
    },
    {
        "question": "Upon approval of a supervisor, news media with proper credentials will be allowed access to a crime scene's ___ perimeter:",
        "options": ["Inner", "Outer", "Secure", "Restricted"],
        "correct_answers": ["Outer"],
        "explanation": "With supervisor approval, credentialed media may access the outer perimeter secured with yellow barrier tape, but not the inner crime scene.",
        "reference": "Crime Scene Protocol Directive",
        "difficulty": "medium"
    },
    {
        "question": "Exculpatory evidence must be:",
        "options": [
            "Disclosed to defense counsel",
            "Preserved and documented",
            "Reported to the State's Attorney",
            "All of the above"
        ],
        "correct_answers": ["All of the above"],
        "explanation": "Exculpatory evidence - evidence favorable to the defendant - must be preserved, documented, and disclosed as required by law (Brady v. Maryland).",
        "reference": "S07-01-09 Exculpatory Evidence",
        "difficulty": "medium"
    },
    
    # INTERVIEWS & INTERROGATIONS (Questions 31-45)
    {
        "question": "Individuals may waive their Miranda rights, provided the waiver is made voluntarily, knowingly, and:",
        "options": ["Promptly", "In writing", "Intelligently", "Witnessed"],
        "correct_answers": ["Intelligently"],
        "explanation": "A valid Miranda waiver must be voluntary, knowing, and intelligent - meaning the person understands what rights they are giving up.",
        "reference": "G04-03 Custodial Interrogations",
        "difficulty": "medium"
    },
    {
        "question": "Miranda warnings are NOT necessary when police conduct:",
        "options": [
            "Questioning of any person regarding facts of a crime",
            "Questioning a suspect at the scene",
            "General, on the scene questioning regarding facts of a crime",
            "Interviews of any potential witness"
        ],
        "correct_answers": ["General, on the scene questioning regarding facts of a crime"],
        "explanation": "Miranda applies to custodial interrogations. General, on-scene questioning about the facts of a crime does not require Miranda warnings.",
        "reference": "G04-03 Custodial Interrogations",
        "difficulty": "hard"
    },
    {
        "question": "When a search warrant has not been served within ___ hours of issuance, it will be returned to the clerk of the court:",
        "options": ["24", "48", "72", "96"],
        "correct_answers": ["96"],
        "explanation": "A search warrant not served within 96 hours of issuance must be signed by the returning officer and returned to the clerk of the court within twenty days.",
        "reference": "S04-19 Search Warrants",
        "difficulty": "medium"
    },
    {
        "question": "According to the Digital Recording of Interrogations directive, digital recordings should be activated:",
        "options": [
            "When the suspect begins talking",
            "Prior to the arrestee entering the interview room",
            "After Miranda warnings are given",
            "When the suspect confesses"
        ],
        "correct_answers": ["Prior to the arrestee entering the interview room"],
        "explanation": "When applicable, digital recordings should be activated prior to the arrestee entering the interview room to capture the entire interaction.",
        "reference": "S04-03-01 Digital Recording of Interrogations",
        "difficulty": "medium"
    },
    {
        "question": "Pursuant to Maryland v. Shatzer, if an individual asserts their 5th Amendment right to an attorney and is then released from custody, members may attempt to question them about the offense after a period of ___ days:",
        "options": ["5", "7", "10", "14"],
        "correct_answers": ["14"],
        "explanation": "Per Maryland v. Shatzer, if a person asserts their right to counsel and is released from custody, police may re-initiate questioning after 14 days have passed.",
        "reference": "Maryland v. Shatzer / Custodial Interrogations",
        "difficulty": "hard"
    },
    {
        "question": "In digitally recorded interrogations where no charge is placed, the detective must verify recordings have been retained within ___ days:",
        "options": ["21", "25", "30", "75"],
        "correct_answers": ["75"],
        "explanation": "In all digitally recorded interrogations where no charge is placed, the detective must within 75 days access the central management system to verify recordings have been retained.",
        "reference": "S04-03-01 Digital Recording of Interrogations",
        "difficulty": "hard"
    },
    {
        "question": "When beginning an interview with a suspect, an officer should open by:",
        "options": [
            "Making a direct, positive accusation",
            "Asking some general, non-confrontational questions",
            "Disclosing information linking the suspect to the crime",
            "Offering excuses for the suspect's behavior"
        ],
        "correct_answers": ["Asking some general, non-confrontational questions"],
        "explanation": "Interviews should begin with general, non-confrontational questions to build rapport and assess the subject's demeanor before addressing the substantive issues.",
        "reference": "Interview and Interrogation Techniques",
        "difficulty": "medium"
    },
    {
        "question": "A suspect advises you that he does not want to consult with his attorney who has arrived. The best procedure is to:",
        "options": [
            "Advise the suspect that the interrogation cannot continue",
            "Advise the attorney he must vacate the premises",
            "Allow the attorney to speak with the suspect after the interrogation",
            "Readvise the suspect of his Miranda Rights and continue if he agrees"
        ],
        "correct_answers": ["Readvise the suspect of his Miranda Rights and continue if he agrees"],
        "explanation": "If a suspect waives their right to counsel despite an attorney's arrival, re-advise them of their Miranda rights. If they still wish to proceed without counsel, the interrogation may continue.",
        "reference": "G04-03 Custodial Interrogations",
        "difficulty": "hard"
    },
    {
        "question": "Before concluding an interrogation in which the suspect confessed, the most important action is to:",
        "options": [
            "Ensure the ERI video is reviewed",
            "Ensure the Felony Minutes Form 101 is completed",
            "Ensure the confession contains admissions only known by the offender",
            "Ensure you have requested a polygraph"
        ],
        "correct_answers": ["Ensure the confession contains admissions only known by the offender"],
        "explanation": "A reliable confession should contain details that only the true perpetrator would know, helping to corroborate the confession's validity.",
        "reference": "Interview and Interrogation Techniques",
        "difficulty": "hard"
    },
    {
        "question": "Which notification must be made before interrogating a suspect at the Area Detective Division?",
        "options": [
            "Patrol sergeant who supervises the area",
            "Ensure the sergeant and lieutenant are aware of the 48-hour status",
            "Contact the State's Attorney's Felony Review Unit",
            "Advise your supervisor of your status"
        ],
        "correct_answers": ["Advise your supervisor of your status"],
        "explanation": "Before beginning an interrogation, you should advise your supervisor of your status to ensure proper coordination and oversight.",
        "reference": "Interview and Interrogation Protocols",
        "difficulty": "medium"
    },
    {
        "question": "If a suspect confesses to a crime and mentions an allegation of misconduct by an arresting officer, the first action should be to:",
        "options": [
            "Notify your supervisor of the allegation",
            "Document the information in your report",
            "Report the statement to the officer's supervisor",
            "Ensure the station supervisor is aware of the claim"
        ],
        "correct_answers": ["Notify your supervisor of the allegation"],
        "explanation": "Any allegation of misconduct must first be reported to your supervisor, who will determine the appropriate course of action.",
        "reference": "Misconduct Allegation Procedures",
        "difficulty": "medium"
    },
    {
        "question": "A Registered Confidential Informant (RCI) is one who:",
        "options": [
            "Is registered with the FBI",
            "Provides information and is eligible for compensation consistent with Department policy",
            "Must remain anonymous in all court proceedings",
            "Cannot be used in search warrant applications"
        ],
        "correct_answers": ["Provides information and is eligible for compensation consistent with Department policy"],
        "explanation": "An RCI voluntarily provides intelligence concerning criminal activity and is eligible to receive monetary compensation consistent with Department policy.",
        "reference": "S04-19 Search Warrants / Confidential Informant Procedures",
        "difficulty": "medium"
    },
    {
        "question": "The 4th Amendment to the Constitution guarantees protection from:",
        "options": [
            "Self-incrimination",
            "Unlawful arrest and unreasonable search and seizure",
            "Double jeopardy",
            "Cruel and unusual punishment"
        ],
        "correct_answers": ["Unlawful arrest and unreasonable search and seizure"],
        "explanation": "The Fourth Amendment protects against unreasonable searches and seizures and requires probable cause for warrants.",
        "reference": "Constitutional Law - 4th Amendment",
        "difficulty": "easy"
    },
    {
        "question": "During a consent to search incident, at least ___ participating member will be in the prescribed seasonal field uniform:",
        "options": ["Zero", "One", "Two", "Three"],
        "correct_answers": ["One"],
        "explanation": "For consent to search incidents, at least one participating member must be attired in the prescribed seasonal field uniform.",
        "reference": "S04-19-01 Consent to Search Incidents",
        "difficulty": "medium"
    },
    {
        "question": "Detectives wanting to interview patients at Cook County Hospital must first report to:",
        "options": [
            "The officer in charge of the police desk",
            "The attending physician",
            "The security center",
            "The head nurse on duty"
        ],
        "correct_answers": ["The officer in charge of the police desk"],
        "explanation": "Before interviewing patients at Cook County Hospital, detectives must report to the officer in charge of the police desk at the rear of the hospital.",
        "reference": "Hospital Interview Procedures",
        "difficulty": "medium"
    },
    
    # ARRESTS & PROCESSING (Questions 46-60)
    {
        "question": "An arrestee taken into custody will be handcuffed unless:",
        "options": [
            "They are cooperative",
            "The arrestee is injured to the extent that he or she is incapable of offering resistance",
            "They are female",
            "The offense is a misdemeanor"
        ],
        "correct_answers": ["The arrestee is injured to the extent that he or she is incapable of offering resistance"],
        "explanation": "An arrestee will be handcuffed unless injured to the extent that they cannot offer resistance, in which case appropriate restraints or medical care take priority.",
        "reference": "G06-01-02 Restraining Arrestees",
        "difficulty": "medium"
    },
    {
        "question": "When feasible, an arrestee will be handcuffed with both hands behind the back and palms positioned:",
        "options": ["Together", "Outward", "Facing each other", "Upward"],
        "correct_answers": ["Outward"],
        "explanation": "When handcuffing, both hands should be behind the back with palms positioned outward, and handcuffs will be double-locked.",
        "reference": "G06-01-02 Restraining Arrestees",
        "difficulty": "easy"
    },
    {
        "question": "When there is a likelihood of a multiple-arrest situation, what devices may be issued?",
        "options": [
            "Leg irons",
            "Body chains",
            "Flexible restraining devices",
            "Cable ties only"
        ],
        "correct_answers": ["Flexible restraining devices"],
        "explanation": "When a multiple-arrest situation is likely, flexible restraining devices (zip ties) may be issued to facilitate processing multiple arrestees.",
        "reference": "G06-01-02 Restraining Arrestees",
        "difficulty": "medium"
    },
    {
        "question": "Arrested persons will be booked, charged, and made eligible for ___ in that order:",
        "options": ["Processing", "Interview", "Bond", "Transport"],
        "correct_answers": ["Bond"],
        "explanation": "The correct sequence is: booking, charging, then bond eligibility determination.",
        "reference": "S06-01 Processing Persons Under Department Control",
        "difficulty": "easy"
    },
    {
        "question": "Every person arrested without a warrant who is not eligible for release on bond will appear in court:",
        "options": [
            "Within 24 hours",
            "Without unnecessary delay",
            "Within 48 hours",
            "The next business day"
        ],
        "correct_answers": ["Without unnecessary delay"],
        "explanation": "Per constitutional requirements, persons arrested without a warrant must appear before a judge without unnecessary delay.",
        "reference": "S06-01 Processing Persons Under Department Control",
        "difficulty": "medium"
    },
    {
        "question": "Juveniles under the age of ___ will not be fingerprinted unless the arrest is a felony offense:",
        "options": ["13", "15", "17", "18"],
        "correct_answers": ["17"],
        "explanation": "Juveniles under 17 will not be fingerprinted unless the arrest is a felony offense and the watch operations lieutenant authorizes the fingerprinting.",
        "reference": "S06-04 Processing of Juveniles and Minors",
        "difficulty": "medium"
    },
    {
        "question": "No juvenile under ___ years of age will be detained in secure custody in a police facility:",
        "options": ["10", "11", "12", "13"],
        "correct_answers": ["10"],
        "explanation": "No juvenile under 10 years of age will be detained in secure custody in a police facility.",
        "reference": "S06-04 Processing of Juveniles and Minors",
        "difficulty": "medium"
    },
    {
        "question": "A juvenile who is at least ___ years of age at the time of certain offenses (1st degree murder, aggravated criminal sexual assault, aggravated battery with firearm) will be processed as an adult:",
        "options": ["12", "13", "15", "16"],
        "correct_answers": ["13"],
        "explanation": "A juvenile at least 13 years old charged with first degree murder, aggravated criminal sexual assault, or aggravated battery with a firearm will be processed as an adult.",
        "reference": "S06-04-03 Processing Juvenile Arrestees Charged As Adults",
        "difficulty": "hard"
    },
    {
        "question": "Arrestees will be provided access to a telephone and be able to make ___ telephone calls at minimum free of charge:",
        "options": ["One", "Two", "Three", "Five"],
        "correct_answers": ["Three"],
        "explanation": "Arrestees will be able to make at least three telephone calls free of charge to communicate with attorney, family, or friends.",
        "reference": "S06-01 Processing Persons Under Department Control",
        "difficulty": "easy"
    },
    {
        "question": "Telephone access must be provided no later than ___ hours after arrival at the first place of custody:",
        "options": ["1", "2", "3", "4"],
        "correct_answers": ["3"],
        "explanation": "Arrestees may communicate with attorney, family, or friends as soon as possible, but no later than 3 hours after arrival at the first place of custody.",
        "reference": "S06-01 Processing Persons Under Department Control",
        "difficulty": "medium"
    },
    {
        "question": "If prisoner personal property is not picked up within ___ hours from the time of inventory, it will be sent to ERPS:",
        "options": ["24", "48", "72", "96"],
        "correct_answers": ["48"],
        "explanation": "If prisoner personal property is not picked up within 48 hours from inventory, it will be manifested and sent to ERPS (Evidence and Recovered Property Section).",
        "reference": "S07-01-01 Inventorying Arrestees' Personal Property",
        "difficulty": "medium"
    },
    {
        "question": "Station supervisors will waive fingerprint results only under ___ circumstances:",
        "options": ["Normal", "Extraordinary", "Emergency", "No"],
        "correct_answers": ["Extraordinary"],
        "explanation": "It is policy to hold all arrestees until completion of identification; supervisors may waive fingerprint results only under extraordinary circumstances and must be prepared to justify the decision.",
        "reference": "S06-01-01 Releasing Arrestees Without Charging",
        "difficulty": "medium"
    },
    {
        "question": "Members will transport an arrestee immediately in a department vehicle equipped with a protective divider or a:",
        "options": ["Partner", "Cage", "Supervisor", "Security guard"],
        "correct_answers": ["Cage"],
        "explanation": "Arrestees should be transported in vehicles with a protective divider or cage unless circumstances make this unreasonable or impractical.",
        "reference": "G06-01-01 Field Arrest Procedures",
        "difficulty": "easy"
    },
    {
        "question": "What type of interim clothing should be provided to an arrestee without a shirt prior to transport to Cook County?",
        "options": [
            "Blue paper gown",
            "White paper coverall",
            "White paper gown",
            "Blue paper coverall"
        ],
        "correct_answers": ["White paper coverall"],
        "explanation": "A white paper coverall should be provided to arrestees who lack appropriate clothing prior to transport.",
        "reference": "Arrestee Transport Procedures",
        "difficulty": "easy"
    },
    {
        "question": "___ arrestees will be given priority over adult arrestees for the completion of the booking process:",
        "options": ["Female", "Juvenile", "Elderly", "First-time"],
        "correct_answers": ["Juvenile"],
        "explanation": "Juvenile arrestees are given priority in the booking process to minimize their time in custody.",
        "reference": "S06-04 Processing of Juveniles and Minors",
        "difficulty": "easy"
    },
    
    # DOMESTIC INCIDENTS & ORDERS OF PROTECTION (Questions 61-70)
    {
        "question": "Which type of Order of Protection is valid for up to 30 days and is issued after the respondent has received notice?",
        "options": [
            "Emergency Order",
            "Plenary Order",
            "Interim Order",
            "Binary Order"
        ],
        "correct_answers": ["Interim Order"],
        "explanation": "An Interim Order of Protection is valid for up to 30 days and is issued after the respondent has received notice and had opportunity to appear.",
        "reference": "G04-04-01 Orders of Protection",
        "difficulty": "medium"
    },
    {
        "question": "Generally, a foreign order of protection will appear 'authentic on its face' when it is signed by or on behalf of a:",
        "options": [
            "Special magistrate",
            "Federal judge",
            "Representative of the United States Government",
            "Judicial officer"
        ],
        "correct_answers": ["Judicial officer"],
        "explanation": "A foreign order appears authentic when it names the parties and court, has issue and expiration dates (not passed), specifies conditions, and is signed by a judicial officer.",
        "reference": "G04-04-01 Orders of Protection",
        "difficulty": "medium"
    },
    {
        "question": "Which is TRUE regarding mutual orders of protection in domestic violence cases?",
        "options": [
            "They are allowed under certain circumstances",
            "They are prohibited",
            "They are generally discouraged",
            "They are sometimes helpful"
        ],
        "correct_answers": ["They are prohibited"],
        "explanation": "Mutual orders of protection are prohibited in domestic violence cases under Illinois law.",
        "reference": "G04-04-01 Orders of Protection",
        "difficulty": "medium"
    },
    {
        "question": "The Bureau of Patrol division is responsible for conducting the preliminary investigation in a domestic incident, including:",
        "options": [
            "Determining whether a valid order of protection exists",
            "Identifying the crime scene",
            "Determining if evidence is present",
            "All of the above"
        ],
        "correct_answers": ["All of the above"],
        "explanation": "Bureau of Patrol is responsible for conducting the preliminary investigation including checking for orders of protection, identifying the crime scene, and determining if evidence is present.",
        "reference": "G04-04 Domestic Incidents",
        "difficulty": "easy"
    },
    {
        "question": "If a subject's identity has been verified and there is an unserved order of protection, law enforcement may:",
        "options": [
            "Arrest the subject if they are in violation",
            "Detain the subject for a reasonable time to complete and serve the short form notification",
            "Notify domestic violence court",
            "Complete an information report"
        ],
        "correct_answers": ["Detain the subject for a reasonable time to complete and serve the short form notification"],
        "explanation": "Officers may detain the subject for a reasonable time to complete and serve the short form notification of the order of protection.",
        "reference": "G04-04-01 Orders of Protection",
        "difficulty": "hard"
    },
    {
        "question": "What standard is required when arresting a subject for violation of an order of protection without witnessing the violation?",
        "options": [
            "Mere suspicion",
            "Reasonable suspicion",
            "Probable cause",
            "Just cause"
        ],
        "correct_answers": ["Probable cause"],
        "explanation": "An officer must have probable cause to believe a violation occurred when arresting for an order of protection violation not witnessed by the officer.",
        "reference": "G04-04-01 Orders of Protection",
        "difficulty": "medium"
    },
    {
        "question": "In dependency cases, the preliminary investigating officer will render assistance by providing protective ___ and medical treatment:",
        "options": ["Services", "Custody", "Observation", "Housing"],
        "correct_answers": ["Custody"],
        "explanation": "In dependency cases, officers provide protective custody and medical treatment as necessary to ensure the child's safety.",
        "reference": "S06-04-05 Abused, Neglected, Dependent Children",
        "difficulty": "medium"
    },
    {
        "question": "If a dependent child status resulted from a 'lockout', which unit should be notified?",
        "options": [
            "Youth Services",
            "DCFS",
            "Bureau of Detectives Area (for detective assignment)",
            "Juvenile Court"
        ],
        "correct_answers": ["Bureau of Detectives Area (for detective assignment)"],
        "explanation": "If a lockout occurs (child not permitted by parents to remain in home), notify the Bureau of Detectives Area for assignment of a detective to interview parents and child.",
        "reference": "S06-04-05 Abused, Neglected, Dependent Children",
        "difficulty": "medium"
    },
    {
        "question": "What document should a domestic violence victim be provided when seeking guidance on obtaining an order of protection?",
        "options": [
            "Domestic incident notice",
            "Domestic complaint form",
            "Domestic order notification",
            "Domestic violence resource card"
        ],
        "correct_answers": ["Domestic incident notice"],
        "explanation": "Victims should be provided with a domestic incident notice containing information about how to obtain an order of protection and available resources.",
        "reference": "G04-04 Domestic Incidents",
        "difficulty": "easy"
    },
    {
        "question": "The AMBER Alert Notification Plan will not be used for persons ___ years of age or older:",
        "options": ["16", "17", "18", "21"],
        "correct_answers": ["18"],
        "explanation": "The AMBER Alert plan is for abducted and endangered children; it will not be used for persons 18 years of age or older.",
        "reference": "S04-05-01 AMBER Alert Notification Plan",
        "difficulty": "easy"
    },
    
    # SPECIAL INVESTIGATIONS (Questions 71-85)
    {
        "question": "A Missing Child is any person under ___ years of age whose whereabouts are unknown to parents or legal guardian:",
        "options": ["13", "16", "18", "21"],
        "correct_answers": ["18"],
        "explanation": "Per the Intergovernmental Missing Child Recovery Act, a missing child is any person under 18 whose whereabouts are unknown to parents or legal guardian.",
        "reference": "S04-05 Missing/Found Persons",
        "difficulty": "easy"
    },
    {
        "question": "A missing tender-age child is a child under ___ years of age:",
        "options": ["8", "10", "13", "15"],
        "correct_answers": ["13"],
        "explanation": "A tender-age child is under 13 years old and receives heightened priority in missing child investigations.",
        "reference": "S04-05 Missing/Found Persons",
        "difficulty": "medium"
    },
    {
        "question": "Under Illinois statute, a parent who believes their child is missing must report to law enforcement within ___ hours if the child is under 13:",
        "options": ["1", "6", "12", "24"],
        "correct_answers": ["24"],
        "explanation": "Parents must report a child under 13 as missing to law enforcement within 24 hours of reasonably believing the child is missing.",
        "reference": "325 ILCS 40 - Intergovernmental Missing Child Recovery Act",
        "difficulty": "medium"
    },
    {
        "question": "Whenever the body of an apparent drowning victim is recovered, the assigned officer will prepare a:",
        "options": [
            "Formal Case Report",
            "Death Case Report",
            "Hospitalization Case Report",
            "Medical Examiner's Case Report"
        ],
        "correct_answers": ["Death Case Report"],
        "explanation": "When a drowning victim's body is recovered, the officer notifies OEMC and prepares a Death Case Report.",
        "reference": "S04-10 Drownings, Procedures for Reporting",
        "difficulty": "medium"
    },
    {
        "question": "The ___ will assume administrative/investigative responsibility of all drowning cases:",
        "options": [
            "Chicago Fire Department",
            "Marine Unit",
            "US Coast Guard",
            "Appropriate Bureau of Detectives Area"
        ],
        "correct_answers": ["Appropriate Bureau of Detectives Area"],
        "explanation": "The appropriate Bureau of Detectives Area assumes responsibility for investigating drowning cases.",
        "reference": "S04-10 Drownings, Procedures for Reporting",
        "difficulty": "medium"
    },
    {
        "question": "Which statement is TRUE regarding interviewing victims of sexual assault?",
        "options": [
            "A third party can relay the story",
            "Reports must be made within 10 years",
            "A victim will not be required to submit to an interview",
            "All interviews must be recorded"
        ],
        "correct_answers": ["A victim will not be required to submit to an interview"],
        "explanation": "Sexual assault victims will not be required to submit to an interview - their participation is voluntary.",
        "reference": "S04-29 Incidents of Sexual Assault and Sexual Abuse",
        "difficulty": "medium"
    },
    {
        "question": "A sworn member who encounters an alleged hate crime will notify their immediate field supervisor and the ___ Unit:",
        "options": [
            "Organized Crime",
            "Civil Rights",
            "Civil Rights Enforcement",
            "Hate Crimes Investigative"
        ],
        "correct_answers": ["Civil Rights Enforcement"],
        "explanation": "Hate crimes require notification to the Civil Rights Enforcement Unit, Special Activities Section, or CPIC.",
        "reference": "G04-06 Hate Crimes",
        "difficulty": "medium"
    },
    {
        "question": "What are key indicators that a hate crime has been committed?",
        "options": [
            "The suspect's gestures or statements that reflect bias and similar incidents that may determine a pattern",
            "The offender is of a different race than the victim",
            "The suspect has no known involvement in bias groups",
            "A witness recognizes the offender as a member of a hate group"
        ],
        "correct_answers": ["The suspect's gestures or statements that reflect bias and similar incidents that may determine a pattern"],
        "explanation": "Key indicators include the suspect's bias-reflecting statements/gestures and whether similar incidents suggest a pattern exists.",
        "reference": "G04-06 Hate Crimes",
        "difficulty": "hard"
    },
    {
        "question": "When interviewing a hate crime victim, what is the most appropriate approach?",
        "options": [
            "Interview the victim alone when practical to minimize trauma",
            "Ensure the victim is interviewed by several officers for consistency",
            "Conduct a recorded interview at the Area",
            "Wait 48 hours for the victim to rest"
        ],
        "correct_answers": ["Interview the victim alone when practical to minimize trauma"],
        "explanation": "Interview the victim alone when practical to minimize trauma and refer them to support services in the community.",
        "reference": "G04-06 Hate Crimes",
        "difficulty": "medium"
    },
    {
        "question": "Stalking occurs when a person knowingly on at least ___ separate occasions follows another person and makes threats:",
        "options": ["1", "2", "3", "4"],
        "correct_answers": ["2"],
        "explanation": "Stalking requires that the conduct occur on at least two separate occasions.",
        "reference": "720 ILCS 5/12-7.3 Stalking",
        "difficulty": "medium"
    },
    {
        "question": "A sex offender who has moved into Chicago must register within ___ days after establishing residence:",
        "options": ["3", "5", "7", "10"],
        "correct_answers": ["3"],
        "explanation": "Sex offenders must register within 3 days of establishing a new residence in Chicago.",
        "reference": "S02-05 Criminal Registration and Community Notification",
        "difficulty": "medium"
    },
    {
        "question": "The LEADS/Hot Desk response will advise that a sex offender in violation of School/Playground/Daycare Zone has been given ___ days to vacate:",
        "options": ["3", "5", "7", "10"],
        "correct_answers": ["7"],
        "explanation": "Sex offenders found in violation of school zone restrictions are given 7 days notice to vacate the premises.",
        "reference": "S02-05 Criminal Registration and Community Notification",
        "difficulty": "medium"
    },
    {
        "question": "Prosecution for murder, aggravated arson, and forgery may be commenced:",
        "options": [
            "Within 3 years",
            "Within 7 years",
            "Within 10 years",
            "At any time"
        ],
        "correct_answers": ["At any time"],
        "explanation": "There is no statute of limitations for murder, aggravated arson, and forgery - prosecution may be commenced at any time.",
        "reference": "720 ILCS 5/3-5 Statute of Limitations",
        "difficulty": "easy"
    },
    {
        "question": "Prosecution for a misdemeanor must commence within ___ years:",
        "options": ["1", "2", "3", "5"],
        "correct_answers": ["18 months"],
        "explanation": "Prosecution for a misdemeanor must commence within 18 months after commission of the offense.",
        "reference": "720 ILCS 5/3-5 Statute of Limitations",
        "difficulty": "medium"
    },
    {
        "question": "When must an arrestee be allowed to communicate with an attorney and family member?",
        "options": [
            "Within a reasonable time after booking",
            "As soon as possible, but no later than 3 hours after arrival at first place of custody",
            "Within one hour of booking completion",
            "Within one hour of arrival at first place of custody"
        ],
        "correct_answers": ["As soon as possible, but no later than 3 hours after arrival at first place of custody"],
        "explanation": "Arrestees must be allowed to communicate with attorney/family as soon as possible, but no later than 3 hours after arrival at first place of custody.",
        "reference": "S06-01 Processing Persons Under Department Control",
        "difficulty": "medium"
    },
    
    # COMMUNICATIONS & TECHNOLOGY (Questions 86-95)
    {
        "question": "The Office of Emergency Management and Communications (OEMC) retains recorded voice transmissions and GPS data for a period of ___ days:",
        "options": ["30", "60", "90", "120"],
        "correct_answers": ["90"],
        "explanation": "OEMC retains recorded voice transmissions and GPS data for 90 days unless specifically requested to retain longer.",
        "reference": "S03-01-03 Recorded Voice Transmissions and GPS Data Requests",
        "difficulty": "medium"
    },
    {
        "question": "All ALPR (Automated License Plate Reader) plate reads will be maintained for a period of ___ days:",
        "options": ["30", "60", "90", "365"],
        "correct_answers": ["90"],
        "explanation": "All ALPR plate reads will be maintained for 90 days from the time created.",
        "reference": "S03-20 Automated License Plate Reader (ALPR) Systems",
        "difficulty": "medium"
    },
    {
        "question": "A Digitally Recorded Data Viewing/Hold/Duplication/Shared Request form must be submitted within ___ days:",
        "options": ["24", "30", "72", "75"],
        "correct_answers": ["30"],
        "explanation": "The request form for viewing, holding, or duplicating digital recordings must be submitted within 30 days.",
        "reference": "Digital Recording Procedures",
        "difficulty": "medium"
    },
    {
        "question": "Body Worn Camera recordings will be reviewed by members:",
        "options": [
            "Before writing any report",
            "After consulting with a supervisor",
            "Only when involved in a use of force",
            "Per current Department policy on BWC review"
        ],
        "correct_answers": ["Per current Department policy on BWC review"],
        "explanation": "BWC review policies balance the need for accurate reporting with the integrity of independent recollection.",
        "reference": "S03-14 Body Worn Cameras",
        "difficulty": "medium"
    },
    {
        "question": "Which statement is NOT TRUE regarding body worn cameras?",
        "options": [
            "BWC will not be used to discipline for isolated minor infractions",
            "Recording law-enforcement encounters is mandatory, not discretionary",
            "BWC will not be activated in private residences without a crime in progress",
            "Members may review BWC prior to writing any report"
        ],
        "correct_answers": ["Members may review BWC prior to writing any report"],
        "explanation": "BWC review before writing reports is subject to specific policies and not automatically permitted in all circumstances.",
        "reference": "S03-14 Body Worn Cameras",
        "difficulty": "hard"
    },
    {
        "question": "In situations where immediate POD video retrieval is necessary, who should be notified?",
        "options": ["District commander", "CPIC", "Watch commander", "ISD"],
        "correct_answers": ["CPIC"],
        "explanation": "For immediate POD video retrieval (homicide, sexual assault, etc.), notify CPIC who will contact appropriate ISD personnel.",
        "reference": "S02-04-01 Police Observation Device (POD) Program",
        "difficulty": "medium"
    },
    {
        "question": "Radios will not be turned off during an assignment unless approval is obtained from a supervisor and ___ is notified:",
        "options": ["CPIC", "OEMC", "The watch commander", "Dispatch"],
        "correct_answers": ["OEMC"],
        "explanation": "Radios should remain on during assignments unless unusual circumstances exist, supervisor approves, and OEMC is notified.",
        "reference": "S03-01 Communications Systems",
        "difficulty": "easy"
    },
    {
        "question": "Wanted messages will be sent for non-criminal incidents when ___ circumstances exist:",
        "options": ["Normal", "Unusual", "Emergency", "Exigent"],
        "correct_answers": ["Exigent"],
        "explanation": "Wanted messages for non-criminal incidents are sent when exigent circumstances exist, such as lost or missing children.",
        "reference": "S03-01 Communications Systems",
        "difficulty": "medium"
    },
    {
        "question": "News media inquiries concerning the investigation of an officer-involved death will be referred to:",
        "options": [
            "COPA",
            "News Affairs",
            "Office of the First Deputy Superintendent",
            "The Superintendent or designee"
        ],
        "correct_answers": ["News Affairs"],
        "explanation": "News media inquiries about officer-involved death investigations are referred to News Affairs.",
        "reference": "G03-06 Firearm Discharge and Officer-Involved Death Incident Response",
        "difficulty": "easy"
    },
    {
        "question": "Any sworn member involved in a firearms discharge incident is required to submit to mandatory ___ testing:",
        "options": [
            "Psychological",
            "Fitness",
            "Alcohol and drug",
            "Medical"
        ],
        "correct_answers": ["Alcohol and drug"],
        "explanation": "Any sworn member involved in a firearms discharge, on or off duty, must submit to mandatory alcohol and drug testing.",
        "reference": "G03-06 Firearm Discharge and Officer-Involved Death Incident Response",
        "difficulty": "easy"
    },
    
    # ILLINOIS CRIMINAL LAW (Questions 96-100)
    {
        "question": "A person commits aggravated vehicular hijacking when during the course of vehicular hijacking a child under ___ years old is in the vehicle:",
        "options": ["10", "12", "14", "16"],
        "correct_answers": ["16"],
        "explanation": "Aggravated vehicular hijacking applies when a child under 16 is in the vehicle during the hijacking.",
        "reference": "720 ILCS 5/18-4 Aggravated Vehicular Hijacking",
        "difficulty": "medium"
    },
    {
        "question": "A person convicted of conspiracy to commit first degree murder shall be sentenced to a Class ___ felony:",
        "options": ["X", "1", "2", "3"],
        "correct_answers": ["X"],
        "explanation": "Conspiracy to commit first degree murder is a Class X felony in Illinois.",
        "reference": "720 ILCS 5/8-2 Conspiracy",
        "difficulty": "hard"
    },
    {
        "question": "Drug induced homicide occurs when a person delivers a controlled substance to another and that person dies as a result of:",
        "options": [
            "Any use of the substance",
            "Injecting the substance",
            "The substance's effect on the body",
            "An allergic reaction"
        ],
        "correct_answers": ["Injecting, inhaling, or ingesting the substance"],
        "explanation": "Drug induced homicide applies when death results from injecting, inhaling, or ingesting the controlled substance delivered.",
        "reference": "720 ILCS 5/9-3.3 Drug Induced Homicide",
        "difficulty": "hard"
    },
    {
        "question": "A subject who intentionally and unlawfully kills another person and then conceals the body may be charged with:",
        "options": [
            "Only the homicide",
            "Both the homicide and concealment of homicidal death",
            "Only concealment",
            "Neither, as concealment is included"
        ],
        "correct_answers": ["Both the homicide and concealment of homicidal death"],
        "explanation": "The homicide and concealment of homicidal death are separate criminal offenses and can both be charged.",
        "reference": "720 ILCS 5/9-3.4 Concealment of Homicidal Death",
        "difficulty": "medium"
    },
    {
        "question": "A theft from an art museum of property valued at $150,000 is classified as a Class ___ felony:",
        "options": ["1", "2", "3", "4"],
        "correct_answers": ["1"],
        "explanation": "Theft from a museum of property exceeding $100,000 is a Class 1 felony in Illinois.",
        "reference": "720 ILCS 5/16-3 Theft from Museums",
        "difficulty": "medium"
    }
]

# Add MCQs to database
print("\nAdding 100 Practice Test MCQs...")
mcq_count = 0
for mcq_data in practice_mcqs:
    question_id = f"mcq_practice_{uuid.uuid4().hex[:12]}"
    mcq = {
        "question_id": question_id,
        "type": "multiple_choice",
        "category_id": "cat_practice_test",
        "category_name": "Practice Test",
        "question": mcq_data["question"],
        "options": mcq_data["options"],
        "correct_answers": mcq_data["correct_answers"],
        "explanation": mcq_data["explanation"],
        "reference": mcq_data["reference"],
        "difficulty": mcq_data["difficulty"],
        "is_practice_test": True,
        "source": "Based on previous practice from the testing company",
        "created_at": now,
        "updated_at": now
    }
    db.questions.insert_one(mcq)
    mcq_count += 1

print(f"Added {mcq_count} Practice Test MCQs")

# ============================================================================
# 5 GOLD SCENARIOS - Based on previous practice from the testing company
# ============================================================================

gold_scenarios = [
    {
        "title": "The Witness Identification",
        "content": """You are a detective assigned to investigate an armed robbery that occurred at 2100 hours at a convenience store. The store clerk, Maria Garcia, witnessed the robbery and describes the offender as a Hispanic male, approximately 25-30 years old, 5'10", wearing a black hoodie and jeans. A customer who was exiting the store, Thomas Williams, also got a brief look at the offender as he fled.

The suspect vehicle was described as a dark-colored sedan. Patrol officers stopped a vehicle matching this description 15 minutes after the robbery, about one mile from the scene. The driver, Roberto Martinez (age 28), matches the general description.

Sergeant Davis informs you that both witnesses are still at the scene and the suspect is being detained. He asks you to coordinate the identification process.

**Questions:**
1. What type of identification procedure would be most appropriate in this situation, and why?
2. What specific steps must you take before conducting this procedure?
3. Who should administer the identification procedure and what instructions must be given to the witnesses?
4. If a positive identification is made, what documentation is required?
5. What are the key legal considerations you must keep in mind throughout this process?""",
        "answer": json.dumps({
            "modelAnswer": {
                "R": [
                    "Ensure store clerk Maria Garcia is assessed for any injuries or shock from the armed robbery",
                    "Document Maria Garcia's physical and emotional condition",
                    "Ensure customer Thomas Williams is assessed and his condition documented",
                    "Confirm the detained suspect Roberto Martinez is secured and his condition documented",
                    "Obtain preliminary statement from Maria Garcia once stable"
                ],
                "E": [
                    "Speak with Sergeant Davis and responding officers for full initial briefing",
                    "Establish inner and outer perimeters around the convenience store crime scene",
                    "Separate Maria Garcia and Thomas Williams immediately to prevent witness contamination",
                    "Assign officers to secure the scene while identification procedure is coordinated",
                    "Keep Roberto Martinez at the detention location — separate from witnesses",
                    "Establish detective command post for coordinating the identification process"
                ],
                "A": [
                    "A show-up identification is most appropriate given the proximity in time (15 minutes) and distance (1 mile)",
                    "Show-ups must be conducted within a reasonable time after the crime — 15 minutes qualifies",
                    "Before conducting the show-up, document Roberto Martinez's appearance and any distinguishing features",
                    "Photograph Martinez before the identification to preserve his appearance at the time of the show-up",
                    "If positive identification is made, arrest Martinez and advise Miranda before any custodial interrogation",
                    "Document any spontaneous statements made by Martinez"
                ],
                "C": [
                    "Interview Maria Garcia and Thomas Williams completely separately — do NOT allow them to discuss the robbery",
                    "Before the show-up, document each witness's independent description of the suspect",
                    "The identification procedure should be administered by an officer NOT involved in the investigation (blind administration preferred)",
                    "Give proper admonishment: the suspect may or may not be present, it is equally important to clear innocent persons",
                    "Instruct witnesses that they should not feel pressured to make an identification",
                    "Conduct the show-up with one witness at a time — never present the suspect to both witnesses simultaneously",
                    "After identification, ask each witness to state their level of certainty",
                    "Instruct witnesses not to discuss their identifications with each other afterward"
                ],
                "T": [
                    "Document each witness's pre-identification description of the suspect in writing",
                    "Photograph Roberto Martinez as he appears at the time of the show-up",
                    "Document the exact time, location, and conditions of the show-up (lighting, distance, weather)",
                    "Record each witness's identification statement verbatim including certainty level",
                    "Complete all required CPD identification procedure forms",
                    "Document the officer administering the procedure and all persons present",
                    "Record the timeline: crime time, stop time, identification time",
                    "Preserve body-worn camera footage of the identification procedure"
                ],
                "I": [
                    "Process the convenience store crime scene for physical evidence: fingerprints, DNA, surveillance video",
                    "Obtain and preserve all surveillance camera footage from the store",
                    "Process Martinez's vehicle for any evidence linking to the robbery (weapon, proceeds, mask)",
                    "Photograph and inventory any items found in Martinez's possession or vehicle",
                    "Preserve all physical evidence with proper chain of custody",
                    "Request Forensic Services Division for scene processing"
                ],
                "O": [
                    "Consult ASA regarding charges based on the identification and evidence",
                    "Ensure the show-up procedure complies with CPD General Order and Illinois case law (Neil v. Biggers factors)",
                    "Legal considerations: necessity of the show-up, suggestiveness, reliability of the identification",
                    "Conduct LEADS and CLEAR checks on Roberto Martinez",
                    "Ensure 4th Amendment compliance with the vehicle stop and detention",
                    "Ensure 5th and 6th Amendment protections during any interrogation"
                ],
                "N": [
                    "If positive identification is made, prepare case for felony review and charging",
                    "If no identification is made, release Martinez and continue investigation through other leads",
                    "Continue processing the crime scene regardless of identification outcome",
                    "Check for any other robberies matching Martinez's description or vehicle",
                    "Prepare complete case file documenting the identification procedure for court",
                    "Follow up with both witnesses for complete formal statements",
                    "Coordinate court preparation and witness availability"
                ]
            }
        }),
        "time_limit": 900,  # 15 minutes
        "is_complex": True,
        "parts": 5,
        "study_tip": """R.E.A.C.T.I.O.N. Framework for Witness Identification Scenarios:

**R**ecognize: Identify the type of ID procedure needed (showup vs lineup)
**E**valuate: Assess timing - showups must be within ~1 hour
**A**ct: Separate witnesses immediately
**C**ommunicate: Coordinate with patrol, witnesses, and administrators
**T**ransport: Bring witness to suspect, not vice versa
**I**nstruct: Caution witness the person may or may not be the suspect
**O**bserve: Document exact words used during identification
**N**otify: Inform zone of positive/negative result"""
    },
    {
        "title": "The Photo Lineup",
        "content": """You are a detective investigating a series of three residential burglaries that occurred over the past two weeks in the same neighborhood. Through your investigation, you have identified a potential suspect, James Wilson, who has a prior arrest for burglary.

One victim, Mrs. Patricia Chen, reported that she came home and surprised the burglar, getting a good look at his face before he fled through the back door. She described the offender as a white male, early 30s, average height, with a distinctive tattoo on his left forearm.

Your supervisor has authorized you to prepare a photo lineup to present to Mrs. Chen. You have obtained a booking photo of Wilson, who matches the general description and has a visible tattoo on his left forearm.

**Questions:**
1. What are the minimum requirements for composing the photo lineup?
2. How should you select the filler photographs, and what considerations must guide your selection?
3. Who should conduct the lineup, and what procedures must be followed?
4. What form(s) must be completed and what must be documented?
5. What happens if Mrs. Chen makes a positive identification? What if she cannot make an identification?""",
        "answer": json.dumps({
            "modelAnswer": {
                "R": [
                    "Contact Mrs. Patricia Chen and assess her emotional condition and readiness for a photo lineup",
                    "Document Mrs. Chen's current physical and emotional state",
                    "Ensure Mrs. Chen has not been exposed to any photos or media coverage of the suspect",
                    "Confirm that Mrs. Chen is willing and able to participate in the identification procedure",
                    "Review Mrs. Chen's original description of the suspect for consistency"
                ],
                "E": [
                    "Prepare the photo lineup well in advance before bringing Mrs. Chen in",
                    "Minimum 6 photographs required for a CPD photo lineup (1 suspect + 5 fillers minimum)",
                    "Arrange a private, comfortable location for conducting the lineup procedure",
                    "Ensure an independent administrator (blind or blinded procedure) is available to conduct the lineup",
                    "Review all three burglary reports to understand the full pattern before proceeding"
                ],
                "A": [
                    "Select filler photographs that match the witness's description: white male, early 30s, average height",
                    "Critical: fillers should also have visible forearm tattoos to avoid making Wilson's tattoo a distinguishing outlier",
                    "Do NOT use fillers who look drastically different from Wilson — they should be similar in age, build, and features",
                    "Fillers should come from the same photo source (booking photos or similar quality/background)",
                    "Ensure Wilson's photo does not stand out due to different background, lighting, or photo quality",
                    "Do NOT inform Mrs. Chen that you have a suspect — maintain neutral posture"
                ],
                "C": [
                    "An independent administrator who does NOT know which photo is the suspect should conduct the lineup (double-blind preferred)",
                    "If double-blind is not possible, use a blinded procedure (folder shuffle method)",
                    "Give Mrs. Chen the standard admonishment BEFORE showing any photos",
                    "Admonishment must include: the suspect may or may not be in the photos, it is important to clear innocent persons",
                    "Instruct Mrs. Chen that the investigation will continue regardless of her identification",
                    "Present photos sequentially (one at a time) or simultaneously per CPD protocol",
                    "Do NOT provide any feedback, verbal or non-verbal, during or after the identification",
                    "Document Mrs. Chen's identification statement verbatim, including her level of certainty"
                ],
                "T": [
                    "Document Mrs. Chen's original description of the suspect before showing the lineup",
                    "Complete CPD Photo Lineup Form with all required information",
                    "Document the composition of the lineup: Wilson's position number and all filler sources",
                    "Record Mrs. Chen's exact response verbatim — whether identification is positive, negative, or uncertain",
                    "Document the administrator's name and their relationship to the case (should be none)",
                    "Document the date, time, and location of the procedure",
                    "Photograph or copy the lineup as it was presented to the witness",
                    "Document the confidence statement immediately after any identification"
                ],
                "I": [
                    "Preserve the physical photo lineup as evidence",
                    "If positive identification: search Wilson's residence (with warrant) for stolen property, tools, and clothing",
                    "Collect and compare latent prints from all three burglary scenes to Wilson's known prints",
                    "Check tool mark evidence from the burglary entry points for comparison",
                    "Photograph Wilson's left forearm tattoo for comparison to witness description",
                    "Process any additional evidence linking Wilson to the burglaries",
                    "Maintain chain of custody for all evidence including the lineup materials"
                ],
                "O": [
                    "If positive identification: consult ASA regarding charges for all three burglaries",
                    "Request search warrant for Wilson's residence, vehicle, and electronic devices",
                    "Conduct LEADS and CLEAR checks on Wilson for prior burglary convictions and arrest history",
                    "Run LEADS query on stolen property from all three burglaries",
                    "Ensure the photo lineup procedure complies with CPD General Order and Manson v. Brathwaite reliability factors",
                    "Ensure 4th Amendment compliance with any subsequent searches"
                ],
                "N": [
                    "If positive identification: arrest Wilson and prepare case for felony review",
                    "If no identification: continue investigation — the identification is one piece of evidence",
                    "Check pawn shops and online marketplaces for stolen property from all three burglaries",
                    "Check if Wilson has access to a vehicle or residence near the burglary pattern area",
                    "Interview Wilson's associates and known contacts",
                    "Monitor for additional burglaries matching the pattern",
                    "Prepare complete case file documenting the identification procedure for prosecution",
                    "Follow up with all three burglary victims regarding stolen property recovery"
                ]
            }
        }),
        "time_limit": 900,
        "is_complex": True,
        "parts": 5,
        "study_tip": """R.E.A.C.T.I.O.N. Framework for Photo Lineup Scenarios:

**R**ecognize: This requires a photo lineup, not a showup (time has passed)
**E**valuate: Ensure 6+ photos, similar fillers, same format
**A**ct: Secure independent administrator or approved alternative procedure
**C**ommunicate: Present Advisory Form, get witness signature
**T**ransport: N/A for photo lineups
**I**nstruct: Witness may or may not recognize anyone, no pressure
**O**bserve: Record the process, document exact statements
**N**otify: Complete all forms, inventory all photos"""
    },
    {
        "title": "The Domestic Violence Call",
        "content": """At 2300 hours, you are called to a residence at 4521 W. Monroe regarding a domestic disturbance. Upon arrival, you observe a woman, Jennifer Martinez (age 32), with visible facial injuries (swelling around left eye, cut on lip) sitting in the living room crying. Her husband, Carlos Martinez (age 35), is in the kitchen being detained by two uniformed officers.

Mrs. Martinez states that her husband came home intoxicated and accused her of infidelity. When she denied it, he punched her multiple times. Their two children, ages 8 and 5, witnessed part of the attack from the hallway before running to their bedroom.

Officer Rodriguez informs you that Mrs. Martinez has an Emergency Order of Protection against Carlos that was issued three days ago. Carlos was served with the order yesterday at his workplace. Additionally, Carlos is currently on probation for a previous domestic battery conviction.

**Questions:**
1. What are your immediate priorities at this scene?
2. What are the specific charges that apply in this situation?
3. How should you handle the interview process with the victim and the children?
4. What documentation and notifications are required?
5. What victim services and safety planning should you address?""",
        "answer": json.dumps({
            "modelAnswer": {
                "R": [
                    "Ensure Jennifer Martinez receives immediate medical attention for facial injuries (swelling around left eye, cut on lip)",
                    "Document Jennifer's injuries with photographs from multiple angles with and without scale",
                    "Assess the two children (ages 8 and 5) for physical injuries and emotional trauma",
                    "Arrange for a forensic interviewer or child specialist to assess the children if needed",
                    "Request EMS for medical evaluation of Jennifer's injuries if not already done",
                    "Obtain preliminary statement from Jennifer once medically stable and in a safe environment"
                ],
                "E": [
                    "Establish the scene: separate Carlos Martinez from Jennifer and the children immediately",
                    "Confirm with Officer Rodriguez that Carlos was served with the Emergency Order of Protection yesterday",
                    "Verify the Order of Protection is active and valid — obtain a copy if available",
                    "Secure the residence as a crime scene — document the condition of each room",
                    "Identify where in the home the assault occurred and preserve that area",
                    "Determine where the children were (hallway) when they witnessed the attack",
                    "Assign an officer to stay with the children in a safe area away from both parents"
                ],
                "A": [
                    "Carlos MUST be arrested — mandatory arrest when probable cause exists for DV battery",
                    "Multiple charges apply: Domestic Battery (720 ILCS 5/12-3.2), Violation of Order of Protection (720 ILCS 5/12-3.4), Aggravated Domestic Battery if great bodily harm",
                    "Violation of OP while on probation for prior DV battery is a Class 4 felony",
                    "Carlos's intoxication is an aggravating factor — document his level of intoxication",
                    "Photograph Carlos including his hands, knuckles, and any defensive injuries",
                    "Advise Miranda prior to any custodial interrogation",
                    "Document any spontaneous statements Carlos makes at the scene or during transport",
                    "Contact Carlos's probation officer regarding the new arrest and OP violation"
                ],
                "C": [
                    "Interview Jennifer in a private, safe setting away from Carlos and the children",
                    "Obtain a complete statement: what was said, the sequence of blows, and where the attack occurred",
                    "Interview the children with age-appropriate techniques and a trained interviewer if available",
                    "Determine what the children witnessed — they saw part of the attack from the hallway",
                    "Interview Officer Rodriguez and other responding officers about scene conditions upon arrival",
                    "Check for neighbors who may have heard or witnessed the disturbance",
                    "Obtain any 911 recordings — who called and what was reported",
                    "Ask Jennifer about the history of abuse, prior incidents, and whether the children have been abused"
                ],
                "T": [
                    "Photograph Jennifer's injuries: swelling around left eye, cut on lip, and any other marks",
                    "Photograph the scene of the assault including any overturned furniture or broken items",
                    "Photograph Carlos's hands, knuckles, and clothing for evidence of the attack",
                    "Document Carlos's level of intoxication and behavior at the scene",
                    "Record all actions in case report following domestic violence protocol",
                    "Document the existence and service of the Emergency Order of Protection",
                    "Document Carlos's prior domestic battery conviction and current probation status",
                    "Preserve copies of the OP, probation records, and prior call history",
                    "Review and secure all responding officers' body-worn camera footage"
                ],
                "I": [
                    "Collect and preserve any physical evidence from the assault (broken objects, blood, torn clothing)",
                    "Preserve Jennifer's clothing if it has blood or other forensic evidence",
                    "Photograph and collect any weapons or objects used in the assault",
                    "Obtain a copy of the Emergency Order of Protection and service documentation",
                    "Preserve the 911 call recording",
                    "Secure body-worn camera footage from all responding officers",
                    "Maintain chain of custody for all evidence"
                ],
                "O": [
                    "Notify ASA regarding charges: Domestic Battery, Violation of Order of Protection, possible Aggravated DV Battery",
                    "The OP violation while on probation elevates charges — consult ASA on felony charging",
                    "Request a no-bond hold given the OP violation, prior conviction, and probation status",
                    "Conduct LEADS and CLEAR checks on Carlos for full criminal history",
                    "Notify Carlos's probation officer of the new arrest",
                    "DCFS notification is required since children witnessed domestic violence",
                    "Ensure all constitutional protections are observed during interrogation"
                ],
                "N": [
                    "Provide Jennifer with the Domestic Violence Rights Pamphlet as required by law",
                    "Connect Jennifer with domestic violence victim advocate services",
                    "Offer Jennifer transportation to a domestic violence shelter if she feels unsafe at home",
                    "Advise Jennifer about the process for obtaining a Plenary Order of Protection",
                    "Develop a safety plan with Jennifer and the children",
                    "Arrange follow-up contact with Jennifer to check on her safety and the children",
                    "Prepare complete case file for felony review including prior history documentation",
                    "Coordinate with the children's school about the situation if appropriate",
                    "Refer media inquiries to Office of Communications"
                ]
            }
        }),
        "time_limit": 900,
        "is_complex": True,
        "parts": 5,
        "study_tip": """R.E.A.C.T.I.O.N. Framework for Domestic Violence Scenarios:

**R**ecognize: This is domestic battery + OP violation + children involved
**E**valuate: Scene safety, verify OP status, assess injuries
**A**ct: Arrest on OP violation, secure medical attention
**C**ommunicate: Separate interviews, trauma-informed approach
**T**ransport: Ensure proper processing of arrestee
**I**nstruct: Victim about her rights, OP process, resources
**O**bserve: Document injuries, scene, exact statements
**N**otify: DCFS, OP-issuing court, Probation, Detectives"""
    },
    {
        "title": "The School Threat Investigation",
        "content": """You are assigned to investigate a threat made against Lincoln Elementary School. This morning, the principal, Dr. Sarah Johnson, discovered a threatening message posted on the school's public social media page. The message stated: "Lincoln will pay for what they did to me. Tomorrow everyone will know my pain."

The message was posted from an account called "JusticeForMe2026" at 0245 hours. The account was created yesterday and has no other activity. The principal immediately contacted police and the school is currently on lockdown.

You arrive at the school at 0815 hours. Dr. Johnson provides you with screenshots of the message and the account profile. She mentions that a 14-year-old student, Marcus Thompson, was expelled last week for fighting and had made verbal threats during his disciplinary hearing, saying "they would be sorry."

**Questions:**
1. What are your immediate investigative steps?
2. How would you work to identify the person behind the social media account?
3. What coordination with other units or agencies is required?
4. If Marcus Thompson is identified as the poster, how would you proceed with the interview?
5. What charges might apply, and what additional considerations exist because the suspect is a juvenile?""",
        "answer": json.dumps({
            "modelAnswer": {
                "R": [
                    "Respond to Lincoln Elementary School and coordinate with school administration on lockdown status",
                    "Assess the threat level: is there an immediate danger to students and staff?",
                    "Ensure all students and staff are accounted for and in secure locations",
                    "Coordinate with school resource officer if one is assigned",
                    "Document Dr. Sarah Johnson's account of discovering the threat and the school's response",
                    "Assess whether additional police resources are needed to secure the school"
                ],
                "E": [
                    "Review the threatening message: 'Lincoln will pay for what they did to me. Tomorrow everyone will know my pain'",
                    "Assess the specificity and credibility of the threat — it references a specific target and timeframe ('tomorrow')",
                    "Establish a command post at the school for coordination with school administration",
                    "Determine whether the lockdown should continue or can be modified based on threat assessment",
                    "Identify all persons recently expelled, suspended, or disciplined by the school",
                    "Review Marcus Thompson's disciplinary hearing statements: 'they would be sorry'",
                    "Establish timeline: threat posted at 0245 hours, account created yesterday, school discovered this morning"
                ],
                "A": [
                    "Marcus Thompson is a juvenile (14 years old) — heightened protections apply throughout",
                    "Before approaching Marcus, obtain his home address and determine his current location",
                    "Contact Marcus's parents/guardians FIRST — they must be notified before any questioning",
                    "Marcus has the right to counsel before questioning (juvenile protections under Illinois law)",
                    "If Marcus is the poster, conduct interview with parent present in age-appropriate manner",
                    "Do NOT interrogate Marcus at school — bring to station with parent for proper juvenile interview",
                    "If probable cause exists, juvenile petition process applies — no adult arrest",
                    "Document any spontaneous statements made by Marcus"
                ],
                "C": [
                    "Interview Dr. Johnson about Marcus's expulsion, disciplinary hearing, and specific threats made",
                    "Interview teachers and staff who were present at Marcus's disciplinary hearing",
                    "Interview Marcus's classmates about his behavior, statements, and social media activity",
                    "Interview Marcus's parents about his behavior since the expulsion and any concerning statements",
                    "Check if other students or staff have received threats or concerning communications",
                    "Preserve screenshots of the threatening social media post and the 'JusticeForMe2026' account",
                    "Check if anyone saw Marcus with a phone or computer at the relevant times"
                ],
                "T": [
                    "Preserve screenshots of the threatening message with timestamps and account details",
                    "Document the 'JusticeForMe2026' account profile information, creation date, and activity history",
                    "Document Marcus's disciplinary records and exact statements at the hearing",
                    "Document the timeline: expulsion date, account creation, threat posting time, school discovery",
                    "Record all investigative actions in case report",
                    "Document school administration actions taken in response to the threat",
                    "Photograph school grounds and any security measures in place"
                ],
                "I": [
                    "Preserve all digital evidence: social media post, account metadata, screenshots",
                    "Request emergency preservation from the social media platform before data is deleted",
                    "Obtain the IP address and device information used to create the account and post the message",
                    "If Marcus is identified as the poster, secure his phone, computer, and any devices with a warrant",
                    "Conduct forensic extraction of Marcus's devices for evidence of account creation and posting",
                    "Preserve school records related to Marcus's expulsion and prior conduct",
                    "Maintain chain of custody for all digital and physical evidence"
                ],
                "O": [
                    "Request emergency disclosure from the social media platform for subscriber info and IP data (exigent circumstances given imminent threat)",
                    "If emergency disclosure is refused, obtain emergency search warrant for the account information",
                    "Subpoena ISP records to trace the IP address to a physical location",
                    "If Marcus is identified: consult ASA regarding juvenile charges",
                    "Potential charges: Disorderly Conduct — Threat (720 ILCS 5/26-1), Intimidation (720 ILCS 5/12-6)",
                    "Juvenile considerations: station adjustment vs. juvenile petition, age-appropriate processing",
                    "Coordinate with school district legal counsel regarding student records and privacy (FERPA)",
                    "Notify DCFS if investigation reveals concerning home environment"
                ],
                "N": [
                    "Coordinate with school administration on threat assessment and when to lift lockdown",
                    "Conduct a thorough threat assessment — is the threat credible and is there means/intent to carry it out?",
                    "Coordinate with school district safety team for ongoing security measures",
                    "Notify school district administration about the investigation",
                    "If Marcus is identified, coordinate with juvenile probation and the school on conditions",
                    "Refer media inquiries to Office of Communications",
                    "Avoid identifying Marcus publicly — juvenile privacy protections apply",
                    "Follow up with school administration on safety plan and return-to-normal procedures",
                    "Prepare complete case file for juvenile court if charges are filed"
                ]
            }
        }),
        "time_limit": 900,
        "is_complex": True,
        "parts": 5,
        "study_tip": """R.E.A.C.T.I.O.N. Framework for School Threat Scenarios:

**R**ecognize: Serious threat requiring immediate action + juvenile suspect
**E**valuate: Credibility of threat, identify potential suspects
**A**ct: Preserve digital evidence, secure scene, request technical assistance
**C**ommunicate: Schools, CPIC, Crime Analysis Technical Group
**T**ransport: If arrested, process as juvenile with extra protections
**I**nstruct: Parents of their rights, juvenile of their rights
**O**bserve: All digital evidence, statements, timeline
**N**otify: Parents, school officials, proper juvenile processing units"""
    },
    {
        "title": "The Live Lineup Challenge",
        "content": """You are a detective investigating a robbery/sexual assault that occurred last night at 2200 hours in an alley behind 3400 S. Kedzie. The victim, Ms. Angela Davis, was attacked at knifepoint by an unknown male who demanded her purse and then sexually assaulted her. She fought back and scratched the offender's face before he fled.

Ms. Davis provided a description: Black male, 25-35 years old, approximately 6 feet tall, medium build, with short hair and a goatee. She states she got a good look at his face during the assault and is confident she can identify him.

Two hours ago, patrol officers arrested Jerome Williams (28 years old, Black male, 6'1", medium build, short hair, goatee) for an unrelated warrant. Williams has fresh scratches on his left cheek. The district station is holding him.

Your supervisor wants you to conduct a live lineup with Ms. Davis. However, Williams has invoked his right to an attorney, and his public defender, Attorney Michelle Roberts, has arrived at the station. Attorney Roberts states that she must be present for any lineup.

**Questions:**
1. Does Attorney Roberts have the right to be present at the lineup? Explain the legal basis.
2. What are the requirements for composing a proper live lineup?
3. Describe the step-by-step procedure you would follow to conduct this lineup.
4. What challenges might arise with the fillers, given Williams' distinctive scratch marks?
5. How would you document this procedure, and what forms are required?""",
        "answer": json.dumps({
            "modelAnswer": {
                "R": [
                    "Ensure Ms. Angela Davis has received medical attention and SANE examination for the sexual assault",
                    "Assess Ms. Davis's physical and emotional readiness to participate in a lineup identification",
                    "Document Ms. Davis's current condition and confirm she is willing to proceed with the lineup",
                    "Confirm that Jerome Williams is being held at the station on his warrant and document his condition",
                    "Document the fresh scratches on Williams's left cheek — consistent with victim's account of scratching her attacker",
                    "Request DNA comparison between Williams's scratches and Ms. Davis's fingernail scrapings from the SANE exam"
                ],
                "E": [
                    "Prepare the lineup room and procedures before bringing in Ms. Davis or Williams",
                    "Attorney Roberts DOES have the right to be present — post-indictment/formal charge right under 6th Amendment (United States v. Wade)",
                    "If Williams has NOT been formally charged with this crime, the 6th Amendment right may not yet attach",
                    "However, if this is post-arrest/formal charging, counsel must be permitted to observe",
                    "Attorney Roberts may observe but may NOT disrupt, coach, or interfere with the procedure",
                    "Attorney Roberts may make objections on the record regarding the fairness of the lineup composition"
                ],
                "A": [
                    "A live lineup requires a minimum of 5 fillers plus the suspect (6 persons total) per CPD policy",
                    "Select fillers who match Ms. Davis's description: Black male, 25-35, approximately 6 feet, medium build, short hair, goatee",
                    "Critical challenge: Williams has fresh scratches on his left cheek — fillers must be addressed to prevent Williams from standing out",
                    "Options for addressing the scratches: apply theatrical makeup to conceal, apply similar marks to fillers, or have all participants hold a card over that area",
                    "The goal is to prevent the scratches from making Williams the obvious choice — the identification must be based on facial recognition",
                    "Fillers should be similar in age, height, build, and overall appearance to Williams",
                    "Do NOT use fillers who look drastically different from Williams"
                ],
                "C": [
                    "An independent administrator who does NOT know which person is the suspect should conduct the lineup (double-blind preferred)",
                    "Give Ms. Davis the standard admonishment BEFORE viewing the lineup",
                    "Admonishment must include: the suspect may or may not be present, it is important to clear innocent persons, the investigation continues regardless",
                    "Instruct Ms. Davis that hairstyles, facial hair, and other features may have changed since the incident",
                    "Present lineup members one at a time or all at once per CPD protocol",
                    "Do NOT provide any verbal or non-verbal feedback during or after the identification",
                    "Document Ms. Davis's identification statement verbatim, including her level of certainty",
                    "Allow Attorney Roberts to observe but ensure she does not communicate with Williams during the procedure"
                ],
                "T": [
                    "Document Ms. Davis's original description of the attacker before the lineup",
                    "Videotape the entire lineup procedure for the record",
                    "Complete all required CPD lineup forms and documentation",
                    "Document the lineup composition: Williams's position number, all fillers' descriptions",
                    "Document how the scratch mark issue was handled (concealment method used)",
                    "Record Ms. Davis's exact response and confidence level verbatim",
                    "Document Attorney Roberts's presence and any objections she made on the record",
                    "Document the administrator's identity and their lack of knowledge about which participant is the suspect"
                ],
                "I": [
                    "Preserve the lineup video recording as evidence",
                    "Request DNA comparison: scrapings from Williams's scratches vs. Ms. Davis's DNA from SANE exam",
                    "Request DNA comparison: Ms. Davis's fingernail scrapings vs. Williams's DNA",
                    "Collect and preserve Williams's clothing for forensic comparison with trace evidence from the victim",
                    "Process the crime scene (alley behind 3400 S. Kedzie) for physical evidence if not already done",
                    "Obtain and preserve the knife if recovered, or continue search for the weapon",
                    "Photograph Williams's scratches in detail for comparison to victim's account",
                    "Maintain strict chain of custody for all evidence"
                ],
                "O": [
                    "Consult ASA regarding charges: Robbery (720 ILCS 5/18-1) and Criminal Sexual Assault (720 ILCS 5/11-1.20)",
                    "Legal basis for Attorney Roberts's presence: Wade/Gilbert right to counsel at post-charge lineups",
                    "If Williams has not been formally charged with this crime, attorney's right to attend is less clear — consult ASA",
                    "Best practice: allow the attorney to observe to prevent future suppression challenges",
                    "Request search warrants for Williams's phone, residence, and clothing",
                    "Conduct LEADS and CLEAR checks on Williams for prior sex offenses or violent crimes",
                    "Ensure the lineup procedure complies with Manson v. Brathwaite reliability factors",
                    "Ensure 5th and 6th Amendment protections throughout"
                ],
                "N": [
                    "If positive identification: file charges through felony review",
                    "If no identification: the DNA evidence and scratches may still support charges — continue investigation",
                    "Submit all forensic evidence (DNA, clothing fibers, trace evidence) to the crime lab expeditiously",
                    "Connect Ms. Davis with victim advocate services and sexual assault support resources",
                    "Develop safety plan for Ms. Davis",
                    "Check if Williams has any connection to similar crimes in the area",
                    "Prepare complete case file documenting the lineup procedure for court — anticipate defense challenge",
                    "Coordinate with ASA on court preparation, particularly regarding the lineup procedure and scratch evidence"
                ]
            }
        }),
        "time_limit": 1200,  # 20 minutes
        "is_complex": True,
        "parts": 5,
        "study_tip": """R.E.A.C.T.I.O.N. Framework for Live Lineup Scenarios:

**R**ecognize: Live lineup appropriate when suspect in custody; know 6th Amendment rules
**E**valuate: Has the suspect been arraigned? This determines attorney rights
**A**ct: Get independent administrator, prepare 6+ participants, handle distinctive features
**C**ommunicate: Advisory Form to witness, document consent for recording
**T**ransport: Bring witness to lineup location
**I**nstruct: Witness that suspect may or may not be present
**O**bserve: Record everything, photograph lineup, document exact words
**N**otify: Complete all forms, note any accommodations made (scratches), inventory"""
    }
]

# Add Gold Scenarios to database
print("\nAdding 5 Gold Scenarios...")
scenario_count = 0
for scenario_data in gold_scenarios:
    question_id = f"scenario_gold_{uuid.uuid4().hex[:12]}"
    scenario = {
        "question_id": question_id,
        "type": "scenario",
        "category_id": "cat_gold_scenarios",
        "category_name": "Gold Scenarios",
        "title": scenario_data["title"],
        "content": scenario_data["content"],
        "answer": scenario_data["answer"],
        "model_answer": scenario_data["answer"],
        "time_limit": scenario_data["time_limit"],
        "is_complex": scenario_data["is_complex"],
        "parts": scenario_data["parts"],
        "study_tip": scenario_data["study_tip"],
        "difficulty": "hard",
        "is_gold": True,
        "source": "Based on previous practice scenarios from the testing company",
        "created_at": now,
        "updated_at": now
    }
    db.questions.insert_one(scenario)
    scenario_count += 1

print(f"Added {scenario_count} Gold Scenarios")

# Final counts
print("\n=== Final Content Counts ===")
fc_count = db.questions.count_documents({'type': 'flashcard'})
print(f'Flashcards: {fc_count}')
sc_count = db.questions.count_documents({'type': 'scenario'})
print(f'Scenarios: {sc_count}')
mcq_count = db.questions.count_documents({'type': 'multiple_choice'})
print(f'MCQs: {mcq_count}')

# Practice test specific
practice_mcq = db.questions.count_documents({'category_id': 'cat_practice_test'})
gold_scenario = db.questions.count_documents({'category_id': 'cat_gold_scenarios'})
print(f'\nPractice Test MCQs: {practice_mcq}')
print(f'Gold Scenarios: {gold_scenario}')

print("\n✅ Content seeding complete!")
