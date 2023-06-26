import unittest
from unittest.mock import MagicMock
from typing import List, Any, Dict
from app.task_resolver.engine import TaskIdentifierResolver

class TesPostProcessRouterResolver(unittest.TestCase):

    def test_run_post_process(self):
        # Arrange
        # resolver = TaskIdentifierResolver()
        # step_data = {}
        # messages = [
        #     {"role":"user", "content": "Hola"},
        #     {"role":"assistant", "content": "Hola, ¿en qué puedo ayudarte?"},
        #     {"role":"user", "content": "Me gustaria reservar una casa para el finde"}
        # ]
        # previous_steps_data = []

        # # Act
        # result = resolver.run(step_data, messages, previous_steps_data)

        # # Assert
        # self.assertIsInstance(result, dict)
        # self.assertEqual(result["task_id"], "MAKE_RESERVATION_TASK")
        pass


if __name__ == '__main__':
    unittest.main()
