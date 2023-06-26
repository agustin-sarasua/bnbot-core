import unittest
from unittest.mock import MagicMock
from typing import List, Any, Dict
from app.tools import SearchDataExtractor
from app.task_resolver.engine import Message
from datetime import datetime
from unittest.mock import patch

class TestSearchDataExtractor(unittest.TestCase):

    @patch('app.tools.search_data_extractor.get_current_datetime')
    def test_run(self, mock_now):
        mock_now.return_value = datetime(2023, 7, 25)
        # Arrange
        data_extractor = SearchDataExtractor()
        test_cases = [
            {
                "chat_history": [
                        Message("user", "Hola"),
                        Message("assistant", "Hola, ¿en qué puedo ayudarte?"),
                        Message("user", "Me gustaría reservar una casa para dos personas, para el jueves que viene por una noche nada mas.")
                ],
                "expected_check_in_date": "2023-07-27",
                "expected_check_out_date": "2023-07-28",
                "expected_num_guests": 2,
            },
            {
                "chat_history": [
                        Message("user", "Hola"),
                        Message("assistant", "Hola, ¿en qué puedo ayudarte?"),
                        Message("user", "Me gustaría reservar una casa para el viernes")
                ],
                "expected_check_in_date": "2023-07-28",
                "expected_check_out_date": None,
                "expected_num_guests": 0,
            }
        ]
        
        for idx, test in enumerate(test_cases):
            print(f"Running test {idx}")
            # Act
            result = data_extractor.run(test["chat_history"])

            # Assert
            self.assertIsNotNone(result)
            self.assertEqual(result["check_in_date"], test["expected_check_in_date"])
            self.assertEqual(result["check_out_date"], test["expected_check_out_date"])
            self.assertEqual(result["num_guests"], test["expected_num_guests"])


if __name__ == '__main__':
    unittest.main()
