"""
Main entry point.

Demonstrates:
  1. BFS on a sample graph.
  2. A* on the 8-puzzle (with Manhattan and Misplaced-tiles heuristics).
  3. A direct comparison of BFS vs A* on the 8-puzzle.
"""

from compare import compare_bfs_graph, compare_8puzzle

# ---------------------------------------------------------------------------
# 1. BFS on a simple undirected graph
# ---------------------------------------------------------------------------

SAMPLE_GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E", "G"],
    "G": ["F"],
}

print("\n" + "#" * 60)
print("# 1.  BFS – general graph search")
print("#" * 60)
compare_bfs_graph(SAMPLE_GRAPH, start="A", goal="G", label="Sample graph (A→G)")
compare_bfs_graph(SAMPLE_GRAPH, start="D", goal="C", label="Sample graph (D→C)")

# ---------------------------------------------------------------------------
# 2. A* on the 8-puzzle
# ---------------------------------------------------------------------------

print("\n" + "#" * 60)
print("# 2.  A* – 8-puzzle")
print("#" * 60)

# Easy (2 moves from goal)
EASY = (1, 2, 3,
        4, 5, 6,
        0, 7, 8)

# Medium difficulty
MEDIUM = (1, 2, 3,
          5, 0, 6,
          4, 7, 8)

# Hard (more shuffles required)
HARD = (8, 6, 7,
        2, 5, 4,
        3, 0, 1)

from astar_8puzzle import astar, manhattan, misplaced

for label, state in [("Easy", EASY), ("Medium", MEDIUM), ("Hard", HARD)]:
    result = astar(state, heuristic=manhattan)
    print(f"\n  8-puzzle [{label}]  expanded={result['expanded_nodes']}  "
          f"steps={len(result['path']) - 1 if result['path'] else 'N/A'}  "
          f"time={result['runtime_ms']:.3f} ms  "
          f"mem={result['memory_kb']:.2f} KB")

# ---------------------------------------------------------------------------
# 3. BFS vs A* comparison on the 8-puzzle
# ---------------------------------------------------------------------------

print("\n" + "#" * 60)
print("# 3.  BFS vs A* – 8-puzzle comparison")
print("#" * 60)

compare_8puzzle(EASY,   label="Easy (2 moves)")
compare_8puzzle(MEDIUM, label="Medium (3 moves)")
compare_8puzzle(HARD,   label="Hard (~26 moves)")
