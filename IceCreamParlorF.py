from IceParlorExceptionF import ValueNotALLOWEDError
from PositionF import Position


class IceCreamParlor:

    def __init__(self, name: str, pos: Position, flavors: list[str], prices: dict[str, float]):
        try:
            if not isinstance(name, str):
                raise ValueNotALLOWEDError("name must be a string")
            if not isinstance(pos, Position):
                raise ValueNotALLOWEDError("pos must be an instance of Position")
            if not isinstance(flavors, list) or not all(isinstance(flavor, str) for flavor in flavors):
                raise ValueNotALLOWEDError("flavors must be a list of strings")
            if not isinstance(prices, dict) or not all(
                    isinstance(key, str) and isinstance(value, float) for key, value in prices.items()):
                raise ValueNotALLOWEDError("prices must be a dictionary of strings and floats")

            self.name = name
            self.pos = pos
            self.flavors = flavors
            if len(flavors) == 0:
                self.flavors = ["Vanilla", "Chocolate", "Strawberry"]
            self.prices = prices
            self.allowed_prices = ["scoop1", "scoop2", "scoop3", "scoop4", "kilo0.5", "kilo1.0"]
        except ValueNotALLOWEDError as e:
            print(f"{e}, try again")

    def add_flavor(self, flavor_name: str) -> None:
        try:
            if not isinstance(flavor_name, str):
                raise ValueNotALLOWEDError("flavor must be a string")
            if flavor_name in self.flavors:
                raise ValueNotALLOWEDError(f"{flavor_name} is already on the menu")
            self.flavors.append(flavor_name)
        except ValueNotALLOWEDError as e:
            print(f"{e}, try again")

    def set_option(self, option_key: str, price: float) -> None:
        try:
            if not isinstance(option_key, str):
                raise ValueNotALLOWEDError("option_key must be a string")
            if not isinstance(price, float):
                raise ValueNotALLOWEDError("price must be a float")
            if option_key not in self.allowed_prices:
                raise ValueNotALLOWEDError(f"{option_key} is not an allowed option")
            self.prices[option_key] = price
        except ValueNotALLOWEDError as e:
            print(f"{e}, try again")

    def __str__(self):
        return f"IceCreamParlor: {self.name}, Location: ({self.pos.x}, {self.pos.y})"

