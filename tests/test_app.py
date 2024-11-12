import unittest
import json
from powerplant_api.app import app


class PowerPlantAPITestCase(unittest.TestCase):

    def setUp(self):
        # Configura el entorno de prueba
        self.app = app.test_client()
        self.app.testing = True

    def test_process_load(self):
        # Definir el payload que se enviará en la solicitud ejemplo 3 de https://raw.githubusercontent.com/gems-st-ib/powerplant-coding-challenge/refs/heads/master/example_payloads/payload3.json
        payload = {
            "load": 910,
            "fuels":
            {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            },
            "powerplants": [
                {
                    "name": "gasfiredbig1",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460
                },
                {
                    "name": "gasfiredbig2",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460
                },
                {
                    "name": "gasfiredsomewhatsmaller",
                    "type": "gasfired",
                    "efficiency": 0.37,
                    "pmin": 40,
                    "pmax": 210
                },
                {
                    "name": "tj1",
                    "type": "turbojet",
                    "efficiency": 0.3,
                    "pmin": 0,
                    "pmax": 16
                },
                {
                    "name": "windpark1",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 150
                },
                {
                    "name": "windpark2",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 36
                }
            ]
        }

        # Enviar la solicitud POST
        response = self.app.post('/productionplan',
                                  data=json.dumps(payload),
                                  content_type='application/json')

        # Comprobar que la respuesta sea 200 OK
        self.assertEqual(response.status_code, 200)

        # Comprobar el contenido de la respuesta https://raw.githubusercontent.com/gems-st-ib/powerplant-coding-challenge/refs/heads/master/example_payloads/response3.json
        expected_response = [
                {
                    "name": "windpark1",
                    "p": 90.0
                },
                {
                    "name": "windpark2",
                    "p": 21.6
                },
                {
                    "name": "gasfiredbig1",
                    "p": 460.0
                },
                {
                    "name": "gasfiredbig2",
                    "p": 338.4
                },
                {
                    "name": "gasfiredsomewhatsmaller",
                    "p": 0.0
                },
                {
                    "name": "tj1",
                    "p": 0.0
                }
            ]

        # Comprobar que la respuesta coincide con lo esperado
        self.assertEqual(response.json, expected_response)

if __name__ == '__main__':
    unittest.main()
