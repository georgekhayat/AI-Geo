"""
BFS (Breadth-First Search) for general graph search.

Tracks the number of expanded nodes, runtime, and memory usage so results
can be compared with A*.
"""

import time
import tracemalloc
from collections import deque


def bfs(graph: dict, start, goal):
    """
    Perform BFS on an unweighted graph.

    Parameters
    ----------
    graph : dict
        Adjacency list representation  {node: [neighbour, ...], ...}.
    start : hashable
        Starting node.
    goal : hashable
        Goal node.

    Returns
    -------
    dict with keys:
        path          : list of nodes from start to goal, or None if unreachable.
        expanded_nodes: number of nodes dequeued (expanded) during the search.
        runtime_ms    : wall-clock time in milliseconds.
        memory_kb     : peak memory usage in kilobytes.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    expanded_nodes = 0
    visited = {start}
    # Each entry: (node, path_so_far)
    queue = deque([(start, [start])])

    path = None
    while queue:
        node, current_path = queue.popleft()
        expanded_nodes += 1

        if node == goal:
            path = current_path
            break

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, current_path + [neighbour]))

    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "path": path,
        "expanded_nodes": expanded_nodes,
        "runtime_ms": (end_time - start_time) * 1000,
        "memory_kb": peak_memory / 1024,
    }
