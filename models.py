from dataclasses import dataclass

@dataclass(eq=True, frozen=False)
class Edge:
    start_index: int
    end_index: int
    weight: int
    type: int

@dataclass
class Vertex:
    x: int
    y: int
    weight: int