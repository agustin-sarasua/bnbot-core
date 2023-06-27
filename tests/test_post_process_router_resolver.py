import unittest
from unittest.mock import MagicMock
from typing import List, Any, Dict
from app.task_resolver.step_resolvers import PostProcessRouterResolver
from app.task_resolver.engine import Message

class TesPostProcessRouterResolver(unittest.TestCase):

    def test_run_post_process(self):
        post_process_resolvers = PostProcessRouterResolver([
            {"name":"GATHER_BOOKING_INFO", "description":"If the user wants to change the check-in or check-out dates that he previously selected."},
            {"name":"OTHER", "description":"If the user has not selected a property."},
        ])

        test_cases = [
            {
                "chat_history": [
                        Message("user", "Me gustaría reservar una casa para dos personas, para el jueves que viene"),
                        Message("assistant", "¡Hola! Claro, para poder ayudarte necesito saber la fecha de salida. ¿Cuándo te gustaría dejar la casa?"),
                        Message("user", "Sería por 2 noches"),
                ],
                "expected_step": "OTHER",
            }
        ]

        for idx, test in enumerate(test_cases):
            print(f"Running test {idx}")
            # Act
            result = post_process_resolvers.run(test["chat_history"], )

            # Assert
            self.assertIsNotNone(result)
            self.assertEqual(test["expected_step"], result["step"])


if __name__ == '__main__':
    unittest.main()
