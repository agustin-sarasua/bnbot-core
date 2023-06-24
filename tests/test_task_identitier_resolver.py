import unittest
from unittest.mock import MagicMock
from typing import List, Any, Dict
from app.task_resolver import TaskIdentifierResolver

class TestTaskIdentifierResolver(unittest.TestCase):

    def test_run_make_reservation_1(self):
        # Arrange
        resolver = TaskIdentifierResolver()
        step_data = {}
        messages = [
            {"role":"user", "content": "Hola"},
            {"role":"assistant", "content": "Hola, ¿en qué puedo ayudarte?"},
            {"role":"user", "content": "Me gustaria reservar una casa para el finde"}
        ]
        previous_steps_data = []

        # Act
        result = resolver.run(step_data, messages, previous_steps_data)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual(result["task_id"], "MAKE_RESERVATION_TASK")
    
    def test_run_make_reservation_2(self):
        # Arrange
        resolver = TaskIdentifierResolver()
        step_data = {}
        messages = [
            {"role":"user", "content": "Hola, estoy buscando alojamiento."}
        ]
        previous_steps_data = []

        # Act
        result = resolver.run(step_data, messages, previous_steps_data)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual(result["task_id"], "MAKE_RESERVATION_TASK")

    def test_run_other_1(self):
        # Arrange
        resolver = TaskIdentifierResolver()
        step_data = {}
        messages = [
            {"role":"user", "content": "Hola, queria saber si son un hotel."}
        ]
        previous_steps_data = []

        # Act
        result = resolver.run(step_data, messages, previous_steps_data)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual(result["task_id"], "PROPERTIES_INFORMATION_TASK")


if __name__ == '__main__':
    unittest.main()
