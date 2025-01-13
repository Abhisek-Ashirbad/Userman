import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database.db import Base, get_db

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)

    def test_get_db(self):
        """Test database session creation and closure"""
        db_generator = get_db()
        db = next(db_generator)
        self.assertIsInstance(db, Session)
        try:
            next(db_generator)
        except StopIteration:
            pass

    def test_db_connection(self):
        """Test database connection is working"""
        db_generator = get_db()
        db = next(db_generator)
        try:
            # Execute a simple query to test connection
            db.execute("SELECT 1")
            self.assertTrue(True)  # If we get here, connection works
        finally:
            try:
                next(db_generator)
            except StopIteration:
                pass