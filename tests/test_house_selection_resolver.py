import unittest
from unittest.mock import MagicMock
from app.task_resolver.engine import Message, StepData
from app.task_resolver.step_resolvers import HouseSelectionResolver

import openai
from dotenv import load_dotenv, find_dotenv

class TestHouseSelectionResolver(unittest.TestCase):
    
    def setUp(self):
        _ = load_dotenv(find_dotenv(filename="../.env")) # read local .env file
        openai.api_key = "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" #= os.environ['OPENAI_API_KEY']
    
    def test_run(self):
        # Arrange
        prev_step_data = StepData()
        prev_step_data.resolver_data = {'booking_information': {'check_in_date': '2023-06-29', 'check_out_date': '2023-07-01', 'num_guests': 2}}
        test_cases = [
            # {
            #     "messages": [
            #         Message("user", "Me gustaría reservar una casa para dos personas, para el jueves que viene."),
            #         Message("assistant", "¡Hola! Claro, para poder ayudarte necesito saber la fecha de salida. ¿Cuándo te gustaría dejar la casa? "),
            #         Message("user", "El sábado."),
            #         Message("assistant", "Actualmente tenemos dos propiedades disponibles para las fechas que solicitaste:    1. Cabaña 'Sol': Impresionante villa con vistas panorámicas a las montañas. Esta lujosa propiedad ofrece un ambiente tranquilo y relajante con amplios espacios interiores y exteriores. Cuenta con una piscina privada, jardines exuberantes y una terraza para disfrutar de las maravillosas vistas. Perfecta para escapadas en familia o con amigos. Amenidades: Wi-Fi, estacionamiento privado, se admiten mascotas, barbacoa, piscina privada. Precio por noche: 250.0 USD    2. Cabaña 'Luna': Impresionante villa con vistas panorámicas a las montañas. Esta lujosa propiedad ofrece un ambiente tranquilo y relajante con amplios espacios interiores y exteriores. Cuenta con una piscina privada, jardines exuberantes y una terraza para disfrutar de las maravillosas vistas. Perfecta para escapadas en familia o con amigos. Amenidades: Wi-Fi, estacionamiento privado, se admiten mascotas, barbacoa, piscina privada. Precio por noche: 120.0 USD    ¿Te gustaría reservar alguna de estas propiedades?"),
            #         Message("user", "Se puede hacer asado?"),
            #     ],
            #     "previous_setp_data": {
            #         "GATHER_BOOKING_INFO": prev_step_data
            #     },
            #     "expected_property_id": None
            # },
            {
                "messages": [
                    Message("user", "Me gustaría reservar una casa para dos personas, para el jueves que viene."),
                    Message("assistant", "¡Hola! Claro, para poder ayudarte necesito saber la fecha de salida. ¿Cuándo te gustaría dejar la casa? "),
                    Message("user", "El sábado."),
                    Message("assistant", "Actualmente tenemos dos propiedades disponibles para las fechas que solicitaste:    1. Cabaña 'Sol': Impresionante villa con vistas panorámicas a las montañas. Esta lujosa propiedad ofrece un ambiente tranquilo y relajante con amplios espacios interiores y exteriores. Cuenta con una piscina privada, jardines exuberantes y una terraza para disfrutar de las maravillosas vistas. Perfecta para escapadas en familia o con amigos. Amenidades: Wi-Fi, estacionamiento privado, se admiten mascotas, barbacoa, piscina privada. Precio por noche: 250.0 USD    2. Cabaña 'Luna': Impresionante villa con vistas panorámicas a las montañas. Esta lujosa propiedad ofrece un ambiente tranquilo y relajante con amplios espacios interiores y exteriores. Cuenta con una piscina privada, jardines exuberantes y una terraza para disfrutar de las maravillosas vistas. Perfecta para escapadas en familia o con amigos. Amenidades: Wi-Fi, estacionamiento privado, se admiten mascotas, barbacoa, piscina privada. Precio por noche: 120.0 USD    ¿Te gustaría reservar alguna de estas propiedades?"),
                    Message("user", "La primera"),
                ],
                "previous_setp_data": {
                    "GATHER_BOOKING_INFO": prev_step_data
                },
                "expected_property_id": None
            }
        ]
        
        for idx, test in enumerate(test_cases):
            print(f"Running test {idx}")
            resolver = HouseSelectionResolver()

            # Act
            result = resolver.run(test["messages"], test["previous_setp_data"])
            
            # Assert
            self.assertIsNotNone(result)
            self.assertEqual(resolver.data["property_picked_info"]["property_id"], test["expected_property_id"])
            # self.assertEqual(result["check_out_date"], test["expected_check_out_date"])
            # self.assertEqual(result["num_guests"], test["expected_num_guests"])



if __name__ == '__main__':
    unittest.main()
