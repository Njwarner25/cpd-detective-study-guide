#!/usr/bin/env python3
"""
Chicago PD Detective Exam Study Guide - Backend API Tests
Tests all backend endpoints for functionality and authentication
"""

import asyncio
import aiohttp
import json
import uuid
from datetime import datetime
import sys
import os

# Backend URL from frontend .env
BACKEND_URL = "https://detective-prep.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.session = None
        self.regular_user_token = None
        self.admin_user_token = None
        self.regular_user_id = None
        self.admin_user_id = None
        self.test_question_id = None
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }

    async def setup_session(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()

    async def cleanup_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

    def log_result(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        
        if success:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            self.results["errors"].append(f"{test_name}: {message}")

    async def test_auth_register(self):
        """Test user registration"""
        test_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
        test_data = {
            "email": test_email,
            "password": "testpass123",
            "name": "Test Detective"
        }
        
        try:
            async with self.session.post(f"{BACKEND_URL}/auth/register", json=test_data) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "user_id" in data and "email" in data:
                        self.regular_user_id = data["user_id"]
                        # Extract session token from cookies
                        cookies = resp.cookies
                        if "session_token" in cookies:
                            self.regular_user_token = cookies["session_token"].value
                            self.log_result("Auth Register", True, f"Created user: {data['email']}")
                        else:
                            self.log_result("Auth Register", False, "No session token in response")
                    else:
                        self.log_result("Auth Register", False, f"Missing user data in response: {data}")
                else:
                    error_text = await resp.text()
                    self.log_result("Auth Register", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Auth Register", False, f"Exception: {str(e)}")

    async def test_auth_login(self):
        """Test user login with admin credentials"""
        admin_data = {
            "email": "admin@cpd.test",
            "password": "admin123"
        }
        
        try:
            async with self.session.post(f"{BACKEND_URL}/auth/login", json=admin_data) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "user_id" in data and data.get("role") == "admin":
                        self.admin_user_id = data["user_id"]
                        # Extract session token from cookies
                        cookies = resp.cookies
                        if "session_token" in cookies:
                            self.admin_user_token = cookies["session_token"].value
                            self.log_result("Auth Login (Admin)", True, f"Admin logged in: {data['email']}")
                        else:
                            self.log_result("Auth Login (Admin)", False, "No session token in response")
                    else:
                        self.log_result("Auth Login (Admin)", False, f"Invalid admin login response: {data}")
                else:
                    error_text = await resp.text()
                    self.log_result("Auth Login (Admin)", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Auth Login (Admin)", False, f"Exception: {str(e)}")

    async def test_auth_me(self):
        """Test get current user endpoint"""
        if not self.regular_user_token:
            self.log_result("Auth Me", False, "No regular user token available")
            return

        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.get(f"{BACKEND_URL}/auth/me", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "user_id" in data and "email" in data:
                        self.log_result("Auth Me", True, f"Retrieved user: {data['email']}")
                    else:
                        self.log_result("Auth Me", False, f"Missing user data: {data}")
                else:
                    error_text = await resp.text()
                    self.log_result("Auth Me", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Auth Me", False, f"Exception: {str(e)}")

    async def test_auth_logout(self):
        """Test logout endpoint"""
        if not self.regular_user_token:
            self.log_result("Auth Logout", False, "No regular user token available")
            return

        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.post(f"{BACKEND_URL}/auth/logout", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "message" in data:
                        self.log_result("Auth Logout", True, "User logged out successfully")
                    else:
                        self.log_result("Auth Logout", False, f"Unexpected response: {data}")
                else:
                    error_text = await resp.text()
                    self.log_result("Auth Logout", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Auth Logout", False, f"Exception: {str(e)}")

    async def test_questions_get_all(self):
        """Test get all questions"""
        if not self.admin_user_token:
            self.log_result("Questions Get All", False, "No admin token available")
            return

        try:
            cookies = {"session_token": self.admin_user_token}
            async with self.session.get(f"{BACKEND_URL}/questions", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        self.log_result("Questions Get All", True, f"Retrieved {len(data)} questions")
                        # Store a question ID for later tests
                        if data and "question_id" in data[0]:
                            self.test_question_id = data[0]["question_id"]
                    else:
                        self.log_result("Questions Get All", False, f"Expected list, got: {type(data)}")
                else:
                    error_text = await resp.text()
                    self.log_result("Questions Get All", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Questions Get All", False, f"Exception: {str(e)}")

    async def test_questions_get_flashcards(self):
        """Test get flashcards only"""
        if not self.admin_user_token:
            self.log_result("Questions Get Flashcards", False, "No admin token available")
            return

        try:
            cookies = {"session_token": self.admin_user_token}
            async with self.session.get(f"{BACKEND_URL}/questions?type=flashcard", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        flashcard_count = len([q for q in data if q.get("type") == "flashcard"])
                        if flashcard_count == len(data):
                            self.log_result("Questions Get Flashcards", True, f"Retrieved {len(data)} flashcards")
                        else:
                            self.log_result("Questions Get Flashcards", False, f"Mixed types in response")
                    else:
                        self.log_result("Questions Get Flashcards", False, f"Expected list, got: {type(data)}")
                else:
                    error_text = await resp.text()
                    self.log_result("Questions Get Flashcards", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Questions Get Flashcards", False, f"Exception: {str(e)}")

    async def test_questions_get_scenarios(self):
        """Test get scenarios only"""
        if not self.admin_user_token:
            self.log_result("Questions Get Scenarios", False, "No admin token available")
            return

        try:
            cookies = {"session_token": self.admin_user_token}
            async with self.session.get(f"{BACKEND_URL}/questions?type=scenario", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        scenario_count = len([q for q in data if q.get("type") == "scenario"])
                        if scenario_count == len(data):
                            self.log_result("Questions Get Scenarios", True, f"Retrieved {len(data)} scenarios")
                        else:
                            self.log_result("Questions Get Scenarios", False, f"Mixed types in response")
                    else:
                        self.log_result("Questions Get Scenarios", False, f"Expected list, got: {type(data)}")
                else:
                    error_text = await resp.text()
                    self.log_result("Questions Get Scenarios", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Questions Get Scenarios", False, f"Exception: {str(e)}")

    async def test_questions_get_specific(self):
        """Test get specific question"""
        if not self.admin_user_token or not self.test_question_id:
            self.log_result("Questions Get Specific", False, "No admin token or question ID available")
            return

        try:
            cookies = {"session_token": self.admin_user_token}
            async with self.session.get(f"{BACKEND_URL}/questions/{self.test_question_id}", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "question_id" in data and data["question_id"] == self.test_question_id:
                        self.log_result("Questions Get Specific", True, f"Retrieved question: {data.get('title', 'No title')}")
                    else:
                        self.log_result("Questions Get Specific", False, f"Question ID mismatch or missing")
                else:
                    error_text = await resp.text()
                    self.log_result("Questions Get Specific", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Questions Get Specific", False, f"Exception: {str(e)}")

    async def test_questions_create_admin(self):
        """Test create question (admin only)"""
        if not self.admin_user_token:
            self.log_result("Questions Create (Admin)", False, "No admin token available")
            return

        question_data = {
            "type": "flashcard",
            "category_id": "cat_001",
            "category_name": "Criminal Law",
            "title": "Test Question - Theft Definition",
            "content": "What constitutes theft under Illinois law?",
            "answer": "Taking property without consent with intent to permanently deprive the owner",
            "explanation": "Illinois Compiled Statutes 720 ILCS 5/16-1",
            "difficulty": "medium",
            "reference": "720 ILCS 5/16-1"
        }

        try:
            cookies = {"session_token": self.admin_user_token}
            async with self.session.post(f"{BACKEND_URL}/questions", json=question_data, cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "question_id" in data and data.get("title") == question_data["title"]:
                        self.log_result("Questions Create (Admin)", True, f"Created question: {data['question_id']}")
                        # Store for update/delete tests
                        self.created_question_id = data["question_id"]
                    else:
                        self.log_result("Questions Create (Admin)", False, f"Invalid response: {data}")
                else:
                    error_text = await resp.text()
                    self.log_result("Questions Create (Admin)", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Questions Create (Admin)", False, f"Exception: {str(e)}")

    async def test_questions_create_regular_user(self):
        """Test create question as regular user (should fail)"""
        if not self.regular_user_token:
            # Re-login regular user since we logged out
            await self.test_auth_register()
        
        if not self.regular_user_token:
            self.log_result("Questions Create (Regular User)", False, "No regular user token available")
            return

        question_data = {
            "type": "flashcard",
            "category_id": "cat_001",
            "category_name": "Criminal Law",
            "title": "Unauthorized Question",
            "content": "This should not be created",
            "answer": "Should fail",
            "difficulty": "easy"
        }

        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.post(f"{BACKEND_URL}/questions", json=question_data, cookies=cookies) as resp:
                if resp.status == 403:
                    self.log_result("Questions Create (Regular User)", True, "Correctly rejected non-admin user")
                elif resp.status == 401:
                    self.log_result("Questions Create (Regular User)", True, "Correctly rejected unauthenticated user")
                else:
                    error_text = await resp.text()
                    self.log_result("Questions Create (Regular User)", False, f"Should have been rejected, got status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Questions Create (Regular User)", False, f"Exception: {str(e)}")

    async def test_bookmarks_toggle(self):
        """Test bookmark toggle"""
        if not self.regular_user_token or not self.test_question_id:
            self.log_result("Bookmarks Toggle", False, "No regular user token or question ID available")
            return

        bookmark_data = {
            "question_id": self.test_question_id
        }

        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.post(f"{BACKEND_URL}/bookmarks/toggle", json=bookmark_data, cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "bookmarked" in data:
                        self.log_result("Bookmarks Toggle", True, f"Bookmark toggled: {data['bookmarked']}")
                    else:
                        self.log_result("Bookmarks Toggle", False, f"Missing bookmarked field: {data}")
                else:
                    error_text = await resp.text()
                    self.log_result("Bookmarks Toggle", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Bookmarks Toggle", False, f"Exception: {str(e)}")

    async def test_bookmarks_get(self):
        """Test get user bookmarks"""
        if not self.regular_user_token:
            self.log_result("Bookmarks Get", False, "No regular user token available")
            return

        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.get(f"{BACKEND_URL}/bookmarks", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        self.log_result("Bookmarks Get", True, f"Retrieved {len(data)} bookmarked questions")
                    else:
                        self.log_result("Bookmarks Get", False, f"Expected list, got: {type(data)}")
                else:
                    error_text = await resp.text()
                    self.log_result("Bookmarks Get", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Bookmarks Get", False, f"Exception: {str(e)}")

    async def test_progress_get(self):
        """Test get progress for a question"""
        if not self.regular_user_token or not self.test_question_id:
            self.log_result("Progress Get", False, "No regular user token or question ID available")
            return

        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.get(f"{BACKEND_URL}/progress/{self.test_question_id}", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "bookmarked" in data:
                        self.log_result("Progress Get", True, f"Retrieved progress data")
                    else:
                        self.log_result("Progress Get", False, f"Missing expected fields: {data}")
                else:
                    error_text = await resp.text()
                    self.log_result("Progress Get", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Progress Get", False, f"Exception: {str(e)}")

    async def test_scenarios_submit(self):
        """Test scenario submission with AI grading"""
        if not self.regular_user_token:
            self.log_result("Scenarios Submit", False, "No regular user token available")
            return

        # First get a scenario question
        scenario_id = None
        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.get(f"{BACKEND_URL}/questions?type=scenario", cookies=cookies) as resp:
                if resp.status == 200:
                    scenarios = await resp.json()
                    if scenarios:
                        scenario_id = scenarios[0]["question_id"]
        except:
            pass

        if not scenario_id:
            self.log_result("Scenarios Submit", False, "No scenario questions available")
            return

        submit_data = {
            "question_id": scenario_id,
            "user_response": "I would first secure the scene, call for backup, and then interview witnesses to gather information about the incident. I would document all evidence and follow proper chain of custody procedures according to CPD directives.",
            "time_taken": 300  # 5 minutes
        }

        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.post(f"{BACKEND_URL}/scenarios/submit", json=submit_data, cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "response_id" in data and "feedback" in data:
                        grade = data.get("grade")
                        if grade is not None:
                            self.log_result("Scenarios Submit", True, f"AI grading successful, grade: {grade}")
                        else:
                            self.log_result("Scenarios Submit", True, "Response submitted (AI grading unavailable)")
                    else:
                        self.log_result("Scenarios Submit", False, f"Missing expected fields: {data}")
                else:
                    error_text = await resp.text()
                    self.log_result("Scenarios Submit", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Scenarios Submit", False, f"Exception: {str(e)}")

    async def test_scenarios_history(self):
        """Test get scenario submission history"""
        if not self.regular_user_token:
            self.log_result("Scenarios History", False, "No regular user token available")
            return

        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.get(f"{BACKEND_URL}/scenarios/history", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        self.log_result("Scenarios History", True, f"Retrieved {len(data)} scenario responses")
                    else:
                        self.log_result("Scenarios History", False, f"Expected list, got: {type(data)}")
                else:
                    error_text = await resp.text()
                    self.log_result("Scenarios History", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Scenarios History", False, f"Exception: {str(e)}")

    async def test_stats_get(self):
        """Test get user statistics"""
        if not self.regular_user_token:
            self.log_result("Stats Get", False, "No regular user token available")
            return

        try:
            cookies = {"session_token": self.regular_user_token}
            async with self.session.get(f"{BACKEND_URL}/stats", cookies=cookies) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    expected_fields = ["total_flashcards", "total_scenarios", "attempted_flashcards", "attempted_scenarios", "bookmarks"]
                    if all(field in data for field in expected_fields):
                        self.log_result("Stats Get", True, f"Retrieved user stats: {data}")
                    else:
                        missing = [f for f in expected_fields if f not in data]
                        self.log_result("Stats Get", False, f"Missing fields: {missing}")
                else:
                    error_text = await resp.text()
                    self.log_result("Stats Get", False, f"Status {resp.status}: {error_text}")
        except Exception as e:
            self.log_result("Stats Get", False, f"Exception: {str(e)}")

    async def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Chicago PD Detective Exam Backend API Tests")
        print(f"📡 Testing against: {BACKEND_URL}")
        print("=" * 60)

        await self.setup_session()

        try:
            # Authentication tests
            print("\n🔐 AUTHENTICATION TESTS")
            await self.test_auth_register()
            await self.test_auth_login()
            await self.test_auth_me()
            await self.test_auth_logout()

            # Question tests
            print("\n📚 QUESTION TESTS")
            await self.test_questions_get_all()
            await self.test_questions_get_flashcards()
            await self.test_questions_get_scenarios()
            await self.test_questions_get_specific()
            await self.test_questions_create_admin()
            await self.test_questions_create_regular_user()

            # Bookmark tests
            print("\n🔖 BOOKMARK TESTS")
            await self.test_bookmarks_toggle()
            await self.test_bookmarks_get()
            await self.test_progress_get()

            # Scenario tests
            print("\n🎭 SCENARIO TESTS")
            await self.test_scenarios_submit()
            await self.test_scenarios_history()

            # Stats tests
            print("\n📊 STATS TESTS")
            await self.test_stats_get()

        finally:
            await self.cleanup_session()

        # Print summary
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print("\n🚨 FAILED TESTS:")
            for error in self.results['errors']:
                print(f"   • {error}")

        success_rate = (self.results['passed'] / (self.results['passed'] + self.results['failed'])) * 100 if (self.results['passed'] + self.results['failed']) > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")

        return self.results['failed'] == 0

async def main():
    """Main test runner"""
    tester = BackendTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())