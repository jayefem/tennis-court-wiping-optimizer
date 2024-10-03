# 3rd party modules


# Project modules
from Point import Point


class TennisCourtLine:
    def __init__(
            self,
            id,
            name,
            description,
            start: Point = None,
            end: Point = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.start = start
        self.end = end

    def length(self):
        return self.start.distance(self.end)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if other == None:
            return False
        return self.name == other.name

    def __repr__(self):
        return f"Line '{self.name}' from ({self.start.x}, {self.start.y}) to ({self.end.x}, {self.end.y}), Length: {self.length():.3f}"
