import unittest
from unittest.mock import MagicMock
from typing import List, Any, Dict
from app.task_resolver import ExitTaskResolver

import os
import openai
from dotenv import load_dotenv, find_dotenv

class TestExitTaskResolver(unittest.TestCase):
    
    def setUp(self):
        _ = load_dotenv(find_dotenv(filename="../.env")) # read local .env file
        openai.api_key = "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" #= os.environ['OPENAI_API_KEY']

    def test_run_exit_task_resolver(self):
        # Arrange
        resolver = ExitTaskResolver()
        step_data = {"current_task_name": "MAKE_RESERVATION_TASK"}
        messages = [
            {"role":"user", "content": "Hola"},
            {"role":"assistant", "content": "Hola, ¿en qué puedo ayudarte?"},
            {"role":"user", "content": "Me gustaria reservar una casa para el finde"}
        ]
        previous_steps_data = []

        # Act
        resolver.run(step_data, messages, previous_steps_data)

        # Assert
        self.assertIsInstance(step_data["result"], dict)
        self.assertEqual(step_data["result"]["conversation_finished"], False)
    
    def test_run_exit_task_resolver_1(self):
        # Arrange
        resolver = ExitTaskResolver()
        step_data = {"current_task_name": "MAKE_RESERVATION_TASK"}
        messages = [
            {"role": "user", "content": "Hola"},
            {"role": "assistant", "content": "Hola, ¿en qué puedo ayudarte?"},
            {"role": "user", "content": "Quiero reservar una casa para el fin de semana para 6 personas."},
            {"role": "assistant", "content": """¡Hola! Tenemos una variedad de propiedades disponibles para el fin de semana para 6 personas. Aquí está un resumen de las propiedades disponibles:

            1. Sol:
            Impresionante villa con vistas panorámicas a las montañas. Esta lujosa propiedad ofrece un ambiente tranquilo y relajante con amplios espacios interiores y exteriores. Cuenta con una piscina privada, jardines exuberantes y una terraza para disfrutar de las maravillosas vistas. Perfecta para escapadas en familia o con amigos.
            Amenidades: Wi-Fi, estacionamiento privado, se admiten mascotas, barbacoa, piscina privada.
            Precio por noche: 250.0 USD

            ¿Te gustaría reservar esta propiedad o te gustaría más información sobre alguna de las otras propiedades?"""},
            {"role": "user", "content": "¿Tienen alguna otra propiedad disponible? El precio es un poco alto para mi presupuesto."},
            {"role": "assistant", "content": "Lo siento, actualmente no tenemos otras propiedades disponibles para el fin de semana para 6 personas. ¿Te gustaría buscar en otras fechas?"},
            {"role": "user", "content": "Gracias por su ayuda, pero no, no necesito buscar en otras fechas."}
        ]
        previous_steps_data = []

        # Act
        resolver.run(step_data, messages, previous_steps_data)

        # Assert
        self.assertIsInstance(step_data["result"], dict)
        self.assertEqual(step_data["result"]["conversation_finished"], True)


if __name__ == '__main__':
    unittest.main()
