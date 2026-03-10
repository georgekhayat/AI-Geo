"""
Comparison utilities: run BFS and A* on matching problems and print a summary
table of expanded nodes, runtime, and peak memory usage.
"""

from __future__ import annotations

import time
import tracemalloc
from collections import deque

from bfs import bfs
from astar_8puzzle import astar, manhattan, misplaced, GOAL_STATE

# ---------------------------------------------------------------------------
# BFS on the 8-puzzle (for a fair side-by-side comparison)
# ---------------------------------------------------------------------------

def bfs_8puzzle(initial_state: tuple):
    """
    Solve the 8-puzzle with plain BFS (no heuristic).

    Shares the same return schema as ``astar`` so the two can be compared
    directly.
    """
    from astar_8puzzle import _successors, is_solvable

    if not is_solvable(initial_state):
        return {
            "path": None,
            "expanded_nodes": 0,
            "runtime_ms": 0.0,
            "memory_kb": 0.0,
        }

    tracemalloc.start()
    start_time = time.perf_counter()

    expanded_nodes = 0
    visited = {initial_state}
    queue = deque([(initial_state, [initial_state])])

    path = None
    while queue:
        state, current_path = queue.popleft()
        expanded_nodes += 1

        if state == GOAL_STATE:
            path = current_path
            break

        for successor in _successors(state):
            if successor not in visited:
                visited.add(successor)
                queue.append((successor, current_path + [successor]))

    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "path": path,
        "expanded_nodes": expanded_nodes,
        "runtime_ms": (end_time - start_time) * 1000,
        "memory_kb": peak_memory / 1024,
    }


# ---------------------------------------------------------------------------
# Pretty-print helpers
# ---------------------------------------------------------------------------

def _fmt_state(state: tuple) -> str:
    rows = []
    for r in range(3):
        row = " ".join(str(state[r * 3 + c]) if state[r * 3 + c] != 0 else "_"
                       for c in range(3))
        rows.append(f"  {row}")
    return "\n".join(rows)


def _print_comparison(puzzle_label: str, bfs_result: dict, astar_manhattan: dict, astar_misplaced: dict):
    headers = ["Metric", "BFS", "A* (Manhattan)", "A* (Misplaced)"]
    col_w = 18

    def row(label, *values):
        cells = [label.ljust(col_w)] + [str(v).ljust(col_w) for v in values]
        return "  ".join(cells)

    sep = "-" * (col_w * 4 + 6)
    print(f"\n{'=' * len(sep)}")
    print(f"  Puzzle: {puzzle_label}")
    print(sep)
    print(row(*headers))
    print(sep)

    # Expanded nodes
    print(row(
        "Expanded nodes",
        bfs_result["expanded_nodes"],
        astar_manhattan["expanded_nodes"],
        astar_misplaced["expanded_nodes"],
    ))
    # Solution length
    bfs_len = len(bfs_result["path"]) - 1 if bfs_result["path"] else "N/A"
    am_len = len(astar_manhattan["path"]) - 1 if astar_manhattan["path"] else "N/A"
    ams_len = len(astar_misplaced["path"]) - 1 if astar_misplaced["path"] else "N/A"
    print(row("Solution length", bfs_len, am_len, ams_len))
    # Runtime
    print(row(
        "Runtime (ms)",
        f"{bfs_result['runtime_ms']:.3f}",
        f"{astar_manhattan['runtime_ms']:.3f}",
        f"{astar_misplaced['runtime_ms']:.3f}",
    ))
    # Memory
    print(row(
        "Peak memory (KB)",
        f"{bfs_result['memory_kb']:.2f}",
        f"{astar_manhattan['memory_kb']:.2f}",
        f"{astar_misplaced['memory_kb']:.2f}",
    ))
    print(sep)


# ---------------------------------------------------------------------------
# Graph BFS demo helper
# ---------------------------------------------------------------------------

def compare_bfs_graph(graph: dict, start, goal, label: str = "Graph"):
    """Run BFS on a graph, print a summary, and return the result."""
    result = bfs(graph, start, goal)
    print(f"\n{'=' * 60}")
    print(f"  BFS on {label}  |  start={start!r}  goal={goal!r}")
    print("-" * 60)
    print(f"  Path           : {result['path']}")
    print(f"  Expanded nodes : {result['expanded_nodes']}")
    print(f"  Runtime (ms)   : {result['runtime_ms']:.3f}")
    print(f"  Peak memory(KB): {result['memory_kb']:.2f}")
    print("=" * 60)
    return result


# ---------------------------------------------------------------------------
# 8-puzzle comparison helper
# ---------------------------------------------------------------------------

def compare_8puzzle(initial_state: tuple, label: str = ""):
    """Run BFS and A* (both heuristics) on *initial_state* and print a table."""
    print(f"\nInitial board ({label}):")
    print(_fmt_state(initial_state))

    bfs_result = bfs_8puzzle(initial_state)
    astar_m = astar(initial_state, heuristic=manhattan)
    astar_mp = astar(initial_state, heuristic=misplaced)

    _print_comparison(label, bfs_result, astar_m, astar_mp)
    return bfs_result, astar_m, astar_mp
