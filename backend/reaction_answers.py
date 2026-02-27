"""
REACTION_ANSWERS - Extracted from seed_comprehensive.py (12 scenarios) and
seed_practice_content.py (5 gold scenarios).

Each key is the exact scenario title. Each value is {"modelAnswer": {<REACTION dict>}}.
"""

REACTION_ANSWERS = {
    # =========================================================================
    # seed_comprehensive.py  (12 scenarios)
    # =========================================================================

    "Armed Robbery Investigation": {
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
    },

    "Domestic Violence Death Investigation": {
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
    },

    "Residential Burglary Pattern": {
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
    },

    "Sexual Assault Investigation": {
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
    },

    "Search and Seizure Challenge": {
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
    },

    "Gang-Related Shooting Investigation": {
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
    },

    "Child Abuse Investigation": {
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
    },

    "Miranda and Confession Issues": {
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
    },

    "Officer-Involved Shooting Investigation": {
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
    },

    "Traffic Stop Drug Investigation": {
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
    },

    "Digital Evidence and Social Media": {
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
    },

    "Missing Person Investigation": {
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
    },

    # =========================================================================
    # seed_practice_content.py  (5 gold scenarios)
    # =========================================================================

    "The Witness Identification": {
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
    },

    "The Photo Lineup": {
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
    },

    "The Domestic Violence Call": {
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
    },

    "The School Threat Investigation": {
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
    },

    "The Live Lineup Challenge": {
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
    },
}
