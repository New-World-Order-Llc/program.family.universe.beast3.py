# program.family.universe.beast3.py
# Beast System 3.0 — Deterministic Universe Map & Topology Module

from dataclasses import dataclass, field
import time
import hashlib

@dataclass
class UniverseNode:
    name: str
    metadata: dict
    ts: float = field(default_factory=time.time)
    hash: str = ""

    def finalize(self):
        serialized = f"{self.name}{self.metadata}{self.ts}".encode("utf-8")
        self.hash = hashlib.sha256(serialized).hexdigest()

@dataclass
class UniverseEdge:
    source: str
    target: str
    relation: str
    ts: float = field(default_factory=time.time)
    hash: str = ""

    def finalize(self):
        serialized = f"{self.source}{self.target}{self.relation}{self.ts}".encode("utf-8")
        self.hash = hashlib.sha256(serialized).hexdigest()

@dataclass
class UniverseMap:
    system_id: str
    nodes: dict = field(default_factory=dict)
    edges: list = field(default_factory=list)
    last_update: float = field(default_factory=time.time)

    def add_node(self, name: str, metadata: dict):
        node = UniverseNode(name, metadata)
        node.finalize()
        self.nodes[name] = node
        self.last_update = node.ts

    def add_edge(self, source: str, target: str, relation: str):
        edge = UniverseEdge(source, target, relation)
        edge.finalize()
        self.edges.append(edge)
        self.last_update = edge.ts

class UniverseEngine:
    def __init__(self, kernel):
        self.kernel = kernel
        self.universes = {}

    def create_universe(self, system_id: str):
        universe = UniverseMap(system_id)
        self.universes[system_id] = universe

        return self.kernel.dispatch(
            module="family.universe",
            action="create_universe",
            payload={"system_id": system_id}
        )

    def add_module(self, system_id: str, module_name: str, metadata: dict):
        if system_id not in self.universes:
            raise ValueError("Universe not found")

        universe = self.universes[system_id]
        universe.add_node(module_name, metadata)

        return self.kernel.dispatch(
            module="family.universe",
            action="add_module",
            payload={"system_id": system_id, "module": module_name, "metadata": metadata}
        )

    def link_modules(self, system_id: str, source: str, target: str, relation: str):
        if system_id not in self.universes:
            raise ValueError("Universe not found")

        universe = self.universes[system_id]
        universe.add_edge(source, target, relation)

        return self.kernel.dispatch(
            module="family.universe",
            action="link_modules",
            payload={
                "system_id": system_id,
                "source": source,
                "target": target,
                "relation": relation
            }
        )

    def get_universe(self, system_id: str):
        return self.universes.get(system_id, None)
