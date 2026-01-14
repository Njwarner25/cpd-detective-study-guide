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

async def seed_additional_questions():
    """Add more questions based on CPD Detective Exam requirements"""
    
    # Based on the exam PDF, these topics are critical
    additional_flashcards = [
        # Community Policing and Procedural Justice
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Procedural Justice Principles",
            "content": "What are the four key principles of procedural justice that CPD detectives must apply?",
            "answer": "1) Voice - giving people opportunity to be heard; 2) Neutrality - making transparent, consistent decisions; 3) Respect - treating people with dignity; 4) Trustworthiness - showing concern for people's needs and rights.",
            "explanation": "Procedural justice is mandated by the Consent Decree and is essential for building community trust. These principles apply to all interactions with the public, witnesses, and suspects.",
            "difficulty": "medium",
            "reference": "Consent Decree - Procedural Justice Requirements"
        },
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "De-escalation Techniques",
            "content": "What are the primary de-escalation strategies detectives should employ during investigations?",
            "answer": "1) Slow down the pace of the encounter; 2) Create distance and use time to your advantage; 3) Use calm verbal communication; 4) Request additional resources/backup; 5) Employ crisis intervention techniques; 6) Assess for mental health crisis; 7) Avoid actions that may escalate.",
            "explanation": "De-escalation is required before force whenever safe and feasible. Detectives often interact with people in crisis and must be skilled at reducing tension.",
            "difficulty": "medium",
            "reference": "Consent Decree - Force Mitigation & De-escalation"
        },
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Impartial Policing",
            "content": "What constitutes bias-based policing and what are detectives required to do to ensure impartial policing?",
            "answer": "Bias-based policing is using race, ethnicity, national origin, religion, disability, gender, gender identity, sexual orientation, or other protected class as a factor in decision-making. Detectives must: 1) Base decisions on reasonable suspicion/probable cause, not stereotypes; 2) Document reasons for all enforcement actions; 3) Treat all persons equally; 4) Report biased policing they observe.",
            "explanation": "Impartial policing is a cornerstone of constitutional policing and required by the Consent Decree. All investigative decisions must be based on objective facts.",
            "difficulty": "hard",
            "reference": "Consent Decree - Impartial Policing"
        },
        
        # Digital Evidence & Technology
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Digital Evidence Collection",
            "content": "What are the proper procedures for collecting and preserving digital evidence from cell phones and computers?",
            "answer": "1) Document device condition, make/model, serial numbers; 2) Photograph device as found; 3) Isolate device from networks (airplane mode, Faraday bag); 4) Do NOT attempt to access without proper authority/training; 5) Maintain chain of custody; 6) Transport in anti-static packaging; 7) Obtain warrant for data extraction; 8) Use certified forensic examiner.",
            "explanation": "Digital evidence is fragile and can be easily altered or destroyed. Improper handling can make evidence inadmissible. Always involve digital forensics specialists.",
            "difficulty": "hard",
            "reference": "CPD Training Bulletin - Digital Evidence Collection"
        },
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Automated License Plate Readers (ALPR)",
            "content": "What are the authorized uses and restrictions for ALPR data in investigations?",
            "answer": "Authorized uses: 1) Locate stolen vehicles; 2) Track vehicles involved in serious crimes; 3) Locate wanted persons; 4) Amber/Silver alerts. Restrictions: 1) Cannot be used for general surveillance; 2) Data retention limited to specific timeframes; 3) Queries must be logged and justified; 4) Cannot be used to track individuals based on First Amendment activities; 5) Must comply with privacy policies.",
            "explanation": "ALPR is a powerful investigative tool but subject to strict policies to protect privacy rights. Misuse can result in discipline and civil liability.",
            "difficulty": "hard",
            "reference": "CPD General Order - ALPR Usage Policy"
        },
        
        # Illinois Criminal Law - Additional Offenses
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Home Invasion - 720 ILCS 5/19-6",
            "content": "What are the elements of Home Invasion in Illinois?",
            "answer": "Home Invasion occurs when a person, without authority, knowingly enters the dwelling place of another when they know or have reason to know someone is present, AND: (1) intentionally inflicts bodily harm, OR (2) is armed with a dangerous weapon, OR (3) uses force or threatens imminent force. It is a Class X felony.",
            "explanation": "Home Invasion is more serious than burglary because it involves occupied dwellings and danger to occupants. No intent to commit felony/theft is required - the dangerous conduct itself is the crime. Carries 6-30 years, no probation.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/19-6"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Unlawful Use of Weapons (UUW) - 720 ILCS 5/24-1",
            "content": "What are the key circumstances that make weapon possession unlawful in Illinois?",
            "answer": "UUW includes: 1) Carrying concealed firearm without valid FOID/CCL; 2) Carrying firearm in vehicle without FOID/CCL and not properly secured; 3) Possessing firearm with defaced serial number; 4) Selling/giving firearm to person without FOID; 5) Possessing firearm while subject to protection order; 6) Gang member with firearm; 7) Felon with firearm (separate statute). Classification varies from Class A misdemeanor to Class 2 felony.",
            "explanation": "UUW has many variations. Must distinguish between simple UUW (Class A misdemeanor) and aggravated UUW (felony based on location, prior convictions, gang membership). FOID Act violations also apply.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/24-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Aggravated Assault - 720 ILCS 5/12-2",
            "content": "What factors elevate simple assault to aggravated assault?",
            "answer": "Assault becomes aggravated when: (1) Committed in a public place; (2) Victim is certain protected persons (police, firefighter, teacher, correctional officer, etc.); (3) Offender uses deadly weapon; (4) Offender wears hood/mask; (5) Offender discharges firearm from vehicle; (6) Victim is over 60 or physically handicapped; (7) Offender knows victim is pregnant. Can be Class A misdemeanor to Class 4 felony depending on circumstances.",
            "explanation": "Assault requires no physical contact - only placing person in reasonable apprehension of receiving battery. Context and victim status determine classification. Public place assault is Class A misdemeanor; assault on police is Class 4 felony.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/12-2"
        },
        
        # CPD Specific Procedures
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Tactical Response Reports (TRR)",
            "content": "When must a detective complete a Tactical Response Report?",
            "answer": "TRR required when officer: 1) Uses force greater than escort techniques; 2) Deploys Taser or OC spray; 3) Discharges firearm (excluding range); 4) Uses impact weapon; 5) Takes action resulting in injury requiring medical treatment; 6) Uses canine to apprehend. Must be completed before end of tour. Supervisor must review and approve.",
            "explanation": "TRRs are critical for documenting force and ensuring accountability. They are reviewed by multiple levels of supervision and analyzed for patterns. Failure to complete TRR or false statements constitute serious policy violations.",
            "difficulty": "medium",
            "reference": "CPD General Order G03-02-01"
        },
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Body-Worn Cameras (BWC) Requirements",
            "content": "When must detectives activate body-worn cameras during investigations?",
            "answer": "BWC must be activated: 1) All law enforcement-related encounters with public; 2) Traffic stops; 3) Arrests; 4) Searches; 5) Witness/victim interviews (unless they object); 6) Any use of force; 7) Pursuits; 8) Responses to calls for service. Must record continuously until conclusion of encounter. Prohibited: recording in sensitive locations (hospitals, schools) without exigency, or recording confidential informants.",
            "explanation": "BWC provides transparency, protects against false claims, and preserves evidence. Detectives must be familiar with activation requirements and prohibited uses. Failure to activate can result in discipline and evidentiary issues.",
            "difficulty": "medium",
            "reference": "CPD Special Order S03-14"
        },
        
        # Crime Analysis and Patterns
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Crime Pattern Analysis",
            "content": "What information must detectives provide to crime analysts to identify patterns and trends?",
            "answer": "Detectives must document: 1) Modus operandi (MO) - method of operation; 2) Suspect description and vehicle information; 3) Property descriptions (serial numbers, unique identifiers); 4) Time/day/location patterns; 5) Victim selection criteria; 6) Tools/weapons used; 7) Suspect statements/language; 8) Physical evidence types. This allows analysts to link cases and identify serial offenders.",
            "explanation": "Pattern recognition is crucial for solving serial crimes. Detailed reporting enables CLEAR system to identify connections. Detectives should proactively review similar cases in their area and coordinate with crime analysts.",
            "difficulty": "medium",
            "reference": "CPD Training - Crime Analysis"
        },
        
        # Special Victims
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Child Abuse Investigations",
            "content": "What are the mandatory reporting and investigation procedures for suspected child abuse?",
            "answer": "1) Immediately notify DCFS hotline (1-800-25-ABUSE) if under 18 years old; 2) Contact specialized detectives (SVU/Area Youth Division); 3) Separate child from caregiver for interview when appropriate; 4) Use forensic interviewers when possible to avoid re-traumatization; 5) Do NOT contaminate child's statements; 6) Photograph injuries; 7) Coordinate with DCFS investigator; 8) Consider protective custody; 9) Document everything thoroughly.",
            "explanation": "Child abuse investigations require specialized training. Officers are mandated reporters under Illinois law. Improper interviewing can contaminate case. Many jurisdictions have Child Advocacy Centers with trained forensic interviewers.",
            "difficulty": "hard",
            "reference": "325 ILCS 5/ - Abused and Neglected Child Reporting Act"
        },
    ]
    
    # Add challenging scenarios based on exam competencies
    additional_scenarios = [
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Officer-Involved Shooting Investigation",
            "content": """You are assigned as the lead detective to investigate an officer-involved shooting that occurred during a foot pursuit. The subject was fleeing from a reported armed robbery and was shot by the pursuing officer. The subject is deceased. Witnesses are present, including community members who are hostile toward police. Body-worn camera footage exists but has not been reviewed yet.

As the lead detective, outline your investigative plan for the first 6 hours. What steps will you take, in what order, and why? Consider evidence preservation, witness management, officer interviews, community relations, and compliance with CPD policies and the Consent Decree.""",
            "answer": """PRIORITY ACTIONS (First 6 Hours):

IMMEDIATE SCENE MANAGEMENT (0-30 minutes):
1. Ensure scene security and medical aid rendered
2. Establish outer perimeter to preserve evidence
3. Request supervisor and additional resources
4. Separate involved officer from witnessing officers
5. Identify and separate all witnesses
6. Request COPA (Civilian Office of Police Accountability) notification
7. Notify command staff and Public Safety Headquarters
8. Request Evidence Technicians and Crime Scene Processing

EVIDENCE PRESERVATION (30 minutes - 2 hours):
1. Photograph scene before any evidence moved
2. Locate and secure all physical evidence (weapon, cartridge casings, blood, etc.)
3. Identify and mark evidence locations
4. Secure BWC and in-car cameras from all officers
5. Canvas for surveillance cameras in area
6. Create scene diagram/sketch
7. DO NOT REVIEW BWC until after officer interview (to preserve independent recollection)

WITNESS MANAGEMENT (1-3 hours):
1. Conduct preliminary interviews with all witnesses separately
2. Obtain contact information and detailed statements
3. Identify witness viewpoints and what they observed
4. Document witness demeanor and credibility factors
5. Consider video recording witness statements
6. For hostile witnesses, remain professional and document concerns
7. Canvas area for additional witnesses

OFFICER PROTOCOLS (2-4 hours):
1. Ensure involved officer has access to union representation
2. Conduct public safety statement (limited to immediate threat info)
3. DO NOT conduct full interview until after 24-hour waiting period
4. Separate officer from scene
5. Secure officer's firearm for evidence
6. Ensure officer has support/counseling services

COMMUNITY RELATIONS (Ongoing):
1. Provide PIO (Public Information Officer) with approved information
2. Ensure community members are treated with respect and dignity
3. Document all community interactions
4. Coordinate with Community Affairs for any necessary outreach
5. Be transparent about process while protecting integrity of investigation

COORDINATION AND COMPLIANCE (3-6 hours):
1. Brief COPA investigators and coordinate roles
2. Ensure compliance with Consent Decree requirements
3. Complete required notifications per General Orders
4. Begin preparing reports and documentation
5. Request Medical Examiner response
6. Coordinate with State's Attorney if criminal investigation warranted
7. Ensure BWC footage secured and preserved

CRITICAL CONSIDERATIONS:
- Under Consent Decree, officer must give statement within 24 hours (with limited exceptions)
- COPA has independent investigative authority
- Community transparency is important but cannot compromise investigation
- All force must be reviewed for compliance with CPD policies
- Pattern and practice implications require thorough documentation
- Officer's actions will be judged by objectively reasonable standard (Graham v. Connor)

PROHIBITED ACTIONS:
- Do not allow officers to confer on facts before statements
- Do not review BWC before officer gives independent account
- Do not make premature conclusions
- Do not allow evidence contamination
- Do not disregard community concerns""",
            "explanation": "Officer-involved shootings are the most scrutinized investigations. They require balancing multiple interests: thorough investigation, officer rights, community trust, and legal requirements. The Consent Decree imposes specific requirements. COPA has primary investigative authority for officer-involved shootings. The detective's role is to assist and ensure proper evidence collection. This scenario tests knowledge of: 1) Crime scene management, 2) Evidence preservation, 3) Consent Decree requirements, 4) COPA coordination, 5) Community relations, 6) Officer rights and protocols.",
            "difficulty": "hard",
            "reference": "Consent Decree, CPD General Order G03-02, COPA enabling ordinance"
        },
        {
            "type": "scenario",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Home Invasion vs. Burglary - Charging Decision",
            "content": """You are investigating a case where the offender forced entry into a residence at 2:00 AM. The homeowner was asleep upstairs when awakened by noise. The offender was found by police inside the home, near the back door, with a crowbar and a pillowcase containing jewelry and electronics. The offender claims he thought the house was vacant and was just there to steal property, not harm anyone. The homeowner was terrified but not physically harmed.

The offender has no weapon other than the crowbar used for entry. The offender states he ran when he heard someone upstairs and was trying to leave when police arrived. There is evidence the offender had been watching the house and knew the owner's schedule.

What charges are supported? Is this Residential Burglary (Class 1 felony) or Home Invasion (Class X felony, 6-30 years mandatory)? Justify your charging decision with legal analysis.""",
            "answer": """LEGAL ANALYSIS:

RESIDENTIAL BURGLARY (720 ILCS 5/19-3):
Elements: (1) Without authority, (2) Knowingly enters or remains within dwelling, (3) With intent to commit felony/theft
Class 1 Felony: 4-15 years

HOME INVASION (720 ILCS 5/19-6):
Elements: (1) Without authority, (2) Knowingly enters dwelling, (3) Knows or has reason to know someone is present, AND (4) Either:
   a) Intentionally inflicts bodily harm, OR
   b) Armed with dangerous weapon, OR  
   c) Uses/threatens imminent force
Class X Felony: 6-30 years, no probation

CHARGING DECISION: HOME INVASION

ANALYSIS:
1. WITHOUT AUTHORITY: ✓ Forced entry through back door - clearly no authority

2. KNOWINGLY ENTERS DWELLING: ✓ Admittedly entered residence

3. KNOWS/REASON TO KNOW PERSON PRESENT: ✓ CRITICAL ELEMENT
   - Home invasion at 2:00 AM when people are typically home
   - Evidence he watched house and knew schedule suggests he knew or should have known someone could be present
   - Residential dwelling creates presumption of occupancy
   - Illinois courts have held that entry in early morning hours supports inference of knowledge of presence

4. ARMED WITH DANGEROUS WEAPON: ✓
   - Crowbar used for entry qualifies as dangerous weapon
   - Not required that weapon be used against person
   - Mere possession during home invasion sufficient
   - Illinois courts consistently hold that burglary tools (crowbars, pry bars) are dangerous weapons for home invasion purposes

OFFENDER'S DEFENSE ARGUMENTS (and Rebuttals):
"I thought house was vacant":
- Rebutted by: surveillance of house, 2 AM entry time, occupancy is presumed in residential dwelling
- 720 ILCS 5/19-6 requires only "reason to know" not actual knowledge
- Willful blindness doctrine applies

"I didn't intend to hurt anyone":
- Irrelevant - no intent to harm required
- Home Invasion complete when armed and knew/should know person present
- Intent to commit theft sufficient

"I was leaving when caught":
- Crime already complete upon armed entry with knowledge/reason to know occupancy
- Abandonment not a defense once elements met

"Crowbar was only for entry, not a weapon":
- Distinction irrelevant under statute
- Any dangerous weapon during home invasion sufficient
- Courts broadly interpret "dangerous weapon"

ALTERNATIVE CHARGE ANALYSIS:
If charged with only Residential Burglary:
- Prosecution would argue insufficient because offender armed with dangerous weapon and had reason to know occupant present
- Judge/jury could potentially find Home Invasion proven even if charged with lesser offense

PROPER CHARGES:
Primary: HOME INVASION (720 ILCS 5/19-6) - Class X
Alternative: RESIDENTIAL BURGLARY (720 ILCS 5/19-3) - Class 1  
Additional: POSSESSION OF BURGLARY TOOLS (720 ILCS 5/19-2) - Class 4
Additional: THEFT (value determines class) - (720 ILCS 5/16-1)

STATE'S ATTORNEY APPROVAL:
Home Invasion requires felony review. Present:
- Fact pattern supporting all elements
- Crowbar as dangerous weapon
- 2 AM entry creating inference of knowledge
- Victim impact (terror/trauma)
- Case law supporting charging decision

RECOMMENDATION: Charge HOME INVASION as primary count with Residential Burglary as alternative. The crowbar, early morning entry time, and evidence of surveillance establish defendant knew or had reason to know the dwelling was occupied. Illinois courts have consistently upheld Home Invasion charges under similar circumstances.""",
            "explanation": "This scenario tests critical analysis skills in differentiating between similar offenses with vastly different penalties. Home Invasion is one of Illinois' most serious offenses due to the danger to occupants. The key distinguishing factors are: (1) knowledge/reason to know of presence, and (2) being armed/using force. Many offenders claim they thought dwelling was vacant, but courts apply an objective standard. The 'reason to know' language is critical - it's not actual knowledge but what a reasonable person should know. Time of day, type of dwelling, and circumstances all factor in. The crowbar issue is important - courts broadly construe 'dangerous weapon' in home invasion cases. This is a Class X vs. Class 1 felony decision with mandatory prison implications.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/19-6, 720 ILCS 5/19-3, People v. Dempsey (Illinois case law)"
        },
    ]
    
    # Insert questions
    now = datetime.now(timezone.utc)
    all_questions = additional_flashcards + additional_scenarios
    
    count = 0
    for q in all_questions:
        q["question_id"] = f"q_{uuid.uuid4().hex[:12]}"
        q["created_at"] = now
        q["updated_at"] = now
        
        await db.questions.update_one(
            {"question_id": q["question_id"]},
            {"$set": q},
            upsert=True
        )
        count += 1
    
    print(f"✓ Added {len(additional_flashcards)} new flashcards and {len(additional_scenarios)} new scenarios")
    print(f"✓ Total questions added: {count}")

async def main():
    print("🌱 Adding additional exam content...")
    await seed_additional_questions()
    print("✅ Additional content seeding complete!")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
