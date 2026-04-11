from fastapi import FastAPI, APIRouter, HTTPException, Depends, Cookie, Response, Header
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import httpx
import stripe

# Try to import emergentintegrations (only available on Emergent platform)
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    HAS_EMERGENT = True
except ImportError:
    HAS_EMERGENT = False
    LlmChat = None
    UserMessage = None

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Stripe configuration
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '').strip() or None
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
STRIPE_PRICE_ID = os.environ.get('STRIPE_PRICE_ID')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://detectiveexamstudyguide.com').strip()

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY.strip() if STRIPE_SECRET_KEY else None

print(f"STRIPE_WEBHOOK_SECRET set: {bool(STRIPE_WEBHOOK_SECRET)}")


# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix

class PaymentRecord(BaseModel):
    payment_id: str
    user_id: str
    stripe_session_id: str
    stripe_payment_intent: Optional[str] = None
    amount: int  # in cents
    currency: str = "usd"
    status: str  # pending, completed, failed
    created_at: datetime

api_router = APIRouter(prefix="/api")

# Current app version - UPDATE THIS WHEN RELEASING NEW VERSIONS
CURRENT_APP_VERSION = "1.5.0"
MINIMUM_REQUIRED_VERSION = "1.5.0"

# LLM Keys
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')

# ========== MODELS ==========

class User(BaseModel):
    user_id: str
    email: str  # Changed from EmailStr to allow usernames
    name: str
    picture: Optional[str] = None
    password_hash: Optional[str] = None
    role: str = "user"  # user or admin
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: str  # Changed from EmailStr to allow username
    password: str

class SessionDataResponse(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    session_token: str

class Category(BaseModel):
    category_id: str
    name: str
    description: str
    order: int = 0

class Question(BaseModel):
    question_id: str
    type: str  # flashcard, scenario, multiple_choice
    category_id: str
    category_name: str
    title: Optional[str] = None  # For flashcards/scenarios
    content: Optional[str] = None  # For flashcards/scenarios
    description: Optional[str] = None  # For complex scenarios
    question: Optional[str] = None  # For MCQs
    options: Optional[list] = None  # For MCQs
    correct_answers: Optional[list] = None  # For MCQs
    answer: Optional[str] = None
    model_answer: Optional[str] = None  # For complex scenarios
    explanation: Optional[str] = None
    difficulty: str = "medium"  # easy, medium, hard
    reference: Optional[str] = None  # e.g., "Illinois Compiled Statutes 720 ILCS 5/12-3"
    time_limit: Optional[int] = None  # For scenarios (in seconds)
    is_complex: Optional[bool] = False  # For multi-part scenarios
    parts: Optional[int] = 1  # Number of parts in scenario
    study_tip: Optional[str] = None  # Study tips/frameworks for scenarios
    created_at: datetime
    updated_at: datetime

class QuestionCreate(BaseModel):
    type: str
    category_id: str
    category_name: str
    title: str
    content: str
    answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: str = "medium"
    reference: Optional[str] = None

class UserProgress(BaseModel):
    progress_id: str
    user_id: str
    question_id: str
    bookmarked: bool = False
    attempts: int = 0
    last_score: Optional[float] = None
    last_attempted: Optional[datetime] = None
    created_at: datetime

class ScenarioResponse(BaseModel):
    response_id: str
    user_id: str
    question_id: str
    user_response: str
    ai_grade: Optional[float] = None
    ai_feedback: Optional[str] = None
    time_taken: int  # seconds
    submitted_at: datetime

class ScenarioSubmit(BaseModel):
    question_id: str
    user_response: str
    time_taken: int

class BookmarkToggle(BaseModel):
    question_id: str

class ChatbotMessage(BaseModel):
    question_id: str
    user_message: str
    conversation_history: List[Dict[str, str]] = []
    user_current_response: str = ""

class TTSRequest(BaseModel):
    text: str
    voice: str = "nova"  # alloy, echo, fable, onyx, nova, shimmer

class ChatbotResponse(BaseModel):
    bot_response: str
    hints_given: int = 0

class RankingSubmit(BaseModel):
    question_id: str
    user_order: List[int]  # User's ranking as list of item indices (0-based)
    time_taken: int  # seconds

class ExamAnswerSubmit(BaseModel):
    question_id: str
    selected_answer: str  # "A", "B", "C", or "D"
    time_taken: int  # seconds

class MiniScenarioSubmit(BaseModel):
    question_id: str
    user_response: str
    time_taken: int  # seconds

class FeedbackSubmit(BaseModel):
    response_id: str          # Links to the scenario_response
    question_id: str          # Which question/scenario
    feedback_type: str        # "incorrect_grade", "missing_info", "wrong_procedure", "general"
    user_message: str         # User's correction/suggestion

class FeedbackReview(BaseModel):
    status: str               # "approved" or "rejected"
    admin_notes: Optional[str] = None

# ========== AUTH HELPERS ==========

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

async def get_current_user(
    session_token: Optional[str] = Cookie(None),
    authorization: Optional[str] = Header(None)
) -> Optional[User]:
    # Try cookie first, then Authorization header
    token = session_token
    if not token and authorization:
        if authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
    
    if not token:
        return None
    
    session = await db.user_sessions.find_one(
        {"session_token": token},
        {"_id": 0}
    )
    
    if not session:
        return None
    
    # Check expiry with timezone-aware comparison
    expires_at = session["expires_at"]
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    if expires_at <= datetime.now(timezone.utc):
        await db.user_sessions.delete_one({"session_token": token})
        return None
    
    user_doc = await db.users.find_one(
        {"user_id": session["user_id"]},
        {"_id": 0}
    )
    
    if user_doc:
        return User(**user_doc)
    return None

async def require_user(user: Optional[User] = Depends(get_current_user)) -> User:
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

async def require_admin(user: User = Depends(require_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# ========== AUTH ENDPOINTS ==========

@api_router.post("/auth/register")
async def register(user_data: UserCreate):
    # Normalize email to lowercase
    email = user_data.email.lower()
    
    # Check if user exists
    existing = await db.users.find_one({"email": email}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = f"user_{uuid.uuid4().hex[:12]}"
    user = User(
        user_id=user_id,
        email=email,
        name=user_data.name,
        password_hash=hash_password(user_data.password),
        role="user",
        created_at=datetime.now(timezone.utc)
    )
    
    await db.users.insert_one(user.model_dump())
    
    # Create session
    session_token = f"session_{uuid.uuid4().hex}"
    await db.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=30),
        "created_at": datetime.now(timezone.utc)
    })
    
    response = JSONResponse(content={
        "user_id": user_id,
        "email": email,
        "name": user_data.name,
        "role": "user",
        "is_guest": False,
        "session_token": session_token
    })
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=30*24*60*60,
        path="/"
    )
    
    return response

@api_router.post("/auth/login")
async def login(credentials: UserLogin):
    # Check if this is a registered email user
    user_doc = await db.users.find_one({"email": credentials.email.lower()}, {"_id": 0})
    
    if user_doc:
        # Verify password for registered users
        if not user_doc.get("password_hash"):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not verify_password(credentials.password, user_doc["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        # No registered user found
        raise HTTPException(status_code=401, detail="Invalid credentials. Please register first or use Guest login.")
    
    # Create session
    session_token = f"session_{uuid.uuid4().hex}"
    await db.user_sessions.insert_one({
        "user_id": user_doc["user_id"],
        "session_token": session_token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=30),
        "created_at": datetime.now(timezone.utc)
    })
    
    response = JSONResponse(content={
        "user_id": user_doc["user_id"],
        "email": user_doc["email"],
        "name": user_doc.get("name", "User"),
        "role": user_doc.get("role", "user"),
        "is_guest": False,
        "session_token": session_token
    })
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=30*24*60*60,
        path="/"
    )
    
    return response

@api_router.post("/auth/guest")
async def guest_login():
    """Login as a guest user - progress is shared among all guests"""
    GUEST_USER_ID = "user_guest_detective"
    GUEST_EMAIL = "guest@cpd-study.app"
    GUEST_NAME = "Guest User"
    
    # Check if guest user exists, create if not
    user_doc = await db.users.find_one({"user_id": GUEST_USER_ID}, {"_id": 0})
    
    if not user_doc:
        user_doc = {
            "user_id": GUEST_USER_ID,
            "email": GUEST_EMAIL,
            "name": GUEST_NAME,
            "role": "guest",
            "created_at": datetime.now(timezone.utc)
        }
        await db.users.insert_one(user_doc)
    
    # Create session
    session_token = f"session_{uuid.uuid4().hex}"
    await db.user_sessions.insert_one({
        "user_id": GUEST_USER_ID,
        "session_token": session_token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc)
    })
    
    response = JSONResponse(content={
        "user_id": GUEST_USER_ID,
        "email": GUEST_EMAIL,
        "name": GUEST_NAME,
        "role": "guest",
        "is_guest": True,
        "session_token": session_token
    })
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7*24*60*60,
        path="/"
    )
    
    return response

@api_router.get("/auth/session-data")
async def get_session_data(x_session_id: str = Header(None)):
    """Exchange session_id from Google OAuth for session data"""
    if not x_session_id:
        raise HTTPException(status_code=422, detail="X-Session-ID header required")
    
    oauth_session_url = os.getenv("OAUTH_SESSION_DATA_URL", "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            oauth_session_url,
            headers={"X-Session-ID": x_session_id}
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid session ID")
        
        user_data = response.json()
    
    # Check if user exists by email
    existing_user = await db.users.find_one({"email": user_data["email"]}, {"_id": 0})
    
    if not existing_user:
        # Create new user
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        user = User(
            user_id=user_id,
            email=user_data["email"],
            name=user_data["name"],
            picture=user_data.get("picture"),
            role="user",
            created_at=datetime.now(timezone.utc)
        )
        await db.users.insert_one(user.model_dump())
    else:
        user_id = existing_user["user_id"]
    
    # Create session
    session_token = f"session_{uuid.uuid4().hex}"
    await db.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc)
    })
    
    return SessionDataResponse(
        id=user_id,
        email=user_data["email"],
        name=user_data["name"],
        picture=user_data.get("picture"),
        session_token=session_token
    )

@api_router.get("/auth/me")
async def get_me(user: User = Depends(require_user)):
    return {
        "user_id": user.user_id,
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
        "role": user.role
    }

@api_router.post("/auth/logout")
async def logout(response: Response, session_token: Optional[str] = Cookie(None)):
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    
    response.delete_cookie(key="session_token", path="/")
    return {"message": "Logged out"}

# ========== HEALTH CHECK ENDPOINT ==========
@api_router.get("/health")
async def health_check():
    """Health check endpoint for Railway/monitoring"""
    try:
        # Test database connection
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "tts_provider": "elevenlabs" if ELEVENLABS_API_KEY else ("openai" if (OPENAI_API_KEY or EMERGENT_LLM_KEY) else "none"),
        }
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

@api_router.post("/migrate-reaction-answers")
async def migrate_reaction_answers():
    """One-time migration: convert flat modelAnswer arrays to REACTION-keyed objects"""
    import json as json_mod
    import re

    REACTION_KEYWORDS = {
        "R": ['safety', 'medical', 'ambulance', 'render aid', 'cfd', 'fire department', 'ems',
              'arrive', 'approach', 'officer safety', 'life-saving', 'paramedic', 'hospital',
              'injured', 'wound', 'triage', 'respond to', 'ensure safety', 'safe approach',
              'ems response', 'rescue', 'first aid'],
        "E": ['perimeter', 'crime scene', 'secure', 'tape', 'log', 'access', 'inner', 'outer',
              'establish', 'scene status', 'uniformed', 'boundary', 'entry point', 'exit point',
              'scene integrity', 'cordon', 'scene supervisor', 'command post'],
        "A": ['miranda', 'custody', 'detain', 'arrest', 'apprehend', 'suspect', 'handcuff',
              'advise', 'rights', 'probable cause', 'in custody', 'taken into', 'booking',
              'warrant for arrest', 'felony arrest'],
        "C": ['witness', 'interview', 'canvass', 'statement', 'separate', 'identify witness',
              'canvas', 'neighbor', 'bystander', 'victim statement', 'victim interview',
              'employee', 'coworker', 'family member', 'next of kin'],
        "T": ['photograph', 'document', 'bwc', 'body worn', 'sketch', 'notes', 'crime scene tech',
              'diagram', 'measure', 'record', 'body-worn', 'notation', 'log entry', 'scene photo',
              'video record'],
        "I": ['preserve', 'physical evidence', 'shell casing', 'chain of custody', 'tag', 'package',
              'forensic', 'ballistic', 'gunshot residue', 'dna', 'trace evidence', 'fingerprint',
              'evidence tech', 'lab', 'blood', 'fiber', 'weapon', 'firearm', 'inventory',
              'collect evidence', 'process evidence', 'swab', 'gsr', 'toxicology'],
        "O": ['asa', 'felony review', 'search warrant', 'consent to search', 'court order',
              'subpoena', 'medical examiner', 'state attorney', 'legal', 'prosecutor',
              "state's attorney", 'warrant', 'copa', 'notification to', 'notify detective',
              'notify supervisor', 'dcfs'],
        "N": ['case report', 'supplementary', 'follow-up', 'surveillance', 'security camera',
              'footage', 'leads', 'pawn shop', 'photo lineup', 'show-up', 'background check',
              'bolo', 'flash message', 'alert', 'monitor', 'coordinate with', 'ongoing',
              'long-term', 'additional investigation', 'social media', 'tipline', 'cleared',
              'close case', 'safety plan', 'victim services', 'resources'],
    }

    updated = 0
    errors = []
    scenarios = await db.questions.find({"type": "scenario"}).to_list(100)

    for scenario in scenarios:
        title = scenario.get("title", "unknown")
        try:
            raw = scenario.get("answer", "")
            # Fix common JSON issues: unescaped quotes inside strings
            if isinstance(raw, str):
                try:
                    parsed = json_mod.loads(raw)
                except json_mod.JSONDecodeError:
                    # Try fixing by replacing problematic characters
                    cleaned = raw.replace('\n', '\\n').replace('\t', '\\t')
                    try:
                        parsed = json_mod.loads(cleaned)
                    except json_mod.JSONDecodeError:
                        # Last resort: use model_answer field if available
                        raw2 = scenario.get("model_answer", "")
                        if raw2:
                            parsed = json_mod.loads(raw2) if isinstance(raw2, str) else raw2
                        else:
                            errors.append(f"{title}: unparseable JSON, skipping")
                            continue
            else:
                parsed = raw

            if not parsed or not isinstance(parsed.get("modelAnswer"), list):
                errors.append(f"{title}: not a flat array, skipping")
                continue

            items = parsed["modelAnswer"]
            buckets = {k: [] for k in "REACTION"}
            used = set()

            for idx, item in enumerate(items):
                lower = item.lower()
                for letter, keywords in REACTION_KEYWORDS.items():
                    if any(kw in lower for kw in keywords):
                        buckets[letter].append(item)
                        used.add(idx)
                        break

            # Put unmatched items in N (Next Steps)
            for idx, item in enumerate(items):
                if idx not in used:
                    buckets["N"].append(item)

            # Remove empty keys
            reaction_obj = {k: v for k, v in buckets.items() if v}

            new_answer = json_mod.dumps({"modelAnswer": reaction_obj})
            await db.questions.update_one(
                {"question_id": scenario["question_id"]},
                {"$set": {"answer": new_answer}}
            )
            updated += 1
        except Exception as e:
            errors.append(f"{title}: {str(e)}")

    return {"updated": updated, "total": len(scenarios), "errors": errors}

@api_router.post("/fix-armed-robbery")
async def fix_armed_robbery():
    """Fix the truncated JSON for ARMED ROBBERY WITH DEATH by using model_answer field"""
    import json as json_mod
    scenario = await db.questions.find_one(
        {"title": "ARMED ROBBERY WITH DEATH", "type": "scenario"},
        {"_id": 0, "question_id": 1, "answer": 1, "model_answer": 1}
    )
    if not scenario:
        return {"error": "not found"}

    # Try model_answer field first
    raw = scenario.get("model_answer", "")
    parsed = None
    if raw:
        try:
            parsed = json_mod.loads(raw) if isinstance(raw, str) else raw
        except Exception:
            pass

    # If model_answer also fails, fix the truncated answer by appending closing brackets
    if not parsed:
        raw = scenario.get("answer", "")
        # The JSON is truncated - try appending closing brackets
        for fix in [']}}', ']}', '}']:
            try:
                parsed = json_mod.loads(raw + fix)
                break
            except Exception:
                continue

    if not parsed or not isinstance(parsed.get("modelAnswer"), list):
        return {"error": "could not parse either field", "model_answer_len": len(str(scenario.get("model_answer", "")))}

    # Now categorize into REACTION keys
    REACTION_KEYWORDS = {
        "R": ['safety', 'medical', 'ambulance', 'render aid', 'ems', 'arrive', 'approach',
              'officer safety', 'life-saving', 'paramedic', 'hospital', 'injured', 'wound',
              'first aid', 'ensure safety', 'respond'],
        "E": ['perimeter', 'crime scene', 'secure', 'tape', 'log', 'access', 'inner', 'outer',
              'establish', 'scene status', 'uniformed', 'scene supervisor', 'command post'],
        "A": ['miranda', 'custody', 'detain', 'arrest', 'apprehend', 'suspect', 'handcuff',
              'advise', 'rights', 'probable cause', 'booking'],
        "C": ['witness', 'interview', 'canvass', 'statement', 'separate', 'canvas', 'neighbor',
              'bystander', 'victim statement', 'employee', 'family member', 'next of kin'],
        "T": ['photograph', 'document', 'bwc', 'body worn', 'sketch', 'notes', 'crime scene tech',
              'diagram', 'measure', 'record', 'body-worn', 'video record', 'scene photo'],
        "I": ['preserve', 'physical evidence', 'shell casing', 'chain of custody', 'tag', 'package',
              'forensic', 'ballistic', 'gunshot residue', 'dna', 'trace evidence', 'fingerprint',
              'evidence tech', 'lab', 'blood', 'fiber', 'weapon', 'firearm', 'inventory',
              'collect evidence', 'process evidence', 'swab', 'gsr', 'toxicology'],
        "O": ['asa', 'felony review', 'search warrant', 'consent to search', 'court order',
              'subpoena', 'medical examiner', 'state attorney', 'legal', 'prosecutor',
              "state's attorney", 'warrant', 'copa', 'notify', 'dcfs'],
        "N": ['case report', 'supplementary', 'follow-up', 'surveillance', 'security camera',
              'footage', 'leads', 'pawn shop', 'photo lineup', 'show-up', 'background check',
              'bolo', 'flash message', 'alert', 'monitor', 'coordinate', 'ongoing',
              'social media', 'safety plan', 'victim services', 'resources'],
    }

    items = parsed["modelAnswer"]
    buckets = {k: [] for k in "REACTION"}
    used = set()
    for idx, item in enumerate(items):
        lower = item.lower()
        for letter, keywords in REACTION_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                buckets[letter].append(item)
                used.add(idx)
                break
    for idx, item in enumerate(items):
        if idx not in used:
            buckets["N"].append(item)

    reaction_obj = {k: v for k, v in buckets.items() if v}
    new_answer = json_mod.dumps({"modelAnswer": reaction_obj})

    await db.questions.update_one(
        {"question_id": scenario["question_id"]},
        {"$set": {"answer": new_answer}}
    )
    return {"status": "fixed", "keys": list(reaction_obj.keys()), "total_items": len(items)}

@api_router.get("/debug-scenario-titles")
async def debug_scenario_titles():
    """Temporary: list all scenario titles and a sample answer"""
    scenarios = await db.questions.find(
        {"type": "scenario"},
        {"_id": 0, "title": 1, "category_id": 1}
    ).to_list(100)
    # Get first scenario's full doc to see field names and answer format
    sample = await db.questions.find_one(
        {"type": "scenario"},
        {"_id": 0}
    )
    if sample:
        # Show all field names and truncated answer
        fields = list(sample.keys())
        answer_raw = sample.get("answer", sample.get("model_answer", ""))
        answer_preview = str(answer_raw)[:800] if answer_raw else "NO ANSWER FIELD"
    else:
        fields = []
        answer_preview = "NO SCENARIOS FOUND"
    return {"count": len(scenarios), "scenarios": scenarios, "fields": fields, "sample_answer_preview": answer_preview}

# ========== VERSION CHECK ENDPOINT ==========
def compare_versions(v1: str, v2: str) -> int:
    """Compare two version strings. Returns: -1 if v1 < v2, 0 if equal, 1 if v1 > v2"""
    v1_parts = [int(x) for x in v1.split('.')]
    v2_parts = [int(x) for x in v2.split('.')]
    
    for i in range(max(len(v1_parts), len(v2_parts))):
        v1_val = v1_parts[i] if i < len(v1_parts) else 0
        v2_val = v2_parts[i] if i < len(v2_parts) else 0
        if v1_val < v2_val:
            return -1
        elif v1_val > v2_val:
            return 1
    return 0

@api_router.get("/version")
async def check_version(client_version: Optional[str] = None):
    """Check if client version is up to date"""
    response = {
        "current_version": CURRENT_APP_VERSION,
        "minimum_version": MINIMUM_REQUIRED_VERSION,
        "update_required": False,
        "update_message": None
    }
    
    if client_version:
        if compare_versions(client_version, MINIMUM_REQUIRED_VERSION) < 0:
            response["update_required"] = True
            response["update_message"] = f"A new version ({CURRENT_APP_VERSION}) is required. Please refresh your browser to get the latest updates."
    
    return response

# Password Reset Endpoints
class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

@api_router.post("/auth/forgot-password")
async def forgot_password(request: PasswordResetRequest):
    """Request password reset - generates token"""
    email = request.email.lower()
    user = await db.users.find_one({"email": email}, {"_id": 0})
    
    if not user:
        # Don't reveal if email exists for security
        return {"message": "If an account exists with this email, a reset code has been generated."}
    
    # Generate reset token (6 digit code for simplicity)
    import random
    reset_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Store reset token with expiry
    await db.password_resets.delete_many({"email": email})  # Remove old tokens
    await db.password_resets.insert_one({
        "email": email,
        "token": reset_code,
        "expires_at": datetime.now(timezone.utc) + timedelta(hours=1),
        "created_at": datetime.now(timezone.utc)
    })
    
    # In production, you would send an email here
    # For now, return the code (in production, this would be sent via email)
    return {
        "message": "If an account exists with this email, a reset code has been generated.",
        "reset_code": reset_code,  # Only for demo - remove in production
        "note": "In production, this code would be sent to your email"
    }

@api_router.post("/auth/reset-password")
async def reset_password(request: PasswordResetConfirm):
    """Reset password using token"""
    # Find valid reset token
    reset_doc = await db.password_resets.find_one({
        "token": request.token,
        "expires_at": {"$gt": datetime.now(timezone.utc)}
    })
    
    if not reset_doc:
        raise HTTPException(status_code=400, detail="Invalid or expired reset code")
    
    if len(request.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    # Update password
    new_hash = hash_password(request.new_password)
    result = await db.users.update_one(
        {"email": reset_doc["email"]},
        {"$set": {"password_hash": new_hash}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update password")
    
    # Delete the used token
    await db.password_resets.delete_one({"token": request.token})
    
    # Invalidate all existing sessions for this user
    user = await db.users.find_one({"email": reset_doc["email"]}, {"_id": 0})
    if user:
        await db.user_sessions.delete_many({"user_id": user["user_id"]})
    
    return {"message": "Password reset successful. Please log in with your new password."}

# ========== CATEGORY ENDPOINTS ==========

@api_router.get("/categories", response_model=List[Category])
async def get_categories():
    categories = await db.categories.find({}, {"_id": 0}).sort("order", 1).to_list(100)
    return categories

@api_router.post("/categories", response_model=Category)
async def create_category(category: Category, user: User = Depends(require_admin)):
    await db.categories.insert_one(category.model_dump())
    return category

# ========== QUESTION ENDPOINTS ==========

@api_router.get("/questions")
async def get_questions(
    type: Optional[str] = None,
    category_id: Optional[str] = None,
    user: User = Depends(require_user)
):
    query = {}
    if type:
        query["type"] = type
    if category_id:
        query["category_id"] = category_id
    questions = await db.questions.find(query, {"_id": 0}).to_list(500)

    # Check premium access (payments collection + has_paid flag for admin-granted)
    has_premium = user.role == "admin"
    if not has_premium:
        payment = await db.payments.find_one(
            {"user_id": user.user_id, "status": "completed"}, {"_id": 0}
        )
        if not payment:
            user_doc = await db.users.find_one({"user_id": user.user_id}, {"_id": 0, "has_paid": 1})
            has_premium = user_doc.get("has_paid", False) if user_doc else False
        else:
            has_premium = True

    # Identify first scenario in cat_detective_part2 for free trial
    first_scenario_id = None
    if category_id == "cat_detective_part2" and type == "scenario":
        scenario_list = [q for q in questions]
        if scenario_list:
            first_scenario_id = scenario_list[0].get("question_id")

    for q in questions:
        is_premium = q.get("is_premium", False)
        q["is_locked"] = is_premium and not has_premium

        # Free trial: unlock the first scenario for all users
        if q.get("question_id") == first_scenario_id and first_scenario_id is not None:
            q["is_locked"] = False
            q["is_free_trial"] = True

        if q["is_locked"]:
            q["answer"] = None
            q["model_answer"] = None
            q["explanation"] = None

    return questions

@api_router.get("/questions/{question_id}")
async def get_question(question_id: str, user: User = Depends(require_user)):
    question = await db.questions.find_one({"question_id": question_id}, {"_id": 0})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_premium = question.get("is_premium", False)
    if is_premium and user.role != "admin":
        payment = await db.payments.find_one(
            {"user_id": user.user_id, "status": "completed"}, {"_id": 0}
        )
        has_paid = False
        if not payment:
            user_doc = await db.users.find_one({"user_id": user.user_id}, {"_id": 0, "has_paid": 1})
            has_paid = user_doc.get("has_paid", False) if user_doc else False
        else:
            has_paid = True
        if not has_paid:
            # Allow free trial: check if this is the first scenario in cat_detective_part2
            is_free_trial = False
            if question.get("category_id") == "cat_detective_part2" and question.get("type") == "scenario":
                first_scenario = await db.questions.find_one(
                    {"category_id": "cat_detective_part2", "type": "scenario"},
                    {"_id": 0, "question_id": 1},
                    sort=[("created_at", 1)]
                )
                if first_scenario and first_scenario.get("question_id") == question_id:
                    is_free_trial = True
            if not is_free_trial:
                raise HTTPException(status_code=403, detail="Premium access required. Please upgrade to access this scenario.")

    return question

@api_router.post("/questions", response_model=Question)
async def create_question(question_data: QuestionCreate, user: User = Depends(require_admin)):
    question_id = f"q_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc)
    
    question = Question(
        question_id=question_id,
        **question_data.model_dump(),
        created_at=now,
        updated_at=now
    )
    
    await db.questions.insert_one(question.model_dump())
    return question

@api_router.put("/questions/{question_id}", response_model=Question)
async def update_question(
    question_id: str,
    question_data: QuestionCreate,
    user: User = Depends(require_admin)
):
    existing = await db.questions.find_one({"question_id": question_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Question not found")
    
    update_data = question_data.model_dump()
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    await db.questions.update_one(
        {"question_id": question_id},
        {"$set": update_data}
    )
    
    updated = await db.questions.find_one({"question_id": question_id}, {"_id": 0})
    return Question(**updated)

@api_router.delete("/questions/{question_id}")
async def delete_question(question_id: str, user: User = Depends(require_admin)):
    result = await db.questions.delete_one({"question_id": question_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted"}

# ========== BULK QUESTIONS ENDPOINT (Performance) ==========
class BulkQuestionsRequest(BaseModel):
    queries: List[Dict[str, Optional[str]]]  # List of {type, category_id}

@api_router.post("/questions/bulk")
async def get_questions_bulk(data: BulkQuestionsRequest, user: User = Depends(require_user)):
    """Fetch questions for multiple type/category combinations in a single request.
    Reduces N+1 API calls from the Scenarios page to a single call."""
    # Check premium access once for all queries
    has_premium = user.role == "admin"
    if not has_premium:
        payment = await db.payments.find_one(
            {"user_id": user.user_id, "status": "completed"},
            {"_id": 0}
        )
        if not payment:
            user_doc = await db.users.find_one({"user_id": user.user_id}, {"_id": 0, "has_paid": 1})
            has_premium = user_doc.get("has_paid", False) if user_doc else False
        else:
            has_premium = True

    results = {}
    for query in data.queries:
        q_type = query.get("type")
        cat_id = query.get("category_id")
        mongo_query = {}
        if q_type:
            mongo_query["type"] = q_type
        if cat_id:
            mongo_query["category_id"] = cat_id

        questions = await db.questions.find(mongo_query, {"_id": 0}).to_list(500)

        for q in questions:
            is_premium_q = q.get("is_premium", False)
            q["is_locked"] = is_premium_q and not has_premium
            if q["is_locked"]:
                q["answer"] = None
                q["model_answer"] = None
                q["explanation"] = None

        # Use category_id as key, fallback to type
        key = cat_id or q_type or "unknown"
        results[key] = questions

    return results

# ========== BOOKMARK ENDPOINTS ==========

@api_router.post("/bookmarks/toggle")
async def toggle_bookmark(data: BookmarkToggle, user: User = Depends(require_user)):
    # Check if progress entry exists
    progress = await db.user_progress.find_one(
        {"user_id": user.user_id, "question_id": data.question_id},
        {"_id": 0}
    )
    
    if progress:
        # Toggle bookmark
        new_value = not progress.get("bookmarked", False)
        await db.user_progress.update_one(
            {"user_id": user.user_id, "question_id": data.question_id},
            {"$set": {"bookmarked": new_value}}
        )
        return {"bookmarked": new_value}
    else:
        # Create new progress entry
        progress_id = f"prog_{uuid.uuid4().hex[:12]}"
        new_progress = UserProgress(
            progress_id=progress_id,
            user_id=user.user_id,
            question_id=data.question_id,
            bookmarked=True,
            created_at=datetime.now(timezone.utc)
        )
        await db.user_progress.insert_one(new_progress.model_dump())
        return {"bookmarked": True}

@api_router.get("/bookmarks", response_model=List[Question])
async def get_bookmarks(user: User = Depends(require_user)):
    # Get bookmarked question IDs - only fetch question_id field for performance
    bookmarks = await db.user_progress.find(
        {"user_id": user.user_id, "bookmarked": True},
        {"_id": 0, "question_id": 1}
    ).to_list(500)
    
    question_ids = [b["question_id"] for b in bookmarks]
    
    if not question_ids:
        return []
    
    # Get questions
    questions = await db.questions.find(
        {"question_id": {"$in": question_ids}},
        {"_id": 0}
    ).to_list(500)
    
    return questions

@api_router.get("/progress/{question_id}")
async def get_progress(question_id: str, user: User = Depends(require_user)):
    progress = await db.user_progress.find_one(
        {"user_id": user.user_id, "question_id": question_id},
        {"_id": 0}
    )
    return progress or {"bookmarked": False}

# ========== SCENARIO ENDPOINTS ==========

@api_router.post("/scenarios/submit")
async def submit_scenario(data: ScenarioSubmit, user: User = Depends(require_user)):
    # Get the question
    question = await db.questions.find_one({"question_id": data.question_id}, {"_id": 0})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Grade with OpenAI using your API Key
    try:
        from openai import AsyncOpenAI
        
        # Use OpenAI API key (user's own key, not Emergent key)
        api_key = OPENAI_API_KEY or EMERGENT_LLM_KEY
        if not api_key:
            raise Exception("No API key configured")
        
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.openai.com/v1"
        )
        
        prompt = f"""Grade this detective exam scenario response using the R.E.A.C.T.I.O.N. framework.

SCENARIO:
{question['content']}

CORRECT ANSWER/KEY POINTS:
{question.get('answer', 'Use your best judgment based on CPD procedures and Illinois law')}

STUDENT RESPONSE:
{data.user_response}

Provide your response in this exact format. For EACH R.E.A.C.T.I.O.N. step, list ALL the specific actions the student should have addressed (4-8 detailed bullet points per step). For each bullet point, indicate whether the student covered it, partially covered it, or missed it entirely. Be scenario-specific — reference the exact facts, people, evidence, and circumstances from this scenario.

GRADE: [number 0-100]
FEEDBACK:
**R – Respond & Render Aid**
- [specific action item 1 with assessment]
- [specific action item 2 with assessment]
- [specific action item 3 with assessment]
- [specific action item 4 with assessment]

**E – Establish the Scene**
- [specific action item 1 with assessment]
- [specific action item 2 with assessment]
- [specific action item 3 with assessment]
- [specific action item 4 with assessment]

**A – Arrest/Detain & Advise**
- [specific action item 1 with assessment]
- [specific action item 2 with assessment]
- [specific action item 3 with assessment]
- [specific action item 4 with assessment]

**C – Collect/Identify Witnesses**
- [specific action item 1 with assessment]
- [specific action item 2 with assessment]
- [specific action item 3 with assessment]
- [specific action item 4 with assessment]

**T – Take Notes & Document**
- [specific action item 1 with assessment]
- [specific action item 2 with assessment]
- [specific action item 3 with assessment]
- [specific action item 4 with assessment]

**I – Inventory & Process Evidence**
- [specific action item 1 with assessment]
- [specific action item 2 with assessment]
- [specific action item 3 with assessment]
- [specific action item 4 with assessment]

**O – Obtain Legal/Consult**
- [specific action item 1 with assessment]
- [specific action item 2 with assessment]
- [specific action item 3 with assessment]
- [specific action item 4 with assessment]

**N – Next Steps & Notification**
- [specific action item 1 with assessment]
- [specific action item 2 with assessment]
- [specific action item 3 with assessment]
- [specific action item 4 with assessment]

**Overall:** [brief summary highlighting strongest areas, critical gaps, and specific recommendations for improvement]"""
        
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are an expert grader for Chicago Police Department detective exam scenarios. You grade using the R.E.A.C.T.I.O.N. framework with detailed, scenario-specific feedback.

R.E.A.C.T.I.O.N. Framework:
  R – Respond & Render Aid: Ensure officer safety, render first aid, request EMS/CFD, document victim conditions, obtain preliminary statements once medically stable, request Medical Examiner if death involved
  E – Establish the Scene: Brief with responding officers/supervisor, establish inner and outer perimeters, assign officers to secure entry/exit, separate all witnesses, identify/document all weapons on scene, establish command post, deploy additional resources
  A – Arrest/Detain & Advise: Speak with apprehending officers, photograph suspect and note injuries/marks, advise Miranda prior to custodial interrogation, conduct electronically recorded interrogation, document spontaneous statements, complete TRR if force used
  C – Collect/Identify Witnesses: Identify, separate, and interview all witnesses individually, obtain detailed victim statement, conduct separate interviews, canvass surrounding area for additional witnesses, obtain/preserve security camera footage, instruct witnesses to preserve independent recollection, conduct photo lineup or show-up as appropriate
  T – Take Notes & Document: Photograph entire scene before evidence movement, document evidence locations, record all actions in case report and Felony 101, log all evidence into PCAD, document firearms/ballistic evidence, preserve digital evidence with timestamps, document chain of custody, review/secure body-worn camera footage
  I – Inventory & Process Evidence: Preserve all physical evidence, photograph and inventory firearms/weapons, request Forensic Services Division, request ballistics comparison, request GSR/DNA testing, secure digital evidence, coordinate forensic extraction, assess exigent circumstances for digital preservation, maintain strict chain of custody
  O – Obtain Legal/Consult: Notify ASA regarding circumstances, consult ASA regarding search warrants, request warrants for phone/digital/surveillance, conduct LEADS and CLEAR checks, ensure 4th Amendment compliance, ensure 5th and 6th Amendment protections, coordinate with Medical Examiner/COPA/DCFS as applicable
  N – Next Steps & Notification: Issue flash message/BOLO with descriptions, continue canvass, monitor media through CPD communications, refer media to Office of Communications, avoid public disclosure that could contaminate statements, prepare complete case file, coordinate follow-up investigation and court preparation

CRITICAL — OFFICER-INVOLVED SHOOTING (OIS) PROCEDURES:
For any scenario involving an officer-involved shooting, the AI MUST reference and grade against the following General Orders:
1. G03-06 (Firearm Discharge Incidents/OIS) — IRT activation is mandatory. The Incident Response Team responds to all officer-involved firearm discharges, officer-involved deaths, and in-custody deaths. IRT secures scene, processes evidence, and coordinates with COPA.
2. G04-02 (Search Warrants) — Search warrants may be needed for the involved officer's vehicle, locker, or electronic devices, and for DNA/blood evidence.
3. G03-02-03 (Firearm Discharge — Property/Reporting) — All firearm discharges require mandatory reporting, supervisor notification, and TRR completion.
4. S03-14 (Body-Worn Cameras) — All BWC footage must be immediately secured by IRT. Involved officers must NOT review BWC before giving statements.
IMPORTANT: The City of Chicago does NOT have IPRA (Independent Police Review Authority) anymore. IPRA was replaced by COPA (Civilian Office of Police Accountability) in 2017. All references must use COPA, never IPRA. If a student references IPRA, note it as outdated/incorrect and explain COPA replaced IPRA.

CRITICAL — COPA NOTIFICATION RULES:
COPA (Civilian Office of Police Accountability) is ONLY contacted for OFFICER-INVOLVED shootings/incidents. Do NOT expect or award points for COPA notification in scenarios involving civilian-on-civilian shootings, civilian self-defense shootings, or any shooting where no CPD officer discharged a firearm or used force. If a student incorrectly mentions COPA in a non-officer-involved scenario, note it as an error. Conversely, COPA is MANDATORY for any scenario where a CPD officer fires their weapon, uses deadly force, or is involved in an in-custody death.

CRITICAL — GENERAL ORDERS & CASE LAW:
Answers MUST be graded against CPD General Orders and relevant case law. Award extra credit for correctly citing specific directives and case law. Deduct points if a student's response contradicts established policy or law. Key references include but are not limited to:

CPD General Orders:
- G03-02: Use of Force (force options, de-escalation requirements, duty to intervene)
- G03-02-01: Force Options (force mitigation, proportional response)
- G03-02-02: Incidents Requiring the Completion of a TRR
- G03-02-03: Firearm Discharge Incidents — Loss or Destruction of Department Property — mandatory reporting when a firearm is discharged including accidental discharges, discharges at animals, and discharges resulting in property damage. Requires immediate supervisor notification, TRR completion, and detailed documentation
- G03-06: Firearm Discharge Incidents / Officer-Involved Shootings (mandatory COPA notification per S08-01-07, IRT activation and response, weapon recovery, officer separation, scene preservation, 24-hr review period before formal statement). The Incident Response Team (IRT) responds to ALL officer-involved firearm discharges, officer-involved deaths, and in-custody deaths. IRT secures the scene, collects and processes evidence, coordinates with COPA investigators, and conducts the administrative investigation. The involved officer must be immediately separated from the scene, provided FOP/union representation, and may invoke the 24-hour review period before giving a formal statement. COPA (not IPRA — IPRA was replaced by COPA in 2017) has independent investigative authority over all officer-involved shootings and must be notified immediately.
- G06-01: Field Arrest Procedures (processing, inventory, bond)
- G06-01-01: Processing Persons Under Department Control
- G06-01-02: Arrests of Juveniles
- G04-02: Search Warrants (preparation, execution, inventory, return) — covers the complete search warrant process including: drafting affidavits with probable cause, obtaining judicial approval, proper execution procedures, knock-and-announce requirements, inventory of seized items, and return of warrant to the court. In officer-involved shooting investigations, search warrants may be required for the involved officer's vehicle, locker, electronic devices, or for DNA/blood evidence at the scene
- G03-03: Exigent Circumstances (warrantless entry/search)
- S04-13-09: Investigatory Stop Reports and Protective Pat Downs (Terry stops)
- G02-01: Human Rights and Community Partnerships
- G02-01-03: Allegations of Misconduct — COPA/BIA notification requirements
- G02-04: Prohibition Regarding Racial Profiling and Other Bias-Based Policing
- G03-02-05: Electronic Control Weapon (Taser) use policy
- G06-22: Crime Scene Protection and Processing
- S06-06: Written Felony Review by the Cook County State's Attorney's Office

Relevant Case Law:
- Terry v. Ohio (1968): Reasonable suspicion standard for stops and frisks
- Miranda v. Arizona (1966): Custodial interrogation rights and warnings
- Graham v. Connor (1989): Objective reasonableness standard for use of force
- Tennessee v. Garner (1985): Deadly force against fleeing felons — must pose imminent threat of serious harm
- Mapp v. Ohio (1961): Exclusionary rule — illegally obtained evidence inadmissible
- Illinois v. Gates (1983): Totality of circumstances for probable cause / warrant issuance
- Carroll v. United States (1925): Vehicle exception to warrant requirement
- Chimel v. California (1969): Search incident to arrest — immediate area of control
- Riley v. California (2014): Warrant required to search cell phone incident to arrest
- Carpenter v. United States (2018): Warrant required for cell-site location information
- People v. Aguilar (2013, IL): Illinois firearm possession — AUUW statute requirements
- 725 ILCS 5/103-2.1: Electronic recording of custodial interrogations (homicide mandatory)
- 720 ILCS 5/7-1: Use of force in defense of person (civilian self-defense justification)

CPD Special Orders:
- S03-14: Body-Worn Camera (BWC) policy — activation requirements, prohibited deactivation, evidentiary procedures. In officer-involved shootings: BWC footage from ALL officers on scene must be immediately secured and preserved by IRT. BWC footage must NOT be reviewed by involved officers before giving independent statements. BWC is critical evidence in COPA investigations and Consent Decree compliance. Supervisors must ensure all BWC units are collected and uploaded
- S03-14-09: In-Car Camera System usage and requirements
- S04-13-09: Investigatory Stop Reports (ISR) — documentation of Terry stops, protective pat downs
- S04-14-06: Emergency Protective Orders — domestic violence situations
- S06-01: Processing Evidence at Crime Scenes
- S06-06: Written Felony Review by Cook County ASA
- S06-06-01: Telephone Felony Review procedures
- S04-19: Domestic Violence procedures and mandatory arrest provisions
- S09-03: DNA Evidence Collection and Preservation
- S04-20: Missing/Found Persons (including endangered/AMBER alerts)
- S04-01-01: Preliminary Investigation — first responding officer duties
- S07-01: Department Reports — case report completion, supplementary reports
- S04-25: Gang-Related Investigations
- S03-10: Canine Unit — deployment protocols
- S04-27: Hate Crime procedures and reporting

When grading, note whether the student:
1. Correctly identifies which General Orders apply to the scenario
2. Follows procedures outlined in those General Orders
3. Recognizes constitutional requirements from relevant case law
4. Avoids actions that would violate established legal precedent
Award bonus points (up to +5) for specific, correct citations of General Orders or case law.

For each R.E.A.C.T.I.O.N. step, provide 4-8 specific, scenario-relevant action items. For each item, assess whether the student addressed it. Grade from 0-100 based on completeness and accuracy."""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=3000
        )
        
        ai_response = response.choices[0].message.content
        
        # Parse AI response
        grade = None
        feedback = ai_response
        
        if "GRADE:" in ai_response:
            parts = ai_response.split("GRADE:", 1)[1].split("FEEDBACK:", 1)
            if len(parts) == 2:
                try:
                    grade = float(parts[0].strip())
                    feedback = parts[1].strip()
                except (ValueError, IndexError):
                    pass
        
    except Exception as e:
        logging.error(f"AI grading error: {e}")
        grade = None
        feedback = "Unable to grade automatically. Please review with instructor."
    
    # Save response
    response_id = f"resp_{uuid.uuid4().hex[:12]}"
    scenario_response = ScenarioResponse(
        response_id=response_id,
        user_id=user.user_id,
        question_id=data.question_id,
        user_response=data.user_response,
        ai_grade=grade,
        ai_feedback=feedback,
        time_taken=data.time_taken,
        submitted_at=datetime.now(timezone.utc)
    )
    
    await db.scenario_responses.insert_one(scenario_response.model_dump())
    
    # Update user progress
    await db.user_progress.update_one(
        {"user_id": user.user_id, "question_id": data.question_id},
        {
            "$set": {
                "last_score": grade,
                "last_attempted": datetime.now(timezone.utc)
            },
            "$inc": {"attempts": 1},
            "$setOnInsert": {
                "progress_id": f"prog_{uuid.uuid4().hex[:12]}",
                "user_id": user.user_id,
                "question_id": data.question_id,
                "bookmarked": False,
                "created_at": datetime.now(timezone.utc)
            }
        },
        upsert=True
    )
    
    return {
        "response_id": response_id,
        "grade": grade,
        "feedback": feedback
    }

@api_router.get("/scenarios/history")
async def get_scenario_history(user: User = Depends(require_user)):
    responses = await db.scenario_responses.find(
        {"user_id": user.user_id},
        {"_id": 0}
    ).sort("submitted_at", -1).to_list(100)

    return responses

# ========== CHATBOT ENDPOINT ==========

@api_router.post("/chatbot/message")
async def chatbot_message(data: ChatbotMessage, user: User = Depends(require_user)):
    """Bot 9165 - AI mentor for scenario practice"""
    try:
        if not ANTHROPIC_API_KEY:
            raise Exception("Anthropic API key not configured")

        # Fetch the scenario from DB
        question = await db.questions.find_one({"question_id": data.question_id}, {"_id": 0})
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        scenario_text = question.get("description") or question.get("content", "")
        model_answer = question.get("model_answer") or question.get("answer", "")

        system_prompt = f"""You are Bot 9165, a friendly and encouraging AI mentor helping a Chicago Police Department officer study for the Detective Exam. You are guiding them through a practice scenario.

SCENARIO THE STUDENT IS WORKING ON:
{scenario_text}

MODEL ANSWER (HIDDEN FROM STUDENT - DO NOT REVEAL):
{model_answer}

THE STUDENT'S CURRENT TYPED RESPONSE SO FAR:
{data.user_current_response or "(Student hasn't typed anything yet)"}

YOUR RULES:
1. NEVER reveal the full model answer or copy/paste sections from it
2. Ask guiding questions to help the student think through the problem
3. Hint at ONE missing R.E.A.C.T.I.O.N. framework area at a time
4. Reference the R.E.A.C.T.I.O.N. framework steps:
   R - Respond & Render Aid (arrive safely, ensure safety, provide medical aid)
   E - Establish the Scene (secure perimeters, control entry/exit)
   A - Arrest/Detain & Advise (locate suspects, Miranda if custodial)
   C - Collect/Identify Witnesses (separate witnesses, conduct interviews)
   T - Take Notes & Document (photos, video/BWC, sketches, notes)
   I - Inventory & Process Evidence (collect, package, chain of custody)
   O - Obtain Legal/Consult (search warrants, Felony Review)
   N - Next Steps & Notification (case reports, notify supervisors, follow-up)
5. Be encouraging but push the student to think deeper
6. Keep responses concise (2-4 sentences max)
7. If the student asks for the answer directly, remind them that working through it builds stronger exam skills
8. Use a professional but supportive tone appropriate for law enforcement training
9. COPA (Civilian Office of Police Accountability) is ONLY for OFFICER-INVOLVED shootings/incidents. If the scenario involves a civilian shooting (not by a CPD officer), do NOT hint at or expect COPA notification. If the student mentions COPA incorrectly, gently correct them.
10. When guiding the student, reference relevant CPD General Orders (e.g., G03-02 Use of Force, G03-06 OIS, G04-02 Search Warrants, G06-22 Crime Scene Processing), Special Orders (e.g., S03-14 BWC, S04-13-09 ISR, S06-06 Felony Review, S04-19 Domestic Violence), and case law (e.g., Terry v. Ohio, Miranda, Graham v. Connor, Tennessee v. Garner, Riley v. California). Help the student connect their actions to the specific directives and legal standards that govern them."""

        import anthropic
        client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

        # Build messages from conversation history (cap at 20)
        messages = []
        history = data.conversation_history[-20:] if len(data.conversation_history) > 20 else data.conversation_history
        for msg in history:
            role = msg.get("role", "user")
            if role in ("user", "assistant"):
                messages.append({"role": role, "content": msg.get("content", "")})

        # Add the current user message
        messages.append({"role": "user", "content": data.user_message})

        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            system=system_prompt,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )

        bot_response = response.content[0].text

        # Count hints given (approximate by counting assistant messages)
        hints_given = len([m for m in history if m.get("role") == "assistant"]) + 1

        return ChatbotResponse(bot_response=bot_response, hints_given=hints_given)

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Chatbot error: {e}")
        return ChatbotResponse(
            bot_response="I'm having trouble connecting right now. Try asking me again in a moment!",
            hints_given=0
        )

# ========== CASE SUMMARY GRADING ENDPOINT ==========

class CaseSummarySubmit(BaseModel):
    question_id: str
    image_data: str  # base64 data URL of the handwritten response photo

@api_router.post("/case-summary/grade")
async def grade_case_summary(data: CaseSummarySubmit, user: User = Depends(require_user)):
    """Grade a handwritten case summary using Claude Vision.
    The student uploads a photo of their handwritten response.
    AI reads the image and grades it against the model answer and key facts."""
    try:
        if not ANTHROPIC_API_KEY:
            raise Exception("Anthropic API key not configured")

        # Fetch the question from DB
        question = await db.questions.find_one({"question_id": data.question_id}, {"_id": 0})
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        case_text = question.get("content", "")
        model_answer = question.get("model_answer", "")
        key_facts = question.get("key_facts", [])

        # Parse the base64 image
        image_data = data.image_data
        if "," in image_data:
            # Strip data URL prefix (e.g., "data:image/jpeg;base64,")
            header, image_data = image_data.split(",", 1)
            media_type = header.split(":")[1].split(";")[0] if ":" in header else "image/jpeg"
        else:
            media_type = "image/jpeg"

        import anthropic
        client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

        system_prompt = f"""You are an expert CPD Detective Exam grader evaluating a handwritten investigative case summary.
You grade strictly in accordance with Chicago Police Department General Orders.

THE CASE THE STUDENT WAS GIVEN:
{case_text}

MODEL ANSWER:
{model_answer}

KEY FACTS THAT SHOULD BE INCLUDED:
{chr(10).join(f'- {f}' for f in key_facts)}

GRADING INSTRUCTIONS (Per CPD General Orders):
1. First, read and transcribe the handwritten text from the image as accurately as possible.
2. Compare the student's summary against the key facts list AND the following CPD General Order standards:
   - G06-01-01 (Field Reports): Case summaries must include all pertinent facts — who, what, when, where, how, and why. Reports must be clear, concise, accurate, and complete.
   - G06-01-02 (Case Supplementary Reports): Follow-up details, witness statements, and evidence documentation must be thorough and properly sequenced.
   - G04-02 (Crime Scene Processing): Evidence handling, chain of custody, and forensic observations must be correctly referenced.
   - G06-03 (Arrest Reports): When applicable, probable cause elements and suspect identification details must be present.
   - S04-14 (Preliminary Investigations): Initial response actions, scene security, and victim/witness canvass details should be documented.
   - G03-02 (Use of Force Reporting): If force was used, documentation must align with department policy.
3. Score out of 100:
   - Key facts coverage (up to 70 pts): Each key fact included = points proportional to total facts
   - General Order compliance (up to 15 pts): Proper report structure, required elements per GO standards
   - Professional quality (up to 15 pts): Clear organization, conciseness, professional tone, proper sequencing
   - Deductions for inaccurate information (-5 per error)
   - Deductions for including opinion instead of facts (-5 per instance)
   - Deductions for missing mandatory GO elements (-3 per omission)
4. Provide specific, actionable feedback referencing which General Orders the student should review.

RESPOND IN THIS EXACT JSON FORMAT (no markdown, just raw JSON):
{{
  "score": <0-100>,
  "feedback": "<2-3 sentences of specific feedback>",
  "key_facts_hit": ["<fact 1 they included>", "<fact 2>"],
  "key_facts_missed": ["<fact they missed 1>", "<fact they missed 2>"],
  "transcription": "<your best reading of their handwritten text>",
  "model_answer": "<the model answer>"
}}"""

        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Please read this handwritten case summary and grade it according to the instructions.",
                        },
                    ],
                }
            ],
            temperature=0.3,
            max_tokens=2000,
        )

        import json
        response_text = response.content[0].text.strip()
        # Try to parse JSON — handle cases where model wraps in markdown
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()

        result = json.loads(response_text)

        # Save the response
        await db.case_summary_responses.insert_one({
            "user_id": user.user_id,
            "question_id": data.question_id,
            "score": result.get("score", 0),
            "feedback": result.get("feedback", ""),
            "transcription": result.get("transcription", ""),
            "submitted_at": datetime.now(timezone.utc),
        })

        return result

    except json.JSONDecodeError:
        logging.error(f"Failed to parse AI grading response: {response_text[:200]}")
        return {
            "score": 0,
            "feedback": "Unable to grade your response. Please ensure the image is clear and try again.",
            "key_facts_hit": [],
            "key_facts_missed": key_facts,
            "model_answer": model_answer,
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Case summary grading error: {e}")
        raise HTTPException(status_code=500, detail=f"Grading failed: {str(e)}")


# ========== TTS ENDPOINT ==========

@api_router.post("/tts")
async def text_to_speech(data: TTSRequest, user: User = Depends(require_user)):
    """Generate high-quality speech audio using ElevenLabs TTS (primary) or OpenAI (fallback)"""
    import httpx

    # Limit text length to control costs
    text = data.text[:5000]

    # --- ElevenLabs (primary) ---
    if ELEVENLABS_API_KEY:
        try:
            # ElevenLabs voice IDs — natural, human-sounding voices
            voice_map = {
                "nova": "EXAVITQu4vr4xnSDxMaL",      # Sarah – warm, engaging female
                "alloy": "pFZP5JQG7iQjIQuC4Bku",      # Lily – calm female narrator
                "echo": "CwhRBWXzGAHq8TQ4Fs17",       # Roger – confident male
                "onyx": "TX3LPaxmHKxFdv7VOQHJ",       # Liam – deep male
                "shimmer": "XB0fDUnXU5powFXDhCwa",     # Charlotte – warm British female
                "fable": "jBpfuIE2acCO8z3wKNLl",       # George – warm British male
            }
            voice_id = voice_map.get(data.voice, voice_map["nova"])

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers={
                        "xi-api-key": ELEVENLABS_API_KEY,
                        "Content-Type": "application/json",
                    },
                    json={
                        "text": text,
                        "model_id": "eleven_turbo_v2_5",
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.75,
                            "style": 0.4,
                            "use_speaker_boost": True,
                        },
                    },
                )
                response.raise_for_status()
                return StreamingResponse(
                    iter([response.content]),
                    media_type="audio/mpeg",
                    headers={"Content-Disposition": "inline; filename=speech.mp3"},
                )
        except Exception as e:
            logging.error(f"ElevenLabs TTS error: {e}")
            # Fall through to OpenAI fallback

    # --- OpenAI fallback ---
    try:
        api_key = OPENAI_API_KEY or EMERGENT_LLM_KEY
        if not api_key:
            raise Exception("No TTS API key configured (set ELEVENLABS_API_KEY or OPENAI_API_KEY)")

        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=api_key)

        response = await client.audio.speech.create(
            model="tts-1-hd",
            voice=data.voice,
            input=text,
            response_format="mp3",
        )

        return StreamingResponse(
            iter([response.content]),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )
    except Exception as e:
        logging.error(f"TTS error (all providers failed): {e}")
        raise HTTPException(status_code=500, detail="Failed to generate speech audio")

# ========== STATS ENDPOINTS ==========

@api_router.get("/stats")
async def get_stats(user: User = Depends(require_user)):
    # Get total questions by type
    total_flashcards = await db.questions.count_documents({"type": "flashcard"})
    total_scenarios = await db.questions.count_documents({"type": "scenario"})
    
    # Get user progress - only fetch needed fields for performance
    progress = await db.user_progress.find(
        {"user_id": user.user_id}, 
        {"_id": 0, "attempts": 1, "last_score": 1}
    ).to_list(500)
    
    attempted_flashcards = len([p for p in progress if p.get("attempts", 0) > 0])
    attempted_scenarios = len([p for p in progress if p.get("last_score") is not None])
    
    bookmarks_count = await db.user_progress.count_documents(
        {"user_id": user.user_id, "bookmarked": True}
    )
    
    # Get average score for scenarios
    responses = await db.scenario_responses.find(
        {"user_id": user.user_id, "ai_grade": {"$ne": None}},
        {"_id": 0, "ai_grade": 1}
    ).to_list(500)
    
    avg_score = None
    if responses:
        scores = [r["ai_grade"] for r in responses if r.get("ai_grade") is not None]
        if scores:
            avg_score = sum(scores) / len(scores)
    
    return {
        "total_flashcards": total_flashcards,
        "total_scenarios": total_scenarios,
        "attempted_flashcards": attempted_flashcards,
        "attempted_scenarios": attempted_scenarios,
        "bookmarks": bookmarks_count,
        "average_score": avg_score,
        "total_responses": len(responses)
    }

# Leaderboard endpoint - shows ranking for registered users
@api_router.get("/leaderboard")
async def get_leaderboard(user: User = Depends(require_user)):
    # Only show leaderboard for registered users (not guests)
    if user.role == "guest":
        return {
            "leaderboard": [],
            "user_rank": None,
            "user_stats": None,
            "message": "Register to see your ranking compared to other users!"
        }
    
    # Aggregate scores for all registered users
    pipeline = [
        {"$match": {"ai_grade": {"$ne": None}}},
        {"$group": {
            "_id": "$user_id",
            "avg_score": {"$avg": "$ai_grade"},
            "total_attempts": {"$sum": 1},
            "best_score": {"$max": "$ai_grade"}
        }},
        {"$sort": {"avg_score": -1}}
    ]
    
    all_scores = await db.scenario_responses.aggregate(pipeline).to_list(100)
    
    # Batch fetch all user info to avoid N+1 queries
    user_ids = [entry["_id"] for entry in all_scores]
    users_cursor = db.users.find(
        {"user_id": {"$in": user_ids}},
        {"_id": 0, "user_id": 1, "full_name": 1, "name": 1, "role": 1}
    )
    users_map = {u["user_id"]: u async for u in users_cursor}
    
    # Get user info for each entry
    leaderboard = []
    user_rank = None
    user_stats = None
    
    for idx, entry in enumerate(all_scores):
        user_info = users_map.get(entry["_id"])
        
        # Skip only admin users from leaderboard (show registered and guests)
        if user_info and user_info.get("role") == "admin":
            continue
        
        rank = len(leaderboard) + 1
        display_name = user_info.get("full_name") or user_info.get("name", "Anonymous") if user_info else "Guest"
        
        leaderboard_entry = {
            "rank": rank,
            "name": display_name,
            "avg_score": round(entry["avg_score"], 1),
            "best_score": round(entry["best_score"], 1),
            "total_attempts": entry["total_attempts"],
            "is_current_user": entry["_id"] == user.user_id
        }
        leaderboard.append(leaderboard_entry)
        
        if entry["_id"] == user.user_id:
            user_rank = rank
            user_stats = leaderboard_entry
    
    return {
        "leaderboard": leaderboard[:20],  # Top 20
        "user_rank": user_rank,
        "user_stats": user_stats,
        "total_participants": len(leaderboard)
    }

# Reset scores endpoint - allows users to reset their progress
@api_router.post("/reset-scores")
async def reset_scores(user: User = Depends(require_user)):
    if user.role == "guest":
        return {"message": "Guest users cannot reset scores. Please register to track progress."}
    
    # Delete all scenario responses for this user
    responses_result = await db.scenario_responses.delete_many({"user_id": user.user_id})
    
    # Reset progress records (but keep bookmarks)
    progress_result = await db.user_progress.update_many(
        {"user_id": user.user_id},
        {"$set": {"attempts": 0, "last_score": None}}
    )
    
    return {
        "message": "Your scores have been reset successfully!",
        "responses_deleted": responses_result.deleted_count,
        "progress_reset": progress_result.modified_count
    }

# ========== ADMIN ANALYTICS ENDPOINTS ==========

async def require_admin(user: User = Depends(require_user)):
    """Dependency to check if user is admin"""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@api_router.get("/admin/analytics")
async def get_admin_analytics(user: User = Depends(require_admin)):
    """Get comprehensive analytics for admin dashboard"""
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # User Statistics
    total_registered_users = await db.users.count_documents({"role": {"$ne": "guest"}})
    total_guest_sessions = await db.user_sessions.count_documents({"is_guest": True})
    
    # Active users (users with sessions in last 24 hours)
    active_today = await db.user_sessions.count_documents({
        "last_activity": {"$gte": today_start}
    })
    
    # Active users this week
    active_this_week = await db.user_sessions.count_documents({
        "last_activity": {"$gte": week_ago}
    })
    
    # Active users this month
    active_this_month = await db.user_sessions.count_documents({
        "last_activity": {"$gte": month_ago}
    })
    
    # New registrations this week
    new_users_week = await db.users.count_documents({
        "role": {"$ne": "guest"},
        "created_at": {"$gte": week_ago}
    })
    
    # Content Statistics
    total_flashcards = await db.questions.count_documents({"type": "flashcard"})
    total_scenarios = await db.questions.count_documents({"type": "scenario"})
    total_mcqs = await db.questions.count_documents({"type": "multiple_choice"})
    
    # Quiz/Activity Statistics
    total_scenario_responses = await db.scenario_responses.count_documents({})
    total_quiz_attempts = await db.user_progress.count_documents({"attempts": {"$gte": 1}})
    
    # Average scores
    score_pipeline = [
        {"$match": {"ai_grade": {"$ne": None}}},
        {"$group": {
            "_id": None,
            "avg_score": {"$avg": "$ai_grade"},
            "total_graded": {"$sum": 1}
        }}
    ]
    score_result = await db.scenario_responses.aggregate(score_pipeline).to_list(1)
    avg_scenario_score = score_result[0]["avg_score"] if score_result else None
    
    # Most popular categories (by question attempts)
    category_pipeline = [
        {"$lookup": {
            "from": "questions",
            "localField": "question_id",
            "foreignField": "question_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$group": {
            "_id": "$question.category_name",
            "attempts": {"$sum": "$attempts"}
        }},
        {"$sort": {"attempts": -1}},
        {"$limit": 5}
    ]
    popular_categories = await db.user_progress.aggregate(category_pipeline).to_list(5)
    
    # Recent activity (last 10 scenario submissions)
    recent_activity = await db.scenario_responses.find(
        {},
        {"_id": 0, "user_id": 1, "question_id": 1, "ai_grade": 1, "submitted_at": 1}
    ).sort("submitted_at", -1).limit(10).to_list(10)
    
    # Batch fetch user names for recent activity to avoid N+1 queries
    activity_user_ids = list(set(a["user_id"] for a in recent_activity))
    activity_users_cursor = db.users.find(
        {"user_id": {"$in": activity_user_ids}},
        {"_id": 0, "user_id": 1, "name": 1, "email": 1}
    )
    activity_users_map = {u["user_id"]: u async for u in activity_users_cursor}
    
    for activity in recent_activity:
        user_doc = activity_users_map.get(activity["user_id"])
        activity["user_name"] = user_doc.get("name", "Guest") if user_doc else "Guest"
    
    # Daily active users for the past 7 days
    daily_stats = []
    for i in range(7):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        day_count = await db.user_sessions.count_documents({
            "last_activity": {"$gte": day_start, "$lt": day_end}
        })
        daily_stats.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "day": day_start.strftime("%a"),
            "active_users": day_count
        })
    daily_stats.reverse()
    
    return {
        "users": {
            "total_registered": total_registered_users,
            "total_guest_sessions": total_guest_sessions,
            "active_today": active_today,
            "active_this_week": active_this_week,
            "active_this_month": active_this_month,
            "new_registrations_week": new_users_week
        },
        "content": {
            "total_flashcards": total_flashcards,
            "total_scenarios": total_scenarios,
            "total_mcqs": total_mcqs,
            "total_questions": total_flashcards + total_scenarios + total_mcqs
        },
        "activity": {
            "total_scenario_responses": total_scenario_responses,
            "total_quiz_attempts": total_quiz_attempts,
            "average_scenario_score": round(avg_scenario_score, 1) if avg_scenario_score else None
        },
        "popular_categories": [
            {"category": cat["_id"] or "Unknown", "attempts": cat["attempts"]}
            for cat in popular_categories
        ],
        "recent_activity": recent_activity,
        "daily_active_users": daily_stats
    }

# Include the router in the main app


# ========== ADMIN DATA MIGRATION ENDPOINT ==========
@api_router.post("/admin/import-data")
async def import_data(data: Dict[str, List[Dict[str, Any]]]):
    """
    Import bulk data into the database
    Expected format: {
        "questions": [...],
        "categories": [...],
        "users": [...]
    }
    """
    try:
        results = {}
        
        # Import questions
        if "questions" in data and data["questions"]:
            await db.questions.delete_many({})
            result = await db.questions.insert_many(data["questions"])
            results["questions"] = len(result.inserted_ids)
        
        # Import categories
        if "categories" in data and data["categories"]:
            await db.categories.delete_many({})
            result = await db.categories.insert_many(data["categories"])
            results["categories"] = len(result.inserted_ids)
        
        # Import users (optional - might want to skip to preserve Railway users)
        if "users" in data and data["users"]:
            # Don't delete all users, just insert if not exists
            for user in data["users"]:
                existing = await db.users.find_one({"email": user.get("email")})
                if not existing:
                    await db.users.insert_one(user)
            results["users"] = "imported (duplicates skipped)"
        
        return {"status": "success", "imported": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@api_router.get("/admin/data-counts")
async def get_data_counts():
    """Get counts of all collections for verification"""
    return {
        "questions": await db.questions.count_documents({}),
        "categories": await db.categories.count_documents({}),
        "users": await db.users.count_documents({}),
        "flashcards": await db.questions.count_documents({"type": "flashcard"}),
        "scenarios": await db.questions.count_documents({"type": "scenario"}),
        "multiple_choice": await db.questions.count_documents({"type": "multiple_choice"}),
    }


@api_router.post("/admin/promote-to-admin")
async def promote_to_admin(email: str):
    """Promote a user to admin role"""
    result = await db.users.update_one(
        {"email": email.lower()},
        {"$set": {"role": "admin"}}
    )
    
    if result.modified_count > 0:
        return {"status": "success", "message": f"User {email} promoted to admin"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


class GrantPremiumRequest(BaseModel):
    email: str

@api_router.post("/admin/grant-premium")
async def grant_premium_by_email(data: GrantPremiumRequest, user: User = Depends(require_admin)):
    """Admin can grant premium access to any user by email"""
    result = await db.users.update_one(
        {"email": data.email.lower()},
        {"$set": {"has_paid": True, "paid_at": datetime.now(timezone.utc), "granted_by": "admin"}}
    )
    if result.modified_count > 0:
        return {"status": "success", "message": f"Premium granted to {data.email}"}
    elif result.matched_count > 0:
        return {"status": "success", "message": f"User {data.email} already has premium"}
    else:
        raise HTTPException(status_code=404, detail=f"User {data.email} not found")

@api_router.post("/admin/revoke-premium")
async def revoke_premium_by_email(data: GrantPremiumRequest, user: User = Depends(require_admin)):
    """Admin can revoke premium access from a user by email"""
    result = await db.users.update_one(
        {"email": data.email.lower()},
        {"$set": {"has_paid": False}, "$unset": {"granted_by": ""}}
    )
    if result.modified_count > 0:
        return {"status": "success", "message": f"Premium revoked from {data.email}"}
    else:
        raise HTTPException(status_code=404, detail=f"User {data.email} not found")

@api_router.get("/admin/users")
async def get_all_users(user: User = Depends(require_admin)):
    """Admin can view all users with their payment status"""
    # Batch fetch all completed payments to avoid N+1 queries
    all_payments = {}
    async for p in db.payments.find({"status": "completed"}, {"_id": 0, "user_id": 1}):
        all_payments[p["user_id"]] = True

    users = []
    async for u in db.users.find({}, {"_id": 0, "password_hash": 0}):
        uid = u.get("user_id")
        users.append({
            "email": u.get("email"),
            "name": u.get("name", ""),
            "role": u.get("role", "user"),
            "has_paid": u.get("has_paid", False) or (uid in all_payments),
            "granted_by": u.get("granted_by"),
            "created_at": str(u.get("created_at", "")),
        })
    return {"users": users, "total": len(users)}

@api_router.post("/admin/grant-premium-bulk")
async def grant_premium_bulk(emails: list[str], user: User = Depends(require_admin)):
    """Admin can grant premium to multiple users at once"""
    results = []
    for email in emails:
        r = await db.users.update_one(
            {"email": email.lower()},
            {"$set": {"has_paid": True, "paid_at": datetime.now(timezone.utc), "granted_by": "admin"}}
        )
        results.append({"email": email, "found": r.matched_count > 0, "updated": r.modified_count > 0})
    return {"results": results}

# Include the router in the main app


# ========== PAYMENT ENDPOINTS ==========

@api_router.get("/payments/status")
async def get_payment_status(user: User = Depends(require_user)):
    if user.role == "admin":
        return {"has_paid": True, "is_premium": True}
    if user.role == "guest":
        return {"has_paid": False, "is_premium": False}
    # Check if user has been manually granted premium
    user_doc = await db.users.find_one({"user_id": user.user_id})
    if user_doc and user_doc.get("has_paid"):
        return {"has_paid": True, "is_premium": True}
    payment = await db.payments.find_one(
        {"user_id": user.user_id, "status": "completed"},
        {"_id": 0}
    )
    has_paid = payment is not None
    return {"has_paid": has_paid, "is_premium": has_paid}


@api_router.post("/payments/create-checkout")
async def create_checkout_session(user: User = Depends(require_user)):
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe is not configured")
    if user.role == "guest":
        raise HTTPException(status_code=403, detail="Please register an account before purchasing premium access")
    existing_payment = await db.payments.find_one(
        {"user_id": user.user_id, "status": "completed"}, {"_id": 0}
    )
    if existing_payment:
        raise HTTPException(status_code=400, detail="You already have premium access")
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": "price_1T3f2sFaKA9n89CX3J8tKstA", "quantity": 1}],
            mode="payment",
            success_url="https://www.detectiveexamstudyguide.com/payment-success",
            cancel_url="https://www.detectiveexamstudyguide.com/upgrade",
            client_reference_id=user.user_id,
            customer_email=user.email,
            metadata={"user_id": user.user_id, "user_email": user.email}
        )
        payment_id = f"pay_{uuid.uuid4().hex[:12]}"
        await db.payments.insert_one({
            "payment_id": payment_id,
            "user_id": user.user_id,
            "stripe_session_id": checkout_session.id,
            "amount": 0, "currency": "usd", "status": "pending",
            "created_at": datetime.now(timezone.utc)
        })
        return {"checkout_url": checkout_session.url, "session_id": checkout_session.id}
    except stripe.error.StripeError as e:
        logging.error(f"Stripe error: {e}")
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")


@api_router.post("/payments/verify")
async def verify_payment(user: User = Depends(require_user)):
    payment = await db.payments.find_one(
        {"user_id": user.user_id, "status": "completed"}, {"_id": 0}
    )
    if payment:
        return {"verified": True, "has_paid": True}
    pending = await db.payments.find_one(
        {"user_id": user.user_id, "status": "pending"}, {"_id": 0}
    )
    if pending and pending.get("stripe_session_id"):
        try:
            session = stripe.checkout.Session.retrieve(pending["stripe_session_id"])
            if session.payment_status == "paid":
                await db.payments.update_one(
                    {"payment_id": pending["payment_id"]},
                    {"$set": {"status": "completed", "stripe_payment_intent": session.payment_intent, "amount": session.amount_total or 0}}
                )
                await db.users.update_one(
                    {"user_id": user.user_id},
                    {"$set": {"has_paid": True, "paid_at": datetime.now(timezone.utc)}}
                )
                return {"verified": True, "has_paid": True}
        except Exception as e:
            logging.error(f"Payment verification error: {e}")
    return {"verified": False, "has_paid": False}




# ========== ADMIN PAYMENT ENDPOINTS ==========

class SetPremiumRequest(BaseModel):
    question_ids: List[str]
    is_premium: bool

@api_router.post("/admin/set-premium")
async def set_questions_premium(data: SetPremiumRequest, user: User = Depends(require_admin)):
    result = await db.questions.update_many(
        {"question_id": {"$in": data.question_ids}},
        {"$set": {"is_premium": data.is_premium}}
    )
    return {"message": f"Updated {result.modified_count} questions", "is_premium": data.is_premium}

@api_router.get("/admin/payments")
async def get_payment_analytics(user: User = Depends(require_admin)):
    total_payments = await db.payments.count_documents({"status": "completed"})
    total_revenue_pipeline = [
        {"$match": {"status": "completed"}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    revenue_result = await db.payments.aggregate(total_revenue_pipeline).to_list(1)
    total_revenue = revenue_result[0]["total"] if revenue_result else 0
    recent_payments = await db.payments.find(
        {"status": "completed"}, {"_id": 0}
    ).sort("created_at", -1).limit(20).to_list(20)
    return {
        "total_payments": total_payments,
        "total_revenue_cents": total_revenue,
        "total_revenue_dollars": total_revenue / 100,
        "recent_payments": recent_payments
    }




# ========== ADMIN GRANT PREMIUM & ACCESS CODES ==========

class GrantPremiumRequest(BaseModel):
    email: str

@api_router.post("/admin/grant-premium")
async def grant_premium_by_email(data: GrantPremiumRequest, user: User = Depends(require_admin)):
    email = data.email.lower()
    target_user = await db.users.find_one({"email": email})
    if not target_user:
        raise HTTPException(status_code=404, detail=f"User {email} not found")
    await db.users.update_one(
        {"email": email},
        {"$set": {"has_paid": True, "paid_at": datetime.now(timezone.utc)}}
    )
    await db.payments.update_one(
        {"user_id": target_user["user_id"], "status": "completed"},
        {"$set": {
            "payment_id": f"admin-grant-{target_user['user_id']}-{int(datetime.now(timezone.utc).timestamp())}",
            "user_id": target_user["user_id"],
            "email": email,
            "status": "completed",
            "amount": 0,
            "stripe_session_id": "admin-granted",
            "created_at": datetime.now(timezone.utc),
            "granted_by": user.email
        }},
        upsert=True
    )
    return {"status": "success", "message": f"Premium access granted to {email}"}


class AccessCodeCreate(BaseModel):
    note: Optional[str] = None

@api_router.post("/admin/access-codes")
async def create_access_code(data: AccessCodeCreate = AccessCodeCreate(), user: User = Depends(require_admin)):
    import secrets
    code = secrets.token_urlsafe(16)
    await db.access_codes.insert_one({
        "code": code,
        "created_by": user.email,
        "created_at": datetime.now(timezone.utc),
        "redeemed": False,
        "redeemed_by": None,
        "redeemed_at": None,
        "note": data.note or ""
    })
    return {"code": code, "message": "Access code created successfully"}


@api_router.get("/admin/access-codes")
async def list_access_codes(user: User = Depends(require_admin)):
    codes = await db.access_codes.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
    return {"codes": codes}


class RedeemCodeRequest(BaseModel):
    code: str

@api_router.post("/access-codes/redeem")
async def redeem_access_code(data: RedeemCodeRequest, user: User = Depends(require_user)):
    if user.role == "guest":
        raise HTTPException(status_code=403, detail="Please register an account first")
    code_doc = await db.access_codes.find_one({"code": data.code, "redeemed": False})
    if not code_doc:
        raise HTTPException(status_code=404, detail="Invalid or already used access code")
    await db.access_codes.update_one(
        {"code": data.code},
        {"$set": {"redeemed": True, "redeemed_by": user.email, "redeemed_at": datetime.now(timezone.utc)}}
    )
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$set": {"has_paid": True, "paid_at": datetime.now(timezone.utc)}}
    )
    await db.payments.update_one(
        {"user_id": user.user_id, "status": "completed"},
        {"$set": {
            "payment_id": f"code-{data.code[:8]}-{user.user_id}",
            "user_id": user.user_id,
            "email": user.email,
            "status": "completed",
            "amount": 0,
            "stripe_session_id": f"access-code-{data.code}",
            "created_at": datetime.now(timezone.utc)
        }},
        upsert=True
    )
    return {"status": "success", "message": "Premium access activated!"}


@api_router.post("/admin/bootstrap-admin")
async def bootstrap_admin(email: str):
    result = await db.users.update_one({"email": email.lower()}, {"$set": {"role": "admin"}})
    if result.modified_count > 0:
        return {"status": "success", "message": f"User {email} promoted to admin"}
    raise HTTPException(status_code=404, detail="User not found")


# ========== RANKING QUESTIONS ==========

def grade_ranking(user_order: List[int], correct_order: List[int]) -> Dict[str, Any]:
    """Grade a ranking response using I/O Solutions differential weighting.

    For each item, score is based on displacement from correct position:
      displacement 0 = +2 (correct position)
      displacement 1 = +1 (close)
      displacement 2 =  0 (neutral)
      displacement 3 = -1 (counterproductive)
      displacement 4+ = -2 (harmful)

    Returns per-item scores and a normalized total (0-100).
    """
    weight_map = {0: 2, 1: 1, 2: 0, 3: -1}
    num_items = len(correct_order)
    item_scores = []

    for i in range(num_items):
        # Find where the user placed item i
        user_pos = user_order.index(i) if i in user_order else num_items - 1
        correct_pos = correct_order.index(i) if i in correct_order else num_items - 1
        displacement = abs(user_pos - correct_pos)
        score = weight_map.get(displacement, -2)
        item_scores.append({
            "item_index": i,
            "user_position": user_pos + 1,      # 1-based for display
            "correct_position": correct_pos + 1,  # 1-based for display
            "displacement": displacement,
            "score": score
        })

    total_raw = sum(s["score"] for s in item_scores)
    max_possible = num_items * 2   # all +2
    min_possible = num_items * -2  # all -2
    # Normalize to 0-100
    normalized = round(((total_raw - min_possible) / (max_possible - min_possible)) * 100) if max_possible != min_possible else 0

    return {
        "item_scores": item_scores,
        "total_raw": total_raw,
        "max_possible": max_possible,
        "normalized_score": normalized
    }


@api_router.post("/rankings/submit")
async def submit_ranking(data: RankingSubmit, user: User = Depends(require_user)):
    # Get the question
    question = await db.questions.find_one({"question_id": data.question_id, "type": "ranking"}, {"_id": 0})
    if not question:
        raise HTTPException(status_code=404, detail="Ranking question not found")

    correct_order = question.get("correct_order", [])
    items = question.get("items", [])

    if len(data.user_order) != len(correct_order):
        raise HTTPException(status_code=400, detail=f"Expected {len(correct_order)} items in ranking, got {len(data.user_order)}")

    # Grade using I/O differential weighting
    result = grade_ranking(data.user_order, correct_order)

    # Enrich item scores with labels and text
    for item_score in result["item_scores"]:
        idx = item_score["item_index"]
        if idx < len(items):
            item_score["label"] = items[idx]["label"]
            item_score["text"] = items[idx]["text"]

    # Save response
    response_id = f"rrank_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc)

    await db.ranking_responses.insert_one({
        "response_id": response_id,
        "user_id": user.user_id,
        "question_id": data.question_id,
        "user_order": data.user_order,
        "correct_order": correct_order,
        "item_scores": result["item_scores"],
        "total_raw": result["total_raw"],
        "normalized_score": result["normalized_score"],
        "time_taken": data.time_taken,
        "submitted_at": now
    })

    # Update user progress
    await db.user_progress.update_one(
        {"user_id": user.user_id, "question_id": data.question_id},
        {
            "$set": {
                "last_score": result["normalized_score"],
                "last_attempted": now
            },
            "$inc": {"attempts": 1},
            "$setOnInsert": {
                "progress_id": f"prog_{uuid.uuid4().hex[:12]}",
                "user_id": user.user_id,
                "question_id": data.question_id,
                "bookmarked": False,
                "created_at": now
            }
        },
        upsert=True
    )

    return {
        "response_id": response_id,
        "normalized_score": result["normalized_score"],
        "total_raw": result["total_raw"],
        "max_possible": result["max_possible"],
        "item_scores": result["item_scores"],
        "explanation": question.get("explanation", "")
    }


@api_router.get("/rankings/history")
async def get_ranking_history(user: User = Depends(require_user)):
    responses = await db.ranking_responses.find(
        {"user_id": user.user_id},
        {"_id": 0}
    ).sort("submitted_at", -1).limit(50).to_list(50)
    return responses


# ========== MIXED EXAM (MCQ) ENDPOINTS ==========

@api_router.post("/exam/submit")
async def submit_exam_answer(data: ExamAnswerSubmit, user: User = Depends(require_user)):
    """Grade a most_appropriate, least_appropriate, legal_trap, or digital_evidence question."""
    question = await db.questions.find_one(
        {"question_id": data.question_id, "type": {"$in": ["most_appropriate", "least_appropriate", "legal_trap", "digital_evidence"]}},
        {"_id": 0}
    )
    if not question:
        raise HTTPException(status_code=404, detail="Exam question not found")

    correct_answer = question.get("correct_answer", "")
    io_scores = question.get("io_scores", {})
    is_correct = data.selected_answer == correct_answer

    # Get I/O score for the selected answer
    io_score = io_scores.get(data.selected_answer, 0)
    max_score = 2  # +2 is always max

    # Normalize to 0-100
    normalized = round(((io_score - (-2)) / (max_score - (-2))) * 100)

    response_id = f"exam_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc)

    await db.exam_responses.insert_one({
        "response_id": response_id,
        "user_id": user.user_id,
        "question_id": data.question_id,
        "question_type": question["type"],
        "selected_answer": data.selected_answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct,
        "io_score": io_score,
        "normalized_score": normalized,
        "time_taken": data.time_taken,
        "submitted_at": now
    })

    # Update user progress
    await db.user_progress.update_one(
        {"user_id": user.user_id, "question_id": data.question_id},
        {
            "$set": {"last_score": normalized, "last_attempted": now},
            "$inc": {"attempts": 1},
            "$setOnInsert": {
                "progress_id": f"prog_{uuid.uuid4().hex[:12]}",
                "user_id": user.user_id,
                "question_id": data.question_id,
                "bookmarked": False,
                "created_at": now
            }
        },
        upsert=True
    )

    # Build per-option feedback
    option_feedback = []
    for opt in question.get("options", []):
        label = opt["label"]
        score = io_scores.get(label, 0)
        option_feedback.append({
            "label": label,
            "text": opt["text"],
            "io_score": score,
            "is_correct": label == correct_answer,
            "is_selected": label == data.selected_answer
        })

    return {
        "response_id": response_id,
        "is_correct": is_correct,
        "selected_answer": data.selected_answer,
        "correct_answer": correct_answer,
        "io_score": io_score,
        "normalized_score": normalized,
        "explanation": question.get("explanation", ""),
        "reference": question.get("reference", ""),
        "option_feedback": option_feedback
    }


@api_router.get("/exam/history")
async def get_exam_history(user: User = Depends(require_user)):
    responses = await db.exam_responses.find(
        {"user_id": user.user_id},
        {"_id": 0}
    ).sort("submitted_at", -1).limit(100).to_list(100)
    return responses


# ========== MINI SCENARIO ENDPOINTS ==========

@api_router.post("/mini-scenarios/submit")
async def submit_mini_scenario(data: MiniScenarioSubmit, user: User = Depends(require_user)):
    """Grade a mini scenario using AI (shorter than full 20-min scenarios)."""
    question = await db.questions.find_one({"question_id": data.question_id, "type": "mini_scenario"}, {"_id": 0})
    if not question:
        raise HTTPException(status_code=404, detail="Mini scenario not found")

    # Grade with OpenAI
    try:
        from openai import AsyncOpenAI

        api_key = OPENAI_API_KEY or EMERGENT_LLM_KEY
        if not api_key:
            raise Exception("No API key configured")

        client = AsyncOpenAI(api_key=api_key, base_url="https://api.openai.com/v1")

        prompt = f"""Grade this detective exam mini-scenario response using the R.E.A.C.T.I.O.N. framework.

SCENARIO:
{question['content']}

CORRECT ANSWER/KEY POINTS:
{question.get('answer', 'Use your best judgment based on CPD procedures and Illinois law')}

STUDENT RESPONSE:
{data.user_response}

This is a MINI SCENARIO — the student was asked to provide 8-12 bullet points of investigative steps. Grade based on:
1. Correct prioritization (most critical actions first)
2. Completeness across R.E.A.C.T.I.O.N. categories
3. Scenario-specific actions (not generic responses)

Use I/O Solutions differential weighting:
+2 = Critical actions correctly prioritized
+1 = Good actions included but lower priority
 0 = Neutral or unnecessary actions
-1 = Actions that could compromise the investigation
-2 = Actions that are harmful or violate procedure

GRADE: [number 0-100]
FEEDBACK:
**R – Respond & Render Aid**
- [assessment of student's actions in this area]

**E – Establish the Scene**
- [assessment]

**A – Arrest/Detain & Advise**
- [assessment]

**C – Collect/Identify Witnesses**
- [assessment]

**T – Take Notes & Document**
- [assessment]

**I – Inventory & Process Evidence**
- [assessment]

**O – Obtain Legal/Consult**
- [assessment]

**N – Next Steps & Notification**
- [assessment]

**Overall:** [brief summary with strongest areas, gaps, and specific recommendations]"""

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert grader for CPD detective exam mini-scenarios. Grade using the R.E.A.C.T.I.O.N. framework with I/O Solutions differential weighting. Be specific and reference the scenario facts. Answers should be graded against CPD General Orders (G03-02 Use of Force, G03-06 OIS, G06-01 Arrests, G04-02 Search Warrants, G06-22 Crime Scene Processing, etc.), Special Orders (S03-14 BWC, S04-13-09 ISR, S06-01 Evidence Processing, S04-19 Domestic Violence, S06-06 Felony Review, etc.), and relevant case law (Terry v. Ohio, Miranda v. Arizona, Graham v. Connor, Tennessee v. Garner, Riley v. California, Carpenter v. United States, Illinois v. Gates, 725 ILCS 5/103-2.1, etc.). Award bonus points for correct citations. CRITICAL: COPA is ONLY for OFFICER-INVOLVED shootings/incidents — do NOT expect COPA in civilian shooting scenarios."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        ai_response = response.choices[0].message.content
        grade = None
        feedback = ai_response

        if "GRADE:" in ai_response:
            parts = ai_response.split("GRADE:", 1)[1].split("FEEDBACK:", 1)
            if len(parts) == 2:
                try:
                    grade = float(parts[0].strip())
                    feedback = parts[1].strip()
                except (ValueError, IndexError):
                    pass

    except Exception as e:
        logging.error(f"Mini scenario AI grading error: {e}")
        grade = None
        feedback = "Unable to grade automatically. Please review with instructor."

    response_id = f"mresp_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc)

    await db.scenario_responses.insert_one({
        "response_id": response_id,
        "user_id": user.user_id,
        "question_id": data.question_id,
        "user_response": data.user_response,
        "ai_grade": grade,
        "ai_feedback": feedback,
        "time_taken": data.time_taken,
        "is_mini": True,
        "submitted_at": now
    })

    await db.user_progress.update_one(
        {"user_id": user.user_id, "question_id": data.question_id},
        {
            "$set": {"last_score": grade, "last_attempted": now},
            "$inc": {"attempts": 1},
            "$setOnInsert": {
                "progress_id": f"prog_{uuid.uuid4().hex[:12]}",
                "user_id": user.user_id,
                "question_id": data.question_id,
                "bookmarked": False,
                "created_at": now
            }
        },
        upsert=True
    )

    return {
        "response_id": response_id,
        "grade": grade,
        "feedback": feedback
    }


# ========== ADMIN SEED ENDPOINT ==========
@api_router.post("/admin/seed-exam-questions")
async def seed_exam_questions():
    """Seed ranking + mixed exam questions into the database.
    No auth required — idempotent upsert, safe to call multiple times."""
    try:
        from seed_ranking_questions import seed_ranking_questions
        from seed_mixed_exam_questions import seed_mixed_exam
        from seed_legal_trap_extra import seed_legal_trap_extra
        from seed_additional_exam_questions import seed_additional_exam_questions
        from seed_g03_06_firearm_discharge import seed_g03_06_questions
        from seed_situational_judgment import seed_situational_judgment
        from seed_case_summary import seed_case_summary

        await seed_ranking_questions(ext_db=db)
        await seed_mixed_exam(ext_db=db)
        await seed_legal_trap_extra(ext_db=db)
        await seed_additional_exam_questions(ext_db=db)
        await seed_g03_06_questions(ext_db=db)
        await seed_situational_judgment(ext_db=db)
        await seed_case_summary(ext_db=db)

        counts = {
            "ranking": await db.questions.count_documents({"type": "ranking"}),
            "most_appropriate": await db.questions.count_documents({"type": "most_appropriate"}),
            "least_appropriate": await db.questions.count_documents({"type": "least_appropriate"}),
            "legal_trap": await db.questions.count_documents({"type": "legal_trap"}),
            "digital_evidence": await db.questions.count_documents({"type": "digital_evidence"}),
            "mini_scenario": await db.questions.count_documents({"type": "mini_scenario"}),
            "g03_06_firearm_discharge": await db.questions.count_documents({"category_id": "cat_g03_06_firearm_discharge"}),
            "situational_judgment": await db.questions.count_documents({"category_id": "cat_situational_judgment"}),
            "case_management": await db.questions.count_documents({"category_id": "cat_case_management"}),
            "case_summary": await db.questions.count_documents({"category_id": "cat_case_summary"}),
        }
        return {"status": "success", "counts": counts}
    except Exception as e:
        logging.error(f"Seed failed: {e}")
        raise HTTPException(status_code=500, detail=f"Seed failed: {str(e)}")


# ========== FEEDBACK ENDPOINTS ==========

@api_router.post("/feedback")
async def submit_feedback(data: FeedbackSubmit, user: User = Depends(require_user)):
    """User submits feedback/correction on AI grading."""
    # Look up the scenario response to capture original grade/feedback
    scenario_resp = await db.scenario_responses.find_one(
        {"response_id": data.response_id},
        {"_id": 0}
    )

    # Look up question title
    question = await db.questions.find_one(
        {"question_id": data.question_id},
        {"_id": 0, "title": 1}
    )

    feedback_id = f"fb_{uuid.uuid4().hex[:12]}"
    feedback_doc = {
        "feedback_id": feedback_id,
        "user_id": user.user_id,
        "user_name": user.name,
        "user_email": user.email,
        "response_id": data.response_id,
        "question_id": data.question_id,
        "question_title": question.get("title", "Unknown") if question else "Unknown",
        "feedback_type": data.feedback_type,
        "user_message": data.user_message,
        "ai_grade": scenario_resp.get("ai_grade") if scenario_resp else None,
        "ai_feedback": scenario_resp.get("ai_feedback") if scenario_resp else None,
        "status": "pending",
        "admin_notes": None,
        "submitted_at": datetime.now(timezone.utc),
        "reviewed_at": None,
    }

    await db.feedback.insert_one(feedback_doc)
    return {"feedback_id": feedback_id, "message": "Feedback submitted successfully"}

@api_router.get("/admin/feedback")
async def get_admin_feedback(status: Optional[str] = None, admin: User = Depends(require_admin)):
    """Admin gets all feedback, optionally filtered by status."""
    query = {}
    if status and status in ("pending", "approved", "rejected"):
        query["status"] = status

    items = await db.feedback.find(query, {"_id": 0}).sort("submitted_at", -1).to_list(200)
    return {"feedback": items}

@api_router.put("/admin/feedback/{feedback_id}")
async def review_feedback(feedback_id: str, data: FeedbackReview, admin: User = Depends(require_admin)):
    """Admin approves or rejects feedback."""
    if data.status not in ("approved", "rejected"):
        raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")

    result = await db.feedback.update_one(
        {"feedback_id": feedback_id},
        {"$set": {
            "status": data.status,
            "admin_notes": data.admin_notes,
            "reviewed_at": datetime.now(timezone.utc),
        }}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return {"message": f"Feedback {data.status}", "feedback_id": feedback_id}

@api_router.get("/admin/feedback/count")
async def get_feedback_count(admin: User = Depends(require_admin)):
    """Get count of pending feedback items."""
    pending = await db.feedback.count_documents({"status": "pending"})
    return {"pending_count": pending}

@api_router.get("/corrections")
async def get_corrections(user: User = Depends(require_user)):
    """Get approved corrections from the last 7 days for users to see."""
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    items = await db.feedback.find(
        {"status": "approved", "reviewed_at": {"$gte": seven_days_ago}},
        {"_id": 0, "feedback_id": 1, "question_title": 1, "feedback_type": 1,
         "user_message": 1, "admin_notes": 1, "reviewed_at": 1, "question_id": 1}
    ).sort("reviewed_at", -1).to_list(50)
    return {"corrections": items}


app.include_router(api_router)


# ========== STRIPE WEBHOOK (on app, not api_router) ==========
from fastapi import Request as FastAPIRequest

async def _handle_stripe_webhook(request: FastAPIRequest):
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event["type"]

    if event_type == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("client_reference_id")
        if user_id:
            await db.payments.update_one(
                {"stripe_session_id": session["id"]},
                {"$set": {"status": "completed", "stripe_payment_intent": session.get("payment_intent"), "amount": session.get("amount_total", 0)}}
            )
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {"has_paid": True, "paid_at": datetime.now(timezone.utc)}}
            )
            logging.info(f"Payment completed for user {user_id}")

    elif event_type == "customer.subscription.created":
        sub = event["data"]["object"]
        cust_id = sub.get("customer")
        if cust_id:
            user = await db.users.find_one({"stripe_customer_id": cust_id})
            if user:
                await db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"has_paid": True, "subscription_status": "active", "stripe_subscription_id": sub["id"]}}
                )
                logging.info(f"Subscription created for customer {cust_id}")

    elif event_type == "customer.subscription.deleted":
        sub = event["data"]["object"]
        cust_id = sub.get("customer")
        if cust_id:
            user = await db.users.find_one({"stripe_customer_id": cust_id})
            if user:
                await db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"has_paid": False, "subscription_status": "cancelled", "stripe_subscription_id": None}}
                )
                logging.info(f"Subscription deleted for customer {cust_id}")

    elif event_type == "invoice.payment_failed":
        invoice = event["data"]["object"]
        cust_id = invoice.get("customer")
        if cust_id:
            user = await db.users.find_one({"stripe_customer_id": cust_id})
            if user:
                await db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"subscription_status": "past_due"}}
                )
                logging.info(f"Payment failed for customer {cust_id}")

    return {"received": True}

@app.post("/stripe/webhook")
async def stripe_webhook(request: FastAPIRequest):
    return await _handle_stripe_webhook(request)

@app.post("/api/webhooks/stripe")
async def stripe_webhook_alt(request: FastAPIRequest):
    return await _handle_stripe_webhook(request)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== STARTUP: CREATE MONGODB INDEXES ==========
@app.on_event("startup")
async def create_indexes():
    """Create MongoDB indexes for performance on startup"""
    try:
        # Questions: speed up filtered queries by type+category
        await db.questions.create_index([("type", 1), ("category_id", 1)])
        await db.questions.create_index("question_id", unique=True)
        # User progress: speed up per-user lookups
        await db.user_progress.create_index([("user_id", 1), ("question_id", 1)])
        await db.user_progress.create_index([("user_id", 1), ("bookmarked", 1)])
        # Scenario responses: speed up history and leaderboard
        await db.scenario_responses.create_index([("user_id", 1), ("submitted_at", -1)])
        await db.scenario_responses.create_index("ai_grade")
        # Sessions: speed up auth lookups
        await db.user_sessions.create_index("session_token", unique=True)
        await db.user_sessions.create_index("user_id")
        await db.user_sessions.create_index("expires_at")
        # Payments: speed up payment status checks
        await db.payments.create_index([("user_id", 1), ("status", 1)])
        # Feedback
        await db.feedback.create_index([("status", 1), ("submitted_at", -1)])
        logging.info("MongoDB indexes created successfully")
    except Exception as e:
        logging.error(f"Failed to create indexes: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# Serve dashboard static files
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="dashboard-assets")

    @app.get("/{full_path:path}")
    async def serve_dashboard(full_path: str):
        """Catch-all route: serve dashboard index.html for non-API routes."""
        file_path = STATIC_DIR / full_path
        if full_path and file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(STATIC_DIR / "index.html"))
