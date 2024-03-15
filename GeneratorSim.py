from IceCreamParlorF import IceCreamParlor
from ParlorCustomerF import ParlorCustomer
from ParlorSimulationF import ParlorSimulation
from PositionF import Position


def simulation_superset(simulation: ParlorSimulation):
    customers = simulation.clients
    parlors = simulation.parlors
    for customer in customers:
        for parlor in parlors:
            yield [customer, parlor]


def main():
    parlors_data = {
        "parlor1": {
            "Location": {"x": 1, "y": 1},
            "Flavors": ["Vanilla", "Chocolate"],
            "Pricing": {"Vanilla": 2.5, "Chocolate": 3.0}
        },
        "parlor2": {
            "Location": {"x": 2, "y": 2},
            "Flavors": ["Strawberry", "Chocolate"],
            "Pricing": {"Strawberry": 3.5, "Chocolate": 3.0}
        }
    }

    # Sample data for customers
    customers_data = {
        "clients": {
            "customer1": {
                "Location": {"x": 0, "y": 0},
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

    parlor_customers = []
    for customer_name, customer_details in customers_data["clients"].items():
        position = Position(customer_details["Location"]["x"], customer_details["Location"]["y"])
        customer_type = customer_details["type"]
        profile = customers_data["client profiles"].get(customer_type, {})
        favorite_tastes = profile.get("Favorites", [])
        hate_tastes = profile.get("Dislikes", [])
        budget = float(profile.get("Budget", 0))
        fav_option = customer_details.get("Preferred Option", "")
        parlor_customers.append(ParlorCustomer(favorite_tastes, hate_tastes, position, budget, fav_option))

    simulation = ParlorSimulation(parlor_customers, ice_cream_parlors)

    for costumer, parlor in simulation_superset(simulation):
        print(costumer, parlor)


if __name__ == "__main__":
    main()
