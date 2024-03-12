import json
from typing import List

from IceCreamParlorF import IceCreamParlor
from IceParlorExceptionF import IceParlorException, ConfigurationFileNotFoundError, DuplicateParlorLocationError
from ParlorCustomerF import ParlorCustomer
from ParlorSimulationF import ParlorSimulation
from PositionF import Position


def create_list_to_json(lst: List) -> List[str]:
    if not lst:
        return []
    return [str(item) for item in lst]


def load_ice_cream_list(data_of_parlors: dict) -> List[IceCreamParlor]:
    ice_cream_list = []
    for shop, details in data_of_parlors.items():
        position = Position(details["Location"]["x"], details["Location"]["y"])
        flavors = details.get("Flavors", [])
        taste_cost = details["Pricing"]

        if isinstance(taste_cost, dict):
            for key, value in taste_cost.items():
                try:
                    taste_cost[key] = float(value)
                except ValueError:
                    print(f"Error: Unable to convert {value} to float.")
        else:
            print("Error: taste_cost is not a dictionary.")
            continue

        ice_cream_list.append(IceCreamParlor(shop, position, flavors, taste_cost))

    return ice_cream_list


def load_customer_list(data_of_clients: dict) -> List[ParlorCustomer]:
    customer_list = []
    for customer, details in data_of_clients["clients"].items():
        position = Position(details["Location"]["x"], details["Location"]["y"])
        customer_type = details["type"]
        profile = data_of_clients["client profiles"].get(customer_type, {})
        favorite_tastes = profile.get("Favorites", [])
        hate_tastes = profile.get("Dislikes", [])
        budget = float(profile.get("Budget", 0))
        fav_option = profile.get("Preferred Option", "")
        customer_list.append(ParlorCustomer(favorite_tastes, hate_tastes, position, budget, fav_option))
    return customer_list


def choosing_action(action: str, simulation: ParlorSimulation):
    if action == "run":
        return simulation.run()
    elif action == "most_profitable":
        return create_list_to_json(simulation.most_profitable())
    elif action == "most_customers":
        return create_list_to_json(simulation.most_customers())
    elif action == "unhappy_customers":
        return create_list_to_json(simulation.unhappy_customers())
    else:
        raise ValueError("Invalid action")


def create_result_json_file() -> None:
    try:
        with open('parlor_configuration.json', 'r') as file:
            data = json.load(file)
            ice_cream_list = load_ice_cream_list(data.get("parlors", {}))
            customer_list = load_customer_list(data)
            action = data["simulation"]["action"]
            simulation = ParlorSimulation(customer_list, ice_cream_list)
            with open('results.json', 'w') as result_file:
                json.dump(choosing_action(action, simulation), result_file)
    except FileNotFoundError:
        with open('results.json', 'w') as result_file:
            json.dump({"error": "parlor_configuration.json file not found."}, result_file)
        raise ConfigurationFileNotFoundError("parlor_configuration.json file not found.")
    except json.JSONDecodeError:
        with open('results.json', 'w') as result_file:
            json.dump({"error": "Unable to decode JSON data from parlor_configuration.json."}, result_file)
        raise IceParlorException("Unable to decode JSON data from parlor_configuration.json.")
    except Exception as e:
        with open('results.json', 'w') as result_file:
            json.dump({"error": str(e)}, result_file)
        raise IceParlorException(e)


def main() -> None:
    create_result_json_file()


if __name__ == "__main__":
    main()
