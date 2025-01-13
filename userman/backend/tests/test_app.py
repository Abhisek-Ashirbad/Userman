import unittest
import coverage
import sys
import os
from dotenv import load_dotenv


def start_coverage():
    cov = coverage.Coverage(
        branch=True,
        source=['app'],
        omit=[
            '*/tests/*',
            '*/venv/*',
            '*/__init__.py'
        ]
    )
    cov.start()
    return cov

def run_test_suite():
    # Get the directory containing test_app.py
    test_dir = os.path.dirname(os.path.abspath(__file__))
    # Add the parent directory to sys.path so that app module can be imported
    parent_dir = os.path.dirname(test_dir)
    sys.path.insert(0, parent_dir)
    # Discover and run tests
    loader = unittest.TestLoader()
    
    discovered_suite = loader.discover(start_dir=test_dir, pattern='test_*.py')
    # Load the TestLoadDotenv suite explicitly
    dotenv_suite = loader.loadTestsFromTestCase(TestLoadDotenv)
    # Combine both suites
    combined_suite = unittest.TestSuite([discovered_suite, dotenv_suite])

    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(combined_suite)


class TestLoadDotenv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary .env file for testing
        cls.env_file_path = ".test_env"
        with open(cls.env_file_path, "w") as f:
            f.write("TEST_KEY=TEST_VALUE\n")

    @classmethod
    def tearDownClass(cls):
        # Remove the temporary .env file
        if os.path.exists(cls.env_file_path):
            os.remove(cls.env_file_path)

    def test_load_dotenv(self):
        # Load the temporary .env file
        load_dotenv(dotenv_path=self.env_file_path)

        # Check if the environment variable is loaded
        self.assertEqual(os.getenv("TEST_KEY"), "TEST_VALUE")

    def test_load_dotenv_without_file(self):
        # Ensure no error occurs when the .env file is missing
        result = load_dotenv(dotenv_path="nonexistent.env")
        self.assertFalse(result)  # Should return False for a missing file

    def test_env_variable_not_loaded(self):
        # Ensure non-existing variables return None
        self.assertIsNone(os.getenv("NON_EXISTENT_KEY"))


if __name__ == '__main__':
    # Start coverage
    cov = start_coverage()
    # Run tests
    result = run_test_suite()
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    # Print coverage report
    print('\nCoverage Summary:')
    cov.report()
    # Generate HTML report
    cov.html_report(directory='htmlcov')    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())
