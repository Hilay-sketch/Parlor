import itertools

from IceCreamParlorF import IceCreamParlor
from ParlorCustomerF import ParlorCustomer
from ParlorSimulationF import ParlorSimulation
from PositionF import Position
from IceParlorExceptionF import OutOfRangeParlorError


def simulation_superset(simulation: ParlorSimulation):
    clients_combinations = [list(itertools.combinations(simulation.clients, i + 1)) for i in
                            range(len(simulation.clients))]
    parlors_combinations = [list(itertools.combinations(simulation.parlors, i + 1)) for i in
                            range(len(simulation.parlors))]
    total_combinations = sum(len(comb) for comb in clients_combinations) * sum(
        len(comb) for comb in parlors_combinations)
    try:
        for clients_combination in clients_combinations:
            for parlors_combination in parlors_combinations:
                for clients in clients_combination:
                    for parlors in parlors_combination:
                        if total_combinations == 0:
                            raise OutOfRangeParlorError(
                                "Number of iterations per parlor is greater than the number of parlors")
                        total_combinations -= 1
                        yield ParlorSimulation(list(clients), list(parlors))
    except OutOfRangeParlorError as e:
        print(e)
        return ParlorSimulation([], [])


def main():
    parlors_data = {
        "parlor1": {
            "Location": {"x": 4, "y": 4},
            "Flavors": ["Vanilla", "Chocolate"],
            "Pricing": {"Vanilla": 2.5, "Chocolate": 3.0}
        },
        "parlor2": {
            "Location": {"x": 5, "y": 5},
            "Flavors": ["Strawberry", "Chocolate"],
            "Pricing": {"Strawberry": 3.5, "Chocolate": 3.0}
        }
    }

    # Sample data for clients
    clients_data = {
        "clients": {
            "customer1": {
                "Location": {"x": 2, "y": 2},
                "type": "regular",
                "Preferred Option": "scoop1"
            },
            "customer2": {
                "Location": {"x": 3, "y": 3},
                "type": "premium",
                "Preferred Option": "kilo0.5"
            }
        },
        "client profiles": {
            "regular": {"Budget": 10.0, "Favorites": ["Chocolate"], "Dislikes": []},
            "premium": {"Budget": 20.0, "Favorites": ["Strawberry", "Vanilla"], "Dislikes": ["Chocolate"]}
        }
    }

    ice_cream_parlors = []
    for parlor_name, parlor_details in parlors_data.items():
        position = Position(parlor_details["Location"]["x"], parlor_details["Location"]["y"])
        flavors = parlor_details.get("Flavors", [])
        pricing = parlor_details["Pricing"]
        ice_cream_parlors.append(IceCreamParlor(parlor_name, position, flavors, pricing))

    parlor_clients = []
    for customer_name, customer_details in clients_data["clients"].items():
        position = Position(customer_details["Location"]["x"], customer_details["Location"]["y"])
        customer_type = customer_details["type"]
        profile = clients_data["client profiles"].get(customer_type, {})
        favorite_tastes = profile.get("Favorites", [])
        hate_tastes = profile.get("Dislikes", [])
        budget = float(profile.get("Budget", 0))
        fav_option = customer_details.get("Preferred Option", "")
        parlor_clients.append(ParlorCustomer(favorite_tastes, hate_tastes, position, budget, fav_option))

    simulation = ParlorSimulation(parlor_clients, ice_cream_parlors)
    count = 0
    ss = simulation_superset(simulation)
    for sim in ss:
        count += 1
        clients_str = ', '.join(str(client) for client in sim.clients)
        parlors_str = ', '.join(str(parlor) for parlor in sim.parlors)
        print(f"{count}: {clients_str}, {parlors_str}")


if __name__ == "__main__":
    main()
