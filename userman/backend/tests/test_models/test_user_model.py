import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.models.user_model import User
from app.database.db import Base

class TestUserModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)

    def test_create_user(self):
        """Test basic user creation"""
        user = User(
            firstname="John",
            lastname="Doe",
            username="johndoe",
            password="hashedpassword",
            gender="male",
            date_of_birth=date(1990, 1, 1),
            age=33,
            email="john@example.com",
            phone_number="+1234567890"
        )
        self.session.add(user)
        self.session.commit()

        saved_user = self.session.query(User).first()
        self.assertEqual(saved_user.firstname, "John")
        self.assertEqual(saved_user.email, "john@example.com")

    def test_unique_username_constraint(self):
        """Test that username must be unique"""
        user1 = User(
            firstname="John",
            lastname="Doe",
            username="johndoe",
            password="hashedpassword",
            gender="male",
            date_of_birth=date(1990, 1, 1),
            age=33,
            email="john@example.com",
            phone_number="+1234567890"
        )
        self.session.add(user1)
        self.session.commit()

        user2 = User(
            firstname="Jane",
            lastname="Doe",
            username="johndoe",  # Same username
            password="hashedpassword",
            gender="female",
            date_of_birth=date(1992, 1, 1),
            age=31,
            email="jane@example.com",
            phone_number="+0987654321"
        )
        
        with self.assertRaises(IntegrityError):
            self.session.add(user2)
            self.session.commit()

    def test_unique_email_constraint(self):
        """Test that email must be unique"""
        user1 = User(
            firstname="John",
            lastname="Doe",
            username="johndoe",
            password="hashedpassword",
            gender="male",
            date_of_birth=date(1990, 1, 1),
            age=33,
            email="john@example.com",
            phone_number="+1234567890"
        )
        self.session.add(user1)
        self.session.commit()

        user2 = User(
            firstname="Jane",
            lastname="Doe",
            username="janedoe",
            password="hashedpassword",
            gender="female",
            date_of_birth=date(1992, 1, 1),
            age=31,
            email="john@example.com",  # Same email
            phone_number="+0987654321"
        )
        
        with self.assertRaises(IntegrityError):
            self.session.add(user2)
            self.session.commit()