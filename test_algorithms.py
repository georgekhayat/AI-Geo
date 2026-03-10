"""
Tests for BFS and A* implementations.
"""

import pytest
from bfs import bfs
from astar_8puzzle import (
    astar,
    manhattan,
    misplaced,
    is_solvable,
    GOAL_STATE,
    _successors,
)
from compare import bfs_8puzzle


# ---------------------------------------------------------------------------
# BFS – graph search
# ---------------------------------------------------------------------------

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E", "G"],
    "G": ["F"],
}


class TestBFSGraph:
    def test_finds_path(self):
        result = bfs(GRAPH, "A", "G")
        assert result["path"] is not None

    def test_path_starts_and_ends_correctly(self):
        result = bfs(GRAPH, "A", "G")
        assert result["path"][0] == "A"
        assert result["path"][-1] == "G"

    def test_path_is_valid(self):
        result = bfs(GRAPH, "A", "G")
        path = result["path"]
        for i in range(len(path) - 1):
            assert path[i + 1] in GRAPH[path[i]], (
                f"{path[i + 1]} is not a neighbour of {path[i]}"
            )

    def test_shortest_path_length(self):
        # Shortest A→G path: A-C-F-G (length 3)
        result = bfs(GRAPH, "A", "G")
        assert len(result["path"]) - 1 == 3

    def test_start_equals_goal(self):
        result = bfs(GRAPH, "A", "A")
        assert result["path"] == ["A"]
        assert result["expanded_nodes"] == 1

    def test_unreachable_goal(self):
        disconnected = {"X": ["Y"], "Y": ["X"], "Z": []}
        result = bfs(disconnected, "X", "Z")
        assert result["path"] is None

    def test_expanded_nodes_positive(self):
        result = bfs(GRAPH, "A", "G")
        assert result["expanded_nodes"] > 0

    def test_runtime_and_memory_recorded(self):
        result = bfs(GRAPH, "A", "G")
        assert result["runtime_ms"] >= 0
        assert result["memory_kb"] >= 0


# ---------------------------------------------------------------------------
# 8-puzzle helpers
# ---------------------------------------------------------------------------

class TestHelpers:
    def test_solvable_goal(self):
        assert is_solvable(GOAL_STATE)

    def test_unsolvable(self):
        # Swap tiles 1 and 2 in goal → one inversion → unsolvable
        state = (2, 1, 3, 4, 5, 6, 7, 8, 0)
        assert not is_solvable(state)

    def test_successors_of_goal(self):
        # Blank is at position 8 (bottom-right), can slide tile above or left
        succs = _successors(GOAL_STATE)
        assert len(succs) == 2

    def test_manhattan_goal_is_zero(self):
        assert manhattan(GOAL_STATE) == 0

    def test_misplaced_goal_is_zero(self):
        assert misplaced(GOAL_STATE) == 0

    def test_manhattan_one_off(self):
        # Move blank from index 8 to index 7 (swap 8 and 0)
        state = (1, 2, 3, 4, 5, 6, 7, 0, 8)
        # Tile 8 is at position 7 (row=2, col=1), goal is (row=2, col=2) → dist=1
        assert manhattan(state) == 1

    def test_misplaced_one_off(self):
        state = (1, 2, 3, 4, 5, 6, 7, 0, 8)
        # Only tile 8 is out of place
        assert misplaced(state) == 1


# ---------------------------------------------------------------------------
# A* on the 8-puzzle
# ---------------------------------------------------------------------------

class TestAstar:
    EASY = (1, 2, 3, 4, 5, 6, 0, 7, 8)   # 2 moves
    MEDIUM = (1, 2, 3, 5, 0, 6, 4, 7, 8)  # 3 moves

    def test_solves_easy_manhattan(self):
        result = astar(self.EASY, heuristic=manhattan)
        assert result["path"] is not None
        assert result["path"][-1] == GOAL_STATE

    def test_solves_easy_misplaced(self):
        result = astar(self.EASY, heuristic=misplaced)
        assert result["path"] is not None
        assert result["path"][-1] == GOAL_STATE

    def test_optimal_path_easy(self):
        result = astar(self.EASY, heuristic=manhattan)
        assert len(result["path"]) - 1 == 2

    def test_solves_medium(self):
        result = astar(self.MEDIUM, heuristic=manhattan)
        assert result["path"] is not None
        assert result["path"][-1] == GOAL_STATE

    def test_goal_state_returns_trivial_path(self):
        result = astar(GOAL_STATE, heuristic=manhattan)
        assert result["path"] == [GOAL_STATE]
        assert result["expanded_nodes"] == 1

    def test_unsolvable_returns_none(self):
        unsolvable = (2, 1, 3, 4, 5, 6, 7, 8, 0)
        result = astar(unsolvable, heuristic=manhattan)
        assert result["path"] is None

    def test_path_validity(self):
        """Every consecutive pair of states in the path must be a valid move."""
        result = astar(self.MEDIUM, heuristic=manhattan)
        path = result["path"]
        for i in range(len(path) - 1):
            assert path[i + 1] in _successors(path[i])

    def test_expanded_nodes_positive(self):
        result = astar(self.EASY, heuristic=manhattan)
        assert result["expanded_nodes"] > 0

    def test_runtime_and_memory_recorded(self):
        result = astar(self.EASY, heuristic=manhattan)
        assert result["runtime_ms"] >= 0
        assert result["memory_kb"] >= 0

    def test_manhattan_expands_fewer_nodes_than_misplaced(self):
        """Manhattan is a tighter heuristic: should expand ≤ nodes than misplaced."""
        result_m = astar(self.MEDIUM, heuristic=manhattan)
        result_mp = astar(self.MEDIUM, heuristic=misplaced)
        assert result_m["expanded_nodes"] <= result_mp["expanded_nodes"]


# ---------------------------------------------------------------------------
# BFS vs A* on the 8-puzzle
# ---------------------------------------------------------------------------

class TestBFSvsAstar:
    MEDIUM = (1, 2, 3, 5, 0, 6, 4, 7, 8)

    def test_bfs_finds_optimal_solution(self):
        result = bfs_8puzzle(self.MEDIUM)
        assert result["path"] is not None
        assert result["path"][-1] == GOAL_STATE

    def test_both_find_same_optimal_length(self):
        bfs_result = bfs_8puzzle(self.MEDIUM)
        astar_result = astar(self.MEDIUM, heuristic=manhattan)
        assert len(bfs_result["path"]) == len(astar_result["path"])

    def test_astar_expands_fewer_nodes_than_bfs(self):
        """A* with Manhattan should expand fewer nodes than BFS on non-trivial puzzles."""
        bfs_result = bfs_8puzzle(self.MEDIUM)
        astar_result = astar(self.MEDIUM, heuristic=manhattan)
        assert astar_result["expanded_nodes"] <= bfs_result["expanded_nodes"]
