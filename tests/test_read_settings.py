import json
import unittest
from source.classes import Course
from source.functions.read_settings import read_settings  

class TestReadSettings(unittest.TestCase):

    def test_read_settings(self):
        """
        Test that it can read settings from a JSON file and return a list of Course objects
        """
        # a known input with known output
        test_settings_file_path = "tests/settings.json"
        
        test_cases = [
            Course("CS101", [1, 2], [1, 3]),
            Course("CS102", [3, 4], [1, 1]),
        ]

        result = read_settings(test_settings_file_path)

        self.assertCountEqual(result, test_cases)


if __name__ == '__main__':
    unittest.main()
