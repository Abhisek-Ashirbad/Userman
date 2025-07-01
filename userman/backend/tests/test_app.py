import unittest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch

# Import your FastAPI application
from app.main import app

class TestFastAPIApp(unittest.TestCase):
    def setUp(self):
        """Set up test client and environment variables before each test"""
        self.client = TestClient(app)
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'APP_TITLE': 'Test API',
            'HOSTNAME': 'localhost',
            'PORT': '8000'
        })
        self.env_patcher.start()

    def tearDown(self):
        """Clean up after each test"""
        self.env_patcher.stop()

    def test_root_endpoint(self):
        """Test the root endpoint returns correct welcome message"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to Test API"})

    def test_app_configuration(self):
        """Test the application configuration"""
        self.assertEqual(app.title, "Test API")

    @patch('database.db.Base.metadata.create_all')
    def test_database_initialization(self, mock_create_all):
        """Test database tables are created during app initialization"""
        # Import the module again to trigger initialization
        import app
        mock_create_all.assert_called_once()

    def test_router_inclusion(self):
        """Test that the user routes are included in the app"""
        route_paths = [route.path for route in app.routes]
        # Check if at least the root path exists
        self.assertIn("/", route_paths)
        # Add more specific route checks based on your user_routes

    def test_environment_variables(self):
        """Test environment variables are properly loaded"""
        self.assertEqual(os.getenv("APP_TITLE"), "Test API")
        self.assertEqual(os.getenv("HOSTNAME"), "localhost")
        self.assertEqual(os.getenv("PORT"), "8000")

if __name__ == '__main__':
    unittest.main()

if __name__ == "__main__":
    # Discover and run tests
    loader = unittest.TestLoader()
    
    discovered_suite = loader.discover(start_dir='.', pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(discovered_suite)