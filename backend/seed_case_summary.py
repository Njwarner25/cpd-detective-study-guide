import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
import uuid
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ.get('MONGO_URL', os.environ.get('MONGODB_URI', ''))
db_name = os.environ.get('DB_NAME', 'cpd_detective')
if mongo_url:
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
else:
    db = None


async def seed_case_summary(ext_db=None):
    """Seed 15 Detective Briefing Exercises (case_summary type).

    Each exercise presents a realistic investigative case report that the student
    must read and distill into a concise factual summary for a supervisor.
    Covers diverse crime types with Chicago-area details.

    Args:
        ext_db: Optional external database connection. If provided, uses it
                instead of the module-level db.
    """
    global db
    if ext_db is not None:
        db = ext_db

    # ======== CATEGORY ========
    await db.categories.update_one(
        {"category_id": "cat_case_summary"},
        {"$set": {
            "category_id": "cat_case_summary",
            "name": "Detective Briefing Exercises",
            "description": "Read case reports and prepare a factual summary for your supervisor. Upload a photo of your handwritten response for AI grading.",
            "order": 32,
            "is_premium": True,
            "section": "part2"
        }},
        upsert=True,
    )
    print("  Seeded cat_case_summary category")

    now = datetime.now(timezone.utc)

    case_summary_questions = [
        # ---- 1. Jewelry Store Diversion Theft (Two-Person Team) ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Jewelry Store Diversion Theft — North Michigan Avenue",
            "content": (
                "On 14 March 2026, at approximately 1435 hours, Beat 1813 responded to a retail theft report at Lakeshore Fine Jewelers, "
                "located at 645 N. Michigan Avenue (018th District). The store manager, Diane Kowalski (W/F, DOB 12 Aug 1978), reported that "
                "two offenders — a male and a female acting in concert — entered the store at approximately 1410 hours. The female offender, "
                "described as a W/F, 30-35 years old, approximately 5'6\", medium build, wearing a long camel-colored coat and oversized "
                "sunglasses, engaged the sales associate, Marcus Chen (M/A, DOB 03 Jan 1995), in an extended conversation about engagement "
                "rings, requesting to view multiple trays of diamond solitaires in the 2-3 carat range. While Chen was occupied, the male "
                "offender, described as a W/M, 35-40 years old, approximately 6'0\", athletic build, dark blazer, moved to an adjacent display "
                "case that had been left unlocked by a second associate who was on a break.\n\n"
                "Surveillance footage recovered from the store's eight-camera DVR system shows the male offender removing three items from "
                "the unlocked case between 1418 and 1422 hours: a platinum diamond tennis bracelet (inventory #LFJ-4417, value $14,200), "
                "a pair of 2-carat diamond stud earrings (inventory #LFJ-4523, value $9,800), and an 18K white gold sapphire pendant "
                "(inventory #LFJ-4601, value $6,350). The male concealed the items in the interior breast pocket of his blazer. At "
                "approximately 1425 hours, the female offender abruptly ended her conversation with Chen, stating she needed to \"think about "
                "it,\" and both offenders exited the store together, walking northbound on Michigan Avenue. Total loss is valued at $30,350.\n\n"
                "Evidence Technician Ramirez (Star #8842) processed the display case and recovered two latent fingerprints from the glass "
                "surface. The prints were submitted to the Crime Lab (Lab Case #2026-031418). Chen provided a written statement and identified "
                "both offenders from surveillance stills. Kowalski confirmed the inventory losses through a physical audit. The store's external "
                "POD camera at Michigan and Erie captured both offenders entering a silver 2019-2021 BMW 3-Series, Illinois plate partial "
                "\"BX7,\" which departed northbound on Michigan. CPIC was notified and the vehicle description was broadcast city-wide. Detective "
                "follow-up includes CLEAR database search for known retail theft teams, submission of latent prints for AFIS comparison, and "
                "canvass of pawn shops and secondary market dealers in the Area."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 14 March 2026, at approximately 1410 hours, two offenders — a white female (30-35, 5'6\", camel coat, sunglasses) and "
                "a white male (35-40, 6'0\", dark blazer) — executed a diversion theft at Lakeshore Fine Jewelers, 645 N. Michigan Avenue "
                "(018th District). The female engaged a sales associate with requests to view engagement rings while the male removed three "
                "items valued at $30,350 (platinum tennis bracelet, diamond stud earrings, and sapphire pendant) from an unlocked display "
                "case. Both offenders exited at approximately 1425 hours and departed northbound in a silver BMW 3-Series, partial Illinois "
                "plate \"BX7.\" The theft was captured on an eight-camera DVR system. Evidence Technician Ramirez recovered two latent prints "
                "from the display case (Lab Case #2026-031418). The store manager confirmed losses via physical audit and the sales associate "
                "provided a written statement. CPIC was notified and a city-wide broadcast was issued. Follow-up includes AFIS comparison of "
                "latent prints, CLEAR database checks for known retail theft teams, and pawn shop canvasses."
            ),
            "key_facts": [
                "Date/time: 14 March 2026, approximately 1410-1425 hours",
                "Location: Lakeshore Fine Jewelers, 645 N. Michigan Avenue, 018th District",
                "Two-person diversion theft team: W/F (30-35, 5'6\", camel coat) and W/M (35-40, 6'0\", dark blazer)",
                "Female distracted sales associate with engagement ring requests while male stole from unlocked case",
                "Three items stolen totaling $30,350: platinum tennis bracelet, diamond stud earrings, sapphire pendant",
                "Offenders departed in silver BMW 3-Series, partial Illinois plate \"BX7\", northbound on Michigan",
                "Eight-camera DVR captured the theft; two latent prints recovered from display case",
                "Lab Case #2026-031418 submitted; CPIC notified; city-wide vehicle broadcast issued",
                "Follow-up: AFIS comparison, CLEAR database search, pawn shop canvass"
            ],
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Retail Theft Investigation Procedures",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 2. Armed Robbery at Gas Station with Surveillance ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Armed Robbery — 79th Street Gas Station",
            "content": (
                "On 22 March 2026, at approximately 2247 hours, Beat 0623 responded to a call of an armed robbery at the BP gas station "
                "located at 2101 W. 79th Street (006th District). The victim/complainant, Amara Okafor (B/F, DOB 18 Nov 1990), the night "
                "cashier, reported that a single male offender entered the station convenience store at approximately 2235 hours, "
                "selected a bag of chips and a beverage, and approached the counter. When Okafor opened the register to complete the "
                "transaction, the offender produced a black semi-automatic handgun, pointed it at her face, and demanded all cash from "
                "the register and the drop safe. The offender is described as a B/M, 20-25 years old, approximately 5'10\", slim build, "
                "wearing a black hoodie with a white logo on the left chest, dark jeans, black Nike shoes with a white swoosh, and a "
                "blue surgical mask covering the lower face.\n\n"
                "Okafor complied and turned over approximately $680 in cash from the register and $1,450 from the drop safe, for a total "
                "loss of approximately $2,130. The offender placed the cash in a dark-colored backpack and exited the store through the "
                "front entrance, fleeing eastbound on 79th Street on foot. Okafor activated the silent alarm at 2238 hours and called 911. "
                "She was not physically injured but reported being in fear for her life.\n\n"
                "The station is equipped with a 16-channel HD surveillance system. Detective Walsh (Star #6219) reviewed footage and "
                "obtained clear images of the offender's face (mask slipped briefly at 2237 hours), the handgun, and the direction of "
                "flight. The footage also captured what appears to be a distinctive tattoo — a star or compass rose — on the offender's "
                "right hand. Evidence Technician Davis (Star #7034) processed the counter area and recovered one latent print from the "
                "beverage bottle left behind by the offender (Lab Case #2026-032206). A POD camera at 79th and Damen captured the offender "
                "running eastbound and entering the passenger side of a dark-colored SUV (possible Chevy Equinox) at 2241 hours. The SUV "
                "departed eastbound. Beat officers canvassed the area; no additional witnesses were located. Follow-up includes AFIS "
                "submission of the latent print, distribution of surveillance stills to Area patrol, and cross-referencing the tattoo "
                "description with gang intelligence databases."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 22 March 2026, at approximately 2235 hours, a lone male offender committed an armed robbery at the BP station, "
                "2101 W. 79th Street (006th District). The offender, described as a B/M, 20-25, 5'10\", slim build, black hoodie with "
                "white logo, dark jeans, black Nike shoes, and blue surgical mask, produced a black semi-automatic handgun and demanded "
                "cash from the night cashier, Amara Okafor. He obtained approximately $2,130 ($680 from register, $1,450 from drop safe) "
                "and fled eastbound on foot on 79th Street, entering a dark-colored SUV (possible Chevy Equinox) captured on a POD camera "
                "at 79th and Damen at 2241 hours. The 16-channel HD surveillance system captured the offender's face when his mask "
                "slipped, as well as a distinctive star/compass rose tattoo on his right hand. One latent print was recovered from a "
                "beverage bottle left at the counter (Lab Case #2026-032206). The victim was not injured. Follow-up includes AFIS "
                "submission, distribution of surveillance stills, and cross-referencing the tattoo with gang intelligence databases."
            ),
            "key_facts": [
                "Date/time: 22 March 2026, approximately 2235 hours",
                "Location: BP gas station, 2101 W. 79th Street, 006th District",
                "Offender: B/M, 20-25, 5'10\", slim, black hoodie with white logo, blue surgical mask, black Nike shoes",
                "Weapon: black semi-automatic handgun pointed at cashier's face",
                "Total loss approximately $2,130 ($680 register + $1,450 drop safe)",
                "Offender fled eastbound on 79th, entered dark SUV (possible Chevy Equinox) at 79th and Damen at 2241 hours",
                "HD surveillance captured offender's face (mask slipped) and distinctive right-hand tattoo (star/compass rose)",
                "One latent print recovered from beverage bottle (Lab Case #2026-032206)",
                "Victim not physically injured; silent alarm activated at 2238 hours",
                "Follow-up: AFIS, surveillance stills to patrol, tattoo cross-reference with gang intel"
            ],
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Armed Robbery Investigation Procedures",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 3. Hit-and-Run with Fatality ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Fatal Hit-and-Run — Western Avenue and Addison",
            "content": (
                "On 08 March 2026, at approximately 1923 hours, Beat 1722 responded to a traffic crash involving a pedestrian at the "
                "intersection of N. Western Avenue and W. Addison Street (017th District). Upon arrival, officers found the victim, "
                "Roberto Garza (H/M, DOB 22 May 1954, age 71), lying unresponsive in the southbound lanes of Western Avenue "
                "approximately 40 feet south of the crosswalk. CFD Ambulance 17 responded and transported Garza to Illinois Masonic "
                "Medical Center, where he was pronounced deceased at 2014 hours by Dr. Anita Patel. The Cook County Medical Examiner "
                "was notified (ME Case #2026-01087).\n\n"
                "Witness #1, Patricia Dunne (W/F, DOB 14 Sep 1983), was stopped at the red light on westbound Addison and observed a "
                "large dark-colored pickup truck — possibly a Dodge Ram or Ford F-150, 2018 or newer — traveling southbound on Western "
                "at a high rate of speed. She stated the truck struck Garza as he was crossing Western in the crosswalk with the "
                "pedestrian signal and continued southbound without stopping. She described the truck's headlights as appearing to be "
                "LED and noted possible damage to the right front quarter panel. Witness #2, James Holt (B/M, DOB 30 Jun 1970), a "
                "CTA bus driver operating Route 49 southbound on Western, reported that the truck passed his bus on the right side "
                "at an excessive speed moments before impact. Holt estimated the truck was traveling 50+ mph in a 30 mph zone. His "
                "dashcam may have captured the collision.\n\n"
                "The Major Accident Investigation Unit (MAIU) responded and processed the scene. Vehicle debris recovered at the "
                "scene included a chrome side mirror housing and fragments of a dark-colored plastic bumper cover. ET Harris (Star "
                "#9156) collected the debris (Inventory #2026-030876) and noted tire marks beginning approximately 20 feet before the "
                "point of impact, suggesting minimal braking. POD camera at Western and Addison was inoperative at the time of the "
                "incident. Private surveillance from Walgreens at the northeast corner is being requested. MAIU is working to "
                "identify the vehicle make/model from the recovered mirror housing. The CTA bus dashcam footage has been requested "
                "through CTA Legal. Next of kin (wife, Maria Garza) was notified by Beat 1722."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 08 March 2026, at approximately 1923 hours, Roberto Garza (H/M, 71) was struck and killed by a hit-and-run vehicle "
                "while crossing N. Western Avenue at W. Addison Street (017th District) in the crosswalk with the pedestrian signal. "
                "Garza was transported to Illinois Masonic Medical Center and pronounced deceased at 2014 hours (ME Case #2026-01087). "
                "Two witnesses observed a large dark-colored pickup truck (possible Dodge Ram or Ford F-150, 2018+) traveling southbound "
                "on Western at an estimated 50+ mph in a 30 mph zone strike the victim and continue without stopping. One witness noted "
                "possible right front quarter panel damage and LED headlights. A CTA bus driver on Route 49 also observed the truck and "
                "his dashcam may have captured the collision; footage has been requested through CTA Legal. MAIU processed the scene and "
                "recovered a chrome mirror housing and dark bumper cover fragments (Inventory #2026-030876). Tire marks suggest minimal "
                "braking. The POD camera at the intersection was inoperative. Private surveillance from a nearby Walgreens is being "
                "requested. MAIU is working to identify the vehicle from recovered debris. Next of kin was notified."
            ),
            "key_facts": [
                "Date/time: 08 March 2026, approximately 1923 hours",
                "Location: N. Western Avenue and W. Addison Street, 017th District",
                "Victim: Roberto Garza, H/M, 71, pronounced deceased at Illinois Masonic at 2014 hours (ME Case #2026-01087)",
                "Victim was in crosswalk with pedestrian signal when struck",
                "Suspect vehicle: large dark pickup truck (possible Dodge Ram/F-150, 2018+), southbound on Western, 50+ mph in 30 mph zone",
                "Vehicle fled southbound without stopping; possible right front quarter panel damage, LED headlights",
                "Two witnesses: Patricia Dunne (stopped at red light) and James Holt (CTA bus driver, Route 49, possible dashcam)",
                "Debris recovered: chrome mirror housing and bumper fragments (Inventory #2026-030876); tire marks show minimal braking",
                "POD camera at intersection was inoperative; Walgreens private surveillance being requested",
                "MAIU responding and processing; CTA dashcam requested through CTA Legal"
            ],
            "difficulty": "hard",
            "reference": "CPD General Order G06-03; Traffic Crash/Hit-and-Run Investigation; MAIU Procedures",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 4. Aggravated Battery / Stabbing at a Bar ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Aggravated Battery / Stabbing — Bridgeport Tavern",
            "content": (
                "On 18 March 2026, at approximately 0117 hours, Beat 0924 responded to a call of a person stabbed at McNally's Pub, "
                "located at 3247 S. Halsted Street (009th District). Upon arrival, officers found the victim, Kevin Driscoll (W/M, "
                "DOB 09 Apr 1989), seated on the floor near the bar with a laceration to the left side of his neck and a puncture "
                "wound to his upper left chest. CFD Ambulance 37 transported Driscoll to Stroger Hospital in serious condition. "
                "Emergency surgery was performed and the victim was stabilized in the ICU. Attending physician Dr. Samuel Rivera "
                "classified both wounds as life-threatening.\n\n"
                "Witness #1, bartender Sean Flaherty (W/M, DOB 15 Dec 1985), stated that Driscoll and the offender, later identified "
                "as Thomas Moran (W/M, DOB 27 Feb 1991, last known address 3515 S. Lowe Avenue), had been drinking at the bar since "
                "approximately 2230 hours and engaged in an escalating verbal argument over a gambling debt. At approximately 0110 "
                "hours, Moran produced a folding knife from his right front pants pocket and slashed at Driscoll, striking him in the "
                "neck, then stabbed him once in the upper chest. Moran then fled through the rear exit into the alley. Witness #2, "
                "patron Lisa Nowak (W/F, DOB 02 Aug 1993), corroborated Flaherty's account and added that Moran shouted \"You owe me "
                "and you'll pay\" immediately before producing the knife. She further stated Moran appeared highly intoxicated.\n\n"
                "ET Kowalski (Star #8310) processed the scene and recovered a blood-stained folding knife (Buck brand, 3.5-inch blade) "
                "from the floor near the rear exit (Inventory #2026-031803). Blood samples were collected from the knife blade and the "
                "floor area around the victim (Lab Case #2026-031804). Surveillance footage from the bar's two interior cameras and one "
                "exterior camera was secured. The footage clearly shows the altercation, the knife being produced, and Moran fleeing "
                "through the rear exit at 0112 hours. An investigative alert was issued for Thomas Moran. His last known address was "
                "checked by Beat 0921 with negative results. A background check revealed Moran has two prior arrests for battery (2018, "
                "2022) and one for aggravated DUI (2020). ASA Kim reviewed the case and approved felony charges of Aggravated Battery "
                "with a Deadly Weapon (720 ILCS 5/12-3.05(f)(1))."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 18 March 2026, at approximately 0110 hours, Thomas Moran (W/M, 35, LKA 3515 S. Lowe Avenue) stabbed Kevin Driscoll "
                "(W/M, 36) with a folding knife at McNally's Pub, 3247 S. Halsted Street (009th District), following an argument over a "
                "gambling debt. Driscoll sustained a life-threatening laceration to the left neck and a puncture wound to the upper left "
                "chest. He was transported to Stroger Hospital in serious condition and stabilized after emergency surgery. Two witnesses "
                "— the bartender and a patron — both observed Moran produce the knife and attack Driscoll; the patron heard Moran state "
                "\"You owe me and you'll pay\" before the attack. Moran fled through the rear exit at approximately 0112 hours. A "
                "blood-stained Buck folding knife (3.5-inch blade) was recovered near the rear exit (Inventory #2026-031803; Lab Case "
                "#2026-031804). Three-camera surveillance footage captured the full altercation. Moran has prior arrests for battery "
                "(2018, 2022) and aggravated DUI (2020). An investigative alert has been issued; his LKA was checked with negative results. "
                "ASA Kim approved felony charges of Aggravated Battery with a Deadly Weapon (720 ILCS 5/12-3.05(f)(1))."
            ),
            "key_facts": [
                "Date/time: 18 March 2026, approximately 0110 hours",
                "Location: McNally's Pub, 3247 S. Halsted Street, 009th District",
                "Victim: Kevin Driscoll (W/M, 36), life-threatening laceration to left neck and puncture wound to upper left chest",
                "Offender: Thomas Moran (W/M, 35), identified by name; LKA 3515 S. Lowe Avenue",
                "Motive: escalating argument over a gambling debt; Moran stated \"You owe me and you'll pay\"",
                "Weapon: Buck folding knife, 3.5-inch blade, recovered blood-stained near rear exit (Inventory #2026-031803)",
                "Two witnesses (bartender and patron) corroborated the account; three-camera surveillance secured",
                "Moran fled through rear exit at 0112 hours; investigative alert issued; LKA checked negative",
                "Moran has prior arrests: battery (2018, 2022), aggravated DUI (2020)",
                "ASA approved Aggravated Battery with a Deadly Weapon charges (720 ILCS 5/12-3.05(f)(1))"
            ],
            "difficulty": "medium",
            "reference": "CPD General Order G06-01-01; Aggravated Battery Investigation; 720 ILCS 5/12-3.05",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 5. Home Invasion with Elderly Victims ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Home Invasion — Elderly Victims in Norwood Park",
            "content": (
                "On 25 March 2026, at approximately 2105 hours, Beat 1631 responded to a home invasion in progress at 6218 N. Canfield "
                "Avenue (016th District, Norwood Park). Victims Harold Jorgensen (W/M, DOB 11 Jan 1944, age 82) and his wife Eleanor "
                "Jorgensen (W/F, DOB 03 Mar 1947, age 79) reported that two male offenders forced entry through the rear kitchen door "
                "by kicking it in. The offenders, both wearing black ski masks and dark clothing, confronted the couple in the living room "
                "where they were watching television. Offender #1, described as a B/M, 25-30 years old, approximately 6'2\", heavy build, "
                "deep voice, was armed with a chrome revolver. Offender #2, described as a B/M, 20-25 years old, approximately 5'8\", "
                "slim build, carried a dark-colored pillowcase that was used to collect items.\n\n"
                "Offender #1 ordered the victims to the floor and zip-tied their wrists behind their backs. Harold Jorgensen was struck "
                "in the face with the butt of the revolver when he initially resisted, causing a laceration above his right eye and a "
                "possible fractured orbital bone. CFD Ambulance 41 transported Harold to Advocate Lutheran General Hospital for treatment. "
                "Eleanor was not physically injured but was treated at the scene for anxiety. The offenders ransacked the master bedroom "
                "and a home office, taking a jewelry box containing Eleanor's wedding ring set (appraised value $8,500), a men's Rolex "
                "Submariner watch (value $12,000), a .38 caliber Smith & Wesson revolver (serial #SAW-77231, registered to Harold), "
                "approximately $2,300 in cash from a desk drawer, and a Dell laptop computer (serial #DELLXPS-44892). Total estimated "
                "loss is $25,100. The offenders were inside the home for approximately 12 minutes before fleeing through the same rear "
                "door and through the backyard toward the alley.\n\n"
                "ET Nunez (Star #7520) processed the scene and recovered a partial shoe impression from the mud near the rear door "
                "(consistent with a size 12 Nike Air Max), tool mark impressions from the door frame, and one zip-tie cut from Eleanor's "
                "wrists that was submitted for DNA analysis from possible touch DNA (Lab Case #2026-032510). A neighbor at 6220 N. "
                "Canfield, Martin Bridges (W/M, DOB 07 Jul 1967), reported seeing a dark-colored sedan — possibly a Nissan Altima — "
                "parked in the alley behind the Jorgensen residence at approximately 2045 hours with its engine running. He did not "
                "observe a plate number. The stolen .38 revolver was entered into LEADS/NCIC as stolen. Area 5 detectives are canvassing "
                "the block for additional surveillance footage and checking pawn databases for the Rolex and laptop."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 25 March 2026, at approximately 2105 hours, two masked male offenders committed a home invasion at 6218 N. Canfield "
                "Avenue (016th District, Norwood Park), targeting elderly victims Harold Jorgensen (82) and Eleanor Jorgensen (79). The "
                "offenders forced entry through the rear kitchen door, confronted the couple at gunpoint (chrome revolver), and zip-tied "
                "their wrists. Harold was pistol-whipped when he resisted, sustaining a facial laceration and possible fractured orbital "
                "bone; he was transported to Advocate Lutheran General. The offenders ransacked the home over approximately 12 minutes, "
                "taking items valued at $25,100 including a wedding ring set ($8,500), Rolex Submariner ($12,000), registered .38 S&W "
                "revolver (serial #SAW-77231), $2,300 cash, and a Dell laptop. Offender #1: B/M, 25-30, 6'2\", heavy build, armed. "
                "Offender #2: B/M, 20-25, 5'8\", slim. Both fled through the backyard toward the alley. Evidence includes a size 12 "
                "Nike Air Max shoe impression, tool marks from the door frame, and a zip-tie submitted for touch DNA (Lab Case "
                "#2026-032510). A neighbor observed a dark sedan (possible Nissan Altima) idling in the alley at 2045 hours. The stolen "
                "revolver was entered into LEADS/NCIC. Canvass for surveillance and pawn database checks are underway."
            ),
            "key_facts": [
                "Date/time: 25 March 2026, approximately 2105 hours",
                "Location: 6218 N. Canfield Avenue, 016th District, Norwood Park",
                "Victims: Harold Jorgensen (82) — pistol-whipped, facial laceration, possible fractured orbital; Eleanor Jorgensen (79) — uninjured",
                "Two offenders: #1 B/M 25-30, 6'2\", heavy, chrome revolver; #2 B/M 20-25, 5'8\", slim, collected items in pillowcase",
                "Forced entry through rear kitchen door (kicked in); victims zip-tied",
                "Total loss $25,100: wedding ring set, Rolex watch, registered .38 revolver (serial #SAW-77231), $2,300 cash, Dell laptop",
                "Evidence: size 12 Nike Air Max shoe impression, tool marks, zip-tie for touch DNA (Lab Case #2026-032510)",
                "Neighbor observed dark sedan (possible Nissan Altima) idling in alley at 2045 hours",
                "Stolen revolver entered into LEADS/NCIC",
                "Offenders inside approximately 12 minutes; fled through backyard to alley"
            ],
            "difficulty": "hard",
            "reference": "CPD General Order G06-01-01; Home Invasion Investigation; 720 ILCS 5/19-6",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 6. Carjacking Pattern (Series of 3) ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Carjacking Pattern — Three Linked Incidents in Area 3",
            "content": (
                "Between 10 March and 16 March 2026, three carjackings with a consistent MO occurred within the 014th and 019th Districts "
                "(Area 3). Crime Pattern #CP-2026-0318 was established by Area 3 Crime Analysts. Incident #1: On 10 March 2026 at "
                "approximately 2215 hours, victim Angela Torres (H/F, DOB 12 Jun 1988) was carjacked at gunpoint while parking her "
                "2022 white Honda Accord (IL plate DT4-2389) in front of her residence at 2744 N. Sawyer Avenue (014th District). Two "
                "male offenders approached on foot from the east, one brandishing a black handgun. They ordered Torres out of the "
                "vehicle and fled westbound on Sawyer. The vehicle was recovered 18 hours later at 4200 W. Jackson Boulevard (011th "
                "District), stripped of its catalytic converter, wheels, and stereo system.\n\n"
                "Incident #2: On 13 March 2026 at approximately 2140 hours, victim David Park (M/A, DOB 25 Sep 1995) was carjacked while "
                "sitting in his 2023 black Toyota RAV4 (IL plate AP7-8812) in the Mariano's parking lot at 3030 N. Broadway (019th "
                "District). Two male offenders — matching the general description from Incident #1 — approached the driver's side. One "
                "pointed a handgun at Park through the window and ordered him out. Park complied and the offenders drove the RAV4 "
                "eastbound out of the lot. The vehicle has not been recovered. Parking lot surveillance captured the offenders arriving "
                "on foot from northbound Broadway at 2133 hours.\n\n"
                "Incident #3: On 16 March 2026 at approximately 2050 hours, victim Rachel Stein (W/F, DOB 04 Feb 2000) was carjacked "
                "at 2900 N. Sheffield Avenue (019th District) while unloading groceries. Two male offenders, one armed with a handgun, "
                "approached from a dark-colored Hyundai Elantra that pulled alongside her 2024 red Kia Sportage (IL plate KS3-1106). "
                "Stein dropped her keys and the unarmed offender picked them up, entered the Kia, and both vehicles fled southbound "
                "on Sheffield. The Kia was recovered two days later at 5500 S. Pulaski Road (008th District) with altered VIN plates. "
                "Across all three incidents, the offenders are consistently described as two B/M, both 18-22, one approximately 5'9\" "
                "and one approximately 6'1\", both wearing dark hoodies. The armed offender in all three incidents displayed a handgun "
                "described as a black semi-automatic. Area 3 detectives are coordinating with Vehicular Hijacking Task Force. Surveillance "
                "images from Incident #2 have been distributed. The dark Hyundai Elantra from Incident #3 is being run through plate "
                "readers and CPIC."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "Three linked carjackings (Crime Pattern #CP-2026-0318) occurred in the 014th and 019th Districts between 10-16 March "
                "2026, all between 2050-2215 hours. In each incident, two B/M offenders (18-22, one 5'9\" and one 6'1\", dark hoodies, "
                "one armed with a black semi-automatic handgun) approached victims at or near their vehicles and took the cars at "
                "gunpoint. Incident #1 (10 Mar, 2744 N. Sawyer, 014th): white 2022 Honda Accord taken from Angela Torres; recovered "
                "stripped at 4200 W. Jackson. Incident #2 (13 Mar, 3030 N. Broadway, 019th): black 2023 Toyota RAV4 taken from David "
                "Park; not recovered; parking lot surveillance captured offenders arriving on foot. Incident #3 (16 Mar, 2900 N. "
                "Sheffield, 019th): red 2024 Kia Sportage taken from Rachel Stein; recovered at 5500 S. Pulaski with altered VIN "
                "plates; offenders arrived in a dark Hyundai Elantra. No victims were physically injured. Area 3 is coordinating with "
                "the Vehicular Hijacking Task Force. Surveillance images from Incident #2 have been distributed. The Hyundai Elantra "
                "is being run through plate readers and CPIC."
            ),
            "key_facts": [
                "Three linked carjackings, Crime Pattern #CP-2026-0318, 014th and 019th Districts, 10-16 March 2026",
                "Consistent MO: two B/M offenders (18-22), one armed with black semi-automatic, dark hoodies, evening hours",
                "Incident #1: 10 Mar, 2215 hrs, 2744 N. Sawyer — white 2022 Honda Accord, recovered stripped at 4200 W. Jackson",
                "Incident #2: 13 Mar, 2140 hrs, 3030 N. Broadway — black 2023 Toyota RAV4, not recovered; surveillance captured offenders",
                "Incident #3: 16 Mar, 2050 hrs, 2900 N. Sheffield — red 2024 Kia Sportage, recovered with altered VIN at 5500 S. Pulaski",
                "In Incident #3, offenders used a dark Hyundai Elantra as a follow vehicle",
                "No victims physically injured across all three incidents",
                "Coordinating with Vehicular Hijacking Task Force; surveillance stills distributed",
                "Hyundai Elantra being run through plate readers and CPIC"
            ],
            "difficulty": "hard",
            "reference": "CPD Special Order S04-16; Vehicular Hijacking Investigation; Pattern Crime Response",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 7. Sexual Assault with Digital Evidence ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Criminal Sexual Assault — Digital Evidence Recovery",
            "content": (
                "On 20 March 2026, at approximately 0930 hours, a walk-in victim, Brianna Wallace (B/F, DOB 17 Oct 2001, age 24), "
                "presented at the Area 4 Detective Division to report a criminal sexual assault that occurred the previous evening. "
                "Wallace stated that on 19 March 2026, at approximately 2300 hours, she attended a house party at 1425 S. Christiana "
                "Avenue (010th District). She was introduced to the offender, later identified as Marcus Tate (B/M, DOB 08 Aug 1998, "
                "age 27), by a mutual acquaintance. Wallace reported that Tate provided her with a mixed drink that she believes was "
                "drugged because she began feeling disoriented and unable to control her movements within 30 minutes. She stated that "
                "Tate led her to an upstairs bedroom where he sexually assaulted her. She recalls partial details of the assault but has "
                "significant memory gaps consistent with drug-facilitated sexual assault.\n\n"
                "Wallace woke at approximately 0500 hours on 20 March in the same bedroom, alone. She left the residence and called a "
                "friend for transport. She did not shower or change clothes before reporting. At the hospital, a SAFE exam was conducted "
                "at Stroger Hospital by SANE Nurse Jennifer Liu at 1115 hours (SAFE Kit #2026-SA-0434). A urine sample was collected for "
                "toxicology screening. The kit and samples were transferred to the Illinois State Police Crime Lab.\n\n"
                "Digital evidence is significant in this case. Wallace provided her iPhone, which contained text message exchanges with "
                "Tate on Instagram from 19 March in which Tate invited her to the party and told her to \"come find me when you get "
                "there.\" After the assault, at 0247 hours on 20 March, Tate sent Wallace a message reading \"u were so wasted lol hope "
                "u got home safe.\" Additionally, the mutual acquaintance, Keisha Brown (B/F, DOB 12 Mar 2000), provided a statement "
                "confirming she introduced Wallace and Tate and that she observed Tate handing Wallace a drink. Another partygoer, "
                "Darnell Simmons (B/M, DOB 22 Nov 1999), told detectives he saw Tate leading Wallace upstairs and that she appeared "
                "\"barely able to walk.\" SVU Detective Reyes (Star #5488) was assigned. An emergency preservation request was sent to "
                "Meta Platforms for Tate's Instagram account data. A search warrant for Tate's cell phone and the residence at 1425 S. "
                "Christiana is being drafted for judicial review."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 19 March 2026, at approximately 2300 hours, Brianna Wallace (B/F, 24) was sexually assaulted at a house party at "
                "1425 S. Christiana Avenue (010th District). The offender, Marcus Tate (B/M, 27), was introduced to Wallace by a mutual "
                "acquaintance and provided her with a drink believed to be drugged. Wallace reported disorientation, memory gaps, and "
                "partial recall of the assault consistent with a drug-facilitated sexual assault. She reported the next morning without "
                "having showered or changed. A SAFE exam was conducted at Stroger Hospital at 1115 hours (Kit #2026-SA-0434) and a urine "
                "sample was collected for toxicology. Digital evidence includes Instagram messages between Tate and Wallace (pre- and "
                "post-assault), including a post-assault message at 0247 hours: \"u were so wasted lol hope u got home safe.\" Witness "
                "Keisha Brown confirmed she introduced them and saw Tate hand Wallace a drink. Witness Darnell Simmons observed Tate "
                "leading Wallace upstairs while she appeared \"barely able to walk.\" SVU Detective Reyes is assigned. An emergency "
                "preservation request was sent to Meta for Tate's Instagram data, and a search warrant for Tate's phone and the "
                "residence is being drafted."
            ),
            "key_facts": [
                "Date/time: 19 March 2026, approximately 2300 hours",
                "Location: house party at 1425 S. Christiana Avenue, 010th District",
                "Victim: Brianna Wallace (B/F, 24); Offender: Marcus Tate (B/M, 27), identified by name",
                "Suspected drug-facilitated sexual assault — victim reports disorientation, memory gaps after consuming drink provided by Tate",
                "SAFE exam conducted at Stroger Hospital (Kit #2026-SA-0434); urine collected for toxicology",
                "Victim did not shower or change before reporting — evidence preserved",
                "Instagram messages: Tate's post-assault message at 0247 hours (\"u were so wasted lol hope u got home safe\")",
                "Witness Keisha Brown saw Tate hand victim a drink; Witness Darnell Simmons saw Tate leading impaired victim upstairs",
                "Emergency preservation request sent to Meta for Tate's Instagram data",
                "Search warrant for Tate's phone and the residence being drafted; SVU Detective Reyes assigned"
            ],
            "difficulty": "hard",
            "reference": "CPD Special Order S04-03; Sexual Assault Investigation; Digital Evidence Preservation",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 8. Arson Investigation at Commercial Building ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Arson Investigation — Commercial Building on Pulaski Road",
            "content": (
                "On 12 March 2026, at approximately 0312 hours, CFD Engine 83 and Truck 47 responded to a structure fire at Sunny Days "
                "Dry Cleaners, 4510 S. Pulaski Road (008th District). The fire was brought under control by 0345 hours. The business "
                "sustained severe fire and smoke damage to the rear storage area and moderate damage to the main customer service area. "
                "No injuries were reported. CFD Fire Investigator Tomczak determined the fire's origin to be in the rear storage room, "
                "specifically near a cluster of cleaning solvent containers along the south wall. Tomczak classified the fire as "
                "incendiary (arson) based on the following indicators: V-pattern burn marks on the south wall consistent with a liquid "
                "accelerant, the presence of two separate and distinct points of origin (south wall and east corner of the storage room), "
                "and a strong chemical odor inconsistent with the cleaning solvents typically stored on site.\n\n"
                "Accelerant detection canine \"Blaze\" (CFD K9 Unit) alerted to two areas in the storage room. Samples were collected "
                "from the floor and south wall (CFD Lab Sample #F-2026-0312-A through D) and submitted to the Illinois State Fire "
                "Marshal's Laboratory for gas chromatography-mass spectrometry (GC-MS) analysis. Preliminary field testing suggests "
                "the presence of gasoline. The building's rear door, which leads to the alley, showed signs of forced entry — the "
                "deadbolt hasp was pried and tool marks were visible on the door frame.\n\n"
                "The business owner, Hyun-soo Kim (M/A, DOB 30 Apr 1971), was contacted at his residence and responded to the scene. "
                "Kim stated the business was closed at approximately 2000 hours on 11 March and he was the last person to leave. He "
                "denied any knowledge of how the fire started and appeared cooperative. However, a preliminary records check revealed "
                "that Kim filed an insurance claim for a water damage loss at the same location 14 months prior, and a second insurance "
                "claim for a theft loss 8 months prior. Both claims were paid by Midwestern Mutual Insurance. Kim's current policy "
                "covers the structure and inventory for $375,000. Beat 0834 canvassed the alley and surrounding businesses. A private "
                "surveillance camera at the auto repair shop at 4514 S. Pulaski captured a figure in dark clothing approaching the rear "
                "of the dry cleaners at approximately 0258 hours. The figure appears to be carrying a container. Bomb and Arson Section "
                "Detective Callahan (Star #6102) is assigned. The insurance carrier has been notified and is conducting a parallel "
                "investigation."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 12 March 2026, at approximately 0312 hours, CFD responded to a structure fire at Sunny Days Dry Cleaners, 4510 S. "
                "Pulaski Road (008th District), which was classified as incendiary (arson) by CFD Fire Investigator Tomczak. The fire "
                "originated in the rear storage room with two separate points of origin, V-pattern burn marks consistent with liquid "
                "accelerant, and an unidentified chemical odor. The CFD accelerant detection canine alerted to two areas; floor and wall "
                "samples were collected for GC-MS analysis (preliminary: gasoline). The rear door was forcibly entered with tool marks "
                "on the frame. Business owner Hyun-soo Kim (M/A, 54) was cooperative but has two prior insurance claims on the same "
                "property in the past 14 months (water damage and theft), both paid by Midwestern Mutual. His current policy covers "
                "$375,000. Private surveillance from a neighboring business captured a figure in dark clothing carrying a container "
                "approaching the rear of the building at approximately 0258 hours. No injuries reported. Bomb and Arson Detective "
                "Callahan is assigned. The insurance carrier is conducting a parallel investigation."
            ),
            "key_facts": [
                "Date/time: 12 March 2026, approximately 0312 hours (fire reported)",
                "Location: Sunny Days Dry Cleaners, 4510 S. Pulaski Road, 008th District",
                "Fire classified as incendiary (arson): two points of origin, V-pattern burn marks, liquid accelerant indicators",
                "CFD accelerant detection canine alerted; samples collected for GC-MS analysis (preliminary: gasoline)",
                "Forced entry through rear door — deadbolt pried, tool marks on frame",
                "Owner Hyun-soo Kim (M/A, 54) has two prior insurance claims in past 14 months at the same location",
                "Current insurance policy covers $375,000 for structure and inventory",
                "Private surveillance captured a figure in dark clothing with a container approaching the rear at 0258 hours",
                "No injuries reported; Bomb and Arson Detective Callahan assigned",
                "Insurance carrier conducting parallel investigation"
            ],
            "difficulty": "hard",
            "reference": "CPD Special Order S04-05; Arson Investigation; Coordination with CFD Office of Fire Investigation",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 9. Drug Trafficking with Controlled Buy ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Narcotics Investigation — Controlled Buy on West Side",
            "content": (
                "On 21 March 2026, Narcotics Unit detectives from Area 4 conducted a controlled purchase of narcotics targeting Deshawn "
                "Carter (B/M, DOB 15 Jun 1993, age 32), who resides at 4812 W. Monroe Street, Apt 2F (011th District). Carter was "
                "identified through a two-month investigation initiated by multiple citizen complaints and street-level intelligence "
                "indicating Carter was distributing heroin and fentanyl from his apartment and the surrounding area along the 4800 "
                "block of W. Monroe.\n\n"
                "Confidential Informant #CI-2026-0084 (reliability established through three prior controlled buys resulting in two "
                "felony convictions) was searched pre-buy at 1430 hours, provided with $300 in pre-recorded CPD funds (serial numbers "
                "documented on Pre-Recorded Funds Log #PRF-2026-0321), and fitted with an audio/video recording device. The CI was "
                "driven to the vicinity of 4812 W. Monroe by Detective Ochoa (Star #4877) and surveillance was established by a "
                "four-detective team. At approximately 1452 hours, the CI entered the building and proceeded to Apt 2F. Audio/video "
                "recordings captured the CI purchasing 10 individually packaged bags of a white powder substance from Carter in exchange "
                "for the $300 in pre-recorded funds. Carter was observed on the recording retrieving the bags from a black duffel bag "
                "in a bedroom closet.\n\n"
                "The CI was recovered at 1505 hours and searched post-buy. The 10 bags were recovered and field-tested positive for "
                "fentanyl (NIK Test Kit, presumptive positive). The substance was inventoried (CPD Inventory #2026-032107, net weight "
                "4.8 grams) and submitted to the Illinois State Police Crime Lab for confirmatory analysis (ISP Lab #2026-N-4412). "
                "Detective Ochoa drafted an affidavit for a search warrant for 4812 W. Monroe, Apt 2F, seeking additional narcotics, "
                "paraphernalia, currency, records, and firearms. ASA Brennan reviewed the affidavit and approved it for judicial "
                "presentation. A search warrant was issued by Judge Delgado (Warrant #SW-2026-3218) at 1645 hours. The warrant "
                "execution is scheduled for 22 March 2026 at 0600 hours. The tactical plan includes a five-officer entry team, "
                "two-officer rear containment, and coordination with Area 4 Evidence Technicians."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 21 March 2026, Area 4 Narcotics detectives conducted a controlled buy targeting Deshawn Carter (B/M, 32) at "
                "4812 W. Monroe Street, Apt 2F (011th District). Carter was identified through a two-month investigation based on "
                "citizen complaints and street-level intelligence for heroin/fentanyl distribution. Confidential Informant #CI-2026-0084 "
                "(three prior buys, two convictions) was searched, provided $300 in pre-recorded funds (Log #PRF-2026-0321), and equipped "
                "with audio/video. At approximately 1452 hours, the CI purchased 10 bags of white powder from Carter in Apt 2F; the "
                "transaction was recorded including Carter retrieving the bags from a black duffel bag in a bedroom closet. The substance "
                "field-tested positive for fentanyl (4.8 grams net, Inventory #2026-032107, ISP Lab #2026-N-4412). ASA Brennan approved "
                "the affidavit and Judge Delgado issued Search Warrant #SW-2026-3218 at 1645 hours for Apt 2F. Warrant execution is "
                "scheduled for 22 March 2026 at 0600 hours with a five-officer entry team, two-officer rear containment, and ET "
                "coordination."
            ),
            "key_facts": [
                "Date: 21 March 2026; controlled buy at approximately 1452 hours",
                "Target: Deshawn Carter (B/M, 32), 4812 W. Monroe Street, Apt 2F, 011th District",
                "Two-month investigation based on citizen complaints and street intel — heroin and fentanyl distribution",
                "CI #CI-2026-0084 (three prior buys, two convictions) — searched pre/post-buy, equipped with audio/video",
                "$300 pre-recorded funds provided (Log #PRF-2026-0321); CI purchased 10 bags from Carter in Apt 2F",
                "Substance field-tested positive for fentanyl, 4.8 grams net weight (Inventory #2026-032107, ISP Lab #2026-N-4412)",
                "Recording captured Carter retrieving bags from black duffel bag in bedroom closet",
                "ASA Brennan approved affidavit; Judge Delgado issued Warrant #SW-2026-3218 at 1645 hours",
                "Warrant execution scheduled 22 March 2026 at 0600 hours: five-officer entry, two-officer rear, ET on standby"
            ],
            "difficulty": "medium",
            "reference": "CPD Special Order S09-03; Narcotics Investigation; Controlled Purchase Procedures",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 10. Missing Person (Young Adult, Suspicious Circumstances) ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Missing Person Under Suspicious Circumstances — Lincoln Park",
            "content": (
                "On 23 March 2026, at approximately 1815 hours, Natasha Volkov (W/F, DOB 04 Dec 2003, age 22) was reported missing by "
                "her roommate, Sophie Andersen (W/F, DOB 19 Mar 2002), at the 018th District station. Andersen stated that Volkov, a "
                "graduate student at DePaul University, left their shared apartment at 2238 N. Seminary Avenue at approximately 2100 "
                "hours on 22 March 2026 to meet someone and has not returned or been heard from since. Volkov's phone goes directly to "
                "voicemail and her location sharing, which is normally active on the Find My app, shows her phone was last active at "
                "2147 hours on 22 March in the vicinity of Fullerton Avenue and the lakefront.\n\n"
                "Andersen described the circumstances as highly unusual and provided several concerning details. Volkov had recently "
                "ended a relationship with ex-boyfriend Ryan Gallagher (W/M, DOB 11 Jul 2001, age 24), who had become increasingly "
                "controlling and had sent threatening text messages after the breakup, including one on 20 March reading \"you'll regret "
                "this\" and another on 21 March reading \"I know where you go at night.\" Andersen also stated that Volkov mentioned she "
                "was meeting \"someone from school\" on 22 March but did not specify who. Volkov left wearing a green jacket, black "
                "leggings, and white Nike running shoes. She carried a tan crossbody purse and her iPhone 15 in a blue case.\n\n"
                "Detective Navarro (Star #5921) was assigned and classified the case as high-risk based on the threatening communications, "
                "the abrupt loss of phone contact, and the out-of-character behavior. Navarro contacted DePaul University Campus Security, "
                "which confirmed Volkov did not attend her 0900 class on 23 March. An emergency ping request was submitted to Apple for "
                "the phone's last known location data. A BOLO was broadcast with Volkov's description and photo. Beat 1824 canvassed "
                "the Fullerton and lakefront area with negative results. Ryan Gallagher was contacted and agreed to come to the Area for "
                "an interview; his initial statement is that he was at his apartment in Wicker Park all evening on 22 March. Detectives "
                "are obtaining surveillance footage from CTA stations near Fullerton, requesting Volkov's phone records from her carrier, "
                "and coordinating with DePaul to identify who she may have been meeting."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 23 March 2026, Natasha Volkov (W/F, 22), a DePaul University graduate student, was reported missing by her roommate "
                "after failing to return from a 22 March outing. Volkov left her apartment at 2238 N. Seminary Avenue (018th District) "
                "at approximately 2100 hours on 22 March to meet \"someone from school\" and has not been heard from since. Her phone "
                "was last active at 2147 hours near Fullerton Avenue and the lakefront, and now goes directly to voicemail. The case is "
                "classified as high-risk due to threatening text messages from ex-boyfriend Ryan Gallagher (W/M, 24), including "
                "\"you'll regret this\" (20 March) and \"I know where you go at night\" (21 March), the abrupt loss of phone contact, "
                "and out-of-character behavior. Gallagher agreed to an interview and claims he was at his Wicker Park apartment all "
                "evening. Volkov did not attend her 0900 class on 23 March. She was last seen wearing a green jacket, black leggings, "
                "and white Nike shoes, carrying a tan crossbody purse. A BOLO has been broadcast. An emergency Apple ping request was "
                "submitted. Detectives are pulling CTA surveillance near Fullerton, requesting phone records, and coordinating with "
                "DePaul to identify who Volkov planned to meet."
            ),
            "key_facts": [
                "Missing person: Natasha Volkov (W/F, 22), DePaul graduate student",
                "Last seen 22 March 2026 at approximately 2100 hours leaving 2238 N. Seminary Avenue, 018th District",
                "Phone last active at 2147 hours near Fullerton Avenue and the lakefront; now goes to voicemail",
                "Left to meet unidentified \"someone from school\" — did not specify who",
                "Ex-boyfriend Ryan Gallagher sent threatening texts: \"you'll regret this\" and \"I know where you go at night\"",
                "Classified high-risk: threatening communications, abrupt phone loss, out-of-character absence",
                "Gallagher claims he was at his Wicker Park apartment; agreed to interview",
                "Volkov missed 0900 class on 23 March; description: green jacket, black leggings, white Nike shoes, tan crossbody purse",
                "BOLO broadcast; emergency Apple ping submitted; CTA surveillance and phone records being requested",
                "DePaul coordination underway to identify who she was meeting"
            ],
            "difficulty": "hard",
            "reference": "CPD Special Order S06-01; Missing Person Investigation; High-Risk Classification Criteria",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 11. Identity Theft / Financial Fraud Ring ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Identity Theft / Financial Fraud Ring — Multi-Victim Investigation",
            "content": (
                "Between January and March 2026, the Area 3 Financial Crimes Unit received 14 separate identity theft complaints "
                "from victims residing in the 019th, 020th, and 024th Districts. Detective Hagen (Star #4533) identified a common "
                "pattern: all 14 victims had their personal information — full names, dates of birth, Social Security numbers, and "
                "home addresses — used to open fraudulent credit card accounts, obtain auto loans, and file false tax returns. "
                "Combined financial losses across all victims exceed $218,000. Seven victims reported that their credit monitoring "
                "services first flagged unauthorized activity between 15 January and 10 February 2026.\n\n"
                "Investigation revealed that 11 of the 14 victims were patients of Northshore Medical Associates, located at 5730 "
                "N. Clark Street (020th District). A review of the medical practice's records, conducted with the cooperation of "
                "practice administrator Dr. Linda Choi, identified a former employee, Reginald \"Reggie\" Boone (B/M, DOB 22 Sep 1988, "
                "age 37, LKA 7200 N. Sheridan Road, Apt 14C), who worked as a medical records clerk from June 2024 until his "
                "termination on 05 January 2026 for excessive tardiness. Boone had unrestricted access to patient records containing "
                "PII during his employment. Digital forensic analysis of the practice's system logs, conducted by CPD DTEC Unit, "
                "showed that Boone accessed over 200 patient records in the two weeks before his termination, far exceeding his "
                "normal workflow of 15-20 records per day.\n\n"
                "Financial institution subpoena returns from Chase, Capital One, and Discover revealed that the fraudulent credit "
                "card applications were submitted online from three IP addresses traced to public Wi-Fi locations in Rogers Park: "
                "a Starbucks at 6753 N. Sheridan Road, a public library branch at 6907 N. Clark Street, and a McDonald's at 7036 "
                "N. Clark Street. Surveillance footage from the Starbucks on 22 January 2026 shows an individual matching Boone's "
                "description using a laptop during the timeframe of two fraudulent applications. Three fraudulent credit cards were "
                "used to purchase electronics totaling $34,500 at Best Buy locations in Evanston and Skokie; store surveillance is "
                "being requested. ASA Rivera has been consulted and recommends charges of Identity Theft (720 ILCS 5/16-30), "
                "Aggravated Identity Theft (720 ILCS 5/16-30(b)), and Wire Fraud (18 U.S.C. 1343) given the interstate nature of "
                "the credit card applications. An arrest warrant is being sought."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "Between January and March 2026, 14 identity theft victims in the 019th, 020th, and 024th Districts reported a combined "
                "loss exceeding $218,000 from fraudulent credit cards, auto loans, and false tax returns filed using their PII. "
                "Investigation identified Reginald Boone (B/M, 37, LKA 7200 N. Sheridan Road, Apt 14C), a former medical records "
                "clerk at Northshore Medical Associates (5730 N. Clark Street, 020th District), as the primary suspect. Boone was "
                "terminated on 05 January 2026 and had unrestricted PII access; system logs show he accessed over 200 patient records "
                "in his final two weeks, far above his normal 15-20 per day. Eleven of 14 victims were patients at the practice. "
                "Subpoena returns from Chase, Capital One, and Discover traced fraudulent applications to three public Wi-Fi locations "
                "in Rogers Park. Starbucks surveillance from 22 January shows an individual matching Boone using a laptop during two "
                "fraudulent applications. Fraudulent cards were used to purchase $34,500 in electronics at Best Buy locations in "
                "Evanston and Skokie. ASA Rivera recommends Identity Theft, Aggravated Identity Theft, and federal Wire Fraud charges. "
                "An arrest warrant is being sought."
            ),
            "key_facts": [
                "14 identity theft victims across 019th, 020th, and 024th Districts; combined loss exceeding $218,000",
                "Fraudulent credit cards, auto loans, and false tax returns filed using stolen PII",
                "Primary suspect: Reginald Boone (B/M, 37), former medical records clerk at Northshore Medical Associates",
                "Boone terminated 05 January 2026; had unrestricted access to patient PII",
                "System logs show Boone accessed 200+ patient records in final two weeks (normal: 15-20/day)",
                "11 of 14 victims were patients at the same medical practice",
                "Fraudulent applications traced to three public Wi-Fi locations in Rogers Park via IP addresses",
                "Starbucks surveillance shows individual matching Boone during timeframe of two fraudulent applications",
                "$34,500 in electronics purchased with fraudulent cards at Best Buy in Evanston and Skokie",
                "ASA recommends Identity Theft, Aggravated Identity Theft, and Wire Fraud charges; arrest warrant being sought"
            ],
            "difficulty": "hard",
            "reference": "CPD Financial Crimes Investigation; 720 ILCS 5/16-30; 18 U.S.C. 1343",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 12. Officer-Involved Shooting Review ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Officer-Involved Shooting Review — Foot Pursuit in Englewood",
            "content": (
                "On 27 March 2026, at approximately 1542 hours, Officers Miguel Santiago (Star #11247, Unit 007, Beat 0733) and "
                "Brenda Hawkins (Star #11890, Unit 007, Beat 0733) were on routine patrol in a marked squad car in the 6600 block "
                "of S. Halsted Street (007th District). Officers observed a male, later identified as Terrence Williams (B/M, DOB "
                "03 Mar 2002, age 24), standing on the corner of 66th and Halsted who, upon seeing the squad car, immediately turned "
                "and ran eastbound through a vacant lot. Officer Santiago observed Williams reach toward his waistband with his right "
                "hand during the initial moments of his flight. Both officers exited their vehicle and pursued on foot. Body-worn "
                "camera footage from both officers was activated.\n\n"
                "The foot pursuit covered approximately two blocks eastbound and then southbound through an alley behind the 6600 block "
                "of S. Green Street. At the south end of the alley, Williams turned and faced Officer Santiago from a distance of "
                "approximately 15 feet. BWC footage from Santiago shows Williams with a dark object in his right hand, which Santiago "
                "perceived to be a firearm. Santiago discharged his department-issued Glock 17 four times. Williams was struck twice "
                "— once in the right shoulder and once in the right hip. He fell to the ground and the object, a black Ruger SR9 "
                "9mm semi-automatic pistol (serial #337-08921), was recovered approximately 3 feet from his right hand. The weapon "
                "was loaded with 12 rounds in the magazine and one in the chamber. Williams is a convicted felon (2021 aggravated "
                "UUW, 2023 robbery) and is prohibited from possessing firearms.\n\n"
                "CFD Ambulance 53 transported Williams to the University of Chicago Medical Center in serious but stable condition. "
                "Officer Santiago was not physically injured. Both officers were separated at the scene per G03-06 protocols. COPA was "
                "notified at 1548 hours (COPA Log #2026-0001247). FOP representatives responded for both officers. The scene was "
                "secured and processed by ET Morrison (Star #8677). Four fired cartridge casings were recovered in the alley "
                "(consistent with Santiago's four reported discharges). The recovered Ruger was processed for fingerprints and DNA "
                "(Lab Case #2026-032709). BWC footage from both officers has been secured and transferred to COPA. The Area Deputy "
                "Chief, Detective Division Chief, and the Superintendent's Office were notified per chain of command requirements. "
                "A Tactical Response Report (TRR) was completed by Officer Santiago."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 27 March 2026, at approximately 1542 hours, Officer Santiago (Star #11247, Beat 0733) discharged his Glock 17 four "
                "times at Terrence Williams (B/M, 24) during a foot pursuit in the 007th District. The encounter began when Williams "
                "fled from officers at 66th and Halsted, reaching toward his waistband. After a two-block foot pursuit through alleys, "
                "Williams turned and faced Santiago at approximately 15 feet with a dark object in his right hand. Santiago discharged "
                "four rounds, striking Williams in the right shoulder and right hip. A loaded Ruger SR9 9mm (serial #337-08921, 12+1 "
                "rounds) was recovered 3 feet from Williams's hand. Williams is a convicted felon (2021 aggravated UUW, 2023 robbery) "
                "prohibited from firearm possession. He was transported to U of C Medical Center in serious but stable condition. "
                "Santiago was not injured. Both officers were separated per G03-06; BWC footage from both was active and has been "
                "transferred to COPA (Log #2026-0001247, notified at 1548 hours). FOP responded for both officers. Four casings were "
                "recovered, consistent with reported discharges. The Ruger was submitted for prints and DNA (Lab Case #2026-032709). "
                "Chain of command notifications were completed and a TRR was filed."
            ),
            "key_facts": [
                "Date/time: 27 March 2026, approximately 1542 hours",
                "Location: alley behind 6600 block of S. Green Street, 007th District",
                "Involved officer: Santiago (Star #11247), Glock 17, four rounds discharged, two strikes (right shoulder, right hip)",
                "Subject: Terrence Williams (B/M, 24), convicted felon (2021 agg UUW, 2023 robbery), prohibited from firearm possession",
                "Williams fled on foot, reached toward waistband, then turned and faced officer with dark object at approximately 15 feet",
                "Recovered: loaded Ruger SR9 9mm (serial #337-08921, 12+1 rounds), 3 feet from Williams's hand",
                "Williams transported to U of C Medical Center, serious but stable; Santiago not injured",
                "BWC active on both officers; footage transferred to COPA (Log #2026-0001247, notified 1548 hours)",
                "Officers separated per G03-06; FOP responded; four casings recovered; TRR completed",
                "Chain of command notified (Area Deputy Chief, Detective Division Chief, Superintendent's Office)"
            ],
            "difficulty": "hard",
            "reference": "CPD General Order G03-06; Officer-Involved Shooting Procedures; COPA Notification Requirements",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 13. Gang-Related Drive-By Shooting ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Gang-Related Drive-By Shooting — Austin District",
            "content": (
                "On 29 March 2026, at approximately 2038 hours, ShotSpotter detected 14 rounds fired in the 5100 block of W. "
                "Congress Parkway (015th District, Beat 1522). Beat 1522 and Beat 1524 responded and found two male victims on the "
                "sidewalk in front of 5134 W. Congress Parkway. Victim #1, Jerome Davis (B/M, DOB 29 Jan 2004, age 22), sustained "
                "gunshot wounds to the torso and left leg and was transported by CFD Ambulance 15 to Stroger Hospital in critical "
                "condition. Victim #2, Antonio Reeves (B/M, DOB 14 Aug 2005, age 20), sustained a gunshot wound to the right arm "
                "and was transported to Mount Sinai Hospital in good condition.\n\n"
                "Witness #1, who requested anonymity and is identified as CW-1 in reports, stated from a second-floor window of "
                "5136 W. Congress that a dark blue or black four-door sedan, possibly a Chevy Malibu (2015-2019 model), slowed in "
                "front of the location and a rear-seat passenger extended a firearm out of the right rear window and fired multiple "
                "shots at the group of males standing on the sidewalk. The vehicle then accelerated westbound on Congress. CW-1 could "
                "not see the shooter clearly but described a \"young black male with short hair.\" Witness #2, a Pace bus driver operating "
                "Route 126, was stopped at a red light at Congress and Laramie and observed the vehicle fleeing westbound at high speed. "
                "He described the vehicle as a dark-colored Chevy Malibu with tinted windows and noted a partial rear plate — \"Illinois, "
                "starts with J.\"\n\n"
                "ET Brooks (Star #7219) processed the scene and recovered 14 fired cartridge casings — 9 from the street and 5 from "
                "the sidewalk — all consistent with 9mm Luger (Lab Case #2026-032905, submitted for NIBIN). Three bullet impact marks "
                "were documented on the building facade at 5134 W. Congress. A POD camera at Congress and Cicero (two blocks east) "
                "captured the dark sedan traveling westbound at 2037 hours. Gang Intelligence reports that the 5100 block of Congress "
                "is claimed by the Conservative Vice Lords, and both victims are documented members. Recent intelligence indicates "
                "an ongoing conflict between the CVL faction at this location and a Four Corner Hustlers faction based around the "
                "5400 block of W. Jackson. Two FCH members — Marquis Brown (B/M, DOB 11 Nov 2001) and Darius Reed (B/M, DOB 05 Apr "
                "2003) — have been identified by Gang Intelligence as persons of interest based on prior ShotSpotter-linked incidents "
                "and social media posts referencing the Congress Parkway CVL set. Area 4 detectives are assigned and coordinating with "
                "Gang Investigation Section."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 29 March 2026, at approximately 2038 hours, a drive-by shooting occurred at 5134 W. Congress Parkway (015th "
                "District) with 14 rounds detected by ShotSpotter. Two victims: Jerome Davis (B/M, 22, documented CVL member) — "
                "critical condition with gunshot wounds to the torso and left leg (Stroger Hospital); Antonio Reeves (B/M, 20, "
                "documented CVL member) — good condition with a gunshot wound to the right arm (Mount Sinai). A rear-seat passenger "
                "in a dark blue/black Chevy Malibu (2015-2019, tinted windows) fired from the right rear window. The vehicle fled "
                "westbound on Congress. A Pace bus driver observed the vehicle and provided a partial plate (Illinois, starts with "
                "\"J\"). A POD camera at Congress and Cicero captured the sedan at 2037 hours. ET Brooks recovered 14 cartridge casings "
                "(9mm Luger) submitted for NIBIN (Lab Case #2026-032905) and documented three bullet impacts on the building facade. "
                "Gang Intelligence identifies this as a CVL vs. Four Corner Hustlers conflict; persons of interest Marquis Brown and "
                "Darius Reed (FCH members) are identified based on prior ShotSpotter incidents and social media. Area 4 detectives "
                "are coordinating with Gang Investigation Section."
            ),
            "key_facts": [
                "Date/time: 29 March 2026, approximately 2038 hours; ShotSpotter detected 14 rounds",
                "Location: 5134 W. Congress Parkway, 015th District",
                "Victim #1: Jerome Davis (B/M, 22), GSW to torso and left leg, critical at Stroger; documented CVL",
                "Victim #2: Antonio Reeves (B/M, 20), GSW to right arm, good condition at Mount Sinai; documented CVL",
                "Suspect vehicle: dark blue/black Chevy Malibu (2015-2019), tinted windows, partial plate \"J\" (Illinois)",
                "Rear-seat passenger fired from right rear window; vehicle fled westbound on Congress",
                "14 casings recovered (9mm Luger), submitted for NIBIN; three bullet impacts on building facade",
                "POD camera at Congress and Cicero captured vehicle at 2037 hours",
                "Gang conflict: CVL (5100 Congress) vs. Four Corner Hustlers (5400 W. Jackson)",
                "Persons of interest: Marquis Brown and Darius Reed (FCH), identified via prior ShotSpotter incidents and social media"
            ],
            "difficulty": "hard",
            "reference": "CPD Special Order S09-05; Gang-Related Shooting Investigation; ShotSpotter/NIBIN Procedures",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 14. Child Abuse / Neglect Investigation ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Child Abuse and Neglect — DCFS Cross-Report Investigation",
            "content": (
                "On 17 March 2026, at approximately 1030 hours, Area 3 SVU received a DCFS cross-report (Hotline #2026-CR-04122) "
                "regarding suspected physical abuse of a minor child. The report was initiated by mandatory reporter Dr. Elena "
                "Vasquez, a pediatrician at Lurie Children's Hospital, who examined the child, Jaylen Morris (B/M, DOB 08 Oct 2020, "
                "age 5), during an emergency visit on 16 March 2026. Dr. Vasquez documented the following injuries inconsistent with "
                "the caretaker's explanation: bruising in various stages of healing on the child's back and buttocks (patterned "
                "bruising consistent with a belt or strap), a healing fracture of the left forearm (approximately 2-3 weeks old based "
                "on X-ray), and a circular burn mark on the child's right hand consistent with a cigarette burn. Dr. Vasquez stated "
                "in her report that the mother, Crystal Morris (B/F, DOB 14 May 1995, age 30, residing at 4418 N. Sheridan Road, "
                "Apt 3B, 023rd District), initially stated Jaylen fell off a bicycle to explain the bruises and fracture. When "
                "confronted with the medical findings, Morris changed her account and stated the child is \"clumsy\" and \"bruises "
                "easily.\"\n\n"
                "SVU Detective Okafor (Star #5344) and DCFS Investigator Terri Washington responded jointly. At the residence, the "
                "apartment was found in a state of severe disrepair: rotting food on counters, no functional smoke detectors, exposed "
                "electrical wiring in the bathroom, and a mattress on the floor with no bedding in the child's room. There was minimal "
                "food in the refrigerator. A second child in the home, Amara Morris (B/F, DOB 22 Jun 2023, age 2), was observed to be "
                "wearing an extremely soiled diaper and appeared underweight. Both children were taken into protective custody by DCFS. "
                "Crystal Morris's live-in boyfriend, Derek Hill (B/M, DOB 30 Nov 1990, age 35), was present and became agitated when "
                "questioned, stating \"I discipline that boy how my daddy disciplined me — ain't nothing wrong with that.\" Hill has a "
                "prior arrest for domestic battery (2022) and two prior DCFS indicated findings for inadequate supervision (2019, 2021) "
                "involving his biological children from a previous relationship.\n\n"
                "Both children were transported to Lurie Children's for full medical evaluations. Jaylen underwent a skeletal survey "
                "that revealed two additional healing rib fractures not previously identified. Amara's exam revealed no acute injuries "
                "but documented failure to thrive (below 3rd percentile for weight). The CAC (Chicago Children's Advocacy Center) was "
                "contacted to schedule a forensic interview with Jaylen. ASA Thornton was consulted and recommended charges of "
                "Aggravated Battery to a Child (720 ILCS 5/12-3.05(b)(1)) against Derek Hill. Felony Review is pending the forensic "
                "interview results."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 17 March 2026, Area 3 SVU received a DCFS cross-report (Hotline #2026-CR-04122) regarding physical abuse of "
                "Jaylen Morris (B/M, 5). The mandatory report was filed by Dr. Vasquez at Lurie Children's Hospital after documenting "
                "injuries inconsistent with the mother's explanation: patterned bruising on back/buttocks (belt/strap), a 2-3 week "
                "healing left forearm fracture, and a cigarette burn on the right hand. Mother Crystal Morris (30, 4418 N. Sheridan "
                "Road, Apt 3B, 023rd District) provided shifting explanations. Joint SVU/DCFS home visit revealed severe neglect "
                "conditions: rotting food, no smoke detectors, exposed wiring, minimal food, and a second child (Amara Morris, 2) in "
                "soiled clothing who appeared underweight. Live-in boyfriend Derek Hill (B/M, 35) made a spontaneous admission about "
                "physical discipline and has a prior domestic battery arrest (2022) and two DCFS indicated findings (2019, 2021). Both "
                "children were taken into protective custody. A skeletal survey of Jaylen revealed two additional healing rib fractures. "
                "Amara was diagnosed with failure to thrive (below 3rd percentile). CAC forensic interview is being scheduled for "
                "Jaylen. ASA Thornton recommends Aggravated Battery to a Child charges against Hill (720 ILCS 5/12-3.05(b)(1)); Felony "
                "Review is pending the forensic interview."
            ),
            "key_facts": [
                "DCFS cross-report (Hotline #2026-CR-04122) received 17 March 2026; mandatory reporter Dr. Vasquez, Lurie Children's",
                "Victim: Jaylen Morris (B/M, 5) — patterned bruising (belt/strap), healing forearm fracture, cigarette burn on right hand",
                "Mother Crystal Morris (30) provided inconsistent explanations; changed account when confronted",
                "Residence: severe neglect conditions — rotting food, no smoke detectors, exposed wiring, minimal food",
                "Second child: Amara Morris (B/F, 2) — soiled diaper, appeared underweight, failure to thrive (below 3rd percentile)",
                "Live-in boyfriend Derek Hill (B/M, 35) made spontaneous statement about physical discipline",
                "Hill has prior: domestic battery arrest (2022), two DCFS indicated findings (2019, 2021)",
                "Both children taken into protective custody; skeletal survey revealed two additional healing rib fractures in Jaylen",
                "CAC forensic interview being scheduled for Jaylen",
                "ASA recommends Aggravated Battery to a Child charges against Hill (720 ILCS 5/12-3.05(b)(1)); Felony Review pending"
            ],
            "difficulty": "hard",
            "reference": "CPD Special Order S06-02; Child Abuse Investigation; DCFS Cross-Report Procedures; 720 ILCS 5/12-3.05(b)(1)",
            "created_at": now,
            "updated_at": now,
        },
        # ---- 15. Cold Case Homicide with New DNA Evidence ----
        {
            "question_id": f"cs_{uuid.uuid4().hex[:12]}",
            "type": "case_summary",
            "category_id": "cat_case_summary",
            "category_name": "Detective Briefing Exercises",
            "title": "Cold Case Homicide — New DNA Hit in 2018 Pilsen Murder",
            "content": (
                "On 02 April 2026, the Illinois State Police Crime Lab notified Area 1 Cold Case Unit Detective Brennan (Star #3871) "
                "of a CODIS hit (CODIS Notification #2026-DNA-0891) linking biological evidence from the unsolved 2018 homicide of "
                "Maria Santos (H/F, DOB 20 Mar 1985, deceased 14 Sep 2018) to a known individual in the DNA database. Santos was found "
                "deceased on 14 September 2018 at approximately 0630 hours by a jogger in Harrison Park, 1824 S. Wood Street (012th "
                "District). The cause of death was determined by the Medical Examiner to be ligature strangulation, and the manner of "
                "death was ruled homicide (ME Case #2018-04872). At the time, evidence collected from under the victim's fingernails "
                "yielded a male DNA profile that did not match any known individual in CODIS. The case went cold after exhausting "
                "investigative leads in 2019.\n\n"
                "The CODIS hit identifies the DNA contributor as Victor Padilla (H/M, DOB 07 Dec 1982, age 43, current address 2650 "
                "W. Cermak Road, Apt 4A, per IDOC records). Padilla entered the CODIS system in November 2024 following his arrest and "
                "conviction for aggravated criminal sexual assault in DuPage County (Case #2024-CF-2291), for which he is currently "
                "serving a 12-year sentence at Stateville Correctional Center. A review of the original case file reveals that Padilla "
                "was never identified as a suspect or person of interest during the initial investigation. However, Padilla's 2018 "
                "address, obtained through CLEAR, was 1910 S. Throop Street — approximately four blocks from the crime scene in "
                "Harrison Park.\n\n"
                "Detective Brennan has requested the original evidence be re-submitted for updated DNA analysis with current STR "
                "methodology to confirm the CODIS match. The original fingernail scrapings (Evidence Inventory #2018-091406) are "
                "in the custody of the ISP Crime Lab. The original case detective, Detective Fuentes (now retired), has been contacted "
                "and agreed to meet to review his case notes. Original witnesses — including the victim's then-boyfriend Carlos Mendez "
                "(H/M, DOB 18 Apr 1984, who was investigated and cleared via alibi in 2018) and the victim's sister Ana Santos (H/F, "
                "DOB 12 Jul 1990) — will need to be re-interviewed. ASA Kowalski from the Cold Case Prosecution Unit has been assigned "
                "and requests a full case presentation before any contact with Padilla. Detective Brennan is coordinating with IDOC to "
                "arrange an interview with Padilla at Stateville. The victim's family has been notified that the case has been reopened."
            ),
            "question": "Review the case reports above. Write a concise factual summary presenting all key facts to your supervisor.",
            "model_answer": (
                "On 02 April 2026, a CODIS hit (Notification #2026-DNA-0891) linked DNA from the unsolved 2018 homicide of Maria Santos "
                "(H/F, 33 at time of death) to Victor Padilla (H/M, 43). Santos was found strangled (ligature strangulation, ME Case "
                "#2018-04872) in Harrison Park, 1824 S. Wood Street (012th District) on 14 September 2018. Male DNA recovered from under "
                "the victim's fingernails had no CODIS match at the time. Padilla entered CODIS in November 2024 after a DuPage County "
                "aggravated criminal sexual assault conviction (Case #2024-CF-2291); he is currently serving 12 years at Stateville. "
                "Padilla was never identified during the original investigation, but his 2018 address (1910 S. Throop Street) was "
                "approximately four blocks from the crime scene. The original evidence (Inventory #2018-091406) is being re-submitted "
                "for updated STR analysis to confirm the CODIS match. The retired case detective has agreed to consult. Original witnesses, "
                "including the cleared ex-boyfriend and the victim's sister, need re-interviewing. ASA Kowalski (Cold Case Unit) requests "
                "a full case presentation before Padilla is contacted. Detective Brennan is coordinating with IDOC for an interview at "
                "Stateville. The victim's family has been notified of the reopening."
            ),
            "key_facts": [
                "CODIS hit (Notification #2026-DNA-0891) received 02 April 2026 linking cold case evidence to Victor Padilla",
                "Victim: Maria Santos (H/F, 33 at death), found strangled in Harrison Park on 14 September 2018 (ME Case #2018-04872)",
                "Cause of death: ligature strangulation, ruled homicide",
                "DNA from victim's fingernail scrapings (Inventory #2018-091406) now matches Victor Padilla (H/M, 43)",
                "Padilla entered CODIS November 2024 after aggravated criminal sexual assault conviction in DuPage County",
                "Padilla currently serving 12 years at Stateville (Case #2024-CF-2291)",
                "Padilla's 2018 address was four blocks from the crime scene; never identified as suspect in original investigation",
                "Original evidence being re-submitted for updated STR analysis to confirm match",
                "Original witnesses (cleared ex-boyfriend Carlos Mendez, sister Ana Santos) need re-interviewing",
                "ASA Kowalski (Cold Case Unit) assigned; requests full case presentation before contact with Padilla"
            ],
            "difficulty": "hard",
            "reference": "CPD Cold Case Investigation Procedures; CODIS Hit Protocol; ISP Crime Lab Coordination",
            "created_at": now,
            "updated_at": now,
        },
    ]

    # Insert all questions with upsert
    inserted = 0
    for q in case_summary_questions:
        q.setdefault("updated_at", now)
        result = await db.questions.update_one(
            {"title": q["title"], "type": "case_summary"},
            {"$set": q},
            upsert=True,
        )
        if result.upserted_id or result.modified_count:
            inserted += 1

    print(f"  Seeded {inserted} case summary questions in 'cat_case_summary' category")
    print(f"  Total case_summary questions in DB: {await db.questions.count_documents({'type': 'case_summary'})}")
    return inserted


if __name__ == "__main__":
    asyncio.run(seed_case_summary())
