from flask import Flask, request, jsonify
from .energy_functions import allocate_power, assign_fuel_and_co2_costs_wind


app = Flask(__name__)


@app.route("/productionplan", methods=["POST"])
def process_payload():
    try:
        # Obtener el JSON del cuerpo de la solicitud
        data = request.get_json()

        # Extraer los datos del JSON
        load = data["load"]
        fuels = data["fuels"]

        powerplants = data["powerplants"]

        assign_fuel_and_co2_costs_wind(powerplants, fuels)

        production_plan = allocate_power(powerplants, load)

        return jsonify(production_plan), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
