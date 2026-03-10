"""
A* search for the 8-puzzle.

The 8-puzzle is a 3×3 sliding tile game.  The blank tile is represented by 0.
States are stored as flat tuples of 9 integers, e.g.:

    (1, 2, 3,
     4, 0, 6,
     7, 5, 8)  →  [[1,2,3],[4,_,6],[7,5,8]]

Goal state: (1, 2, 3, 4, 5, 6, 7, 8, 0)

Two heuristics are provided:
  - ``manhattan``  : sum of Manhattan distances of each tile to its goal position.
  - ``misplaced``  : number of tiles not in their goal position (excluding blank).

Tracks the number of expanded nodes, runtime, and memory usage so results can
be compared with BFS.
"""

import heapq
import time
import tracemalloc

# ---------------------------------------------------------------------------
# Goal state and helpers
# ---------------------------------------------------------------------------

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Pre-compute goal positions for each tile value (tile → (row, col)).
_GOAL_POSITIONS: dict[int, tuple[int, int]] = {
    GOAL_STATE[i]: (i // 3, i % 3) for i in range(9)
}


def _blank_index(state: tuple) -> int:
    return state.index(0)


def _successors(state: tuple) -> list[tuple]:
    """Return all states reachable by sliding one tile into the blank."""
    blank = _blank_index(state)
    row, col = blank // 3, blank % 3
    moves = []
    # (row_delta, col_delta)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            neighbour = new_row * 3 + new_col
            lst = list(state)
            lst[blank], lst[neighbour] = lst[neighbour], lst[blank]
            moves.append(tuple(lst))
    return moves


# ---------------------------------------------------------------------------
# Heuristics
# ---------------------------------------------------------------------------

def manhattan(state: tuple) -> int:
    """Sum of Manhattan distances of each tile to its goal position."""
    total = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_row, goal_col = _GOAL_POSITIONS[tile]
        cur_row, cur_col = i // 3, i % 3
        total += abs(cur_row - goal_row) + abs(cur_col - goal_col)
    return total


def misplaced(state: tuple) -> int:
    """Number of tiles not in their goal position (blank excluded)."""
    return sum(
        1 for i, tile in enumerate(state) if tile != 0 and tile != GOAL_STATE[i]
    )


# ---------------------------------------------------------------------------
# Solvability check
# ---------------------------------------------------------------------------

def is_solvable(state: tuple) -> bool:
    """
    An 8-puzzle is solvable if and only if the number of inversions is even.

    An *inversion* is a pair (i, j) with i < j where state[i] > state[j],
    ignoring the blank tile.
    """
    tiles = [t for t in state if t != 0]
    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )
    return inversions % 2 == 0


# ---------------------------------------------------------------------------
# A* search
# ---------------------------------------------------------------------------

def astar(initial_state: tuple, heuristic=manhattan):
    """
    Solve the 8-puzzle from *initial_state* using A*.

    Parameters
    ----------
    initial_state : tuple of 9 ints
        Starting board configuration.
    heuristic : callable
        A function (state) → non-negative int estimating cost to goal.
        Defaults to ``manhattan``.

    Returns
    -------
    dict with keys:
        path          : list of states from initial_state to GOAL_STATE,
                        or None if the puzzle is unsolvable.
        expanded_nodes: number of nodes popped from the priority queue.
        runtime_ms    : wall-clock time in milliseconds.
        memory_kb     : peak memory usage in kilobytes.
    """
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

    # Priority queue entries: (f, g, state, path_so_far)
    # Using g as a tiebreaker keeps the heap order stable.
    h0 = heuristic(initial_state)
    heap = [(h0, 0, initial_state, [initial_state])]
    # best g-cost seen for each state
    best_g: dict[tuple, int] = {initial_state: 0}

    path = None
    while heap:
        f, g, state, current_path = heapq.heappop(heap)

        # Stale entry check
        if g > best_g.get(state, float("inf")):
            continue

        expanded_nodes += 1

        if state == GOAL_STATE:
            path = current_path
            break

        for successor in _successors(state):
            new_g = g + 1
            if new_g < best_g.get(successor, float("inf")):
                best_g[successor] = new_g
                h = heuristic(successor)
                heapq.heappush(heap, (new_g + h, new_g, successor, current_path + [successor]))

    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "path": path,
        "expanded_nodes": expanded_nodes,
        "runtime_ms": (end_time - start_time) * 1000,
        "memory_kb": peak_memory / 1024,
    }
