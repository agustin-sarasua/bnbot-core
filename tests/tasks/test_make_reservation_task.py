import unittest
from unittest.mock import MagicMock
from typing import List, Any, Dict
from app.task_resolver.engine import TaskIdentifierResolver

class TestMakeReservationTask(unittest.TestCase):

    def test_run_conversaion_done(self):
        """return CONVERSATION_DONE when the previous task EXIT_TASK_STEP decided to do it"""
        # Arrange
        resolver = TaskIdentifierResolver()
        step_data = {}
        messages = [
            {"role":"user", "content": "Hola"},
            {"role":"assistant", "content": "Hola, ¿en qué puedo ayudarte?"},
            {"role":"user", "content": "Me gustaria reservar una casa para el finde"}
        ]
        previous_steps_data = {
            "EXIT_TASK_STEP": {
                "result": {
                    "conversation_finished": True
                }
            }
        }

        # Act
        result = resolver.run(step_data, messages, previous_steps_data)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual(result["task_id"], "CONVERSATION_DONE")


if __name__ == '__main__':
    unittest.main()
