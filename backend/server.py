from fastapi import FastAPI, APIRouter, HTTPException, Depends, Cookie, Response, Header
from fastapi.responses import JSONResponse
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

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Current app version - UPDATE THIS WHEN RELEASING NEW VERSIONS
CURRENT_APP_VERSION = "1.5.0"
MINIMUM_REQUIRED_VERSION = "1.5.0"

# LLM Key
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')

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
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

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

@api_router.get("/questions", response_model=List[Question])
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
    
    # Limit results for production performance
    questions = await db.questions.find(query, {"_id": 0}).to_list(500)
    return questions

@api_router.get("/questions/{question_id}", response_model=Question)
async def get_question(question_id: str, user: User = Depends(require_user)):
    question = await db.questions.find_one({"question_id": question_id}, {"_id": 0})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
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
    
    # Grade with AI (if available)
    if not HAS_EMERGENT:
        # Fallback when emergentintegrations is not available (e.g., on Railway)
        return {
            "grade": 75,
            "feedback": "AI grading is not available in this deployment. Your response has been recorded. Please review the model answer below for self-assessment.",
            "model_answer": question.get('answer', 'Model answer not available'),
            "ai_graded": False
        }
    
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"grading_{uuid.uuid4().hex[:8]}",
            system_message="""You are an expert grader for Chicago Police Department detective exam scenarios. 
Your job is to evaluate responses based on:
- Knowledge of relevant laws and procedures
- Proper application of Chicago PD directives
- Logical reasoning and decision-making
- Clarity and completeness of response

Provide a grade from 0-100 and detailed feedback."""
        ).with_model("openai", "gpt-5.2")
        
        prompt = f"""Grade this detective exam scenario response:

SCENARIO:
{question['content']}

CORRECT ANSWER/KEY POINTS:
{question.get('answer', 'Use your best judgment based on CPD procedures and Illinois law')}

STUDENT RESPONSE:
{data.user_response}

Provide your response in this exact format:
GRADE: [number 0-100]
FEEDBACK: [detailed feedback explaining the grade, what was correct, what was missing, and how to improve]"""
        
        message = UserMessage(text=prompt)
        ai_response = await chat.send_message(message)
        
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

app.include_router(api_router)

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

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
# 1769751098
