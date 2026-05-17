from dataclasses import dataclass
from enum import IntEnum


class EdgeType(IntEnum):
    DIRECTED = 0
    UNDIRECTED = 1

    @classmethod
    def from_value(cls, value):
        try:
            return cls(value)
        except (TypeError, ValueError):
            return cls.UNDIRECTED


def normalize_weight(value, default=1):
    try:
        weight = int(value)
    except (TypeError, ValueError):
        return default
    return weight if weight > 0 else default


@dataclass(eq=True, frozen=False)
class Edge:
    start_index: int
    end_index: int
    weight: int = 1
    edge_type: EdgeType = EdgeType.UNDIRECTED

    def __post_init__(self):
        self.weight = normalize_weight(self.weight)
        self.edge_type = EdgeType.from_value(self.edge_type)

    @property
    def type(self):
        return int(self.edge_type)

    @type.setter
    def type(self, value):
        self.edge_type = EdgeType.from_value(value)


@dataclass
class Vertex:
    x: float
    y: float
    weight: int = 1
