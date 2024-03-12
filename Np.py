import numpy as np
from PositionF import Position
from ParlorCustomerF import ParlorCustomer

# Define some sample data for customers
customer_data = [
    {
        "fav_flavors": ["Chocolate", "Vanilla"],
        "hated_flavors": ["Strawberry", "Pistachio", "Neg", "ss"],
        "pos_x": 0,
        "pos_y": 0,
        "max_price": 15.0,
        "fav_option": "scoop2"
    },
    {
        "fav_flavors": ["Strawberry", "Mint"],
        "hated_flavors": ["Vanilla"],
        "pos_x": 3,
        "pos_y": 3,
        "max_price": 20.0,
        "fav_option": "kilo1.0"
    }
]

# Find the maximum set of flavors among all customers
all_flavors = set()
all_hated_flavors = set()
for data in customer_data:
    all_flavors.update(data["fav_flavors"])
    all_hated_flavors.update(data["hated_flavors"])

# Convert the set of flavors and hated flavors to a list
all_flavors = list(all_flavors)
all_hated_flavors = list(all_hated_flavors)

# Create ParlorCustomer objects and store their data in a NumPy array
num_customers = len(customer_data)
num_flavors = len(all_flavors)
num_hated_flavors = len(all_hated_flavors)

customer_array = np.zeros((num_customers, 2 + 2*num_flavors + num_hated_flavors + 1), dtype=object)

for i, data in enumerate(customer_data):
    position = Position(data["pos_x"], data["pos_y"])
    fav_flavors = data["fav_flavors"]
    hated_flavors = data["hated_flavors"]
    max_price = data["max_price"]
    fav_option = data["fav_option"]

    # Encode favorite and hated flavors using one-hot encoding
    fav_flavors_encoded = [1 if flavor in fav_flavors else 0 for flavor in all_flavors]
    hated_flavors_encoded = [1 if flavor in hated_flavors else 0 for flavor in all_hated_flavors]

    # Encode favorite option
    fav_option_encoded = [1 if fav_option == option else 0 for option in ["scoop1", "scoop2", "scoop3", "scoop4", "kilo0.5", "kilo1.0"]]

    # Populate the customer array
    customer_array[i, 0] = position.x
    customer_array[i, 1] = position.y
    customer_array[i, 2:2+num_flavors] = fav_flavors_encoded
    customer_array[i, 2 + 2 * num_flavors: 2 + 2 * num_flavors + len(hated_flavors_encoded)] = hated_flavors_encoded
    customer_array[i, -2] = max_price

print("Customers represented as a NumPy array:")
print(customer_array)
