# AI-Geo – BFS and A\* Search Algorithms

A Python implementation of two classical AI search algorithms with a
side-by-side performance comparison.

---

## Algorithms

### 1. BFS – Breadth-First Search (`bfs.py`)

General-purpose BFS for unweighted graphs.  
Input: an adjacency-list dictionary, a start node, and a goal node.  
Output: shortest path, expanded-node count, runtime (ms), and peak memory (KB).

### 2. A\* – 8-Puzzle Solver (`astar_8puzzle.py`)

A\* search applied to the classic 3×3 sliding-tile puzzle.  
Goal state: `1 2 3 / 4 5 6 / 7 8 _`

Two admissible heuristics are provided:

| Heuristic | Description |
|-----------|-------------|
| `manhattan` | Sum of Manhattan distances of each tile to its goal position |
| `misplaced` | Number of tiles not in their goal position (blank excluded) |

### 3. Comparison (`compare.py`)

Helper functions that run both BFS and A\* on the same 8-puzzle instance and
print a comparison table of:

- **Expanded nodes** – how many states were dequeued/popped
- **Solution length** – number of moves to reach the goal
- **Runtime (ms)** – wall-clock time
- **Peak memory (KB)** – measured with `tracemalloc`

---

## Quick Start

```bash
# Run the full demo (BFS on a graph + A* on puzzles + comparison table)
python main.py

# Run the test suite
python -m pytest test_algorithms.py -v
```

No external dependencies are required – the code uses only the Python
standard library (`collections`, `heapq`, `time`, `tracemalloc`).

### Generate the PDF Report

```bash
pip install -r requirements.txt   # one-time: installs fpdf2
python generate_report.py         # creates report.pdf
```

A two-page PDF summarising the algorithms, performance comparison, and key
findings will be saved as `report.pdf` in the project root.

---

## Sample Output

```
# 3.  BFS vs A* – 8-puzzle comparison

Puzzle: Hard (~26 moves)
----------------------------------------------------------------------
Metric              BFS           A* (Manhattan)  A* (Misplaced)
----------------------------------------------------------------------
Expanded nodes      181439        21198           143849
Solution length     31            31              31
Runtime (ms)        1804.879      374.782         2578.477
Peak memory (KB)    35442.39      6978.59         28781.59
----------------------------------------------------------------------
```

### Key observations

* **A\* with Manhattan** expands the fewest nodes and uses the least memory
  because Manhattan distance is a tighter (closer-to-true-cost) heuristic
  than the misplaced-tiles count.
* **BFS** finds the optimal solution but explores the search space blindly,
  expanding far more nodes than A\*.
* **A\* with Misplaced** sits between the two: it is guided by a heuristic but
  that heuristic under-estimates the true cost more than Manhattan does.

---

## File Overview

| File | Purpose |
|------|---------|
| `bfs.py` | BFS for general unweighted graphs |
| `astar_8puzzle.py` | A\* for the 8-puzzle (Manhattan & misplaced heuristics) |
| `compare.py` | Comparison helpers (BFS vs A\* on the 8-puzzle) |
| `main.py` | Demo entry point |
| `generate_report.py` | Generates a two-page PDF report (`report.pdf`) |
| `requirements.txt` | Python dependencies for PDF generation |
| `test_algorithms.py` | Pytest test suite (28 tests) |
