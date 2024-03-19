from typing import List

from IceCreamParlorF import IceCreamParlor
from IceParlorExceptionF import ValueNotALLOWEDError
from ParlorCustomerF import ParlorCustomer


class ParlorSimulation:

    def __init__(self, clients: list[ParlorCustomer], parlors: List[IceCreamParlor]):
        try:
            if not isinstance(clients, list) or not all(
                    isinstance(client, ParlorCustomer) for client in clients):
                raise ValueNotALLOWEDError("clients must be a list of ParlorCustomer instances")
            if not isinstance(parlors, list) or not all(
                    isinstance(parlor, IceCreamParlor) for parlor in parlors):
                raise ValueNotALLOWEDError("parlors must be a list of IceCreamParlor instances")
            self.clients = clients
            if len(parlors) == 0:
                raise ValueNotALLOWEDError("There are no parlors")
            for parlor1 in parlors:
                for parlor2 in parlors:
                    if parlor1 != parlor2 and parlor1.pos == parlor2.pos:
                        raise ValueNotALLOWEDError("There are two parlors with the same postion")
            self.parlors = parlors
        except ValueNotALLOWEDError as e:
            print(f"{e}, try again")

    def run(self) -> dict[str, float]:
        profits = {parlor.name: 0 for parlor in self.parlors}
        for client in self.clients:
            chosen_parlor = client.choose(self.parlors)
            if chosen_parlor is not None:
                spent_money = client.buy(chosen_parlor)
                profits[chosen_parlor.name] += spent_money
        return profits

    def most_profitable(self) -> List[IceCreamParlor]:
        max_profit = max(self.run().values())
        return [parlor for parlor in self.parlors if self.run()[parlor.name] == max_profit]

    def most_customers(self) -> List[IceCreamParlor]:
        max_customers = max(len([client for client in self.clients if client.choose([parlor]) == parlor]) for parlor in
                            self.parlors)
        return [parlor for parlor in self.parlors if
                len([client for client in self.clients if client.choose([parlor]) == parlor]) == max_customers]

    def unhappy_customers(self) -> List[ParlorCustomer]:
        return [client for client in self.clients if client.buy(client.choose(self.parlors)) == 0.0]


