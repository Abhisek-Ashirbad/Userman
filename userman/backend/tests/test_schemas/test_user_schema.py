import unittest
from datetime import date
from pydantic import ValidationError
from app.schemas.user_schema import UserBase, UserCreate, UserResponse

class TestUserSchema(unittest.TestCase):
    def test_valid_user_base(self):
        """Test valid user data validation"""
        user_data = {
            "firstname": "John",
            "lastname": "Doe",
            "username": "johndoe",
            "gender": "male",
            "date_of_birth": date(1990, 1, 1),
            "email": "john@example.com",
            "phone_number": "+1234567890"
        }
        user = UserBase(**user_data)
        self.assertEqual(user.firstname, "John")
        self.assertEqual(user.gender, "male")

    def test_invalid_gender(self):
        """Test gender validation"""
        user_data = {
            "firstname": "John",
            "lastname": "Doe",
            "username": "johndoe",
            "gender": "invalid",
            "date_of_birth": date(1990, 1, 1),
            "email": "john@example.com",
            "phone_number": "+1234567890"
        }
        with self.assertRaises(ValidationError):
            UserBase(**user_data)

    def test_invalid_phone_number(self):
        """Test phone number validation"""
        user_data = {
            "firstname": "John",
            "lastname": "Doe",
            "username": "johndoe",
            "gender": "male",
            "date_of_birth": date(1990, 1, 1),
            "email": "john@example.com",
            "phone_number": "invalid"
        }
        with self.assertRaises(ValidationError):
            UserBase(**user_data)

    def test_invalid_email(self):
        """Test email validation"""
        user_data = {
            "firstname": "John",
            "lastname": "Doe",
            "username": "johndoe",
            "gender": "male",
            "date_of_birth": date(1990, 1, 1),
            "email": "invalid-email",
            "phone_number": "+1234567890"
        }
        with self.assertRaises(ValidationError):
            UserBase(**user_data)
