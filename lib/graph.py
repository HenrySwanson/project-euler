from collections import defaultdict
from heapq import heappop, heappush, heappushpop, heapreplace
from typing import Dict, Iterable, Mapping, TypeVar


T = TypeVar("T")


def node_costs_to_edge_costs(
    node_costs: Dict[T, int], edges: Mapping[T, Iterable[T]]
) -> Dict[T, Dict[T, int]]:
    """
    Many problems involve traversing a graph that has costs on the nodes, rather than edges.
    This function transforms a graph with costs on the vertices to one with costs on the edges.

    Specifically, an edge connecting node A to B will inherit the cost of node B. This means that
    the cost of the very first node in a path must be specially handled by the calling code.
    """

    return {src: {dst: node_costs[dst] for dst in dsts} for src, dsts in edges.items()}


def dijkstra(start_node: T, end_node: T, edge_costs: Dict[T, Dict[T, int]]) -> int:
    frontier = [(0, start_node)]
    min_cost = dict()

    while frontier:
        # Find the cheapest node in the frontier
        (cost, node) = heappop(frontier)
        min_cost[node] = cost

        if node == end_node:
            return cost

        # Explore this node
        for (dst_node, addl_cost) in edge_costs.get(node, {}).items():
            if dst_node in min_cost:
                assert addl_cost + cost >= min_cost[dst_node]
                continue
            heappush(frontier, (cost + addl_cost, dst_node))

    raise ValueError(f"No path found from {start_node} to {end_node}!")
