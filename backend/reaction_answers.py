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
                "Secure crime scene, establish perimeter",
                "Ensure victim receives any needed medical attention",
                "Issue flash message with suspect and vehicle description",
                "Request K-9 track if suspect fled on foot recently"
            ],
            "E": [
                "Secure crime scene, establish perimeter around convenience store",
                "Check for similar pattern robberies in area"
            ],
            "C": [
                "Obtain detailed statement from clerk while memory fresh",
                "Canvas for additional witnesses in parking lot and nearby businesses"
            ],
            "T": [
                "Photograph scene from multiple angles",
                "Document victim's injuries or distress",
                "Complete comprehensive case report",
                "Update crime analysis with pattern information"
            ],
            "I": [
                "Obtain all surveillance video (store and nearby businesses)",
                "Process counter/register area for fingerprints",
                "Preserve register for potential DNA evidence",
                "Collect any physical evidence left by suspect",
                "Check for NIBIN hits if weapon later recovered",
                "Review license plate readers in area"
            ],
            "O": [
                "Coordinate with ASA on charges when appropriate",
                "Prepare photo array if suspect identified"
            ],
            "N": [
                "Analyze video with tech unit for suspect/vehicle details",
                "Enter suspect description in robbery pattern database",
                "Check pawn databases for any activity",
                "Review recent robbery arrests for similar MO",
                "Contact confidential informants",
                "Issue BOLO for vehicle description",
                "Monitor social media for suspect activity",
                "Coordinate with robbery unit on known offenders"
            ]
        }
    },

    "Domestic Violence Death Investigation": {
        "modelAnswer": {
            "R": [
                "Secure scene as homicide until determined otherwise",
                "Request homicide detectives and crime scene unit",
                "Notify Medical Examiner immediately",
                "Do NOT move body without ME approval"
            ],
            "E": [
                "Separate husband from scene - do NOT let him contaminate evidence",
                "Begin crime scene log - document all persons present",
                "Identify and separate all potential witnesses"
            ],
            "A": [
                "Husband is not free to leave - invoke investigative detention",
                "Obtain his voluntary statement before advising Miranda if non-custodial",
                "If probable cause develops, arrest and then Miranda",
                "Timeline his whereabouts - verify alibi"
            ],
            "C": [
                "Interview neighbors who heard argument",
                "Interview family, friends about relationship history",
                "Pull all prior domestic calls to address",
                "Check for protective orders or pending divorce",
                "Review social media accounts"
            ],
            "T": [
                "Extensive photography of victim and entire scene",
                "Document position of body, any disturbance",
                "Document his clothing, injuries (photograph scratches)",
                "Document signs of struggle",
                "Photograph dog, document any dog injuries",
                "Document everything for domestic violence prosecution protocol"
            ],
            "I": [
                "Collect potential murder weapon(s)",
                "Swab blood evidence, document spatter patterns",
                "Process for fingerprints throughout",
                "Collect victim's fingernail scrapings for DNA",
                "Collect husband's clothing and swab scratches for victim DNA",
                "Obtain DNA/fingernail scrapings with warrant or consent",
                "Check hands for defensive injuries",
                "Seize all electronic devices (cell phones, computers) - warrant required",
                "Request expedited DNA analysis"
            ],
            "O": [
                "Collect clothing as evidence (get search warrant if necessary)",
                "Subpoena phone records for both parties",
                "Coordinate with State's Attorney on charging",
                "Work with ME on autopsy findings"
            ],
            "N": [
                "Check for life insurance policies",
                "Investigate financial situation",
                "Review social media accounts for relationship history"
            ]
        }
    },

    "Residential Burglary Pattern": {
        "modelAnswer": {
            "R": [
                "Create detailed matrix of all six burglaries",
                "Map locations - identify geographic cluster",
                "Timeline analysis - day of week, time patterns",
                "Identify why these homes were selected (vacant, routine)"
            ],
            "E": [
                "Analyze exact entry methods, tools used",
                "Compare items taken - specific preferences",
                "Review MO details for unique signatures",
                "Check for any forensic evidence connections"
            ],
            "C": [
                "Canvas all six neighborhoods for van sightings",
                "Alert informants about pattern and tattoo description",
                "Check probation/parole records for residential burglars",
                "Query CLEAR for tattoo description",
                "Review recent burglary arrests in surrounding districts"
            ],
            "T": [
                "Review surveillance footage from all scenes",
                "Check traffic cameras for white work vans in area during burglary times",
                "Review license plate readers for patterns",
                "Create comprehensive photo array when suspect identified"
            ],
            "I": [
                "Ensure all fingerprints from six scenes processed for comparison",
                "Check for tool mark matches between scenes",
                "Any DNA evidence cross-referenced",
                "Check pawn shops for stolen items",
                "Search databases for burglars with similar MO"
            ],
            "N": [
                "Identify potential target area based on pattern",
                "Request plainclothes surveillance during peak hours",
                "Coordinate with district tactical teams",
                "Alert patrol to watch for white vans in residential areas",
                "Consider bait house operation if approved",
                "Alert neighborhood watch groups",
                "Issue community notification via social media",
                "Provide prevention tips (lock windows, timers for lights)",
                "Request increased patrol visibility during peak hours"
            ]
        }
    },

    "Sexual Assault Investigation": {
        "modelAnswer": {
            "R": [
                "Express belief and empathy - no judgment",
                "Explain that showering doesn't eliminate all evidence",
                "Explain she has options - evidence collection doesn't require prosecution decision",
                "Connect with victim advocate immediately",
                "Let her make informed choices, respect autonomy",
                "Provide written information on resources/rights",
                "Reassure that intoxication does not equal consent"
            ],
            "E": [
                "Identify party location and attendees",
                "Identify whose house/room she woke in",
                "Check for surveillance cameras near party location"
            ],
            "A": [
                "Approach suspect without revealing full case",
                "Establish timeline and opportunity",
                "Let him describe events before revealing details",
                "Document any admissions about her intoxication",
                "If interview reveals probable cause, arrest and Miranda"
            ],
            "C": [
                "Locate Derek - check with party host, social media",
                "Canvas for witnesses who saw them together",
                "Interview witnesses about victim's level of intoxication",
                "Interview suspect - document any admissions about intoxication level",
                "Obtain her detailed statement when ready"
            ],
            "T": [
                "Photograph any visible injuries",
                "Document her emotional state and demeanor",
                "Document evidence of inability to consent due to intoxication",
                "Document her wishes regarding prosecution"
            ],
            "I": [
                "SANE exam - still valuable even after shower",
                "DNA may persist in body cavities up to 5-7 days",
                "Document any injuries, even minor",
                "Toxicology for drug-facilitated assault",
                "Collect clothing worn to party (even if different from now)",
                "Obtain video/photos from party (phones, social media)",
                "Secure any digital communications",
                "Medical evidence of assault",
                "Determine if drugs may have been used (toxicology)"
            ],
            "O": [
                "Witness statements about victim's condition",
                "Any statements by suspect about victim's state",
                "Coordinate with SVU and victim services"
            ],
            "N": [
                "Keep victim informed of investigation progress",
                "Let her set pace when possible",
                "Prepare her for what to expect in process",
                "Provide safety planning if suspect may have contact"
            ]
        }
    },

    "Search and Seizure Challenge": {
        "modelAnswer": {
            "R": [
                "The warrantless entry into a home is presumptively unconstitutional - exceptions must apply",
                "Shots fired call provides reason to investigate, but you arrived at scene and didn't observe active shooting",
                "Yelling heard suggests disturbance but not necessarily emergency",
                "Cannabis smell - in Illinois post-legalization, cannabis odor alone is NOT an exigent circumstance",
                "Gun in plain view alone (without threat) does not create emergency",
                "Subject at door - no one in apparent danger"
            ],
            "E": [
                "For entry to be valid, need probable cause plus exigency",
                "Hot pursuit exception not applicable - suspect at door, not fleeing",
                "Emergency aid exception not applicable - no one in apparent distress",
                "Imminent evidence destruction weak - subject wasn't destroying anything",
                "Prevent escape not applicable - subject was conversing at door"
            ],
            "A": [
                "The home receives highest Fourth Amendment protection",
                "Warrantless entry requires articulated exigent circumstances",
                "You can secure the scene and station officer at door to prevent evidence destruction"
            ],
            "T": [
                "Document specific facts showing imminent danger if claiming exigency",
                "Document why entry was immediately necessary",
                "Document what threat existed to persons",
                "Document why waiting for warrant was not feasible"
            ],
            "I": [
                "Gun on coffee table - seized during unlawful entry, likely suppressed",
                "Cocaine in kitchen - fruit of unlawful entry, likely suppressed",
                "Ammunition in closet - exceeded any protective sweep authority, likely suppressed",
                "All evidence likely suppressed under exclusionary rule"
            ],
            "O": [
                "Secure scene and call supervisor and ASA",
                "Apply for search warrant based on observations: shots fired call, yelling heard, gun in plain view",
                "Execute warrant once obtained - all evidence then admissible",
                "When time permits, ALWAYS get a warrant for home entry"
            ],
            "N": [
                "All evidence likely suppressed leading to case dismissal",
                "Potential civil rights lawsuit",
                "Violation of CPD policy",
                "COPA review likely",
                "Lesson: 'I saw contraband' is not an emergency - secure scene and seek judicial authorization"
            ]
        }
    },

    "Gang-Related Shooting Investigation": {
        "modelAnswer": {
            "R": [
                "Establish expanded perimeter - evidence likely spread",
                "Request crime scene unit and additional detectives",
                "Medical examiner notification for DOA",
                "Assign officers to hospitals with surviving victims",
                "Request ShotSpotter data for exact shot timing/locations"
            ],
            "E": [
                "Document all persons in area before they leave",
                "Canvass for surveillance cameras (business, residential, city)",
                "Document gang graffiti and territorial markers",
                "Recover all shell casings with proper documentation"
            ],
            "C": [
                "Understand reluctance is fear-based, not hostile",
                "Separate potential witnesses for individual contact",
                "Provide business cards - may cooperate later",
                "Look for witnesses from windows, parked cars",
                "Identify anonymous caller who reported shots",
                "Check if anyone sought medical attention who left scene",
                "Use Crime Stoppers for anonymous tips",
                "Hospital bedside interviews when medically cleared",
                "Have victim advocate present",
                "Explain safety resources available",
                "Offer to relocate family if cooperation given",
                "Non-fatal victims may become cooperative later",
                "Document any spontaneous statements to medical staff"
            ],
            "T": [
                "Comprehensive evidence preservation",
                "Document all tips regardless of source",
                "Create timeline with all evidence",
                "Maintain informant confidentiality",
                "Preserve the anonymous video immediately (screenshot, screen record)"
            ],
            "I": [
                "Match shell casings to prior shooting cases (NIBIN)",
                "Compare bullets recovered from victims",
                "Check if vehicle identified through surveillance",
                "Process scene for DNA, fingerprints despite low probability",
                "Analyze ShotSpotter for number of shooters",
                "Issue preservation letter to social media platform",
                "Work with tech unit to identify account owner",
                "Search for additional posts about incident",
                "Monitor gang members' social media for admissions",
                "Look for rival gang taunting or claiming credit"
            ],
            "O": [
                "Coordinate with gang intelligence unit",
                "Identify which gangs claim this territory",
                "Check for recent gang conflicts or retaliations",
                "Review recent arrests of gang members",
                "Identify any ongoing feuds",
                "Check for social media beefs between groups",
                "Consider federal prosecution for gang conspiracy",
                "Coordinate with U.S. Attorney if appropriate"
            ],
            "N": [
                "This investigation may take months",
                "Cultivate confidential informants",
                "Monitor for retaliation incidents",
                "Build case through circumstantial evidence"
            ]
        }
    },

    "Child Abuse Investigation": {
        "modelAnswer": {
            "R": [
                "Contact DCFS investigator - coordinate, don't duplicate",
                "Determine if child is in immediate danger",
                "If danger present, protective custody may be needed",
                "Establish information sharing protocol with DCFS",
                "Joint investigation preferred when possible"
            ],
            "E": [
                "Document home conditions",
                "Document sleeping arrangements",
                "Note cleanliness, food availability"
            ],
            "A": [
                "Non-custodial interview preferred initially",
                "Let suspect explain injuries before revealing evidence",
                "Document inconsistencies in explanations",
                "Be aware of who has access to child",
                "Determine primary caregiver",
                "If probable cause, arrest and continue with Miranda"
            ],
            "C": [
                "Refer to Child Advocacy Center for forensic interview",
                "DO NOT conduct your own detailed interview first - one interview protects child and case",
                "Observe forensic interview behind glass",
                "Forensic interviewer is trained for child witnesses",
                "Interview will be recorded for court use",
                "Avoid leading questions, multiple interviews",
                "Interview teacher and school personnel",
                "Obtain school records - attendance, behavior changes",
                "Interview mother separately from boyfriend",
                "Interview boyfriend separately",
                "Interview neighbors about household",
                "Interview child's other contacts (relatives, friends' parents)"
            ],
            "T": [
                "Photograph all injuries with scale",
                "Document all injuries with photographs",
                "Medical opinion on whether injuries consistent with explanation",
                "Determine age of injuries - are there healing injuries?",
                "Full body examination for hidden injuries",
                "Growth chart review for malnutrition signs"
            ],
            "I": [
                "Refer for medical examination by child abuse specialist",
                "Seize any implements that may have caused injuries",
                "Preserve child's clothing if relevant",
                "Background checks on all adults in home",
                "Check for prior DCFS history",
                "Check for prior police calls to address",
                "Obtain medical records for child's prior injuries"
            ],
            "O": [
                "Work closely with ASA specializing in child abuse",
                "Prepare child for court process",
                "Consider use of recorded forensic interview at trial",
                "Address hearsay exceptions for child statements",
                "Expert testimony on abuse indicators",
                "If arrest made, seek no-contact order"
            ],
            "N": [
                "Ensure safety plan in place with DCFS",
                "Monitor for witness intimidation",
                "Keep child informed in age-appropriate way",
                "Connect family with victim services"
            ]
        }
    },

    "Miranda and Confession Issues": {
        "modelAnswer": {
            "R": [
                "Under Davis v. United States, Miranda invocation must be unambiguous",
                "'Maybe I should have a lawyer' is ambiguous - police may seek clarification",
                "Your response 'that's up to you' is permissible",
                "Subsequent clear waiver 'I'll talk' is valid",
                "Initial Miranda portion likely survives challenge"
            ],
            "A": [
                "Clarification appropriate: 'Are you asking for an attorney or do you want to talk to me?'",
                "Get clear answer before proceeding",
                "When he asked to stop due to fatigue - STOP QUESTIONING",
                "Let him rest or resume another day",
                "Continuing undermines voluntariness of entire confession"
            ],
            "C": [
                "'Can we do this tomorrow?' is ambiguous invocation of right to silence",
                "Combined with stated fatigue, shows duress",
                "Statements after this point MORE vulnerable to suppression",
                "Four-hour interrogation - lengthy but not per se unconstitutional"
            ],
            "T": [
                "Only one bathroom break - concerning for voluntariness",
                "No food provided - concerning for voluntariness",
                "Duration plus lack of food/breaks plus tired request equals coercive environment",
                "Even if valid waiver initially, voluntariness can erode",
                "Document all breaks given and comfort provided",
                "Record everything to prove voluntariness"
            ],
            "I": [
                "Initial confession (before tired statement) - likely ADMISSIBLE",
                "Ambiguous counsel reference properly handled with clear subsequent waiver",
                "Statements after 'I'm tired, can we do this tomorrow?' - VULNERABLE to suppression",
                "'We're almost done' could be seen as coercive",
                "Additional details about home selection may be suppressed"
            ],
            "O": [
                "Provide food and water during interviews",
                "Regular breaks every 1-2 hours",
                "Proper response to fatigue: 'We can stop now and continue tomorrow'",
                "His request was not unambiguous, but prudent to honor",
                "Continuing risks entire confession being suppressed"
            ],
            "N": [
                "Shorter, focused interviews are best practice",
                "Take 'I'm tired' seriously",
                "When in doubt, stop and resume later",
                "Statements made under fatigue/duress may be excluded"
            ]
        }
    },

    "Officer-Involved Shooting Investigation": {
        "modelAnswer": {
            "R": [
                "Ensure all life-saving measures provided to subject",
                "Separate Officer Davis from scene immediately",
                "DO NOT interview Officer Davis - he has right to representation and 24-hour review period",
                "Notify COPA immediately - they have primary jurisdiction on OIS",
                "Notify command staff through chain"
            ],
            "E": [
                "Request crime scene unit",
                "Establish expanded perimeter - alley and surrounding area",
                "Officer Kim also separated but can be briefly interviewed"
            ],
            "A": [
                "Officer Davis entitled to union representation",
                "24-hour review period before statement (if invoked)",
                "Access to BWC before statement",
                "Administrative investigation separate from criminal",
                "COPA will conduct independent investigation",
                "Detective Division conducts criminal investigation in parallel"
            ],
            "C": [
                "Civilian witness - detailed statement immediately",
                "Document her vantage point - what she could actually see",
                "Officer Kim statement on what he observed (not opinions)",
                "Canvas for additional witnesses",
                "Keep witnesses separated",
                "Obtain contact information from all",
                "Civilian witness distance and lighting conditions",
                "What was her actual view - obstructions?",
                "Officer Kim's corroboration of 'gun' statement"
            ],
            "T": [
                "Document exact position of body",
                "Document distance from Officer Davis's position",
                "Shell casing locations documented",
                "Body-worn camera footage - preserve immediately",
                "Photograph and document everything",
                "Complete and comprehensive reports",
                "Video evidence preserved with chain of custody",
                "Witness statements in their own words",
                "Scene diagrams and measurements",
                "All notifications documented with times"
            ],
            "I": [
                "Comprehensive search for weapon - expand search area",
                "Officer Davis's weapon recovered and inventoried",
                "Search subject's body and clothing",
                "Canvas entire area for surveillance cameras",
                "ShotSpotter data if available",
                "Expand search extensively - weapons can be thrown",
                "Check dumpsters, bushes, under vehicles",
                "Forensic evidence of subject's hand position (GSR)",
                "Body-worn camera footage is critical evidence",
                "All evidence properly inventoried"
            ],
            "O": [
                "Did subject have accomplices who may have retrieved weapon?",
                "Interview subject's associates about weapon possession",
                "Check subject's criminal history for weapons offenses",
                "Social media may show prior weapon possession",
                "Absence of gun doesn't mean it wasn't there - continue searching"
            ],
            "N": [
                "Compassion is paramount with family",
                "Do not provide details of investigation to family",
                "Connect family with victim services",
                "Do not allow family access to scene",
                "PIO should handle media inquiries",
                "Department policy on releasing BWC",
                "Community meetings may be necessary",
                "Transparency builds trust",
                "Investigation integrity is priority",
                "Look for corroborating or contradicting evidence"
            ]
        }
    },

    "Traffic Stop Drug Investigation": {
        "modelAnswer": {
            "R": [
                "Extreme nervousness observed: sweating, shaking, no eye contact",
                "Cross-country travel from California to New York (drug courier indicator)",
                "Strong air freshener smell (masking odor indicator)",
                "Energy drinks/fast food suggest non-stop travel",
                "Valid license and registration - clean driving record",
                "Nervousness is normal during police contact"
            ],
            "A": [
                "Rodriguez v. United States (2015): traffic stop cannot be extended beyond time needed to complete the stop's mission",
                "K-9 sniff that prolongs stop beyond ordinary time is unconstitutional unless you have reasonable suspicion",
                "Nervous behavior alone may not be sufficient for reasonable suspicion",
                "If K-9 arrives during normal processing, sniff is permissible",
                "15 minutes likely exceeds normal stop time for taillight",
                "Cannot artificially slow down processing to wait for K-9"
            ],
            "T": [
                "Process license and registration normally",
                "Ask conversational questions about trip during normal processing",
                "Note responses and any inconsistencies",
                "Observe anything in plain view",
                "Document specific facts supporting reasonable suspicion",
                "Document observations for future reference if same vehicle encountered"
            ],
            "I": [
                "If additional indicators found (inconsistent story, visible contraband, admission) - RS exists, extend for K-9 justified",
                "If just nervousness and travel pattern - risky to extend, common in innocent travelers",
                "Totality of circumstances analysis required"
            ],
            "O": [
                "You may ask for consent to search - must be voluntary, not coerced",
                "If consent granted, document clearly",
                "If consent refused, cannot use refusal as reasonable suspicion",
                "Consider alerting agencies in travel direction"
            ],
            "N": [
                "Without stronger indicators than nervousness and travel, complete stop and release",
                "Weak RS leads to suppressed evidence and civil liability",
                "Issue warning/citation and release if RS insufficient",
                "Best practice: document everything in case vehicle encountered again"
            ]
        }
    },

    "Digital Evidence and Social Media": {
        "modelAnswer": {
            "R": [
                "Do NOT rely solely on screenshots - get originals",
                "Preserve original emails with full headers",
                "Document social media profile before it's deleted",
                "Screenshot all posts, followers, following",
                "Check if accounts still active",
                "Note exact URLs and usernames",
                "Document timeline of threats and vandalism"
            ],
            "E": [
                "Surveillance from business for vandalism",
                "Any evidence left at vandalism scene",
                "Method of vandalism match threats?",
                "Timeline supports same actor"
            ],
            "C": [
                "Who would threaten this business?",
                "Any disputes with employees, competitors, customers?",
                "Prior complaints or conflicts?",
                "Financial issues that might relate to 'pay up'?",
                "Interview employees, former employees",
                "Business competitors",
                "Anyone with access who might know vulnerabilities",
                "Check for similar threats to other businesses"
            ],
            "T": [
                "Screenshot/preserve everything at each step",
                "Hash values for digital evidence integrity",
                "Maintain chain of custody for all records",
                "Expert may be needed to explain at trial",
                "Compare threat language to known communications",
                "Spelling/grammar patterns analysis",
                "Phrase usage that might identify writer",
                "Time of day messages sent"
            ],
            "I": [
                "IP addresses from email headers",
                "IP logs from social media logins",
                "VPN usage masks real IP - be aware",
                "Public WiFi complicates identification",
                "Dynamic IPs require exact time stamp",
                "Search warrant for suspect's devices once identified",
                "Compare writing samples",
                "Check for saved threatening messages",
                "Browser history showing accounts"
            ],
            "O": [
                "Send preservation letter to Google immediately - preserves records for 90 days",
                "Search warrant required for content of emails",
                "Warrant needs probable cause linking account to crime, specific records sought, account identifiers",
                "Google may provide: subscriber info, IP logs, account activity, email content",
                "Preservation letter to social media platform",
                "Search warrant for social media content",
                "Subpoena to ISP for subscriber info",
                "Platforms have law enforcement portals",
                "Charges: Intimidation (720 ILCS 5/12-6), criminal damage, computer tampering, possibly extortion"
            ],
            "N": [
                "While awaiting records, investigate traditionally",
                "Interview with confrontation of evidence once suspect identified",
                "Parallel investigation to build case during legal process delays"
            ]
        }
    },

    "Missing Person Investigation": {
        "modelAnswer": {
            "R": [
                "Purse and phone left behind - out of character",
                "Car still at residence",
                "No contact with anyone",
                "Failed to appear at work (unusual)",
                "Recent relationship conflict with angry communications from ex-boyfriend",
                "Classification: HIGH-RISK MISSING PERSON - treat as potential foul play from outset",
                "Enter into LEADS/NCIC immediately",
                "Issue BOLO with photo",
                "Notify command - potential criminal case",
                "Request additional investigative resources",
                "Check hospitals and morgue",
                "Check jail systems"
            ],
            "E": [
                "Treat apartment as potential crime scene",
                "Document condition of apartment",
                "Check if any items missing that she would take",
                "Obtain gas station surveillance video immediately",
                "Was she alone at gas station? Any other vehicles?",
                "Did she appear distressed?",
                "Direction of travel after gas station?"
            ],
            "A": [
                "Ex-boyfriend is primary person of interest",
                "Interview immediately - where was he at 8 PM that night?",
                "Obtain his phone for angry messages",
                "Check his car and residence (consent or warrant)",
                "Verify alibi completely",
                "Check his GPS/phone location data",
                "Social media monitoring of ex-boyfriend",
                "Prior DV history?"
            ],
            "C": [
                "Interview roommate thoroughly",
                "Witnesses at gas station",
                "Canvas entire apartment complex",
                "Interview all friends and family",
                "Interview coworkers",
                "Check sex offender registry in area",
                "Any similar missing persons in region?"
            ],
            "T": [
                "Timeline of last known activities",
                "All interviews documented",
                "Evidence properly preserved",
                "Chain of custody maintained",
                "Regular updates to command"
            ],
            "I": [
                "Process apartment for evidence - fingerprints, DNA, blood",
                "Luminol test for cleaned blood",
                "Examine all electronics left behind",
                "Check for any diary, notes, calendar",
                "K-9 search if evidence of foul play develops",
                "Check surveillance along route from gas station to home"
            ],
            "O": [
                "Search warrant for Sarah's phone records",
                "Text messages with ex-boyfriend",
                "Last location data from phone",
                "Social media account activity",
                "Email accounts",
                "Dating apps (was she meeting someone new?)",
                "Bank/credit card records for activity after gas station",
                "Case becomes criminal investigation when evidence of foul play discovered, body found, witness reports abduction, or suspect provides incriminating evidence"
            ],
            "N": [
                "Coordinate with PIO on media release",
                "Photo and description to media",
                "Family may help with social media sharing",
                "Keep family informed but don't compromise investigation",
                "Consider tip line",
                "Based on circumstances, investigate as probable foul play"
            ]
        }
    },

    # =========================================================================
    # seed_practice_content.py  (5 gold scenarios)
    # =========================================================================

    "The Witness Identification": {
        "modelAnswer": {
            "R": [
                "A showup would be most appropriate given the suspect was detained within a short time frame (15 minutes) following the offense",
                "Per S06-02, showups are used only when the suspect is detained within a short time frame, generally within one hour of the offense"
            ],
            "E": [
                "Evaluate timing - suspect detained 15 minutes after offense, within the one-hour rule for showups",
                "Do not present the same suspect to the same witness more than once"
            ],
            "A": [
                "Separate the witnesses immediately to prevent communication",
                "Transport witnesses to the location of the suspect (not vice versa, unless the scene is the crime location)"
            ],
            "C": [
                "Caution each witness that the person they are about to see may or may not be the perpetrator",
                "An independent administrator should coordinate when feasible",
                "Keep witnesses separated before, during, and after the showup",
                "Do not allow witnesses to confer",
                "Follow Limited English Proficiency directive if applicable for Ms. Garcia"
            ],
            "T": [
                "If positive: Document time and location, description given by witness, description of suspect prior to showup, officers present, outcome, and exact words used by witness in original case report or supplemental",
                "If negative: Document encounter on Investigatory Stop Report (CPD-11.910) and reference in original report",
                "Document the exact words used by each witness during identification"
            ],
            "O": [
                "The showup must be conducted within a reasonable time to be legally valid",
                "Per Kirby v. Illinois, suspects are not entitled to counsel prior to adversarial criminal proceedings",
                "Failure to follow proper procedures can lead to inadmissibility of identification",
                "Avoid any suggestive behavior that could taint the identification"
            ],
            "N": [
                "Inform the zone via radio whether the showup was positive or negative",
                "Follow LEP directive if applicable for Ms. Garcia"
            ]
        }
    },

    "The Photo Lineup": {
        "modelAnswer": {
            "R": [
                "Recognize that a photo lineup is needed because significant time has passed since the offense",
                "A showup would not be appropriate as the suspect was not detained near the time of the crime"
            ],
            "E": [
                "Compose lineup with minimum of 6 photographs (1 suspect + minimum 5 fillers)",
                "Photos must be uniquely numbered, contemporary, same size and basic composition",
                "Do not mix color and black & white photos",
                "Do not mix mug shots with other photo types",
                "Cover any portions that provide identifying information",
                "Fillers should match race, sex, approximate height, weight, age, and physical appearance",
                "Fillers should match any descriptive features given by the witness (including visible tattoo)",
                "Suspect should not appear substantially different from fillers based on eyewitness description",
                "Avoid fillers who too closely resemble the suspect, making distinction difficult",
                "If the witness has viewed a previous lineup for this case, use different fillers"
            ],
            "A": [
                "Must be conducted by an independent administrator not participating in the investigation",
                "If independent administrator unavailable, use a procedure (automated program or folder method) that prevents the administrator from knowing the suspect's position",
                "Supervisory approval required if no independent administrator is used"
            ],
            "C": [
                "Present Photo/Live Lineup Advisory Form (CPD-11.900) before lineup",
                "Instruct witness that the suspect may or may not be present in the photos",
                "Present photos simultaneously to the witness",
                "Nothing should be communicated that might influence the identification",
                "No comment on outcomes in presence of witness",
                "Audio/video record if practical and witness consents"
            ],
            "T": [
                "Complete Photo/Live Lineup Advisory Form (CPD-11.900)",
                "Complete Supplementary Report (CPD-11.411-A or B) including date, time, location of lineup",
                "Document administrator information and witness information",
                "Document information about each participant (name, sex, race, etc.)",
                "Document whether identification was made and any statements made by witness",
                "Confirm photos/recordings taken"
            ],
            "I": [
                "All photos used must be inventoried regardless of outcome"
            ],
            "O": [
                "If positive identification: Do not provide any information about the person identified until lineup is completed; continue investigation with this evidence",
                "If no identification: Document that no identification was made; this does not mean the suspect is cleared; continue investigation with other evidence"
            ],
            "N": [
                "Complete all required documentation and inventory photos in either case"
            ]
        }
    },

    "The Domestic Violence Call": {
        "modelAnswer": {
            "R": [
                "Ensure scene is secure and all parties are safe",
                "Ensure medical attention is offered/provided to Mrs. Martinez",
                "Ensure children are safe and attended to"
            ],
            "E": [
                "Separate all parties (husband, wife, children)",
                "Verify the Emergency Order of Protection through LEADS/Law Enforcement Agencies Data System",
                "Begin evidence collection (photograph injuries, scene)"
            ],
            "A": [
                "Domestic Battery (720 ILCS 5/12-3.2) for the physical attack",
                "Violation of Order of Protection (720 ILCS 5/12-3.4) - he violated the order by being at the residence",
                "Aggravated Domestic Battery (if injuries are severe) (720 ILCS 5/12-3.3)",
                "His probation status from previous domestic battery should be noted",
                "Potential charges related to children witnessing the violence"
            ],
            "C": [
                "Interview Mrs. Martinez privately, minimize trauma",
                "Use trauma-informed interview techniques",
                "Document her exact words regarding the assault",
                "For children (ages 8 and 5): Contact DCFS per protocol",
                "Children should be interviewed by trained professionals (consider Chicago Children's Advocacy Center)",
                "Do NOT interview children in presence of either parent if they witnessed the violence"
            ],
            "T": [
                "Domestic Incident Notice to be provided to victim",
                "General Offense Case Report documenting all aspects",
                "Photograph all injuries",
                "Document exact statements from all parties"
            ],
            "O": [
                "Notify the court that issued the Order of Protection of the violation",
                "Notify Probation/Parole of violation",
                "DCFS notification required as children witnessed domestic violence",
                "Notify appropriate Bureau of Detectives Area"
            ],
            "N": [
                "Provide Mrs. Martinez with Domestic Incident Notice",
                "Explain the Order of Protection process (Emergency can become Interim/Plenary)",
                "Connect with victim services and advocacy organizations",
                "Discuss safety planning (safe place to go, important documents, emergency contacts)",
                "Explain criminal justice process and what to expect",
                "Provide resources for domestic violence counseling",
                "Address immediate safety of children"
            ]
        }
    },

    "The School Threat Investigation": {
        "modelAnswer": {
            "R": [
                "Ensure scene is secure and students are safe",
                "Report to the Bureau of Patrol supervisor on scene"
            ],
            "E": [
                "Obtain original screenshots and document all evidence",
                "Request preservation of social media evidence (contact provider)",
                "Review school security camera footage",
                "Check school technology resources (was school WiFi used?)"
            ],
            "A": [
                "Miranda warnings are required before custodial interrogation",
                "Contact parents/guardians - they have right to be present",
                "Per Illinois law, juveniles require additional protections",
                "All custodial interrogations of juveniles must be digitally recorded",
                "Use age-appropriate, trauma-informed interview techniques",
                "Do not use coercive tactics",
                "Consider having a youth officer or detective trained in juvenile interviews"
            ],
            "C": [
                "Canvass for witnesses (students/staff who might have information)",
                "Interview potential suspects about their social media activity",
                "Check if any known associates can identify the account",
                "Contact Bureau of Detectives Crime Analysis Technical Group for assistance",
                "Request emergency disclosure from social media platform (Meta/Facebook Threat Operations)"
            ],
            "T": [
                "Document all digital evidence including screenshots and timestamps",
                "Document all statements from witnesses and suspects",
                "Document complete timeline of events"
            ],
            "I": [
                "Request Forensic Services for digital evidence",
                "Obtain subpoena or search warrant for subscriber information and IP logs"
            ],
            "O": [
                "Disorderly Conduct (720 ILCS 5/26-1) - false threat",
                "Potentially Threatening Public Official (if applicable)",
                "Computer Fraud/Unauthorized Access if school systems were compromised",
                "At age 14, generally processed through juvenile court",
                "Fingerprinting only if felony and authorized by watch operations lieutenant",
                "Juvenile has right to counsel",
                "DCFS assessment may be appropriate",
                "Juvenile records have special confidentiality requirements"
            ],
            "N": [
                "Notify watch operations lieutenant",
                "Contact Bureau of Detectives for assignment if serious",
                "Coordinate with School Resource Officers",
                "Notify CPIC for threat assessment",
                "Consider FBI notification if terrorism nexus suspected",
                "Coordinate with Chicago Public Schools administration",
                "Alert DCFS if child welfare concerns arise",
                "Parents must be notified",
                "Possible diversion program consideration"
            ]
        }
    },

    "The Live Lineup Challenge": {
        "modelAnswer": {
            "R": [
                "Recognize that a live lineup is appropriate when the suspect is in custody",
                "Understand 6th Amendment attachment rules - right to counsel depends on whether adversarial proceedings have begun",
                "Per Kirby v. Illinois, suspects are NOT entitled to counsel PRIOR to adversarial criminal proceedings"
            ],
            "E": [
                "Determine if adversarial criminal proceedings have begun for the robbery/sexual assault charges",
                "Williams arrested on unrelated warrant and has not been arraigned on these charges, so adversarial proceedings have not begun for this offense",
                "If the 6th Amendment right has attached (post-arraignment), counsel MUST be notified and given opportunity to observe",
                "Per CPD policy: If the suspect's attorney is present and not disruptive, they may observe"
            ],
            "A": [
                "One suspect per lineup with minimum of 6 individuals (1 suspect + 5 fillers), but no less than 3 fillers",
                "Supervisory approval required if fewer than 5 fillers",
                "Fillers must match suspect in race, sex, approximate height, weight, age, physical appearance",
                "Suspect should not substantially differ from fillers based on eyewitness description",
                "Fillers should not too closely resemble suspect",
                "All participants may be required to speak words or perform actions",
                "Community members can be used as fillers when feasible; police officers as fillers only as last resort",
                "Handle distinctive scratch marks: apply similar makeup/prosthetic scratches to fillers, cover scratches on all participants, or position to minimize visibility",
                "Whatever is done to disguise/reveal scratches must be done uniformly",
                "Consult with supervisor on best approach for scratch mark accommodation"
            ],
            "C": [
                "Present Photo/Live Lineup Advisory Form (CPD-11.900) to Ms. Davis",
                "Have her read, understand, and sign the form",
                "Get consent/non-consent for video recording",
                "Instruct witness that the suspect may or may not be present",
                "Ensure Ms. Davis has not seen suspect or fillers beforehand",
                "Do not communicate anything that might influence identification",
                "Do not comment on outcome in witness presence"
            ],
            "T": [
                "Complete Photo/Live Lineup Advisory Form (CPD-11.900) signed by witness",
                "Complete Supplementary Report (CPD-11.411-A or B) documenting date, time, location",
                "Document administrator's name, rank, star number, unit",
                "Document name and address of witness and all information on each participant",
                "Document names of others present and type of lineup conducted",
                "Document source of fillers used, whether identification was made and by whom",
                "Document exact statements by witness and confirmation of photos/recordings",
                "Document any refusals by witness and reasons if directive requirements were not strictly followed",
                "Document attorney's comments and unusual circumstances (scratch marks accommodation)",
                "Photograph the lineup regardless of outcome",
                "Audio/video record the procedure"
            ],
            "I": [
                "Inventory all materials",
                "Document photos/recordings in eTrack on Crime Scene Processing Report",
                "Record inventory numbers"
            ],
            "O": [
                "Attorney Roberts does NOT have a constitutional right to be present since adversarial proceedings have not begun for this offense",
                "Obtain an independent administrator (detective not involved in investigation)",
                "If independent administrator unavailable, get supervisory approval",
                "Conduct in appropriate location (not district lockup unless necessary)",
                "Ensure no one who knows suspect's identity is present except witness and attorney"
            ],
            "N": [
                "Complete all required forms and documentation",
                "Note all accommodations made for distinctive features (scratch marks)",
                "Document any unusual circumstances",
                "If speaking is required, all participants must speak, even after identification is made"
            ]
        }
    },
}
