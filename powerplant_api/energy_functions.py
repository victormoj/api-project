from .constants import (
    emissions_co2_per_mwh,
    FUEL_COST_GAS,
    FUEL_COST_KEROSINE,
    CO2_COST,
    WIND_PERCENTAGE,
    PLANT_TYPE_GASFIRED,
    PLANT_TYPE_TURBOJET,
    PLANT_TYPE_WINDTURBINE
)


def calculate_marginal_cost(plant_type, efficiency, fuel_cost, co2_cost):
    """
    Calculates the marginal cost of an energy plant.

    :param plant_type: Type of plant (e.g., 'gasfired', 'turbojet', 'windturbine')
    :param efficiency: Efficiency of the plant (value between 0 and 1)
    :param fuel_cost: Cost of fuel in euros/MWh
    :param co2_cost: Cost of CO2 in euros/ton

    :return: Marginal cost in euros/MWh
    """
    # Calculate the base marginal cost without including CO2
    marginal_cost = fuel_cost / efficiency

    # Add the CO2 cost if applicable
    if plant_type in emissions_co2_per_mwh:
        marginal_cost += co2_cost * emissions_co2_per_mwh[plant_type]

    return round(marginal_cost, 2)


def calculate_merit_order(powerplants):
    """
    Calculates the merit order of a list of power plants based on their marginal costs.

    :param powerplants: A list of dictionaries, where each dictionary contains details of a power plant
                        (e.g., {'name': 'plant1', 'type': 'gasfired', 'efficiency': 0.53,
                        'fuel_cost': 13.4, 'co2_cost': 20})

    :return: A sorted list of plants based on their marginal costs
    """
    for plant in powerplants:
        # Calculate marginal cost for each plant
        plant["marginal_cost"] = calculate_marginal_cost(
            plant["type"],
            plant["efficiency"],
            plant["fuel_cost"],
            plant["co2_cost"]
        )

    # Sort plants by marginal cost
    sorted_plants = sorted(powerplants, key=lambda x: x["marginal_cost"])

    return sorted_plants


def allocate_power(powerplants, load):
    """
    Allocates power from a list of plants according to demand,
    considering their pmin, pmax, and availability.

    :param powerplants: List of dictionaries with details of the power plants.
    :param load: Total demand in MWh.

    :return: List of dictionaries with the allocated power for each plant.
    """

    # Sort the plants by their marginal cost
    powerplants = calculate_merit_order(powerplants)

    for plant in powerplants:
        if load > 0:
            # Determine how much power can be allocated to this plant
            power_to_allocate = min(plant["pmax"], max(plant["pmin"], load))
            # Round power_to_allocate to the nearest 0.1 MW
            power_to_allocate = round(power_to_allocate, 1)
            plant["p"] = power_to_allocate  # Update the allocated power for the plant
            load -= power_to_allocate  # Decrease the remaining load
        else:
            plant["p"] = 0  # If no load remains, set allocated power to 0

    return [{"name": plant["name"], "p": round(plant["p"], 1)} for plant in powerplants]


def assign_fuel_and_co2_costs_wind(powerplants, fuels):
    """
    Assigns fuel and CO2 costs for each power plant based on its type.

    :param powerplants: List of dictionaries with details of the power plants.
    :param fuels: Dictionary containing fuel costs.

    :return: None (modifies the input list in place)
    """
    for plant in powerplants:
        plant["p"] = 0  # Initialize allocated power
        if plant["type"] == PLANT_TYPE_GASFIRED:
            plant["fuel_cost"] = fuels[FUEL_COST_GAS]
            plant["co2_cost"] = fuels[CO2_COST]
        elif plant["type"] == PLANT_TYPE_TURBOJET:
            plant["fuel_cost"] = fuels[FUEL_COST_KEROSINE]
            plant["co2_cost"] = fuels[CO2_COST]
        elif plant["type"] == PLANT_TYPE_WINDTURBINE:
            plant["fuel_cost"] = 0  # Wind turbines have no fuel cost
            plant["co2_cost"] = 0  # Wind turbines have no CO2 cost
            plant["pmin"] = round(plant["pmin"] * (fuels[WIND_PERCENTAGE] / 100), 2)
            plant["pmax"] = round(plant["pmax"] * (fuels[WIND_PERCENTAGE] / 100), 2)
            plant["efficiency"] = fuels[WIND_PERCENTAGE] / 100  # Set the efficiency based on wind availability
