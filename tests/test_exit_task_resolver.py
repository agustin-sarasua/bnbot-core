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


    def test_run_exit_task_resolver_false(self):

        conversations = [
            # [
            #     {"role":"user", "content": "Hola"},
            #     {"role":"assistant", "content": "Hola, ¿en qué puedo ayudarte?"},
            #     {"role":"user", "content": "Me gustaria reservar una casa para el finde"}
            # ],
            # [
            #     {"role": "user", "content": "Hola"},
            #     {"role": "assistant", "content": "Hola, ¿en qué puedo ayudarte?"},
            #     {"role": "user", "content": "Me gustaría reservar una casa"},
            #     {"role": "assistant", "content": "¡Perfecto! Para poder ayudarte a reservar una casa, necesito que me proporciones algunos detalles. ¿Cuál es la fecha de check-in que tienes en mente?"},
            #     {"role": "user", "content": "Es pra el martes que viene por 2 noches"}
            # ],
            # [
            #     {"role": "user", "content": "Hola"},
            #     {"role": "assistant", "content": "Hola, ¿en qué puedo ayudarte?"},
            #     {"role": "user", "content": "Me gustaría reservar una casa"},
            #     {"role": "assistant", "content": "¡Perfecto! Para poder ayudarte a reservar una casa, necesito que me proporciones algunos detalles. ¿Cuál es la fecha de check-in que tienes en mente?"},
            #     {"role": "user", "content": "Seria para el viernes que viene por 2 noches"},
            #     {"role": "assistant", "content": "Entendido, ¿y cuál es la fecha de check-out?"},
            #     {"role": "user", "content": "El domingo"}
            # ],
            # [
            #     {"role": "user", "content": "Quiero reservar una casa para el lunes"},
            #     {"role": "assistant", "content": "¡Hola! Para poder ayudarte a reservar una casa, necesito saber la fecha de salida y la cantidad de personas que se hospedarán. ¿Podrías proporcionarme esa información, por favor?"},
            #     {"role": "user", "content": "2 adultos y entraría el 25 de junio y me voy el 26"},
            #     {"role": "assistant", "content": """Tenemos dos opciones disponibles para tu estadía:

            #     1. Cabaña 'Sol': Impresionante villa con vistas panorámicas a las montañas. Esta lujosa propiedad ofrece un ambiente tranquilo y relajante con amplios espacios interiores y exteriores. Cuenta con una piscina privada, jardines exuberantes y una terraza para disfrutar de las maravillosas vistas. Perfecta para escapadas en familia o con amigos. Amenidades: Wi-Fi, private parking, pet-friendly, barbecue, private pool. Precio por noche: 250.0 USD.

            #     2. Cabaña 'Luna': Impresionante villa con vistas panorámicas a las montañas. Esta lujosa propiedad ofrece un ambiente tranquilo y relajante con amplios espacios interiores y exteriores. Cuenta con una piscina privada, jardines exuberantes y una terraza para disfrutar de las maravillosas vistas. Perfecta para escapadas en familia o con amigos. Amenidades: Wi-Fi, private parking, pet-friendly, barbecue, private pool. Precio por noche: 120.0 USD.

            #     ¿Te gustaría reservar alguna de estas opciones?"""},
            #     {"role": "user", "content": "Si, la segunda"},
            #     {"role": "assistant", "content": "¡Perfecto! Para reservar la cabaña 'Luna' necesito tu nombre y correo electrónico, por favor."},
            #     {"role": "user", "content": "Soledad Ruiz\nsoledad.ruiz.camp@gmail.com"}
            # ],
            [
                {"role": "user", "content": "Me gustaría reservar una casa para el lunes"},
                {"role": "assistant", "content": "¡Hola! Claro, para poder ayudarte necesito saber ¿cuándo sería tu fecha de salida? y ¿cuántas personas se hospedarán contigo?"},
                {"role": "user", "content": "Es por dos noches y solos 3 adultos y 2 niños"},
                {"role": "assistant", "content": "¡Hola! Tenemos disponible la propiedad Cabaña 'Sol' que cuenta con capacidad para 8 personas y tiene un precio de 250 USD por noche. La propiedad cuenta con Wi-Fi, estacionamiento privado, es pet-friendly, tiene una parrilla y una piscina privada. ¿Te gustaría reservar esta propiedad?"},
                {"role": "user", "content": "Si"},
                {"role": "assistant", "content": "¡Genial! Para reservar la propiedad, necesito que me proporciones tu nombre y correo electrónico."},
                {"role": "user", "content": "Agustin   Agustin@gmail.com"}
            ]
        ]
        resolver = ExitTaskResolver()
        step_data = {"current_task_name": "MAKE_RESERVATION_TASK"}
        for idx, conv in enumerate(conversations):
            print(f"Running test {idx}")
            previous_steps_data = []
            
            # Act
            resolver.run(step_data, conv, previous_steps_data)

            # Assert
            self.assertIsInstance(step_data["result"], dict)
            self.assertEqual(step_data["result"]["conversation_finished"], False)




if __name__ == '__main__':
    unittest.main()
