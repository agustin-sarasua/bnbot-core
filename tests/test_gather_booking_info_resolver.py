import unittest
from unittest.mock import MagicMock
from app.task_resolver.engine import Message
from app.task_resolver.step_resolvers import GatherBookingInfoResolver

import openai
from dotenv import load_dotenv, find_dotenv

class TestGatherBookingInfoResolver(unittest.TestCase):
    
    def setUp(self):
        _ = load_dotenv(find_dotenv(filename="../.env")) # read local .env file
        openai.api_key = "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" #= os.environ['OPENAI_API_KEY']
    
    def test_run_exit_task_resolver_false(self):

        conversations = [
            [
                Message("user", "Hola"),
                Message("assistant", "Hola, ¿en qué puedo ayudarte?"),
                Message("user", "Me gustaría reservar una casa para dos personas, para el jueves que viene.")
            ]
        ]
        resolver = GatherBookingInfoResolver()
        # step_data = {"current_task_name": "MAKE_RESERVATION_TASK"}
        for idx, conv in enumerate(conversations):
            print(f"Running test {idx}")
            previous_steps_data = dict()
            
            # Act
            resolver.run(conv, previous_steps_data)

            # Assert
            self.assertEqual(resolver.is_done(), False)


if __name__ == '__main__':
    unittest.main()
