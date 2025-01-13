import unittest
from fastapi.testclient import TestClient
from app import app
from app.database.db import Base, engine
from datetime import date

class TestUserRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        Base.metadata.create_all(bind=engine)

    def setUp(self):
        # Setup test data if needed
        pass

    def tearDown(self):
        # Clean up test data
        pass

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def test_create_user_success(self):
        """Test successful user creation"""
        user_data = {
            "firstname": "John",
            "lastname": "Doe",
            "username": "johndoe",
            "password": "password123",
            "gender": "male",
            "date_of_birth": str(date(1990, 1, 1)),
            "email": "john@example.com",
            "phone_number": "+1234567890"
        }
        response = self.client.post("/users/", json=user_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["firstname"], "John")
        self.assertEqual(data["username"], "johndoe")

    def test_create_user_duplicate_username(self):
        """Test user creation with duplicate username"""
        user_data = {
            "firstname": "John",
            "lastname": "Doe",
            "username": "johndoe",
            "password": "password123",
            "gender": "male",
            "date_of_birth": str(date(1990, 1, 1)),
            "email": "john1@example.com",
            "phone_number": "+1234567890"
        }
        # Create first user
        self.client.post("/users/", json=user_data)
        
        # Try to create user with same username
        user_data["email"] = "john2@example.com"
        response = self.client.post("/users/", json=user_data)
        self.assertEqual(response.status_code, 400)

    def test_get_user(self):
        """Test getting a user by ID"""
        # First create a user
        user_data = {
            "firstname": "John",
            "lastname": "Doe",
            "username": "johndoe",
            "password": "password123",
            "gender": "male",
            "date_of_birth": str(date(1990, 1, 1)),
            "email": "john@example.com",
            "phone_number": "+1234567890"
        }
        create_response = self.client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]

        response = self.client.get(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "johndoe")

    def test_get_nonexistent_user(self):
        """Test getting a non-existent user"""
        response = self.client.get("/users/999999")
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """Test updating a user"""
        # First create a user
        user_data = {
            "firstname": "John",
            "lastname": "Doe",
            "username": "johndoe",
            "password": "password123",
            "gender": "male",
            "date_of_birth": str(date(1990, 1, 1)),
            "email": "john@example.com",
            "phone_number": "+1234567890"
        }
        create_response = self.client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]

        # Update the user
        update_data = user_data.copy()
        update_data["firstname"] = "Jane"
        response = self.client.put(f"/users/{user_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["firstname"], "Jane")

    def test_delete_user(self):
        """Test deleting a user"""
        # First create a user
        user_data = {
            "firstname": "John",
            "lastname": "Doe",
            "username": "johndoe",
            "password": "password123",
            "gender": "male",
            "date_of_birth": str(date(1990, 1, 1)),
            "email": "john@example.com",
            "phone_number": "+1234567890"
        }
        create_response = self.client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]

        # Delete the user
        response = self.client.delete(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)

        # Verify user is deleted
        get_response = self.client.get(f"/users/{user_id}")
        self.assertEqual(get_response.status_code, 404)