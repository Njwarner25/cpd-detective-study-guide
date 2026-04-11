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


async def seed_legal_trap_extra(ext_db=None):
    """Seed 20 additional legal trap questions for CPD Detective Study Guide.

    These questions cover advanced legal doctrines not addressed in the
    original seed_mixed_exam_questions.py legal trap section. Each question
    is designed to be tricky — the obvious answer is often WRONG.

    Topics covered:
      1.  Curtilage doctrine and Fourth Amendment
      2.  Good faith exception to exclusionary rule
      3.  Inevitable discovery doctrine
      4.  Community caretaking exception
      5.  Open fields doctrine
      6.  Protective sweep during arrest (expanded scenario)
      7.  Consent search withdrawal
      8.  Standing to challenge search
      9.  Franks hearing (challenging warrant affidavit)
      10. Silver platter / private search doctrine
      11. Attenuation doctrine
      12. Independent source doctrine
      13. Plain feel doctrine (Terry frisk)
      14. Hot pursuit / exigent circumstances scope
      15. Inventory search requirements
      16. Knock and announce requirements (expanded)
      17. DNA collection at arrest (Maryland v. King)
      18. Cell site location information (Carpenter v. US)
      19. Riley v. California (cell phone search incident to arrest)
      20. Implied consent and DUI investigations in Illinois

    Args:
        ext_db: Optional external database connection. If provided, uses it
                instead of the module-level db.
    """
    global db
    if ext_db is not None:
        db = ext_db

    now = datetime.now(timezone.utc)

    questions = [
        # ──────────────────────────────────────────────
        # 1. Curtilage Doctrine and Fourth Amendment
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_001",
            "title": "Curtilage Doctrine — Backyard Observation",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "While investigating a narcotics complaint, you walk up the driveway of a "
                "suspect's home to knock on the front door. No one answers. You then walk "
                "around the side of the house, through a closed but unlocked gate, into the "
                "fenced backyard. From the backyard you observe marijuana plants growing in "
                "a garden plot through a gap in the fence. You did not have a warrant."
            ),
            "options": {
                "A": "The marijuana plants are admissible because they were in plain view once you were in the backyard.",
                "B": "The marijuana plants are likely inadmissible because the fenced backyard is curtilage, and entering through the closed gate exceeded the implied license to approach the front door.",
                "C": "The marijuana plants are admissible under the open fields doctrine since the backyard is outside the home.",
                "D": "The marijuana plants are admissible because you had an implied invitation to be on the property due to the narcotics complaint."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -1},
            "explanation": (
                "Under the curtilage doctrine established in Oliver v. United States (1984) and "
                "refined in Florida v. Jardines (2013), the area immediately surrounding a home — "
                "including a fenced backyard — receives full Fourth Amendment protection. While "
                "officers have an implied license to approach the front door via normal access routes "
                "(sidewalk, driveway, front porch), that license does NOT extend to circumnavigating "
                "the house and entering a fenced backyard through a closed gate. The factors from "
                "United States v. Dunn (1987) — proximity to the home, enclosure, nature of use, "
                "and steps taken to protect from observation — all weigh in favor of curtilage here. "
                "Option A is wrong because plain view requires the officer to be lawfully present, "
                "which they were not. Option C misapplies the open fields doctrine — a fenced "
                "backyard is NOT an open field. Option D fabricates a legal standard; a complaint "
                "does not create an implied invitation to trespass into curtilage."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 2. Good Faith Exception to Exclusionary Rule
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_002",
            "title": "Good Faith Exception — Defective Warrant",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "You obtain a search warrant from a Cook County judge based on information from "
                "a confidential informant. You execute the warrant in good faith and recover a "
                "large quantity of heroin. Defense counsel later proves that the warrant affidavit "
                "contained a material misstatement of fact — however, you were unaware of the "
                "error and the affidavit was prepared by another detective. The judge who signed "
                "the warrant had a reasonable basis for finding probable cause based on the "
                "affidavit as presented."
            ),
            "options": {
                "A": "The heroin must be suppressed because the warrant was based on false information, regardless of your knowledge.",
                "B": "The heroin is admissible under the good faith exception because you reasonably relied on a facially valid warrant issued by a neutral magistrate.",
                "C": "The heroin is admissible only if the confidential informant testifies at trial to verify the information.",
                "D": "The heroin must be suppressed because the exclusionary rule has no exceptions."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": 0, "D": -2},
            "explanation": (
                "Under United States v. Leon (1984), the good faith exception to the exclusionary "
                "rule allows evidence obtained through objectively reasonable reliance on a facially "
                "valid warrant issued by a neutral and detached magistrate. The exception applies "
                "even if the warrant is later invalidated — as long as the officer's reliance was "
                "objectively reasonable. Leon identifies four situations where good faith does NOT "
                "apply: (1) the magistrate was misled by the affiant's knowing or reckless falsehoods "
                "(Franks v. Delaware), (2) the magistrate wholly abandoned the judicial role, "
                "(3) the affidavit was so lacking in probable cause that no reasonable officer would "
                "rely on it, or (4) the warrant was so facially deficient that executing officers "
                "could not reasonably presume it was valid. Here, you were unaware of the error "
                "and the affidavit appeared sufficient, so good faith applies. Option A ignores "
                "the good faith doctrine. Option D is factually wrong."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 3. Inevitable Discovery Doctrine
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_003",
            "title": "Inevitable Discovery — Body Location",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "During interrogation, a suspect confesses to a murder and reveals the location "
                "of the victim's body. Defense counsel successfully argues the confession was "
                "obtained in violation of the suspect's Sixth Amendment right to counsel (the "
                "suspect had been formally charged and an attorney appointed, but was questioned "
                "without the attorney present). The prosecution argues the body would have been "
                "found anyway because a volunteer search party was already systematically "
                "searching the area and would have reached the location within hours."
            ),
            "options": {
                "A": "The body and all related physical evidence must be suppressed because the confession was illegally obtained.",
                "B": "The body is admissible under the inevitable discovery doctrine if the prosecution can prove by a preponderance of the evidence that it would have been discovered through lawful means.",
                "C": "The body is admissible only if the prosecution can prove beyond a reasonable doubt that it would have been found.",
                "D": "The confession AND the body are both fully admissible because physical evidence is never subject to suppression."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": 1, "D": -2},
            "explanation": (
                "This scenario is based on Nix v. Williams (1984) (Williams II), the landmark case "
                "establishing the inevitable discovery doctrine. The Supreme Court held that evidence "
                "obtained through constitutional violations need not be suppressed if the prosecution "
                "can demonstrate by a preponderance of the evidence that the evidence would "
                "inevitably have been discovered through lawful means. Note the burden of proof: "
                "preponderance of the evidence, NOT beyond a reasonable doubt (which is why C "
                "earns partial credit but is not correct). Option A ignores this well-established "
                "exception to the exclusionary rule. Option D is entirely wrong — physical evidence "
                "is absolutely subject to suppression under the Fourth and Fifth Amendments."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 4. Community Caretaking Exception
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_004",
            "title": "Community Caretaking — Warrantless Home Entry",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "Neighbors call 911 reporting they haven't seen an elderly resident in over a "
                "week. Mail is piling up and newspapers are stacked on the porch. You respond "
                "and knock repeatedly with no answer. You detect no odors. A neighbor says the "
                "resident lives alone and has no known medical conditions. You decide to force "
                "entry into the home to conduct a welfare check. Inside, you find the resident "
                "is fine — she was on vacation — but you also observe illegal firearms in plain "
                "view on the kitchen table."
            ),
            "options": {
                "A": "The firearms are admissible under the community caretaking exception because you entered to check on the resident's welfare.",
                "B": "The firearms are admissible under exigent circumstances because the resident could have been in medical distress.",
                "C": "The firearms are likely inadmissible because the community caretaking exception does not extend to warrantless entry into a home, and the facts did not support true exigent circumstances.",
                "D": "The firearms are admissible under the plain view doctrine regardless of how you entered."
            },
            "correct_answer": "C",
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -2},
            "explanation": (
                "In Caniglia v. Strom (2021), the Supreme Court unanimously held that the "
                "community caretaking exception — originally developed for vehicle impoundment "
                "in Cady v. Dombrowski (1973) — does NOT create a freestanding license for "
                "warrantless entry into homes. The Fourth Amendment's protection of the home is "
                "at its zenith. While genuine exigent circumstances (actual evidence of medical "
                "emergency, sounds of distress, etc.) can justify warrantless entry, the facts "
                "here — no odors, no known medical conditions, only an absence — likely fall "
                "short of true exigency. Option A misapplies community caretaking to homes. "
                "Option B overstates the exigency based on these facts. Option D incorrectly "
                "states that plain view operates independently of lawful presence — it does not. "
                "An officer must be lawfully present for plain view to apply."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 5. Open Fields Doctrine
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_005",
            "title": "Open Fields Doctrine — Rural Property",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "Acting on an anonymous tip about a methamphetamine lab, you drive to a rural "
                "property outside Chicago. The property has a farmhouse with a yard surrounded "
                "by a picket fence. Beyond the fenced yard, there are 40 acres of farmland. "
                "Without a warrant, you walk past 'No Trespassing' signs posted along the road "
                "and hike across the open farmland. About a quarter mile from the house, you "
                "discover a makeshift meth lab in a barn."
            ),
            "options": {
                "A": "The meth lab evidence must be suppressed because the 'No Trespassing' signs established a reasonable expectation of privacy.",
                "B": "The meth lab evidence is admissible under the open fields doctrine because the barn is in an open field beyond the curtilage of the home, and 'No Trespassing' signs do not create Fourth Amendment protection.",
                "C": "The meth lab evidence must be suppressed because you were trespassing under Illinois law.",
                "D": "The meth lab evidence is only admissible if the anonymous tip was corroborated first."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": 0},
            "explanation": (
                "Under the open fields doctrine established in Hester v. United States (1924) and "
                "reaffirmed in Oliver v. United States (1984), areas outside the curtilage of a "
                "home — even privately owned land — are not protected by the Fourth Amendment. "
                "The Supreme Court explicitly held in Oliver that 'No Trespassing' signs and fences "
                "do NOT create a reasonable expectation of privacy in open fields. The barn, located "
                "a quarter mile from the house and well beyond the curtilage, falls within the open "
                "fields doctrine. Option A incorrectly assumes signs create Fourth Amendment rights. "
                "Option C conflates state trespass law with constitutional protections — while the "
                "officer may technically be trespassing under state law (720 ILCS 5/21-3), the "
                "evidence is still admissible because the Fourth Amendment does not protect open "
                "fields. Option D is irrelevant to the Fourth Amendment analysis."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 6. Protective Sweep — Scope Limitations
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_006",
            "title": "Protective Sweep — Exceeding Lawful Scope",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "You execute an arrest warrant at a suspect's apartment for armed robbery. After "
                "handcuffing the suspect in the hallway, you conduct a protective sweep. In the "
                "bedroom closet, while checking for persons who could pose a danger, you notice "
                "a shoebox on the top shelf. You open the shoebox and find a bag of cocaine. "
                "No person could fit in the shoebox."
            ),
            "options": {
                "A": "The cocaine is admissible because it was found during a lawful protective sweep incident to arrest.",
                "B": "The cocaine is admissible under the plain view doctrine because you were lawfully in the closet.",
                "C": "The cocaine is likely inadmissible because opening the shoebox exceeded the scope of a protective sweep, which is limited to places where a person could be hiding.",
                "D": "The cocaine is admissible under the search incident to arrest exception."
            },
            "correct_answer": "C",
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -1},
            "explanation": (
                "Under Maryland v. Buie (1990), a protective sweep is limited to a cursory visual "
                "inspection of those spaces where a person could be hiding. Opening a shoebox — a "
                "container far too small to conceal a person — exceeds the permissible scope of a "
                "protective sweep. Option A incorrectly broadens the sweep's scope. Option B "
                "misapplies plain view — while the officer may have been lawfully in the closet, "
                "the cocaine was not in plain view; it was inside a closed container that had to be "
                "opened. Plain view requires that the incriminating nature of the item be "
                "immediately apparent without further search (Horton v. California, 1990). "
                "Option D is wrong because search incident to arrest under Chimel v. California "
                "(1969) is limited to the area within the arrestee's immediate control (wingspan), "
                "and the suspect was already handcuffed in the hallway, not in the bedroom."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 7. Consent Search Withdrawal
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_007",
            "title": "Consent Search — Mid-Search Withdrawal",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "A suspect voluntarily consents to a search of his vehicle during a traffic stop. "
                "You begin searching the passenger compartment. Midway through, the suspect says: "
                "\"Actually, I changed my mind. Stop searching my car.\" At that point, you have "
                "not yet found any contraband, but you have not finished searching."
            ),
            "options": {
                "A": "You may continue the search because once consent is given, it cannot be revoked mid-search.",
                "B": "You must immediately cease the search because a person may withdraw consent at any time, and any evidence found after withdrawal will be suppressed.",
                "C": "You may continue searching only the areas you have already started but cannot open new compartments.",
                "D": "You may continue the search for an additional 60 seconds to complete any area currently being examined."
            },
            "correct_answer": "B",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "explanation": (
                "The right to withdraw consent is well established. In Florida v. Jimeno (1991), "
                "the Supreme Court recognized that consent defines the scope of a search, and a "
                "person may limit or revoke consent at any time. When consent is unambiguously "
                "withdrawn, the search must stop immediately. Any evidence discovered after "
                "withdrawal is obtained without legal authority and is subject to suppression. "
                "Evidence found BEFORE the withdrawal remains admissible. Option A is flatly "
                "wrong — consent is revocable. Options C and D fabricate legal standards that do "
                "not exist. There is no '60-second grace period' or 'areas already started' "
                "exception. Per CPD General Order G06-01-02, members shall immediately cease "
                "a consent search when consent is withdrawn."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 8. Standing to Challenge Search
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_008",
            "title": "Standing — Passenger in Borrowed Vehicle",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "Officers conduct an unlawful traffic stop and search a vehicle. The driver "
                "borrowed the car from a friend, and a passenger in the back seat is found with "
                "a firearm tucked under the seat. The passenger has no ownership interest in the "
                "vehicle, was not driving, and did not know the driver. Defense counsel files a "
                "motion to suppress the firearm on behalf of the passenger."
            ),
            "options": {
                "A": "The passenger has automatic standing to challenge the search because the stop itself was unlawful.",
                "B": "The passenger has standing because anyone present during an illegal search can challenge it.",
                "C": "The passenger likely lacks standing to challenge the vehicle search because he had no reasonable expectation of privacy in someone else's borrowed car, but he may challenge the legality of the stop itself.",
                "D": "The passenger has no legal options whatsoever — only the vehicle's registered owner can challenge any search."
            },
            "correct_answer": "C",
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -1},
            "explanation": (
                "Under Rakas v. Illinois (1978), a defendant must demonstrate a legitimate "
                "expectation of privacy in the area searched to have standing to challenge a "
                "search. Mere presence in a vehicle does not confer standing. In Byrd v. United "
                "States (2018), the Court held that authorized drivers of borrowed/rented cars "
                "generally DO have standing, but this extends to the driver — not necessarily a "
                "random passenger. However, the passenger CAN challenge the legality of the "
                "traffic stop itself under Brendlin v. California (2007), which held that all "
                "occupants are 'seized' during a stop. If the stop was unlawful, the passenger "
                "can argue the firearm is fruit of the unlawful seizure. Option A oversimplifies. "
                "Option B is too broad — standing requires a personal expectation of privacy. "
                "Option D is too restrictive and ignores the stop challenge."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 9. Franks Hearing (Challenging Warrant Affidavit)
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_009",
            "title": "Franks Hearing — False Statements in Affidavit",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "A detective obtains a search warrant by including in the affidavit a statement "
                "that a confidential informant made a controlled buy at the target address within "
                "the past 48 hours. In reality, no controlled buy occurred — the detective "
                "fabricated this fact to bolster probable cause. The warrant is executed and "
                "narcotics are recovered. Defense counsel learns of the fabrication and seeks "
                "a hearing."
            ),
            "options": {
                "A": "The evidence is still admissible under the good faith exception because the officers who executed the warrant relied on it in good faith.",
                "B": "The defense must request a Franks hearing; if they show the affiant made deliberate or reckless false statements material to probable cause, the warrant is voided and evidence is suppressed.",
                "C": "The evidence is admissible because the warrant was signed by a neutral judge, which validates it regardless of the affidavit's contents.",
                "D": "The only remedy is a civil lawsuit against the detective — the criminal case is unaffected."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -1},
            "explanation": (
                "Under Franks v. Delaware (1978), a defendant is entitled to a hearing (a 'Franks "
                "hearing') if they make a substantial preliminary showing that (1) the affiant "
                "knowingly, intentionally, or with reckless disregard for the truth included a "
                "false statement in the warrant affidavit, and (2) the false statement was "
                "necessary to the finding of probable cause. If the defendant prevails, the "
                "warrant is voided and the fruits of the search are suppressed under the "
                "exclusionary rule. Option A is incorrect because the good faith exception under "
                "Leon does NOT apply when the affiant (the person who prepared the affidavit) "
                "deliberately misled the magistrate — this is one of Leon's explicit exceptions. "
                "Option C misunderstands judicial review — a judge's signature does not immunize "
                "a fraudulent affidavit. Option D understates the remedy."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 10. Silver Platter / Private Search Doctrine
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_010",
            "title": "Private Search Doctrine — Landlord Discovers Evidence",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "A landlord enters a tenant's apartment to repair a leaking pipe (as permitted "
                "under the lease for emergency maintenance). While inside, the landlord discovers "
                "what appears to be a large quantity of counterfeit currency and a printing press. "
                "The landlord photographs everything and calls police. When you arrive, the "
                "landlord shows you the photographs and offers to let you into the apartment."
            ),
            "options": {
                "A": "You may enter the apartment with the landlord's permission since the landlord has a key and discovered the evidence first.",
                "B": "You should obtain a search warrant based on the landlord's observations and photographs before entering the apartment, even though the initial private search was lawful.",
                "C": "The evidence is inadmissible because the landlord violated the tenant's Fourth Amendment rights.",
                "D": "You may enter but only search the exact areas the landlord already observed."
            },
            "correct_answer": "B",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": 0},
            "explanation": (
                "The Fourth Amendment restricts government actors, not private citizens. Under the "
                "private search doctrine (United States v. Jacobsen, 1984), a search conducted by "
                "a private party (here, the landlord) does not violate the Fourth Amendment. "
                "However, once a private party notifies police, the police become government actors "
                "and MUST comply with the Fourth Amendment. A landlord cannot consent to a search "
                "of a tenant's apartment on behalf of police — the tenant holds the Fourth "
                "Amendment interest (Chapman v. United States, 1961). The correct approach is to "
                "use the landlord's observations as the basis for a search warrant affidavit. "
                "Option A is wrong — landlord consent does not substitute for a warrant. Option C "
                "incorrectly applies the Fourth Amendment to the landlord's private actions. "
                "Option D partially reflects the Jacobsen 'scope of private search' rule but "
                "still requires a warrant or exception for police entry."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 11. Attenuation Doctrine
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_011",
            "title": "Attenuation Doctrine — Outstanding Warrant Discovery",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "An officer conducts an unlawful Terry stop without reasonable suspicion. During "
                "the stop, the officer runs the subject's name and discovers a valid outstanding "
                "arrest warrant. The officer arrests the subject on the warrant and, during a "
                "search incident to arrest, finds methamphetamine. Defense moves to suppress."
            ),
            "options": {
                "A": "The methamphetamine must be suppressed because the initial stop was unlawful and all subsequent evidence is fruit of the poisonous tree.",
                "B": "The methamphetamine is admissible under the attenuation doctrine because the pre-existing arrest warrant broke the causal chain between the unlawful stop and the discovery of evidence.",
                "C": "The methamphetamine is admissible because the search incident to arrest is always a valid exception, regardless of how the arrest came about.",
                "D": "The methamphetamine is inadmissible unless the officer can prove he would have eventually encountered the subject and discovered the warrant."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": 0},
            "explanation": (
                "This scenario is directly based on Utah v. Strieff (2016), where the Supreme "
                "Court held that the discovery of a valid, pre-existing arrest warrant attenuates "
                "the connection between an unlawful stop and evidence found during a search "
                "incident to the subsequent arrest. The Court applied the three Brown v. Illinois "
                "(1975) attenuation factors: (1) temporal proximity, (2) intervening circumstances, "
                "and (3) purpose and flagrancy of the misconduct. The pre-existing warrant was a "
                "critical intervening circumstance that broke the causal chain. Option A ignores "
                "the attenuation doctrine. Option C is dangerously wrong — the legality of a "
                "search incident to arrest depends on the lawfulness of the arrest itself. "
                "Option D describes inevitable discovery, not attenuation."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 12. Independent Source Doctrine
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_012",
            "title": "Independent Source Doctrine — Parallel Investigation",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "Detectives illegally enter a warehouse without a warrant and observe large "
                "quantities of cocaine. They leave without seizing anything. Later, a separate "
                "team of detectives — with NO knowledge of the illegal entry — independently "
                "develops probable cause through surveillance, informant tips, and controlled "
                "buys. They obtain a valid search warrant for the same warehouse and recover "
                "the cocaine."
            ),
            "options": {
                "A": "The cocaine must be suppressed because the first team's illegal entry taints all subsequent discovery of the same evidence.",
                "B": "The cocaine is admissible under the independent source doctrine because the second warrant was based entirely on information obtained independently from the illegal entry.",
                "C": "The cocaine is admissible only if the first team of detectives is disciplined for the illegal entry.",
                "D": "The cocaine is admissible under the inevitable discovery doctrine, not the independent source doctrine."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": 1},
            "explanation": (
                "Under the independent source doctrine (Murray v. United States, 1988; Segura v. "
                "United States, 1984), evidence initially discovered during an unlawful search is "
                "admissible if later obtained through a genuinely independent source untainted by "
                "the illegal conduct. The key requirements are: (1) the warrant must be based on "
                "information wholly independent of the illegal entry, and (2) the decision to seek "
                "the warrant must not have been prompted by the illegal entry. Here, the second "
                "team had no knowledge of the first entry and independently developed probable "
                "cause. Option A ignores this established exception. Option C invents a requirement "
                "— officer discipline is not a legal prerequisite for admissibility. Option D "
                "gets partial credit because inevitable discovery is related but distinct — "
                "independent source deals with evidence actually obtained through a separate legal "
                "channel, while inevitable discovery is hypothetical."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 13. Plain Feel Doctrine (Terry Frisk)
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_013",
            "title": "Plain Feel Doctrine — Object Identification During Frisk",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "During a lawful Terry stop, you develop reasonable suspicion the subject is "
                "armed and conduct a pat-down frisk. While patting the subject's jacket pocket, "
                "you feel a small, soft object that you cannot immediately identify. You squeeze "
                "and manipulate the object through the fabric for several seconds and determine "
                "it is a bag of crack cocaine. You reach into the pocket and seize it."
            ),
            "options": {
                "A": "The cocaine is admissible under the plain feel doctrine because you identified it during a lawful frisk.",
                "B": "The cocaine is admissible because any contraband found during a Terry frisk is automatically admissible.",
                "C": "The cocaine is likely inadmissible because the plain feel doctrine requires that the contraband's identity be immediately apparent without additional manipulation beyond what is needed to determine the object is not a weapon.",
                "D": "The cocaine is inadmissible because the plain feel doctrine does not exist in Illinois."
            },
            "correct_answer": "C",
            "io_scores": {"A": -1, "B": -2, "C": 2, "D": -1},
            "explanation": (
                "Under Minnesota v. Dickerson (1993), the Supreme Court recognized the 'plain "
                "feel' doctrine as an analog to the plain view doctrine. During a lawful Terry "
                "frisk, an officer may seize non-threatening contraband if its identity is "
                "'immediately apparent' through plain touch — without further manipulation. The "
                "critical fact here is that the officer had to squeeze and manipulate the object "
                "for several seconds to determine it was crack cocaine. This additional "
                "manipulation exceeded the scope of a weapons frisk and violated the plain feel "
                "doctrine. The incriminating nature was NOT immediately apparent. Option A ignores "
                "the 'immediately apparent' requirement. Option B is dangerously overbroad — a "
                "Terry frisk is limited to weapons detection. Option D is incorrect — Illinois "
                "courts do recognize the plain feel doctrine."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 14. Hot Pursuit / Exigent Circumstances Scope
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_014",
            "title": "Hot Pursuit — Misdemeanor Flight Into Home",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "You observe a man playing loud music and drinking on his front lawn in violation "
                "of a local noise ordinance (a misdemeanor). When you approach, the man runs "
                "inside his home and slams the door. You pursue, force open the door, and enter "
                "the home. Inside, you see illegal narcotics on the coffee table in plain view."
            ),
            "options": {
                "A": "The narcotics are admissible because hot pursuit of any fleeing suspect justifies warrantless home entry.",
                "B": "The narcotics are admissible because the man's flight created exigent circumstances.",
                "C": "The narcotics are likely inadmissible because the hot pursuit exception does not categorically apply to suspected misdemeanants fleeing into their own homes; a case-by-case exigency analysis is required.",
                "D": "The narcotics are admissible because once you were lawfully inside, the plain view doctrine applies."
            },
            "correct_answer": "C",
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -1},
            "explanation": (
                "In Lange v. California (2021), the Supreme Court held that pursuit of a "
                "suspected misdemeanant does NOT create a categorical exigent circumstance "
                "justifying warrantless home entry. Instead, courts must conduct a case-by-case "
                "analysis of whether true exigency exists — considering factors such as threat to "
                "persons, risk of evidence destruction, or risk of escape. A noise ordinance "
                "violation with no threat of violence or evidence destruction likely does not "
                "satisfy this standard. Option A is wrong — Lange rejected the categorical "
                "approach for misdemeanors. Option B overstates the exigency. Option D fails "
                "because plain view requires lawful presence, and the entry itself was likely "
                "unlawful. Note: Hot pursuit remains a more readily available justification for "
                "fleeing felony suspects (Warden v. Hayden, 1967)."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 15. Inventory Search Requirements
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_015",
            "title": "Inventory Search — Deviation from Policy",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "After a lawful arrest, you impound the suspect's vehicle per CPD policy. During "
                "the inventory search, you come across a locked briefcase in the trunk. Standard "
                "CPD inventory procedure states that locked containers should be tagged and stored "
                "without being opened. However, you are curious about the contents and force open "
                "the briefcase, discovering a large amount of cash and documents linking the "
                "suspect to a money laundering operation."
            ),
            "options": {
                "A": "The evidence is admissible because inventory searches allow opening all containers in the vehicle.",
                "B": "The evidence is admissible because you had probable cause to believe the briefcase contained evidence of a crime.",
                "C": "The evidence is likely inadmissible because you deviated from the standardized inventory search procedures by forcing open the locked briefcase.",
                "D": "The evidence is admissible as long as you document the briefcase contents on the inventory form."
            },
            "correct_answer": "C",
            "io_scores": {"A": -1, "B": 0, "C": 2, "D": -1},
            "explanation": (
                "Under Colorado v. Bertine (1987) and Florida v. Wells (1990), inventory searches "
                "must be conducted according to standardized criteria — they cannot be used as a "
                "pretext for an investigatory rummage. When departmental policy specifically states "
                "that locked containers should be tagged and stored without opening, deviating from "
                "that policy transforms the administrative inventory into an unlawful warrantless "
                "search. The Supreme Court emphasized in Wells that an inventory search must follow "
                "standardized procedures to be valid. CPD General Order E05-02 governs inventory "
                "procedures, and deviation from established protocols jeopardizes admissibility. "
                "Option A overstates inventory authority. Option B conflates inventory searches "
                "with probable cause searches — if you had PC, you should have sought a warrant. "
                "Option D is irrelevant — documentation does not cure the procedural violation."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 16. Knock and Announce — Scope of Exclusionary Rule
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_016",
            "title": "Knock and Announce — Violation and Suppression",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "Officers have a valid search warrant for a residence. In their eagerness, they "
                "fail to knock and announce their presence before forcing entry. During the "
                "search, they recover a stolen firearm listed in the warrant. The defense moves "
                "to suppress the firearm based on the knock-and-announce violation."
            ),
            "options": {
                "A": "The firearm must be suppressed because any constitutional violation during warrant execution invalidates all evidence recovered.",
                "B": "The firearm is admissible because a knock-and-announce violation does not trigger the exclusionary rule — the social costs of suppression outweigh the benefits.",
                "C": "The firearm is suppressed only if the officers acted intentionally in violating knock-and-announce.",
                "D": "The firearm is admissible only if the officers can prove exigent circumstances existed at the time of entry."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": 0},
            "explanation": (
                "In Hudson v. Michigan (2006), the Supreme Court held that a violation of the "
                "knock-and-announce rule does NOT require suppression of evidence found during "
                "the execution of a valid search warrant. Justice Scalia, writing for the majority, "
                "reasoned that the interests protected by knock-and-announce (protection of life "
                "and limb, property, and dignity) have nothing to do with the seizure of evidence "
                "described in the warrant. The causal connection between the violation and the "
                "evidence is too attenuated. This was a significant limitation on the exclusionary "
                "rule. Option A incorrectly assumes automatic suppression. Option C invents an "
                "intent standard that does not govern this analysis. Option D describes when "
                "no-knock entry might be justified, but the question is about the remedy for "
                "the violation, not its justification."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 17. DNA Collection at Arrest (Maryland v. King)
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_017",
            "title": "DNA Collection at Arrest — Scope and Limits",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "A suspect is arrested for a qualifying felony (aggravated battery). During "
                "booking at the station, you want to collect a buccal (cheek) swab for DNA "
                "purposes. The suspect has not been convicted — only arrested. The suspect "
                "objects and demands a warrant before any DNA is collected."
            ),
            "options": {
                "A": "You must obtain a warrant because collecting DNA from an arrestee before conviction violates the Fourth Amendment.",
                "B": "You may collect the DNA swab without a warrant because the Supreme Court has held that DNA collection from arrestees charged with serious offenses is a reasonable booking procedure analogous to fingerprinting.",
                "C": "You may collect DNA only if the suspect signs a written consent form.",
                "D": "You may collect DNA only after the suspect has been formally indicted by a grand jury."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -1},
            "explanation": (
                "In Maryland v. King (2013), the Supreme Court held (5-4) that the collection of "
                "DNA via buccal swab from individuals arrested for serious offenses is a "
                "reasonable search under the Fourth Amendment, analogous to fingerprinting and "
                "photographing during booking. The Court found that the government's interest in "
                "identifying arrestees outweighs the minimal intrusion of a cheek swab. Illinois "
                "law (730 ILCS 5/5-4-3) authorizes DNA collection from persons arrested for "
                "qualifying offenses, consistent with King. The key limitations are: the offense "
                "must be a qualifying serious crime, and the collection must follow standardized "
                "booking procedures. Option A is wrong — King authorizes this. Option C invents "
                "a consent requirement that does not exist for booking procedures. Option D "
                "incorrectly delays collection until indictment — the purpose is identification "
                "at the booking stage."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 18. Cell Site Location Information (Carpenter v. US)
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_018",
            "title": "CSLI — Warrant Requirement for Cell Tower Records",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "You are investigating a string of armed robberies. You want to obtain 60 days "
                "of historical cell site location information (CSLI) from the suspect's wireless "
                "carrier to place him near the robbery locations. The ASA advises you to obtain "
                "a court order under the Stored Communications Act (18 U.S.C. 2703(d)), which "
                "requires only 'reasonable grounds' — a standard lower than probable cause."
            ),
            "options": {
                "A": "The court order under the Stored Communications Act is sufficient because cell phone records are business records held by a third party, and the third-party doctrine eliminates any expectation of privacy.",
                "B": "You need a full search warrant supported by probable cause because the Supreme Court has held that historical CSLI is protected by the Fourth Amendment.",
                "C": "No warrant or court order is needed — carriers routinely share this data with law enforcement upon request.",
                "D": "A subpoena is sufficient because CSLI is not content — it is only metadata."
            },
            "correct_answer": "B",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -1},
            "explanation": (
                "In Carpenter v. United States (2018), the Supreme Court held (5-4) that the "
                "government's acquisition of historical CSLI constitutes a search under the "
                "Fourth Amendment, requiring a warrant supported by probable cause. The Court "
                "declined to extend the third-party doctrine (Smith v. Maryland; United States "
                "v. Miller) to CSLI, reasoning that cell phone location records provide an "
                "intimate window into a person's life and that individuals do not meaningfully "
                "\"voluntarily\" share their location with carriers. The Court specifically noted "
                "that a mere court order under 2703(d) is insufficient. Option A incorrectly "
                "applies the third-party doctrine — Carpenter carved out an exception. Option C "
                "ignores constitutional requirements entirely. Option D confuses the content/ "
                "metadata distinction — the Court found that even non-content data can be "
                "constitutionally protected. Note: Illinois also has the Freedom from Drone "
                "Surveillance Act (725 ILCS 167) and other state protections reinforcing "
                "location privacy."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 19. Riley v. California (Cell Phone Search)
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_019",
            "title": "Riley — Cell Phone Search Incident to Arrest",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "You arrest a suspect for aggravated assault. During the search incident to "
                "arrest, you seize the suspect's smartphone from his pocket. At the station, "
                "without obtaining a warrant, you scroll through the phone's text messages and "
                "find evidence linking the suspect to a separate drug trafficking conspiracy. "
                "You had no exigent circumstances requiring immediate access to the phone."
            ),
            "options": {
                "A": "The text messages are admissible because a cell phone found on a person during arrest can be searched like any other item under the search-incident-to-arrest exception.",
                "B": "The text messages are inadmissible because the Supreme Court requires a warrant to search the digital contents of a cell phone, even when the phone is seized incident to a lawful arrest.",
                "C": "The text messages are admissible because the phone was in the suspect's pocket, within his immediate control at the time of arrest.",
                "D": "The text messages are admissible because they relate to a separate, more serious crime."
            },
            "correct_answer": "B",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "explanation": (
                "In Riley v. California (2014), the Supreme Court unanimously held that the "
                "search-incident-to-arrest exception to the warrant requirement does NOT apply "
                "to the digital contents of a cell phone. The Court reasoned that cell phones "
                "differ fundamentally from other physical items in both a quantitative and "
                "qualitative sense — they contain the 'privacies of life' and are essentially "
                "minicomputers. Officers may seize the phone to prevent destruction of evidence "
                "and to protect officer safety, but searching its digital contents requires a "
                "warrant. The Court noted that exigent circumstances may justify a warrantless "
                "search in rare cases, but none were present here. Option A applies pre-Riley "
                "reasoning that the Court explicitly rejected. Option C misapplies the Chimel "
                "wingspan rule to digital content. Option D is irrelevant — the seriousness of "
                "the crime discovered does not retroactively validate an unlawful search."
            ),
            "is_premium": True,
            "created_at": now,
        },
        # ──────────────────────────────────────────────
        # 20. Implied Consent and DUI in Illinois
        # ──────────────────────────────────────────────
        {
            "question_id": "legal_trap_extra_020",
            "title": "Implied Consent — DUI Blood Draw Without Warrant",
            "type": "legal_trap",
            "category_id": "cat_legal_trap",
            "scenario": (
                "You arrest a driver for DUI after he fails field sobriety tests. At the "
                "station, you request a breath test, but the driver refuses. You then instruct "
                "a phlebotomist to draw the driver's blood without his consent and without a "
                "warrant, citing Illinois' implied consent law (625 ILCS 5/11-501.1) as your "
                "legal authority."
            ),
            "options": {
                "A": "The blood draw is lawful because Illinois' implied consent statute authorizes warrantless blood draws from all DUI suspects who refuse breath tests.",
                "B": "The blood draw is lawful because the natural dissipation of alcohol in the bloodstream always constitutes an exigent circumstance justifying a warrantless blood draw.",
                "C": "The blood draw is likely unlawful — while implied consent statutes impose administrative penalties for refusal (license suspension), the Supreme Court has held that a warrant is generally required for a blood draw, and natural dissipation alone does not categorically create exigent circumstances.",
                "D": "The blood draw is lawful because a DUI arrest automatically gives officers the right to take any biological sample."
            },
            "correct_answer": "C",
            "io_scores": {"A": -1, "B": -1, "C": 2, "D": -2},
            "explanation": (
                "This question tests the intersection of implied consent statutes and the Fourth "
                "Amendment after the Supreme Court's rulings in Missouri v. McNeely (2013) and "
                "Birchfield v. North Dakota (2016). In McNeely, the Court held that the natural "
                "dissipation of alcohol in the bloodstream does NOT create a per se exigent "
                "circumstance — courts must analyze exigency on a case-by-case basis. In "
                "Birchfield, the Court held that while breath tests may be administered incident "
                "to arrest, blood tests are significantly more intrusive and generally require a "
                "warrant. Illinois' implied consent law (625 ILCS 5/11-501.1) imposes "
                "administrative consequences (statutory summary suspension of driving privileges) "
                "for refusal, but it does NOT authorize forcible warrantless blood draws absent "
                "true exigent circumstances or a warrant. Option A conflates administrative "
                "penalties with Fourth Amendment authorization. Option B was explicitly rejected "
                "in McNeely. Option D is dangerously overbroad."
            ),
            "is_premium": True,
            "created_at": now,
        },
    ]

    # ──────────────────────────────────────────────
    # Normalize and upsert all questions into the database
    # ──────────────────────────────────────────────
    total_upserted = 0
    for q in questions:
        # Normalize field names: "scenario" → "content"
        if "scenario" in q and "content" not in q:
            q["content"] = q.pop("scenario")

        # Normalize options: dict {"A": "text"} → list [{"label": "A", "text": "..."}]
        if isinstance(q.get("options"), dict):
            q["options"] = [
                {"label": k, "text": v}
                for k, v in sorted(q["options"].items())
            ]

        # Add missing standard fields
        if "question" not in q:
            q["question"] = "Select the correct answer."
        if "category_name" not in q:
            q["category_name"] = "Legal Trap"
        if "difficulty" not in q:
            q["difficulty"] = "hard"
        if "reference" not in q:
            q["reference"] = ""
        if "updated_at" not in q:
            q["updated_at"] = now

        result = await db.questions.update_one(
            {"question_id": q["question_id"]},
            {"$set": q},
            upsert=True
        )
        if result.upserted_id or result.modified_count:
            total_upserted += 1

    print(f"Seeded {total_upserted} extra legal trap questions")
    print(f"  Total Legal Trap in DB: {await db.questions.count_documents({'type': 'legal_trap'})}")


if __name__ == "__main__":
    asyncio.run(seed_legal_trap_extra())
