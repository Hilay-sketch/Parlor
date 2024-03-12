class Position:
    def __init__(self, x: int, y: int):
        try:
            self.x = int(x)
            self.y = int(y)
        except ValueError:
            raise ValueError("Position coordinates must be integers")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, other) -> float:
        if not isinstance(other, Position):
            raise TypeError("other must be an instance of Position")
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __str__(self):
        return f"({self.x}, {self.y})"
