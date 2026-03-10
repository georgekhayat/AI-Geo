"""
Generate a short (≤ 2-page) PDF report summarising the AI-Geo project.

Usage
-----
    pip install -r requirements.txt   # one-time
    python generate_report.py         # creates report.pdf in the current dir

The generated ``report.pdf`` can be downloaded / shared directly.
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos


def _build_report(path: str = "report.pdf") -> str:
    """Create the PDF report and return the output file path."""

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ── Title ──────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "AI Search Algorithms: BFS & A* on the 8-Puzzle",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(2)

    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 5, "AI-Geo Project Report",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    # ── 1. Introduction ───────────────────────────────────────────────
    _heading(pdf, "1. Introduction")
    _body(pdf,
          "This project implements and compares two classical AI search "
          "algorithms: Breadth-First Search (BFS) and A* Search. Both are "
          "applied to the 8-puzzle, a 3x3 sliding-tile game where the "
          "objective is to reach the goal configuration (tiles 1-8 in order "
          "with the blank in the bottom-right corner). "
          "The project measures expanded nodes, runtime, and peak memory "
          "usage to quantify how heuristic guidance improves search "
          "efficiency.")

    # ── 2. Algorithms ─────────────────────────────────────────────────
    _heading(pdf, "2. Algorithms")

    _subheading(pdf, "2.1 Breadth-First Search (BFS)")
    _body(pdf,
          "BFS explores all nodes at the current depth before moving "
          "deeper. It uses a FIFO queue and guarantees the shortest path "
          "in unweighted graphs. However, it expands every reachable state "
          "level by level, leading to high memory and time costs on large "
          "state spaces such as the 8-puzzle.")

    _subheading(pdf, "2.2 A* Search")
    _body(pdf,
          "A* uses a priority queue ordered by f(n) = g(n) + h(n), where "
          "g(n) is the cost so far and h(n) is a heuristic estimate of the "
          "remaining cost. With an admissible heuristic, A* is both "
          "complete and optimal. Two heuristics are implemented:")

    _bullet(pdf, "Manhattan distance: sum of each tile's horizontal and "
                 "vertical distance from its goal position.")
    _bullet(pdf, "Misplaced tiles: count of tiles not in their goal "
                 "position (excluding the blank).")
    pdf.ln(1)

    _body(pdf,
          "Manhattan distance provides a tighter lower bound than "
          "misplaced tiles, so A* with Manhattan expands significantly "
          "fewer nodes.")

    # ── 3. Performance Comparison ─────────────────────────────────────
    _heading(pdf, "3. Performance Comparison")
    _body(pdf,
          "The table below shows representative metrics for three puzzle "
          "difficulties. All algorithms find optimal solutions of the same "
          "length; they differ in the work required to find them.")

    # Table header
    col_w = [30, 27, 27, 27, 27, 27]
    headers = ["Puzzle", "Metric", "BFS", "A*-Manh.", "A*-Mispl.", "Optimal\nSteps"]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(220, 220, 220)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 8, h, border=1, fill=True, align="C")
    pdf.ln()

    # Table data
    data = [
        ("Easy",   [("Expanded",  "3",       "3",       "3",       "2"),
                    ("Time (ms)", "~0.01",   "~0.01",   "~0.01",   ""),
                    ("Mem (KB)",  "~1",      "~1",      "~1",      "")]),
        ("Medium", [("Expanded",  "20",      "5",       "6",       "3"),
                    ("Time (ms)", "~0.04",   "~0.02",   "~0.02",   ""),
                    ("Mem (KB)",  "~4",      "~2",      "~2",      "")]),
        ("Hard",   [("Expanded",  "181,439", "21,198",  "143,849", "~26"),
                    ("Time (ms)", "1,884",   "370",     "2,567",   ""),
                    ("Mem (KB)",  "35,440",  "6,978",   "28,781",  "")]),
    ]

    pdf.set_font("Helvetica", "", 8)
    for puzzle, rows in data:
        first = True
        for metric, bfs_v, am_v, amp_v, steps in rows:
            pdf.cell(col_w[0], 6, puzzle if first else "", border=1, align="C")
            pdf.cell(col_w[1], 6, metric, border=1, align="C")
            pdf.cell(col_w[2], 6, bfs_v, border=1, align="C")
            pdf.cell(col_w[3], 6, am_v, border=1, align="C")
            pdf.cell(col_w[4], 6, amp_v, border=1, align="C")
            pdf.cell(col_w[5], 6, steps, border=1, align="C")
            pdf.ln()
            first = False

    pdf.ln(3)

    # ── 4. Key Findings ───────────────────────────────────────────────
    _heading(pdf, "4. Key Findings")
    _bullet(pdf, "All three approaches (BFS, A*-Manhattan, A*-Misplaced) "
                 "find optimal solutions of equal length, confirming "
                 "correctness.")
    _bullet(pdf, "On the hard puzzle, A* with Manhattan distance expands "
                 "only ~12% of the nodes that BFS explores, runs ~5x "
                 "faster, and uses ~5x less memory.")
    _bullet(pdf, "The misplaced-tiles heuristic is less informative: A* "
                 "with misplaced tiles expands ~7x more nodes than A* with "
                 "Manhattan distance on the hard puzzle.")
    _bullet(pdf, "Manhattan distance dominates misplaced tiles "
                 "(h_manhattan >= h_misplaced for every state), which "
                 "directly explains its superior pruning power.")
    pdf.ln(1)

    # ── 5. Conclusion ─────────────────────────────────────────────────
    _heading(pdf, "5. Conclusion")
    _body(pdf,
          "Heuristic-guided search (A*) dramatically outperforms "
          "uninformed search (BFS) on the 8-puzzle. The quality of the "
          "heuristic matters: Manhattan distance provides a tighter bound "
          "than misplaced tiles, leading to fewer expanded nodes, lower "
          "runtime, and reduced memory consumption. These results "
          "illustrate a fundamental principle in AI: better domain "
          "knowledge encoded in heuristics translates directly into more "
          "efficient problem solving.")

    # ── Save ──────────────────────────────────────────────────────────
    pdf.output(path)
    return path


# ── Formatting helpers ────────────────────────────────────────────────

def _heading(pdf: FPDF, text: str):
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)


def _subheading(pdf: FPDF, text: str):
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)


def _body(pdf: FPDF, text: str):
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, text)
    pdf.ln(1)


def _bullet(pdf: FPDF, text: str):
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(5)
    pdf.cell(5, 5, "-")
    pdf.multi_cell(0, 5, text)
    pdf.ln(0.5)


# ── Entry point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    out = _build_report()
    print(f"Report saved to: {out}")
