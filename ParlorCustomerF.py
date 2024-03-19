import copy
import random
from typing import Any

from PositionF import Position
from IceCreamParlorF import IceCreamParlor
from IceParlorExceptionF import IceParlorException, ValueNotALLOWEDError


class ParlorCustomer:
    def __init__(self, fav_flavors: list[str], hated_flavors: list[str], pos: Position, max_price: float,
                 fav_option: str):
        try:
            if not isinstance(fav_flavors, list) or not all(isinstance(flavor, str) for flavor in fav_flavors):
                raise ValueNotALLOWEDError("fav_flavors must be a list of strings")
            if not isinstance(hated_flavors, list) or not all(isinstance(flavor, str) for flavor in hated_flavors):
                raise ValueNotALLOWEDError("hated_flavors must be a list of strings")
            if not isinstance(pos, Position):
                raise ValueNotALLOWEDError("pos must be an instance of Position")
            if not isinstance(max_price, float):
                raise ValueNotALLOWEDError("max_price must be a float")
            if not isinstance(fav_option, str):
                raise ValueNotALLOWEDError("fav_option must be a string")

            self.fav_flavors = fav_flavors
            if len(fav_flavors) == 0:
                self.fav_flavors = []
            self.hated_flavors = hated_flavors
            if len(hated_flavors) == 0:
                self.hated_flavors = []
            self.pos = pos
            self.max_price = max_price
            if fav_option not in ["scoop1", "scoop2", "scoop3", "scoop4", "kilo0.5", "kilo1.0"]:
                raise ValueNotALLOWEDError(f"{fav_option} is not an allowed option")
            self.fav_option = fav_option

        except ValueNotALLOWEDError as e:
            print(f"{e}, try again")

    def choose(self, options: list[IceCreamParlor]) -> IceCreamParlor | None | Any:
        try:
            if not options:
                raise ValueNotALLOWEDError("There are no options to choose from")
            if not isinstance(options, list) or not all(
                    isinstance(option, IceCreamParlor) for option in options):
                raise ValueNotALLOWEDError("options must be a list of IceCreamParlor instances")

            affordable_parlors = [parlor for parlor in options if
                                  any(price <= self.max_price for price in parlor.prices.values())]
            if len(affordable_parlors) == 1:
                return affordable_parlors[0]

            max_fav_flavors = 0
            for parlor in affordable_parlors:
                current_fav_flavors = 0
                for flavor_in_parlor in parlor.flavors:
                    if flavor_in_parlor in self.fav_flavors:
                        current_fav_flavors += 1
                if current_fav_flavors > max_fav_flavors:
                    max_fav_flavors = current_fav_flavors

            parlors_with_fav_flavors = []
            for parlor in affordable_parlors:
                current_fav_flavors = 0
                for flavor_in_parlor in parlor.flavors:
                    if flavor_in_parlor in self.fav_flavors:
                        current_fav_flavors += 1
                if current_fav_flavors == max_fav_flavors:
                    parlors_with_fav_flavors.append(parlor)

            if len(parlors_with_fav_flavors) == 1:
                return parlors_with_fav_flavors[0]

            parlors_with_fav_flavors2 = copy.deepcopy(parlors_with_fav_flavors)

            for parlor in parlors_with_fav_flavors2:
                for flavor in parlor.flavors:
                    if flavor in self.hated_flavors:
                        parlor.flavors.remove(flavor)

            parlors_with_most_flavors = []
            max_flavors = max(len(parlor.flavors) for parlor in parlors_with_fav_flavors2)
            for parlor in parlors_with_fav_flavors2:
                if len(parlor.flavors) == max_flavors:
                    parlors_with_most_flavors.append(parlor)

            if len(parlors_with_most_flavors) == 1:
                return parlors_with_most_flavors[0]

            min_distance = min(round(parlor.pos.distance(self.pos), -2) for parlor in parlors_with_most_flavors)
            closest_parlors = [parlor for parlor in parlors_with_most_flavors
                               if round(parlor.pos.distance(self.pos), -2) == min_distance]

            if len(closest_parlors) == 1:
                return closest_parlors[0]

            parlors_with_fav_option = [parlor for parlor in closest_parlors if
                                       self.fav_option in parlor.prices and parlor.prices[
                                           self.fav_option] <= self.max_price]
            if len(parlors_with_fav_option) == 1:
                return parlors_with_fav_option[0]

            return random.choice(parlors_with_fav_option)
        except ValueNotALLOWEDError as e:
            print(f"{e}, try again")
            return None

    def buy(self, parlor: IceCreamParlor) -> float:
        try:
            if parlor is None:
                return 0.0

            if not isinstance(parlor, IceCreamParlor):
                raise IceParlorException("parlor must be an instance of IceCreamParlor")

            if self.fav_option in parlor.prices and parlor.prices[self.fav_option] <= self.max_price:
                return parlor.prices[self.fav_option]

            affordable_options = [price for price in parlor.prices.values() if price <= self.max_price]
            if affordable_options:
                return max(affordable_options)

            return 0.0

        except ValueNotALLOWEDError as e:
            print(f"{e}, try again")
            return 0.0

    def __str__(self) -> str:
        return f"Customer at {self.pos} with a budget of {self.max_price} and a preference for {self.fav_option}"
