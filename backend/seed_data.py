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
        }
    ]
    
    for cat in categories:
        await db.categories.update_one(
            {"category_id": cat["category_id"]},
            {"$set": cat},
            upsert=True
        )
    print(f"✓ Seeded {len(categories)} categories")

async def seed_questions():
    """Create mock flashcard and scenario questions"""
    
    flashcards = [
        # General Orders
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Use of Force - General Order G03-02",
            "content": "According to CPD General Order G03-02, when is deadly force authorized?",
            "answer": "Deadly force is authorized when it is objectively reasonable and necessary to prevent death or great bodily harm to the member or another person, or to prevent a forcible felony.",
            "explanation": "This follows the constitutional standard set by Graham v. Connor and Tennessee v. Garner. Officers must consider the totality of circumstances and de-escalate when safe and feasible.",
            "difficulty": "medium",
            "reference": "General Order G03-02: Use of Force"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Chain of Command",
            "content": "What is the proper chain of command starting from a Detective?",
            "answer": "Detective → Sergeant → Lieutenant → Captain → Commander → Deputy Chief → Bureau Chief → First Deputy Superintendent → Superintendent",
            "explanation": "Understanding the chain of command is essential for proper reporting and communication within the department structure.",
            "difficulty": "easy",
            "reference": "General Order G01-02: Organization for Command"
        },
        {
            "type": "flashcard",
            "category_id": "cat_general_orders",
            "category_name": "General Orders",
            "title": "Miranda Rights",
            "content": "When must Miranda warnings be given during an investigation?",
            "answer": "Miranda warnings must be given before any custodial interrogation - when a person is in custody (not free to leave) AND being interrogated by law enforcement.",
            "explanation": "Both elements must be present: custody + interrogation. Voluntary statements made without questioning do not require Miranda.",
            "difficulty": "medium",
            "reference": "General Order G03-01-01: Arrest and Detention"
        },
        
        # Illinois Criminal Law
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Aggravated Battery - 720 ILCS 5/12-3.05",
            "content": "What elevates a battery to aggravated battery under Illinois law?",
            "answer": "Battery becomes aggravated when: (1) Great bodily harm or permanent disability/disfigurement occurs, (2) The victim is certain protected persons (police, firefighter, teacher, etc.), (3) A deadly weapon or firearm is used, (4) Battery occurs in a public place, or (5) The victim is over 60 or physically handicapped.",
            "explanation": "Aggravated battery is a Class 3 felony, but can be enhanced to Class X with firearm involvement.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/12-3.05"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Burglary - 720 ILCS 5/19-1",
            "content": "What are the elements of burglary in Illinois?",
            "answer": "Burglary requires: (1) Knowingly entering or remaining within a building, (2) Without authority, (3) With intent to commit a felony or theft therein. No actual theft or felony needs to occur - only the intent at time of entry.",
            "explanation": "Intent is critical and must exist at the time of entry. Residential burglary is a Class 1 felony; other burglary is Class 2.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/19-1"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Armed Robbery - 720 ILCS 5/18-2",
            "content": "What distinguishes armed robbery from robbery in Illinois?",
            "answer": "Armed robbery occurs when during a robbery, the offender carries or is armed with a dangerous weapon, indicates verbally or by actions possession of a weapon, or discharges a firearm. It is a Class X felony with mandatory prison time.",
            "explanation": "Even a fake weapon qualifies if the victim reasonably believes it's real. Armed robbery with firearm discharge carries 20-life sentence.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/18-2"
        },
        {
            "type": "flashcard",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Theft Classification - 720 ILCS 5/16-1",
            "content": "At what dollar amounts does theft classification change in Illinois?",
            "answer": "Under $500: Class A misdemeanor; $500-$10,000: Class 3 felony; $10,000-$100,000: Class 2 felony; $100,000-$500,000: Class 1 felony; Over $500,000 or theft from place of worship: Class X felony.",
            "explanation": "Theft from a person (regardless of amount) is also a felony. Multiple thefts as part of a single scheme can be aggregated.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/16-1"
        },
        
        # Evidence Handling
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Chain of Custody",
            "content": "What are the critical elements of maintaining chain of custody for evidence?",
            "answer": "Chain of custody requires documenting: (1) Who collected the evidence, (2) Date/time of collection, (3) Every person who handled it, (4) Dates/times of transfers, (5) Storage location, (6) Purpose of each transfer. Any break can render evidence inadmissible.",
            "explanation": "Proper documentation is essential. Use evidence logs, seals, and secure storage. Minimize the number of handlers.",
            "difficulty": "medium",
            "reference": "General Order G03-02-01: Evidence and Property Management"
        },
        {
            "type": "flashcard",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Search Warrant Execution",
            "content": "What are the time restrictions for executing a search warrant in Illinois?",
            "answer": "Search warrants must be executed within 96 hours of issuance (unless nighttime service is authorized). Service is generally between 6:00 AM and 10:00 PM unless the warrant specifically authorizes nighttime execution based on good cause.",
            "explanation": "Nighttime warrants require showing that evidence will be destroyed, removed, or that suspect poses danger. Must announce presence and authority unless no-knock authorized.",
            "difficulty": "medium",
            "reference": "725 ILCS 5/108-9"
        },
        
        # Procedures
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Lineups and Identifications",
            "content": "What are the requirements for conducting a proper lineup?",
            "answer": "Requirements include: (1) At least 5-6 individuals of similar appearance, (2) Only one suspect per lineup, (3) Blind or blinded administration (officer doesn't know suspect position), (4) Pre-lineup instructions to witness, (5) Video/audio recording when possible, (6) Document witness confidence statement.",
            "explanation": "Photo arrays follow same principles. Avoid suggestive procedures that could lead to misidentification and false convictions.",
            "difficulty": "hard",
            "reference": "General Order G03-06: Eyewitness Identification Procedures"
        },
        {
            "type": "flashcard",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Juvenile Interrogations",
            "content": "What special protections apply when interrogating a juvenile suspect?",
            "answer": "Juveniles have right to: (1) Have parent/guardian present during questioning, (2) Consult with attorney before and during questioning, (3) Be advised of rights in age-appropriate manner. Officers must consider age and maturity when evaluating whether Miranda waiver was knowing and voluntary.",
            "explanation": "Illinois requires heightened scrutiny for juvenile confessions. Age under 13 requires special handling. Document all attempts to contact parents/guardians.",
            "difficulty": "hard",
            "reference": "705 ILCS 405/1-5"
        }
    ]
    
    scenarios = [
        # Scenario 1
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Armed Robbery Investigation",
            "content": """You are assigned to investigate an armed robbery that occurred at a convenience store at 2:00 AM. The store clerk reports that a male offender wearing a ski mask displayed what appeared to be a black handgun and demanded cash. The offender fled on foot with approximately $350.

Security footage shows the incident and the suspect's approximate height and build. A witness in the parking lot saw a vehicle (described as a dark sedan) speed away seconds after the robbery. The clerk is shaken but willing to cooperate.

As the lead detective, outline your investigative plan for the first 24 hours. What are your priorities, what evidence will you collect, and what investigative steps will you take?""",
            "answer": """Priority actions within first 24 hours:

IMMEDIATE SCENE ACTIONS:
1. Secure and process crime scene - collect security footage, dust for prints on counter/door
2. Obtain detailed witness statements while memory is fresh
3. Canvas area for additional witnesses/cameras
4. Issue flash message with suspect/vehicle description
5. Check for similar pattern robberies in area

EVIDENCE COLLECTION:
1. Obtain all surveillance video from store and nearby businesses
2. Preserve register/counter for potential DNA/prints
3. Document positions and viewpoints of witnesses
4. Photograph scene from multiple angles
5. Collect any dropped items or physical evidence

FOLLOW-UP INVESTIGATION:
1. Review recent similar robberies for MO patterns
2. Check pawn databases for stolen property
3. Check recent arrests for similar offenses
4. Interview store employees about suspicious customers
5. Monitor social media/informant sources
6. Coordinate with gang/robbery units on known suspects
7. Analyze surveillance video with tech unit for vehicle details
8. Issue BOLO for vehicle and suspect description
9. Prepare photo array if suspect identified
10. Document all actions and maintain chain of custody

WITNESS HANDLING:
1. Obtain written statements
2. Advise about victim services
3. Schedule follow-up contact
4. Prepare for possible lineup if suspect identified

REPORTING:
1. Complete case report with all details
2. Coordinate with ASA on charges once suspect identified
3. Update command staff on investigation status""",
            "explanation": "This scenario tests knowledge of investigative priorities, evidence collection, witness management, and proper procedures. Key elements include: acting quickly while memory/evidence is fresh, coordinating with other units, following proper evidence protocols, and considering pattern analysis.",
            "difficulty": "hard",
            "reference": "General Order G03-15: Detective Division Operations"
        },
        
        # Scenario 2
        {
            "type": "scenario",
            "category_id": "cat_criminal_law",
            "category_name": "Illinois Criminal Law",
            "title": "Domestic Battery with Weapon",
            "content": """You respond to a domestic disturbance call. Upon arrival, you find a female victim with visible injuries to her face and a laceration on her arm requiring stitches. She states her boyfriend struck her multiple times with his fists and then grabbed a kitchen knife, threatening to kill her before she escaped and called 911.

The boyfriend is located nearby and taken into custody. He claims she attacked him first with the knife and he was defending himself. No witnesses observed the incident. The knife is recovered from the kitchen sink. Both parties have been drinking.

What charges are supported by the evidence? What additional investigation is needed? How do you handle the conflicting statements?""",
            "answer": """RECOMMENDED CHARGES:
1. Aggravated Domestic Battery (720 ILCS 5/12-3.3) - Use of deadly weapon (knife) and causes injury
2. Domestic Battery (720 ILCS 5/12-3.2) - Bodily harm to family/household member  
3. Aggravated Assault (720 ILCS 5/12-2) - Threat with knife (deadly weapon)

EVIDENCE REQUIRED:
1. PHOTOGRAPH all injuries extensively (multiple angles, with measurements)
2. Obtain medical records documenting injuries
3. Document any defensive wounds (or lack thereof) on both parties
4. Process knife for fingerprints
5. Document condition of scene - signs of struggle, blood, broken items
6. Check for any surveillance cameras in area
7. Canvas for witnesses who may have heard altercation
8. Document any prior domestic violence history
9. Obtain written statement from victim (if she recants later, statement preserved)
10. Check for protection orders or prior domestic incidents

HANDLING CONFLICTING STATEMENTS:
1. Physical evidence often resolves conflicts - her injuries vs. his lack of defensive wounds
2. Victim's injuries and location consistent with her account
3. His claim of self-defense undermined if he has no injuries
4. Pattern of injuries (facial vs defensive) tells the story
5. Document exactly what each person says
6. Do not force victim to decide on charges - that's State's decision
7. Illinois law allows prosecution even if victim doesn't cooperate

MANDATORY ACTIONS:
1. State's Attorney felony review for aggravated charges
2. Offer victim services/shelter information
3. Follow mandatory domestic violence protocols
4. Document everything thoroughly
5. Consider victim safety and lethality assessment

SELF-DEFENSE ANALYSIS:
His claim fails if: (1) He was initial aggressor, (2) He used excessive force, (3) He had safe retreat option, (4) His actions were not proportional""",
            "explanation": "This scenario tests understanding of: domestic violence laws, evidence collection, charge selection, self-defense claims, and victim safety. Critical to photograph injuries immediately, preserve all evidence, and understand that Illinois has mandatory arrest policies for domestic violence when probable cause exists.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/12-3.2, 720 ILCS 5/12-3.3"
        },
        
        # Scenario 3
        {
            "type": "scenario",
            "category_id": "cat_procedures",
            "category_name": "Investigative Procedures",
            "title": "Burglary with Questionable Consent",
            "content": """You are investigating a residential burglary. The homeowner reports $5,000 in jewelry and electronics stolen. During your investigation, you learn that the homeowner's ex-boyfriend had a key to the residence (from when they dated). The ex-boyfriend admits he entered the home and took items, but claims the homeowner told him he could "take whatever you want" during an argument about belongings left at the residence.

The homeowner denies giving any permission and wants him prosecuted. The ex-boyfriend has text messages showing they argued about belongings, but no message explicitly gives permission. He claims he thought the permission was implied.

Is this burglary? What additional information do you need? How do you resolve this case?""",
            "answer": """LEGAL ANALYSIS:
Burglary requires: (1) Entering or remaining in a building, (2) Without authority, (3) With intent to commit felony/theft

KEY ISSUE: Did he have authority to enter?

AUTHORITY ANALYSIS:
1. Having a key does NOT equal authority if relationship ended
2. Past permission does not equal current authority
3. "Implied" permission is not legal authority
4. Permission to retrieve "belongings" ≠ permission to take homeowner's property

LIKELY CHARGES:
1. BURGLARY (720 ILCS 5/19-1) - Entered without authority with intent to commit theft
   - His own admission establishes he took property
   - No valid consent to enter
   - Former key holder status provides no authority after relationship ends
   
2. THEFT (720 ILCS 5/16-1) - Taking property without authorization
   - $5,000 value = Class 3 Felony
   - His claim of "permission" negated by homeowner's denial
   - Burden on him to prove permission

ADDITIONAL INVESTIGATION NEEDED:
1. Review ALL text messages between parties (full context)
2. Interview any witnesses to the "permission" conversation
3. Determine exactly WHEN their relationship ended
4. Check if any previous disputes over property
5. Verify ownership of taken items (receipts, photos)
6. Document which items were his vs. hers
7. Check for any protection orders or no-contact orders
8. Determine if he returned the key or was asked to
9. Review any prior police calls to address
10. Get itemized list of stolen property with values

DISTINGUISHING CIVIL VS CRIMINAL:
- This is CRIMINAL because:
  * No valid authority to enter
  * Property clearly belonged to homeowner (not joint property)
  * Taking exceeded any claimed permission
  * Intent to deprive owner of property

- Would be CIVIL if:
  * Dispute over jointly owned property
  * Valid authority to enter
  * Good faith belief in right to property

PROSECUTION STRATEGY:
1. His admission of entry + taking = strong case
2. Homeowner credibility vs his credibility
3. Lack of clear permission in texts hurts his defense
4. Criminal "unauthorized entry" vs civil "property dispute"
5. Present to State's Attorney for felony approval

RECOMMENDATION: Charge Residential Burglary (Class 1 Felony) and Theft. His "implied permission" defense is weak and for jury to decide.""",
            "explanation": "This scenario tests understanding of: burglary elements, concept of authority/consent, distinguishing criminal vs civil matters, and analyzing defenses. Key concept: past relationships don't create ongoing authority to enter property, and taking property without clear permission is theft even if parties have history.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/19-1, 720 ILCS 5/16-1"
        },
        
        # Scenario 4
        {
            "type": "scenario",
            "category_id": "cat_evidence",
            "category_name": "Evidence Handling",
            "title": "Search and Seizure Issues",
            "content": """Responding to a shots fired call, you arrive at an apartment building and hear yelling from an apartment. You knock and a male answers. You smell cannabis and see what appears to be a handgun on the coffee table behind him. He does not consent to entry. You push past him, secure the gun, and find ammunition and cocaine on the kitchen counter.

The subject is arrested for weapons and drug offenses. Was the entry legal? Will the evidence be suppressed? What should you have done differently?""",
            "answer": """LEGAL ANALYSIS OF ENTRY:

FOURTH AMENDMENT ISSUE:
The entry and search are PROBLEMATIC and evidence likely SUPPRESSED unless exigent circumstances exist.

WARRANTLESS ENTRY REQUIRES:
1. Consent (denied here), OR
2. Exigent circumstances, OR  
3. Search warrant

EXIGENT CIRCUMSTANCES ANALYSIS:
Could potentially justify entry if:
1. Emergency aid exception (someone injured/in danger)
2. Hot pursuit of fleeing felon
3. Imminent destruction of evidence
4. Preventing serious harm

YOUR SCENARIO:
✓ Shots fired call (original reason for presence - OK)
✓ Yelling heard (suggests possible disturbance - supports knock)
✗ Cannabis smell alone - NOT exigent (Illinois decriminalized small amounts)
✗ Gun in plain view inside home - NOT immediate threat from outside
✗ "Pushing past" without clear emergency - VIOLATION
✗ No consent to enter - VIOLATION
✗ No indication of active emergency once door answered

LIKELY COURT RULING:
Evidence SUPPRESSED because:
1. No valid exception to warrant requirement
2. No exigent circumstances clearly articulated
3. Cannabis smell insufficient in Illinois post-legalization
4. Gun visible but not being wielded/threatening
5. Entry was not justified by circumstances

WHAT YOU SHOULD HAVE DONE:

OPTION 1 - SECURE AND GET WARRANT:
1. Smell cannabis/see gun but resident refuses entry
2. Secure perimeter (prevent destruction of evidence)
3. Leave officer at door to ensure no one exits
4. Call for supervisor and State's Attorney
5. Apply for search warrant immediately
6. Document all observations for warrant affidavit
7. Execute warrant once approved

OPTION 2 - IF TRUE EMERGENCY:
1. Articulate specific threat to safety
2. Ensure someone inside needs aid
3. Make limited entry for emergency only
4. Secure area and then get warrant for full search

PROPER DOCUMENTATION:
Must be able to articulate:
- Specific facts creating emergency
- Why entry was immediately necessary
- What threat existed to persons/evidence
- Why waiting for warrant was not feasible

CONSEQUENCE:
Current scenario likely results in:
- Evidence suppressed
- Case dismissed
- Possible civil rights lawsuit
- Violations of CPD policy
- Review by COPA

TRAINING POINT:
When time permits, ALWAYS get a warrant. Courts highly protective of home privacy. "I saw contraband" is not an emergency requiring immediate entry. Secure scene and get judicial authorization.""",
            "explanation": "This scenario tests Fourth Amendment knowledge, understanding of exigent circumstances, and proper procedure when evidence is observed but entry is denied. Key lesson: Cannabis legalization in Illinois changes analysis, and seeing contraband through door is not automatically an emergency. Should secure scene and obtain warrant.",
            "difficulty": "hard",
            "reference": "U.S. Constitution Amendment IV, Illinois Cannabis Regulation Act, General Order G03-02"
        }
    ]
    
    # Insert all questions
    all_questions = flashcards + scenarios
    now = datetime.now(timezone.utc)
    
    for q in all_questions:
        q["question_id"] = f"q_{uuid.uuid4().hex[:12]}"
        q["created_at"] = now
        q["updated_at"] = now
        
        await db.questions.update_one(
            {"question_id": q["question_id"]},
            {"$set": q},
            upsert=True
        )
    
    print(f"✓ Seeded {len(flashcards)} flashcards and {len(scenarios)} scenarios")

async def create_admin_user():
    """Create default admin user for testing"""
    import bcrypt
    
    admin_email = "admin@cpd.test"
    existing = await db.users.find_one({"email": admin_email})
    
    if not existing:
        password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_user = {
            "user_id": f"user_{uuid.uuid4().hex[:12]}",
            "email": admin_email,
            "name": "Admin User",
            "password_hash": password_hash,
            "role": "admin",
            "created_at": datetime.now(timezone.utc)
        }
        await db.users.insert_one(admin_user)
        print(f"✓ Created admin user: {admin_email} / admin123")
    else:
        print("✓ Admin user already exists")

async def main():
    print("🌱 Seeding database...")
    await seed_categories()
    await seed_questions()
    await create_admin_user()
    print("✅ Database seeding complete!")
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
