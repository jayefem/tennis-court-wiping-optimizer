import math


class Point:
    def __init__(
            self,
            x=0.0,
            y=0.0):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def normalize(self):
        return ("x" + str("%.1f" % self.x) + "-y" + str("%.1f" % self.y)).replace(".", "_")

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"
