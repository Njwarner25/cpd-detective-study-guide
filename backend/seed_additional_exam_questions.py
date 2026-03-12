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


async def seed_additional_exam_questions(ext_db=None):
    """Seed 20 additional questions for each of: Most Appropriate, Least Appropriate, and Ranking.

    This supplements the existing questions in seed_mixed_exam_questions.py and
    seed_ranking_questions.py with 60 new questions total.

    Args:
        ext_db: Optional external database connection.
    """
    global db
    if ext_db is not None:
        db = ext_db

    now = datetime.now(timezone.utc)

    # ================================================================
    # SECTION 1: MOST APPROPRIATE — 20 NEW QUESTIONS
    # ================================================================
    most_appropriate = [
        {
            "title": "Suspect Detained During Traffic Stop",
            "content": "While conducting a traffic stop for a minor violation, you observe what appears to be a firearm partially visible under the passenger seat. The driver has been cooperative.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Order the driver out and conduct a full vehicle search"},
                {"label": "B", "text": "Secure the driver, request backup, and conduct a protective sweep based on plain view"},
                {"label": "C", "text": "Ignore the firearm and issue the traffic citation"},
                {"label": "D", "text": "Ask the driver if the firearm is registered"}
            ],
            "correct_answer": "B",
            "explanation": "Under the plain view doctrine and Michigan v. Long (1983), when an officer has reasonable suspicion of danger during a traffic stop, a protective sweep of the passenger compartment is justified. Ordering a full search (A) exceeds the scope without probable cause. Ignoring the weapon (C) is a safety hazard. Asking about registration (D) delays securing a potential threat.",
            "io_scores": {"A": 0, "B": 2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "Michigan v. Long, 463 U.S. 1032 (1983); Plain View Doctrine"
        },
        {
            "title": "Conflicting Witness Accounts at Robbery",
            "content": "Two witnesses to an armed robbery give contradictory descriptions of the offender. One says the suspect was a tall male in a red jacket; the other says it was a medium-build male in a dark hoodie.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Discard the less credible statement"},
                {"label": "B", "text": "Interview each witness separately and document both accounts in detail"},
                {"label": "C", "text": "Bring both witnesses together to reconcile their accounts"},
                {"label": "D", "text": "Use only the first witness's account since they reported first"}
            ],
            "correct_answer": "B",
            "explanation": "Separate, detailed interviews preserve the integrity of each witness's independent recollection. Discarding a statement (A) loses potential evidence. Bringing witnesses together (C) risks cross-contamination of their memories. Prioritizing based on reporting order (D) has no investigative basis. All witness accounts must be documented regardless of consistency.",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Witness Management"
        },
        {
            "title": "Suspect Offers Bribe During Investigation",
            "content": "During a burglary investigation, the homeowner's neighbor approaches you privately and offers you $500 to \"make sure\" the investigation points to a specific person he has a dispute with.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Accept the money as evidence and continue the investigation"},
                {"label": "B", "text": "Decline the offer and continue investigating without documenting the interaction"},
                {"label": "C", "text": "Decline the offer, document the attempted bribery, and notify your supervisor immediately"},
                {"label": "D", "text": "Tell the neighbor you will consider his information"}
            ],
            "correct_answer": "C",
            "explanation": "Any attempted bribe must be declined, documented, and reported to a supervisor. This protects the integrity of the investigation and creates a record. Accepting the money (A) is corruption regardless of stated intent. Not documenting (B) fails to create a record of the misconduct. Appearing to entertain the offer (D) could constitute official misconduct.",
            "io_scores": {"A": -2, "B": 0, "C": 2, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G08-01; Ethics and Integrity; 720 ILCS 5/33-1 Bribery"
        },
        {
            "title": "Forensic Evidence Contamination Risk",
            "content": "You arrive at a sexual assault crime scene. A patrol officer informs you that the victim's clothing was placed in a plastic bag by a well-meaning family member before police arrived.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Accept the clothing as-is and submit it to the crime lab"},
                {"label": "B", "text": "Document the contamination issue, repackage in a paper bag, and note the chain of custody break"},
                {"label": "C", "text": "Discard the clothing since it has been contaminated"},
                {"label": "D", "text": "Return the clothing to the family until needed"}
            ],
            "correct_answer": "B",
            "explanation": "Biological evidence must be stored in paper bags to prevent degradation from moisture. While the chain of custody has been compromised, the evidence is not worthless — documenting the contamination issue and repackaging properly preserves whatever probative value remains. Discarding (C) destroys potential evidence. Returning to the family (D) worsens the chain of custody break.",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "CPD Special Order S06-04; Evidence Collection and Preservation"
        },
        {
            "title": "Undercover Officer Identified at Scene",
            "content": "While processing a drug-related homicide scene, a bystander loudly identifies one of the people in the crowd as an undercover police officer working narcotics.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Confirm the person's identity to establish credibility"},
                {"label": "B", "text": "Deny any knowledge and immediately arrange for the undercover officer to safely leave the area"},
                {"label": "C", "text": "Arrest the bystander for obstruction"},
                {"label": "D", "text": "Ignore the situation and continue processing"}
            ],
            "correct_answer": "B",
            "explanation": "Officer safety is paramount. The undercover officer's cover has been compromised, creating an immediate safety risk. Denying knowledge and arranging safe extraction protects the officer. Confirming identity (A) endangers the officer further. Arresting the bystander (C) draws more attention and is likely not legally justified. Ignoring the situation (D) leaves the officer in danger.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "CPD Special Order S09-07; Undercover Operations Safety"
        },
        {
            "title": "Juvenile Suspect Miranda Considerations",
            "content": "You are about to interview a 15-year-old suspect in a vehicle theft. The juvenile's mother is present and demands to sit in during the interview. The juvenile states he wants to talk without his mother present.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Allow the juvenile to be interviewed alone since he consented"},
                {"label": "B", "text": "Require the mother to be present regardless of the juvenile's preference"},
                {"label": "C", "text": "Ensure the juvenile understands his rights with a simplified Miranda warning and allow a parent/guardian to be present per Illinois law"},
                {"label": "D", "text": "Delay the interview until a public defender arrives"}
            ],
            "correct_answer": "C",
            "explanation": "Illinois law (705 ILCS 405/5-170) requires that a minor be advised of rights in age-appropriate language and that a concerned adult be present during questioning. The juvenile's desire to exclude his mother does not override the statutory requirement for a guardian or responsible adult to be present. Interviewing alone (A) violates juvenile protections. Delaying for a PD (D) is unnecessary if rights are properly administered with a guardian present.",
            "io_scores": {"A": -2, "B": 1, "C": 2, "D": 0},
            "difficulty": "hard",
            "reference": "705 ILCS 405/5-170; Juvenile Court Act; CPD Special Order S06-01"
        },
        {
            "title": "Discovery of Additional Crime During Warrant",
            "content": "While executing a search warrant for stolen electronics at a residence, you discover a large quantity of what appears to be narcotics in plain view on the kitchen table.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Seize the narcotics under the plain view doctrine and document the discovery"},
                {"label": "B", "text": "Ignore the narcotics since they are outside the scope of the warrant"},
                {"label": "C", "text": "Stop the search entirely and obtain a new warrant for narcotics"},
                {"label": "D", "text": "Have another officer seize the narcotics to avoid tainting the original warrant"}
            ],
            "correct_answer": "A",
            "explanation": "Under Horton v. California (1990), items in plain view during a lawful search may be seized if their incriminating nature is immediately apparent. The officers are lawfully present executing a valid warrant, and the narcotics are in plain view. Ignoring the evidence (B) is a dereliction of duty. Stopping entirely (C) is unnecessary — the plain view doctrine applies. Having another officer seize them (D) adds no legal protection.",
            "io_scores": {"A": 2, "B": -2, "C": 0, "D": -1},
            "difficulty": "medium",
            "reference": "Horton v. California, 496 U.S. 128 (1990); Plain View Doctrine"
        },
        {
            "title": "Victim with Protective Order Violated",
            "content": "A victim calls to report that her ex-husband, who has an active Order of Protection against him, showed up at her workplace and left threatening notes. She is visibly frightened but does not want him arrested.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Respect the victim's wishes and take a report only"},
                {"label": "B", "text": "Explain that a violation of an Order of Protection is a mandatory arrest offense, take enforcement action, and document the evidence"},
                {"label": "C", "text": "Issue a warning to the ex-husband by phone"},
                {"label": "D", "text": "Advise the victim to call back if he returns"}
            ],
            "correct_answer": "B",
            "explanation": "Under 750 ILCS 60/223, violation of an Order of Protection is a mandatory arrest offense in Illinois. The victim's preference not to arrest does not override the statutory mandate. Simply taking a report (A) or advising callback (D) fails to enforce the law. Issuing a phone warning (C) is inadequate for a criminal violation and may escalate danger.",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "750 ILCS 60/223; Illinois Domestic Violence Act; CPD General Order G06-03"
        },
        {
            "title": "Suspect Requests to Use Restroom During Interview",
            "content": "During a lengthy interrogation of a homicide suspect who has waived Miranda rights, the suspect asks to use the restroom. The interview has been productive and you are close to obtaining a confession.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Deny the request to maintain momentum in the interview"},
                {"label": "B", "text": "Allow a supervised restroom break and resume the interview afterward"},
                {"label": "C", "text": "Tell the suspect he can use the restroom after he confesses"},
                {"label": "D", "text": "End the interview permanently"}
            ],
            "correct_answer": "B",
            "explanation": "Denying basic needs such as restroom use can render a subsequent confession involuntary and subject to suppression under the voluntariness test. A supervised break does not terminate the interview. Denying the request (A) or conditioning it on a confession (C) constitutes coercion. Ending the interview permanently (D) is unnecessary — the waiver remains valid through reasonable breaks.",
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": 0},
            "difficulty": "medium",
            "reference": "Voluntariness Standard; 5th Amendment; Mincey v. Arizona"
        },
        {
            "title": "Anonymous Tip Regarding Officer Misconduct",
            "content": "You receive an anonymous tip that a fellow detective in your unit has been stealing cash from evidence in drug cases. You have not personally witnessed any misconduct.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Confront the detective directly with the allegation"},
                {"label": "B", "text": "Report the allegation to your supervisor or the Internal Affairs Division immediately"},
                {"label": "C", "text": "Investigate the matter yourself before reporting"},
                {"label": "D", "text": "Ignore the tip since it is anonymous and unverified"}
            ],
            "correct_answer": "B",
            "explanation": "CPD policy requires that allegations of misconduct be reported to a supervisor or Internal Affairs immediately. Officers have a duty to report. Confronting the detective (A) could compromise an investigation and alert a potential suspect. Self-investigating (C) is outside your authority and risks evidence destruction. Ignoring the tip (D) violates the duty to report and could constitute complicity.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G08-01; Duty to Report Misconduct"
        },
        {
            "title": "Critical Incident Stress After Officer-Involved Shooting",
            "content": "You just witnessed your partner fatally shoot an armed subject. Your partner appears to be in shock and is not speaking. A supervisor arrives and orders your partner to immediately provide a detailed statement.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Encourage your partner to comply with the supervisor's order immediately"},
                {"label": "B", "text": "Inform the supervisor that your partner should receive a critical incident debriefing and consult with a union representative before giving a detailed statement"},
                {"label": "C", "text": "Tell your partner to refuse to give any statement"},
                {"label": "D", "text": "Provide the statement on your partner's behalf"}
            ],
            "correct_answer": "B",
            "explanation": "After an officer-involved shooting, CPD General Order G03-06 provides for critical incident procedures, including the right to consult with a union representative and legal counsel before providing a detailed statement. Immediate detailed statements under stress may be inaccurate and could harm the investigation. Refusing any statement (C) is different from exercising procedural rights. Providing someone else's statement (D) is improper.",
            "io_scores": {"A": -1, "B": 2, "C": 0, "D": -2},
            "difficulty": "hard",
            "reference": "CPD General Order G03-06; Officer-Involved Shooting Procedures"
        },
        {
            "title": "Gang Retaliation Intelligence During Interview",
            "content": "While interviewing a shooting victim in the hospital, he tells you that his gang is planning retaliation against a rival faction tonight at a specific location. He refuses to put this in a formal statement.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Ignore the information since the victim will not provide a formal statement"},
                {"label": "B", "text": "Immediately relay the intelligence to the Gang Investigation Division and district tactical teams, documenting the information received"},
                {"label": "C", "text": "Go to the rival gang's location yourself to prevent the retaliation"},
                {"label": "D", "text": "Tell the victim to call 911 if the retaliation occurs"}
            ],
            "correct_answer": "B",
            "explanation": "Intelligence about imminent violence must be acted upon immediately regardless of whether a formal statement is provided. Relaying to the appropriate specialized units allows for a coordinated response. Ignoring the information (A) could result in deaths. Responding alone (C) is tactically dangerous. Telling the victim to call 911 (D) abdicates your responsibility to act on known threats.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "CPD Special Order S09-03; Gang Violence Prevention"
        },
        {
            "title": "Crime Scene on Private Property Without Consent",
            "content": "Neighbors report hearing gunshots from inside a residence. You arrive and find blood on the front porch but no one answers the door. No warrant has been obtained.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Force entry based on probable cause from the blood evidence alone"},
                {"label": "B", "text": "Enter under exigent circumstances doctrine — the blood and gunshots suggest someone may need immediate aid"},
                {"label": "C", "text": "Wait at the scene until a search warrant is obtained"},
                {"label": "D", "text": "Leave and return later with a warrant"}
            ],
            "correct_answer": "B",
            "explanation": "Under the emergency aid exception to the warrant requirement, officers may enter a dwelling without a warrant when they have an objectively reasonable basis to believe someone inside needs immediate assistance. Reported gunshots plus blood evidence meets this standard. Waiting for a warrant (C/D) could result in death of a victim inside. Entering on probable cause alone (A) misidentifies the legal basis — exigent circumstances is the correct doctrine.",
            "io_scores": {"A": 0, "B": 2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "Brigham City v. Stuart, 547 U.S. 398 (2006); Exigent Circumstances"
        },
        {
            "title": "Body Camera Malfunction During Arrest",
            "content": "During a felony arrest, you realize your body-worn camera malfunctioned and did not record the encounter. The arrest involved a brief use of force when the suspect resisted.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Do not mention the camera failure in your report"},
                {"label": "B", "text": "Document the camera malfunction in your report, note the reason, and immediately notify your supervisor"},
                {"label": "C", "text": "Recreate the missing footage using a different camera after the fact"},
                {"label": "D", "text": "Wait to see if anyone complains before addressing the malfunction"}
            ],
            "correct_answer": "B",
            "explanation": "Transparency requires immediate documentation of any BWC malfunction, especially during use-of-force incidents. Failure to disclose (A) or waiting for complaints (D) suggests concealment. Recreating footage (C) would be fabrication of evidence. Prompt notification allows supervisors to ensure alternative documentation methods are used.",
            "io_scores": {"A": -2, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "CPD Special Order S03-14; Body Worn Cameras"
        },
        {
            "title": "Informant Provides Information About Planned Robbery",
            "content": "A registered confidential informant tells you about a planned armed robbery of a currency exchange tomorrow morning. The CI has been reliable in the past but wants significant compensation for this information.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Promise the CI whatever compensation they request to secure the information"},
                {"label": "B", "text": "Document the intelligence, corroborate through independent investigation, and coordinate with your supervisor regarding CI compensation per department policy"},
                {"label": "C", "text": "Act on the tip immediately without verification"},
                {"label": "D", "text": "Decline the information since the CI is demanding payment"}
            ],
            "correct_answer": "B",
            "explanation": "CI management requires proper documentation, independent corroboration of intelligence, and compensation handled through official channels with supervisory approval. Making unauthorized promises (A) violates CI management protocols. Acting without verification (C) could lead to a compromised operation. Declining actionable intelligence about violent crime (D) is irresponsible.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD Special Order S09-01; Confidential Informant Management"
        },
        {
            "title": "Victim Identifies Suspect from Social Media",
            "content": "A robbery victim calls you the day after the incident and says she found her attacker's profile on social media. She is certain of the identification and wants him arrested immediately.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Arrest the identified person immediately based on the victim's certainty"},
                {"label": "B", "text": "Conduct a proper photo array following department procedures, using the social media lead to identify the suspect for inclusion"},
                {"label": "C", "text": "Tell the victim to message the suspect on social media to confirm"},
                {"label": "D", "text": "Show the victim only the social media photo for confirmation"}
            ],
            "correct_answer": "B",
            "explanation": "A single-photo identification is highly suggestive and may not withstand legal challenge. Proper procedure requires a photo array with fillers following CPD identification procedures to ensure reliability. Arresting without proper identification (A) risks false arrest. Having the victim contact the suspect (C) could alert him and create danger. Showing only one photo (D) is a suggestive identification procedure.",
            "io_scores": {"A": -1, "B": 2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "CPD Special Order S04-13; Identification Procedures; Manson v. Brathwaite"
        },
        {
            "title": "Multi-Agency Task Force Information Sharing",
            "content": "You are assigned to a federal task force investigating a drug trafficking organization. The FBI case agent asks you to share CPD intelligence files on several subjects without going through the department's formal information-sharing process.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Share the files immediately since you are on the same task force"},
                {"label": "B", "text": "Follow CPD's formal information-sharing procedures and coordinate through your departmental liaison before releasing any files"},
                {"label": "C", "text": "Refuse to share any information with federal agencies"},
                {"label": "D", "text": "Share the files but ask the FBI agent not to attribute them to CPD"}
            ],
            "correct_answer": "B",
            "explanation": "Even on a joint task force, CPD intelligence files must be shared through proper channels following departmental policy. Bypassing the process (A) could violate regulations and compromise ongoing CPD investigations. Refusing all cooperation (C) hinders the task force mission. Sharing without attribution (D) still violates policy and removes accountability.",
            "io_scores": {"A": -1, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G10-01; Information Sharing Protocols"
        },
        {
            "title": "Finding Unrelated Contraband During Consent Search",
            "content": "During a consent search of a vehicle for a stolen laptop, you find a bag of cannabis exceeding the legal possession limit in the trunk, but no laptop.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Seize the cannabis and charge the driver with possession"},
                {"label": "B", "text": "Ignore the cannabis since the consent was for searching for a laptop"},
                {"label": "C", "text": "Expand the search to look for additional contraband throughout the vehicle"},
                {"label": "D", "text": "Return the cannabis to the driver since it is now legal in Illinois"}
            ],
            "correct_answer": "A",
            "explanation": "During a valid consent search, any contraband found in plain view during the lawful scope of the search may be seized. The trunk is a reasonable place to look for a laptop, making the cannabis discovery within the scope. Ignoring it (B) is a dereliction. Expanding the search (C) may exceed the scope of consent. Cannabis over the legal limit (D) is still unlawful possession under Illinois law.",
            "io_scores": {"A": 2, "B": -2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "Florida v. Jimeno, 500 U.S. 248 (1991); Illinois Cannabis Regulation Act"
        },
        {
            "title": "Suspect Provides Alibi with Verifiable Evidence",
            "content": "Your primary suspect in an aggravated battery case presents surveillance footage from a gas station that appears to show him at a different location at the time of the offense. The footage timestamp matches the incident time.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Disregard the alibi evidence since the suspect is obviously lying"},
                {"label": "B", "text": "Verify the alibi by independently obtaining the footage from the gas station and investigating its authenticity"},
                {"label": "C", "text": "Immediately release the suspect and close the case"},
                {"label": "D", "text": "Arrest the suspect anyway and let the prosecutor evaluate the alibi"}
            ],
            "correct_answer": "B",
            "explanation": "All evidence, including exculpatory evidence, must be thoroughly investigated. Independent verification of the alibi through the gas station is essential for a fair investigation. Disregarding evidence (A) violates investigative integrity. Immediately releasing without verification (C) is premature. Arresting despite unexamined alibi evidence (D) may constitute a Brady violation if the alibi is not disclosed to the defense.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -1},
            "difficulty": "hard",
            "reference": "Brady v. Maryland, 373 U.S. 83 (1963); Due Process"
        },
        {
            "title": "Homeless Encampment Near Crime Scene",
            "content": "You are investigating a sexual assault that occurred in a park. A homeless encampment is located approximately 50 yards from the scene. Several individuals in the encampment may have witnessed the assault but are reluctant to speak with police.",
            "question": "What is the MOST appropriate action?",
            "options": [
                {"label": "A", "text": "Threaten to arrest the encampment residents for trespassing if they do not cooperate"},
                {"label": "B", "text": "Approach the potential witnesses respectfully, explain the seriousness of the case, and offer victim services resources to build rapport"},
                {"label": "C", "text": "Skip the encampment residents since their testimony would be unreliable"},
                {"label": "D", "text": "Send patrol officers to clear the encampment before approaching"}
            ],
            "correct_answer": "B",
            "explanation": "Building rapport with reluctant witnesses through respectful engagement is the most effective approach for obtaining cooperation. Threatening arrest (A) is coercive and may produce false statements. Dismissing potential witnesses based on housing status (C) is discriminatory and poor investigative practice. Clearing the encampment (D) would scatter potential witnesses and destroy their willingness to cooperate.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Witness Engagement"
        },
    ]

    # ================================================================
    # SECTION 2: LEAST APPROPRIATE — 20 NEW QUESTIONS
    # ================================================================
    least_appropriate = [
        {
            "title": "Conducting Lineup Without Attorney Present",
            "content": "You have arrested a suspect for armed robbery. The victim is available for a lineup identification. The suspect's attorney has not yet been notified.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Proceed with the lineup immediately without notifying the suspect's attorney"},
                {"label": "B", "text": "Notify the suspect's attorney and schedule the lineup"},
                {"label": "C", "text": "Conduct a photo array instead, following proper procedures"},
                {"label": "D", "text": "Wait for the attorney and conduct the lineup with proper safeguards"}
            ],
            "correct_answer": "A",
            "explanation": "Under United States v. Wade (1967) and the 6th Amendment right to counsel, a post-indictment lineup requires that the suspect's attorney be notified and given the opportunity to be present. Proceeding without attorney notification violates the right to counsel and the identification will likely be suppressed.",
            "io_scores": {"A": 2, "B": -2, "C": -1, "D": -2},
            "difficulty": "hard",
            "reference": "United States v. Wade, 388 U.S. 218 (1967); 6th Amendment"
        },
        {
            "title": "Discussing Case Details with Non-Involved Officer",
            "content": "You are investigating a politically sensitive case involving a local alderman. An officer from another unit, who is a friend, asks you casually about the details of the investigation over lunch.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Share general details since the officer has a security clearance"},
                {"label": "B", "text": "Politely decline to discuss the case citing confidentiality"},
                {"label": "C", "text": "Refer your friend to the case supervisor if they have a legitimate need"},
                {"label": "D", "text": "Share only publicly available information"}
            ],
            "correct_answer": "A",
            "explanation": "Sharing case details with officers who have no investigative need-to-know violates confidentiality protocols, regardless of security clearance or personal relationship. This is especially critical in politically sensitive cases where leaks could compromise the investigation or create the appearance of impropriety.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "CPD General Order G08-01; Confidentiality of Investigations"
        },
        {
            "title": "Using Personal Vehicle for Evidence Transport",
            "content": "After collecting critical DNA evidence from a crime scene, you realize the evidence transport vehicle is unavailable. Your personal vehicle is nearby.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Transport the evidence in your personal vehicle to expedite processing"},
                {"label": "B", "text": "Secure the evidence at the scene and request an official transport vehicle"},
                {"label": "C", "text": "Have a patrol unit with a squad car transport the evidence"},
                {"label": "D", "text": "Contact the crime lab to arrange evidence pickup"}
            ],
            "correct_answer": "A",
            "explanation": "Transporting evidence in a personal vehicle compromises chain of custody, creates defense challenges, and violates evidence handling protocols. The chain of custody must be maintained through official channels. All other options maintain proper evidence handling procedures and protect the integrity of the evidence.",
            "io_scores": {"A": 2, "B": -2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD Special Order S06-04; Evidence Handling and Chain of Custody"
        },
        {
            "title": "Interrogation After Suspect Invokes Silence",
            "content": "A murder suspect clearly states 'I want to remain silent' during interrogation. Thirty minutes later, while sitting in the interview room, the suspect appears restless and sighs heavily.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Interpret the sighing as a desire to talk and resume questioning"},
                {"label": "B", "text": "Remain in the room but do not initiate conversation"},
                {"label": "C", "text": "Ensure the invocation is documented and cease questioning"},
                {"label": "D", "text": "Offer the suspect basic amenities without discussing the case"}
            ],
            "correct_answer": "A",
            "explanation": "Under Michigan v. Mosley (1975) and the 5th Amendment, once a suspect invokes the right to silence, questioning must cease. Non-verbal cues like sighing cannot be interpreted as a reinitiation of communication. Only a clear, unambiguous reinitiation by the suspect allows questioning to resume. Interpreting body language as willingness to talk violates Miranda protections.",
            "io_scores": {"A": 2, "B": -1, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "Michigan v. Mosley, 423 U.S. 96 (1975); Miranda v. Arizona"
        },
        {
            "title": "Photographing Suspect Injuries Without Consent",
            "content": "A suspect arrested for aggravated battery has visible injuries consistent with self-defense claims. You want to document his injuries for the investigation file.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Photograph the suspect's injuries as part of standard booking documentation procedures"},
                {"label": "B", "text": "Request medical evaluation and photograph injuries with proper documentation"},
                {"label": "C", "text": "Force the suspect to remove clothing for full-body photography over his objections"},
                {"label": "D", "text": "Document visible injuries in your report with photographs of exposed areas"}
            ],
            "correct_answer": "C",
            "explanation": "Forcing a suspect to disrobe for photography without a warrant or valid exception violates the 4th Amendment protection against unreasonable searches and the suspect's dignity. While photographing visible injuries during booking is standard, compelled removal of clothing requires either consent, a warrant, or specific legal authority such as a strip search warrant.",
            "io_scores": {"A": -1, "B": -2, "C": 2, "D": -2},
            "difficulty": "hard",
            "reference": "4th Amendment; CPD General Order G06-01-03; Search and Seizure"
        },
        {
            "title": "Interviewing Victim at Hospital Without Advocate",
            "content": "A sexual assault victim is being treated at the hospital. The victim is conscious and willing to speak. No victim advocate has been contacted yet.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Conduct a full detailed interview immediately to capture fresh details before memory fades"},
                {"label": "B", "text": "Contact a victim advocate and conduct a preliminary interview while waiting"},
                {"label": "C", "text": "Obtain basic information and schedule a comprehensive interview with an advocate present"},
                {"label": "D", "text": "Allow the SANE nurse to complete the examination before interviewing"}
            ],
            "correct_answer": "A",
            "explanation": "Conducting a comprehensive interview of a sexual assault victim without a victim advocate present and during medical treatment is the least appropriate action. It can retraumatize the victim, compromise the quality of information obtained, and may violate department protocols regarding victim sensitivity. While time-sensitive details should be noted, a full interview should await proper support.",
            "io_scores": {"A": 2, "B": -1, "C": -2, "D": -2},
            "difficulty": "medium",
            "reference": "CPD Special Order S06-05; Sexual Assault Investigations; VAWA Guidelines"
        },
        {
            "title": "Running License Plates for Personal Reasons",
            "content": "You are off-duty and notice a car you don't recognize parked in front of your neighbor's house for several days. Out of curiosity, you use your MDT access to run the plate.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Run the plate through the MDT for personal curiosity"},
                {"label": "B", "text": "Ask your neighbor about the unfamiliar vehicle"},
                {"label": "C", "text": "If genuinely concerned, report it through proper channels as a community member"},
                {"label": "D", "text": "Note the plate number and check during your next shift if it relates to any active cases"}
            ],
            "correct_answer": "A",
            "explanation": "Using law enforcement databases (LEADS/NCIC) for personal or non-official purposes is a federal and state violation. The Driver's Privacy Protection Act (18 U.S.C. § 2721) and CPD policy strictly prohibit personal use of these systems. Officers have been terminated and criminally charged for misuse of database access.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "18 U.S.C. § 2721; Driver's Privacy Protection Act; CPD General Order G03-02"
        },
        {
            "title": "Releasing Crime Scene Before Processing Complete",
            "content": "Pressure is mounting from the property owner and alderman's office to release a crime scene at a commercial building. The evidence technicians have processed the main area but have not yet examined secondary rooms.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Release the entire scene to appease the property owner and political pressure"},
                {"label": "B", "text": "Maintain the scene until all areas are fully processed"},
                {"label": "C", "text": "Release the processed areas while maintaining the unprocessed rooms"},
                {"label": "D", "text": "Document the pressure and escalate to your commanding officer"}
            ],
            "correct_answer": "A",
            "explanation": "Releasing a crime scene before processing is complete due to political or external pressure compromises the investigation. Once a scene is released, evidence may be destroyed, contaminated, or lost. The integrity of the investigation must take priority over external pressure. Documenting the pressure (D) creates a record protecting all parties.",
            "io_scores": {"A": 2, "B": -2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Crime Scene Integrity"
        },
        {
            "title": "Failing to Impound Vehicle Used in Crime",
            "content": "You have probable cause that a vehicle was used as the getaway car in an armed robbery. The registered owner, who was not involved in the robbery, asks you not to impound the vehicle because they need it for work.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Release the vehicle to the owner out of sympathy for their work situation"},
                {"label": "B", "text": "Impound the vehicle as evidence and process it for forensic evidence"},
                {"label": "C", "text": "Impound the vehicle and advise the owner on the process for retrieving it after processing"},
                {"label": "D", "text": "Obtain a warrant to search the vehicle and impound it"}
            ],
            "correct_answer": "A",
            "explanation": "A vehicle used as an instrumentality of a crime must be impounded and processed for evidence regardless of the owner's personal circumstances. Releasing potential evidence compromises the investigation and could result in the loss of forensic evidence such as DNA, fingerprints, and fibers connecting suspects to the crime.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-02; Vehicle Impoundment; Evidence Preservation"
        },
        {
            "title": "Posting Crime Scene Photos on Social Media",
            "content": "You respond to a particularly unusual crime scene. A fellow officer takes photos and posts them to a private police social media group for discussion.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Report the social media posting to your supervisor immediately"},
                {"label": "B", "text": "Share additional details in the comments to add context"},
                {"label": "C", "text": "Ask the officer to remove the post and explain why it is improper"},
                {"label": "D", "text": "Document the incident for potential disciplinary action"}
            ],
            "correct_answer": "B",
            "explanation": "Adding additional case details to an already improper social media post compounds the violation. Sharing crime scene photos and case details on social media — even in \"private\" groups — violates victim privacy, compromises investigations, and violates CPD social media policy. The correct responses are to report, document, and request removal.",
            "io_scores": {"A": -2, "B": 2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD Special Order S09-10; Social Media Policy; Victim Privacy"
        },
        {
            "title": "Accepting Gift from Grateful Victim",
            "content": "After successfully solving a robbery case, the victim sends you an expensive watch as a thank-you gift to the station.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Accept the watch and wear it proudly"},
                {"label": "B", "text": "Politely decline the gift and explain department policy on gratuities"},
                {"label": "C", "text": "Return the gift through proper channels with a thank-you note"},
                {"label": "D", "text": "Report the gift to your supervisor for proper handling"}
            ],
            "correct_answer": "A",
            "explanation": "Accepting gifts, gratuities, or rewards from anyone connected to a case violates CPD ethics policy and creates the appearance of impropriety. It could also be construed as a bribe or could compromise the officer's objectivity in future interactions with the victim. All gifts must be declined or returned through proper channels.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -2},
            "difficulty": "easy",
            "reference": "CPD General Order G08-01; Ethics; Gratuities and Gifts Policy"
        },
        {
            "title": "Detaining Witness Who Wants to Leave",
            "content": "A key witness to a drive-by shooting tells you she has to pick up her children from school and cannot stay to give a statement right now.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Physically prevent the witness from leaving and compel a statement"},
                {"label": "B", "text": "Obtain the witness's contact information and arrange a follow-up interview"},
                {"label": "C", "text": "Get a brief preliminary statement and arrange a comprehensive follow-up"},
                {"label": "D", "text": "Offer to drive the witness to pick up her children and interview afterward"}
            ],
            "correct_answer": "A",
            "explanation": "Witnesses (unlike suspects) generally cannot be detained against their will to compel statements. Physically preventing a witness from leaving could constitute false imprisonment and violates the witness's rights. Effective witness management involves obtaining contact information, getting preliminary details, and scheduling follow-up interviews.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "4th Amendment; Witness Rights; CPD General Order G06-01-01"
        },
        {
            "title": "Entering Suspect Information into Wrong System",
            "content": "You accidentally enter a suspect's personal information and arrest details into the wrong database field, associating it with an unrelated case number.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Leave the error and hope no one notices"},
                {"label": "B", "text": "Immediately correct the error and document the mistake"},
                {"label": "C", "text": "Notify your supervisor and the records division to correct the entry"},
                {"label": "D", "text": "Create a supplementary report documenting the data entry error"}
            ],
            "correct_answer": "A",
            "explanation": "Leaving incorrect information in law enforcement databases is the least appropriate action. Errors in criminal justice databases can result in wrongful arrests, incorrect background checks, and civil liability. Data integrity is critical. All errors must be immediately corrected and documented to maintain the reliability of the system.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -1},
            "difficulty": "easy",
            "reference": "CPD General Order G03-02; Records Management; Data Integrity"
        },
        {
            "title": "Using Deceptive Interrogation Tactics on Juvenile",
            "content": "You are interrogating a 16-year-old suspect in a shooting. The juvenile has waived Miranda with a parent present. You consider telling the juvenile that his co-offender has already confessed and implicated him (which is false).",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Use the false confession deception to pressure the juvenile"},
                {"label": "B", "text": "Use age-appropriate, non-deceptive interview techniques"},
                {"label": "C", "text": "Present actual evidence and allow the juvenile to respond"},
                {"label": "D", "text": "Use rapport-building techniques appropriate for juvenile suspects"}
            ],
            "correct_answer": "A",
            "explanation": "Under Illinois law (725 ILCS 5/103-2.2), deceptive interrogation tactics are prohibited when questioning minors. Using false claims of co-defendant confessions is specifically the type of deception banned by statute. Even in jurisdictions where some deception is permitted for adults, juveniles receive heightened protections due to their vulnerability to coercion.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "725 ILCS 5/103-2.2; Juvenile Interrogation Protections"
        },
        {
            "title": "Failing to Secure Firearm Evidence Properly",
            "content": "You recover a firearm at a crime scene. Due to a shortage of evidence bags, a responding officer suggests placing the gun in a cardboard box found at the scene.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Place the firearm in the cardboard box from the scene"},
                {"label": "B", "text": "Request proper evidence packaging from the evidence technician"},
                {"label": "C", "text": "Secure the firearm in your vehicle's lockbox until proper packaging arrives"},
                {"label": "D", "text": "Use the gun's trigger guard to hang it in an evidence bag alternative"}
            ],
            "correct_answer": "A",
            "explanation": "Using materials from the crime scene to package evidence introduces contamination. The cardboard box may contain trace evidence, DNA, or other materials that could cross-contaminate the firearm evidence. Proper evidence packaging must be used, and if unavailable, the evidence should be secured using the best available alternative that does not risk contamination.",
            "io_scores": {"A": 2, "B": -2, "C": -1, "D": -1},
            "difficulty": "medium",
            "reference": "CPD Special Order S06-04; Firearms Evidence Handling"
        },
        {
            "title": "Interviewing Witness Under Influence",
            "content": "An important witness to a homicide is clearly intoxicated. She is willing to give a statement but is slurring her words and having difficulty focusing.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Take a comprehensive, detailed statement and use it as your primary witness account"},
                {"label": "B", "text": "Note the witness's condition, obtain basic details, and schedule a sober follow-up"},
                {"label": "C", "text": "Document the witness's apparent intoxication and obtain what information you can"},
                {"label": "D", "text": "Record the witness's contact information and re-interview when sober"}
            ],
            "correct_answer": "A",
            "explanation": "Relying on a comprehensive statement from an intoxicated witness as your primary account is problematic. The statement may be unreliable, easily challenged in court, and the witness's impaired state affects recall and accuracy. While you should document what information is available, the primary detailed interview should be conducted when the witness is sober.",
            "io_scores": {"A": 2, "B": -2, "C": -1, "D": -2},
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Witness Interviews; Evidence Reliability"
        },
        {
            "title": "Improper Storage of Digital Evidence",
            "content": "You seize a suspect's cell phone as evidence in a fraud case. You plan to examine it yourself using a personal data cable and your desk computer.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Connect the phone to your personal computer and browse its contents"},
                {"label": "B", "text": "Submit the phone to the digital forensics unit with a proper chain of custody form"},
                {"label": "C", "text": "Place the phone in airplane mode, power it down, and store it in a Faraday bag"},
                {"label": "D", "text": "Document the phone's condition and submit it through proper evidence channels"}
            ],
            "correct_answer": "A",
            "explanation": "Connecting seized digital evidence to a non-forensic computer can alter data, metadata, and timestamps — destroying the evidentiary value and chain of custody. Under Riley v. California (2014), cell phone searches require warrants, and examination must be performed by trained digital forensics examiners using write-blocking tools to preserve evidence integrity.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -2},
            "difficulty": "hard",
            "reference": "Riley v. California, 573 U.S. 373 (2014); CPD Special Order S06-06; Digital Evidence"
        },
        {
            "title": "Threatening Suspect's Family During Interrogation",
            "content": "During interrogation of a robbery suspect who is not cooperating, you consider mentioning that his wife could be charged as an accessory based on limited evidence.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Threaten to charge the suspect's wife to pressure a confession"},
                {"label": "B", "text": "Present the actual evidence against the suspect factually"},
                {"label": "C", "text": "Use approved interrogation techniques to build rapport"},
                {"label": "D", "text": "Advise the suspect of the strength of the evidence and potential penalties he faces"}
            ],
            "correct_answer": "A",
            "explanation": "Threatening to charge family members without probable cause to coerce a confession is coercive and may render any resulting statement involuntary and inadmissible. This tactic violates due process and could constitute prosecutorial/police misconduct. Threats against third parties to extract confessions have been consistently condemned by courts.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -1},
            "difficulty": "hard",
            "reference": "14th Amendment Due Process; Voluntariness Standard; Lynumn v. Illinois"
        },
        {
            "title": "Conducting Surveillance Without Authorization",
            "content": "You develop a hunch that a local business owner is involved in money laundering. Without obtaining supervisory approval, you begin parking near the business during your lunch break to observe activity.",
            "question": "What is the LEAST appropriate action?",
            "options": [
                {"label": "A", "text": "Continue unauthorized surveillance based on your hunch"},
                {"label": "B", "text": "Document your suspicions and present them to your supervisor for review"},
                {"label": "C", "text": "Request a formal surveillance operation through the chain of command"},
                {"label": "D", "text": "Conduct open-source research to develop your suspicions before requesting authorization"}
            ],
            "correct_answer": "A",
            "explanation": "Conducting unauthorized surveillance operations — even during personal time — without supervisory approval violates departmental policy and could expose the department to civil liability. All surveillance activities must be coordinated through the chain of command to ensure legal compliance, proper resource allocation, and officer safety.",
            "io_scores": {"A": 2, "B": -2, "C": -2, "D": -1},
            "difficulty": "medium",
            "reference": "CPD Special Order S09-05; Surveillance Operations; Supervisory Authorization"
        },
    ]

    # ================================================================
    # SECTION 3: RANKING — 20 NEW QUESTIONS
    # ================================================================
    ranking_questions = [
        {
            "title": "Carjacking with GPS Tracking — Pursuit Priority",
            "content": "A victim reports their vehicle was just carjacked at gunpoint. The victim has a GPS tracker on the vehicle and can see it moving westbound. Two suspects are armed. Beat officers are nearby. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Broadcast a flash message with the vehicle description, direction of travel, and suspect descriptions"},
                {"label": "B", "text": "Ensure the victim is safe and request medical attention if needed"},
                {"label": "C", "text": "Coordinate with OEMC to track the GPS signal and direct responding units"},
                {"label": "D", "text": "Obtain a detailed description of the weapons used from the victim"},
                {"label": "E", "text": "Canvas the area for surveillance cameras and witnesses"},
                {"label": "F", "text": "Complete the case report and vehicle theft documentation"}
            ],
            "correct_order": [1, 0, 2, 3, 4, 5],
            "explanation": "Victim safety (B) is always the first priority. Broadcasting (A) the flash message is critical while the vehicle is still moving and suspects can be apprehended. Coordinating GPS tracking (C) provides tactical advantage. Obtaining weapon descriptions (D) helps responding officers understand the threat level. Canvassing for evidence (E) follows. Documentation (F) is the final step.",
            "difficulty": "hard",
            "reference": "CPD General Order G06-01-01; Carjacking Response Protocol"
        },
        {
            "title": "Home Invasion with Hostage — Tactical Response",
            "content": "Dispatch reports a home invasion in progress with at least one hostage. Screaming can be heard in the background of the 911 call. You are the first detective notified. Patrol units are 3 minutes away. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Establish a perimeter and contain the scene"},
                {"label": "B", "text": "Request SWAT/HBT activation through the chain of command"},
                {"label": "C", "text": "Ensure responding patrol units have suspect information and scene details"},
                {"label": "D", "text": "Attempt to establish phone contact with the hostage or suspects"},
                {"label": "E", "text": "Gather intelligence on the location layout from neighbors or property records"},
                {"label": "F", "text": "Begin interviewing any escaped occupants for suspect details"}
            ],
            "correct_order": [2, 0, 1, 3, 5, 4],
            "explanation": "Ensuring responding officers have critical information (C) is first since they arrive before you. Establishing a perimeter (A) to contain the scene protects the public and prevents escape. Requesting SWAT (B) for a hostage situation is essential. Establishing communication (D) may de-escalate. Interviewing escaped occupants (F) provides immediate intelligence. Gathering location intel (E) supports tactical planning.",
            "difficulty": "hard",
            "reference": "CPD Special Order S04-20; Hostage/Barricade Situations"
        },
        {
            "title": "Officer Down — Emergency Response",
            "content": "You hear a radio transmission that an officer has been shot during a foot pursuit in your district. The suspect fled with the officer's weapon. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Respond to the officer's location to render aid and secure the scene"},
                {"label": "B", "text": "Broadcast an emergency message with the suspect description and that the suspect is armed with a police weapon"},
                {"label": "C", "text": "Ensure EMS is en route and establish a trauma corridor"},
                {"label": "D", "text": "Establish a perimeter and coordinate the search for the armed suspect"},
                {"label": "E", "text": "Notify the Watch Commander and request additional resources"},
                {"label": "F", "text": "Preserve the shooting scene and document the officer's position and condition"}
            ],
            "correct_order": [0, 1, 2, 4, 3, 5],
            "explanation": "Rendering aid to the officer (A) is the top priority — life safety comes first. Broadcasting the suspect information (B) immediately — especially that the suspect has a police weapon — is critical for officer safety across the district. Ensuring EMS response (C) follows. Notifying command (E) brings additional resources. Establishing a perimeter (D) to search for the suspect. Scene preservation (F) comes last.",
            "difficulty": "hard",
            "reference": "CPD General Order G03-06; Officer-Involved Shooting; G06-01-01"
        },
        {
            "title": "Bank Robbery Just Occurred — Investigation Sequence",
            "content": "You are called to a bank robbery that occurred 10 minutes ago. The suspects fled in a vehicle. Dye pack has detonated. Several employees and customers are inside, some are visibly upset. The bank manager has surveillance footage available. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Secure the scene and ensure all persons inside are safe"},
                {"label": "B", "text": "Obtain suspect descriptions and broadcast a flash message"},
                {"label": "C", "text": "Separate witnesses to prevent cross-contamination of accounts"},
                {"label": "D", "text": "Obtain and preserve the surveillance footage"},
                {"label": "E", "text": "Interview the teller(s) who were directly confronted by the suspects"},
                {"label": "F", "text": "Request the FBI respond to the scene per federal bank robbery jurisdiction"}
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": "Scene safety (A) is always first. Broadcasting suspect descriptions (B) while fresh aids apprehension. Separating witnesses (C) before they discuss what happened preserves account integrity. Preserving surveillance footage (D) before it could be overwritten is time-sensitive. Interviewing primary witnesses (E) provides detailed suspect information. FBI notification (F) is required but not the most urgent action.",
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Bank Robbery Response; 18 U.S.C. § 2113"
        },
        {
            "title": "Child Abduction Alert — Response Priority",
            "content": "A parent reports their 6-year-old was grabbed by an unknown person in a van outside their school 15 minutes ago. The parent has a partial plate number and saw the van heading north. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Initiate an AMBER Alert through proper channels with all available information"},
                {"label": "B", "text": "Broadcast an emergency flash message with the van description and partial plate"},
                {"label": "C", "text": "Request OEMC pull all POD camera footage from the area"},
                {"label": "D", "text": "Interview the parent for a detailed description of the child, suspect, and van"},
                {"label": "E", "text": "Canvass the school for additional witnesses including staff and students"},
                {"label": "F", "text": "Coordinate with the school to confirm the child is not inside the building"}
            ],
            "correct_order": [1, 5, 3, 0, 2, 4],
            "explanation": "An immediate broadcast (B) is essential with every passing minute. Confirming the child is actually missing (F) prevents a resource-intensive response if the child is safe inside. Getting detailed descriptions from the parent (D) supports the investigation. Initiating the AMBER Alert (A) with verified information follows. POD camera footage (C) may show the vehicle route. School canvassing (E) is important but can be delegated.",
            "difficulty": "hard",
            "reference": "CPD Special Order S06-02; Missing/Abducted Children; AMBER Alert Protocol"
        },
        {
            "title": "Multi-Victim Shooting at Public Event — Triage",
            "content": "A shooting occurs at a large outdoor festival with multiple victims. You arrive as the first detective on scene. Patrol has established a loose perimeter. At least 5 people are down with gunshot wounds. The crowd is panicking. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Coordinate with patrol to establish a secure perimeter and identify the threat status"},
                {"label": "B", "text": "Ensure CFD/EMS staging and triage for the injured"},
                {"label": "C", "text": "Identify and separate witnesses from the crowd before they disperse"},
                {"label": "D", "text": "Begin collecting shell casings and physical evidence"},
                {"label": "E", "text": "Request additional detective and evidence technician resources"},
                {"label": "F", "text": "Establish a command post and coordinate with the incident commander"}
            ],
            "correct_order": [0, 1, 5, 4, 2, 3],
            "explanation": "Confirming the threat status and securing the perimeter (A) ensures no ongoing danger. EMS triage (B) for the injured follows immediately. Establishing a command post (F) brings order to a chaotic scene. Requesting additional resources (E) is critical given the scale. Separating witnesses (C) before they leave preserves testimony. Physical evidence collection (D) comes after scene security and life safety are addressed.",
            "difficulty": "hard",
            "reference": "CPD Special Order S04-20; Mass Casualty Incident Response"
        },
        {
            "title": "Cold Case DNA Hit — Investigation Restart",
            "content": "You receive a CODIS DNA hit linking a convicted felon to an unsolved 2015 sexual assault. The original detective has retired. The case file is in storage. The statute of limitations has not expired. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Locate and review the complete original case file"},
                {"label": "B", "text": "Verify the CODIS hit through an independent DNA confirmation"},
                {"label": "C", "text": "Locate and contact the victim to inform them of the development"},
                {"label": "D", "text": "Determine the suspect's current location and criminal history"},
                {"label": "E", "text": "Consult with the ASA on charging and warrant options"},
                {"label": "F", "text": "Contact the original detective for case background and notes"}
            ],
            "correct_order": [0, 1, 3, 5, 4, 2],
            "explanation": "Reviewing the case file (A) provides essential context before any action. Verifying the DNA hit (B) confirms the match is valid. Locating the suspect (D) determines if arrest is feasible. Contacting the original detective (F) provides institutional knowledge. Consulting the ASA (E) ensures proper legal approach. Victim notification (C) comes last — you need confirmed information before re-contacting a victim.",
            "difficulty": "hard",
            "reference": "CPD Special Order S06-05; Cold Case Investigations; CODIS Protocol"
        },
        {
            "title": "Suspicious Package at Government Building — Response",
            "content": "Security at a government office building reports a suspicious package left in the lobby. The package is unattended, has no return address, and appears to have wires protruding. The building has approximately 200 occupants. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Order immediate evacuation of the building"},
                {"label": "B", "text": "Establish a perimeter at a safe distance (minimum 300 feet)"},
                {"label": "C", "text": "Request the Bomb Squad and notify OEMC"},
                {"label": "D", "text": "Prevent anyone from approaching or touching the package"},
                {"label": "E", "text": "Review security camera footage to identify who left the package"},
                {"label": "F", "text": "Interview building security about when the package appeared and any suspicious persons"}
            ],
            "correct_order": [3, 0, 1, 2, 5, 4],
            "explanation": "Preventing approach to the package (D) stops the immediate risk. Evacuation (A) protects all building occupants. Establishing a perimeter (B) at a safe distance protects responders and public. Requesting the Bomb Squad (C) brings the appropriate specialized response. Interviewing security (F) may provide time-sensitive suspect information. Camera review (E) is important but can happen during the response.",
            "difficulty": "hard",
            "reference": "CPD Special Order S04-07; Suspicious Package/Bomb Threat Response"
        },
        {
            "title": "Fatal Hit-and-Run with Witness — Investigation Steps",
            "content": "You respond to a fatal hit-and-run. A pedestrian is deceased in the roadway. One witness saw the vehicle and obtained a partial plate. Debris from the vehicle is scattered at the scene. Traffic is backing up. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Secure the scene and establish traffic control around the area"},
                {"label": "B", "text": "Broadcast the vehicle description and partial plate to all units"},
                {"label": "C", "text": "Preserve and photograph all physical evidence including vehicle debris and victim position"},
                {"label": "D", "text": "Interview the witness who obtained the partial plate"},
                {"label": "E", "text": "Request the Major Accident Investigation Section respond"},
                {"label": "F", "text": "Canvas for additional witnesses and surveillance cameras"}
            ],
            "correct_order": [0, 1, 4, 3, 2, 5],
            "explanation": "Scene safety and traffic control (A) prevents additional injuries. Broadcasting the vehicle information (B) while fresh aids apprehension. Requesting MAIS (E) ensures proper investigation of a fatal crash. Interviewing the key witness (D) captures perishable information. Preserving physical evidence (C) documents the scene. Canvassing (F) for additional evidence follows.",
            "difficulty": "medium",
            "reference": "CPD Special Order S04-04; Traffic Crash Investigations; Fatal/Serious Injury"
        },
        {
            "title": "Domestic Violence Strangulation — Medical Priority",
            "content": "You respond to a domestic violence call. The victim reports being strangled by her partner, who has fled. The victim appears to be breathing normally but has red marks on her neck. She insists she is fine and does not want medical attention. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Strongly encourage and arrange medical evaluation — strangulation injuries can be delayed and fatal"},
                {"label": "B", "text": "Photograph the victim's neck injuries and document her statements"},
                {"label": "C", "text": "Broadcast a flash message with the offender's description and direction of flight"},
                {"label": "D", "text": "Complete the domestic violence report and check for Orders of Protection"},
                {"label": "E", "text": "Provide the victim with domestic violence resource information"},
                {"label": "F", "text": "Request an evidence technician to document the scene and injuries"}
            ],
            "correct_order": [0, 2, 1, 5, 3, 4],
            "explanation": "Medical evaluation (A) is the top priority — strangulation victims can die hours later from delayed swelling, and injuries may not be immediately apparent. Broadcasting (C) the offender description supports apprehension. Photographing injuries (B) before marks fade preserves evidence. Evidence technician documentation (F) creates an official record. Completing reports (D) and providing resources (E) follow.",
            "difficulty": "hard",
            "reference": "CPD Special Order S06-04; Domestic Violence; 720 ILCS 5/12-3.05 Aggravated DV"
        },
        {
            "title": "Recovered Stolen Vehicle with Evidence — Processing",
            "content": "Patrol locates a stolen vehicle used in an armed robbery series. The vehicle is unoccupied in a parking lot. You can see what appears to be a ski mask and gloves on the passenger seat through the window. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Secure the vehicle and establish a perimeter to prevent contamination"},
                {"label": "B", "text": "Obtain a search warrant for the vehicle"},
                {"label": "C", "text": "Request evidence technicians for processing"},
                {"label": "D", "text": "Run the VIN to confirm the vehicle identity and check for additional wants"},
                {"label": "E", "text": "Canvas the parking lot for surveillance cameras"},
                {"label": "F", "text": "Notify the robbery detectives handling the pattern"}
            ],
            "correct_order": [0, 3, 1, 2, 5, 4],
            "explanation": "Securing the vehicle (A) prevents evidence loss or contamination. Confirming the VIN (D) verifies it is the stolen vehicle and checks for additional connections. Obtaining a search warrant (B) provides legal authority for a thorough search beyond plain view. Requesting ET (C) ensures proper forensic processing. Notifying pattern detectives (F) coordinates the broader investigation. Camera canvassing (E) supports identifying who parked it.",
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-02; Vehicle Processing; Search Warrant Requirements"
        },
        {
            "title": "Witness Protection Concern — Intimidation Report",
            "content": "A key grand jury witness in a gang murder case reports that unknown persons have been following her and leaving threatening notes at her home. She is terrified and considering recanting her testimony. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Assess the immediate threat level and ensure the witness's current safety"},
                {"label": "B", "text": "Notify the assigned ASA about the witness intimidation"},
                {"label": "C", "text": "Document the threatening notes as evidence and investigate their origin"},
                {"label": "D", "text": "Arrange for temporary protective measures (safe house, increased patrol)"},
                {"label": "E", "text": "File witness intimidation charges and request a court order of protection"},
                {"label": "F", "text": "Coordinate with the State's Attorney's Witness Protection Unit"}
            ],
            "correct_order": [0, 3, 1, 5, 2, 4],
            "explanation": "Assessing the threat and ensuring immediate safety (A) is paramount. Arranging protective measures (D) provides ongoing security. Notifying the ASA (B) is essential for the pending case. Coordinating with Witness Protection (F) provides professional support. Documenting the threats (C) builds the intimidation case. Filing charges (E) provides legal consequences for the intimidation.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/32-4a; Witness Intimidation; CPD Special Order S06-07"
        },
        {
            "title": "Narcotics Overdose at Residence — Scene Management",
            "content": "You respond to assist patrol at a narcotics overdose death. The victim is deceased. Narcotics paraphernalia is visible throughout the residence. Two other occupants are present and appear to be under the influence. One occupant states they called 911. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Request EMS evaluation for the two living occupants who appear impaired"},
                {"label": "B", "text": "Secure the scene and preserve evidence of the narcotics and paraphernalia"},
                {"label": "C", "text": "Determine if the 911 caller qualifies for immunity under the Drug-Induced Homicide Good Samaritan provision"},
                {"label": "D", "text": "Interview the occupants about the source of the narcotics and timeline of events"},
                {"label": "E", "text": "Request evidence technicians for scene processing and death investigation"},
                {"label": "F", "text": "Notify the medical examiner and your supervisor of the death"}
            ],
            "correct_order": [0, 1, 5, 2, 4, 3],
            "explanation": "Medical evaluation of the living occupants (A) is the top life-safety priority — they may also be at risk of overdose. Scene preservation (B) protects evidence. Notifying the ME and supervisor (F) initiates the death investigation process. Checking Good Samaritan immunity (C) affects how you interact with the 911 caller. Requesting ET (E) for proper processing. Detailed interviews (D) can occur after immediate priorities are addressed.",
            "difficulty": "hard",
            "reference": "720 ILCS 570/414; Good Samaritan Overdose Act; CPD Death Investigation Procedures"
        },
        {
            "title": "Fleeing Suspect Enters Third-Party Residence — Pursuit Decision",
            "content": "During a foot pursuit of an armed robbery suspect, the suspect runs into an occupied apartment through an unlocked door. You can hear screaming from inside. Other officers are arriving. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Immediately enter the apartment to protect the occupants under exigent circumstances"},
                {"label": "B", "text": "Establish containment around the building and cover all exits"},
                {"label": "C", "text": "Broadcast the suspect's location and request SWAT/tactical support"},
                {"label": "D", "text": "Attempt verbal communication with the suspect and occupants"},
                {"label": "E", "text": "Evacuate adjacent apartments for civilian safety"},
                {"label": "F", "text": "Obtain identifying information about the apartment occupants from neighbors"}
            ],
            "correct_order": [0, 1, 2, 3, 4, 5],
            "explanation": "Exigent circumstances — an armed suspect entering an occupied dwelling with screaming heard — justifies immediate entry (A) to protect innocent occupants from imminent harm. Establishing containment (B) prevents escape if the suspect attempts to flee. Broadcasting location (C) brings resources. Verbal communication (D) may de-escalate. Evacuating adjacent units (E) protects neighbors. Identifying occupants (F) assists tactical planning.",
            "difficulty": "hard",
            "reference": "Brigham City v. Stuart; Exigent Circumstances; CPD Use of Force Policy"
        },
        {
            "title": "Identity Theft Ring — Complex Investigation Steps",
            "content": "Financial crimes unit receives reports from 15 victims across 3 districts whose identities were stolen and used to open fraudulent accounts. A common thread is they all used the same medical clinic. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Interview victims to identify common patterns and the timeline of identity theft"},
                {"label": "B", "text": "Serve a subpoena on the medical clinic for employee records and access logs"},
                {"label": "C", "text": "Coordinate with financial institutions to identify the fraudulent accounts and money flow"},
                {"label": "D", "text": "Check if any clinic employees have criminal histories for fraud or identity theft"},
                {"label": "E", "text": "Obtain and analyze the victims' financial records with their consent"},
                {"label": "F", "text": "Brief the State's Attorney on the scope of the investigation for charging guidance"}
            ],
            "correct_order": [0, 4, 2, 3, 1, 5],
            "explanation": "Victim interviews (A) establish the scope, timeline, and common factors. Obtaining financial records with consent (E) maps the fraud. Coordinating with financial institutions (C) traces the money. Checking employee histories (D) identifies likely suspects. Serving the subpoena (B) requires some investigative foundation. ASA briefing (F) comes when you have sufficient evidence for charging decisions.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/16-30; Identity Theft; CPD Financial Crimes Investigation"
        },
        {
            "title": "Arson at Occupied Building — Initial Response",
            "content": "You respond to an occupied apartment building fire where arson is suspected. CFD is on scene fighting the fire. Several residents are displaced. One resident claims to have seen someone pouring liquid around the building before the fire started. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Ensure all occupants are accounted for and receiving assistance"},
                {"label": "B", "text": "Interview the witness who saw the suspicious person immediately"},
                {"label": "C", "text": "Coordinate with CFD arson investigators on the origin and cause investigation"},
                {"label": "D", "text": "Broadcast suspect description based on the witness's account"},
                {"label": "E", "text": "Preserve the exterior areas where the liquid was reportedly poured"},
                {"label": "F", "text": "Canvas the area for surveillance cameras and additional witnesses"}
            ],
            "correct_order": [0, 1, 3, 4, 2, 5],
            "explanation": "Accounting for all occupants (A) is the life-safety priority. Interviewing the eyewitness (B) immediately captures perishable information. Broadcasting the suspect description (D) aids in apprehension while the suspect may still be nearby. Preserving the exterior evidence (E) before it is destroyed by fire operations. Coordinating with CFD arson (C) aligns the investigation. Canvassing (F) expands the evidence base.",
            "difficulty": "hard",
            "reference": "CPD Special Order S04-12; Arson Investigation; CFD/CPD Coordination"
        },
        {
            "title": "Police Impersonator Traffic Stops — Pattern Response",
            "content": "Three victims in one week report being pulled over by someone impersonating a police officer using a vehicle with flashing lights. In each case, the impersonator demanded cash. The incidents occurred in the same general area. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Issue a community alert warning residents about the police impersonator"},
                {"label": "B", "text": "Analyze the three incidents for common patterns in time, location, and suspect description"},
                {"label": "C", "text": "Coordinate surveillance of the target area during the identified pattern times"},
                {"label": "D", "text": "Check for similar reports in adjacent districts and through CLEAR"},
                {"label": "E", "text": "Interview all three victims together to develop a composite description"},
                {"label": "F", "text": "Request traffic camera and POD footage from the incident areas and times"}
            ],
            "correct_order": [1, 3, 5, 0, 2, 4],
            "explanation": "Pattern analysis (B) identifies the common thread. Checking for additional reports (D) may reveal more victims. Obtaining camera footage (F) may capture the suspect vehicle. Community alert (A) warns potential victims. Coordinating surveillance (C) may catch the suspect in action. Interviewing victims together (E) should be avoided — individual interviews prevent cross-contamination.",
            "difficulty": "medium",
            "reference": "720 ILCS 5/32-5.1; Police Impersonation; CPD Pattern Investigation"
        },
        {
            "title": "Evidence Room Discrepancy — Accountability",
            "content": "During a routine audit, you discover that a piece of evidence — a firearm from a pending murder case — is missing from the evidence room. The evidence log shows it was last signed out by a now-retired detective. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Notify your supervisor and the evidence custodian immediately"},
                {"label": "B", "text": "Review the complete chain of custody log for the missing firearm"},
                {"label": "C", "text": "Contact the retired detective to determine the firearm's location"},
                {"label": "D", "text": "Notify the ASA handling the murder case about the evidence issue"},
                {"label": "E", "text": "Conduct a thorough search of the evidence room for misfiled items"},
                {"label": "F", "text": "Generate an official incident report documenting the discrepancy"}
            ],
            "correct_order": [0, 5, 1, 4, 2, 3],
            "explanation": "Immediate supervisor notification (A) initiates the proper response chain. Creating an official incident report (F) documents the discovery. Reviewing the chain of custody (B) traces the firearm's movement. Searching for misfiled evidence (E) may resolve the discrepancy. Contacting the retired detective (C) may locate the item. Notifying the ASA (D) is essential but can occur after initial investigation establishes the scope of the problem.",
            "difficulty": "hard",
            "reference": "CPD Special Order S06-04; Evidence Management; Chain of Custody"
        },
        {
            "title": "Cyberstalking Victim — Digital Safety Priority",
            "content": "A victim reports being cyberstalked by an ex-partner who has been tracking her location, accessing her email, and sending threatening messages. She has brought screenshots of the threats. She believes he installed spyware on her phone. Rank the following actions in the correct priority order.",
            "items": [
                {"label": "A", "text": "Advise the victim to immediately change all passwords and secure her accounts"},
                {"label": "B", "text": "Preserve the screenshots and digital evidence she has brought"},
                {"label": "C", "text": "Have the victim's phone examined for spyware by the digital forensics unit"},
                {"label": "D", "text": "Develop a safety plan with the victim including an Order of Protection"},
                {"label": "E", "text": "Obtain an emergency Order of Protection based on the threatening messages"},
                {"label": "F", "text": "Serve a preservation letter on the relevant email and social media platforms"}
            ],
            "correct_order": [1, 3, 0, 2, 4, 5],
            "explanation": "Preserving the evidence she brought (B) is critical before anything changes. Developing a safety plan (D) addresses her immediate danger. Advising on account security (A) stops ongoing unauthorized access. Forensic phone examination (C) may reveal the spyware and provide evidence. An Order of Protection (E) provides legal protection. Platform preservation letters (F) ensure digital evidence is retained.",
            "difficulty": "hard",
            "reference": "720 ILCS 5/12-7.5; Cyberstalking; CPD Special Order S06-06; Digital Evidence"
        },
    ]

    # ================================================================
    # INSERT ALL NEW QUESTIONS
    # ================================================================
    total_inserted = 0

    for q_data in most_appropriate:
        q = {
            "question_id": f"mexam2_{uuid.uuid4().hex[:12]}",
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
        if result.upserted_id:
            total_inserted += 1

    for q_data in least_appropriate:
        q = {
            "question_id": f"lexam2_{uuid.uuid4().hex[:12]}",
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
        if result.upserted_id:
            total_inserted += 1

    for q_data in ranking_questions:
        q = {
            "question_id": f"rank2_{uuid.uuid4().hex[:12]}",
            "type": "ranking",
            "category_id": "cat_ranking",
            "category_name": "Ranking Questions",
            "title": q_data["title"],
            "content": q_data["content"],
            "items": q_data["items"],
            "correct_order": q_data["correct_order"],
            "explanation": q_data["explanation"],
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
        if result.upserted_id:
            total_inserted += 1

    print(f"Additional exam questions seeded: {total_inserted} new")
    return total_inserted


if __name__ == "__main__":
    asyncio.run(seed_additional_exam_questions())
