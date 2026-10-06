"""
================================================================================
 PROBLEM: Maximal Rectangle (LeetCode 85)
================================================================================
Given a `rows x cols` binary matrix `matrix` filled with the CHARACTERS "0"
and "1", find the largest rectangle containing ONLY "1"s and return its AREA.

Example:
    matrix = [["1","0","1","0","0"],
              ["1","0","1","1","1"],
              ["1","1","1","1","1"],
              ["1","0","0","1","0"]]
    -> 6   (the 2 x 3 block of 1s in rows 1-2, columns 2-4)

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Are the cells the STRINGS "0"/"1" or the integers 0/1? (Strings in the
  LeetCode signature — comparing against the int 1 is the #1 silent bug here.)
- Must the rectangle be filled ENTIRELY with 1s and be axis-aligned? (Yes —
  every cell inside must be "1"; no rotation, no holes.)
- Do I return the AREA or the dimensions? (The area, a single integer.)
- Can the matrix be empty / all zeros? (Yes -> return 0; guard `not matrix or
  not matrix[0]`.)
- What are the sizes? (Up to 200 x 200 -> 40,000 cells. O(R^2 * C^2) is up to
  ~1.6 * 10^9 steps = too slow; the intended solution is O(R * C).)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "MAXIMAL RECTANGLE IN A MATRIX" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Turn each ROW into a HISTOGRAM and reuse LC 84:                   │
    │     heights[j] = number of consecutive "1"s going UP from this row  │
    │                  in column j  (reset to 0 when the cell is "0").    │
    │   The largest rectangle whose BOTTOM edge lies on the current row   │
    │   = largest rectangle in that histogram.                            │
    │   Answer = max over all rows. O(R * C) time, O(C) space.            │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the 2-D CAPSTONE of the monotonic-stack family: Daily Temperatures ->
Next Greater -> Stock Span -> Largest Rectangle in Histogram (LC 84) -> THIS.
The only new idea is the reduction from a matrix to a sequence of histograms.
Key ideas:

1. **Fix the BOTTOM row of the rectangle.** Every all-ones rectangle has a
   bottom row `r`. For that row, the cells above it that are still 1s form
   vertical bars — exactly a histogram.

2. **`heights` is updated incrementally row by row:**
   `heights[j] = heights[j] + 1 if matrix[r][j] == "1" else 0`.
   One O(C) pass per row; the array is reused (O(C) space, not O(R*C)).

3. **The best rectangle with bottom edge on row `r` is the largest rectangle
   in `heights`** (a rectangle of height h over columns [a, b] needs every bar
   in [a, b] to have height >= h — exactly the LC 84 condition). Run the O(C)
   monotonic-stack solution on it.

4. **A "0" cell resets its column to height 0,** which acts as a wall in the
   histogram: no positive-area rectangle can cross it.

5. **Total cost = rows x (O(C) update + O(C) stack pass) = O(R * C),** which is
   optimal — every cell must be read at least once.

6. **Alternative view (DP):** for each column track `height[j]`, `left[j]` and
   `right[j]` (how far the current "1"-run of that height extends left/right).
   Area = `(right[j] - left[j]) * height[j]`. Same O(R*C), no stack.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Choose every top-left corner `(r1, c1)` and every bottom-right corner
`(r2, c2)`, check that every cell inside is "1", and track the biggest area.
There are O(R^2 * C^2) corner pairs and each check costs O(R * C) ->
O(R^3 * C^3). Correct, hopeless for 200 x 200.

### First improvement: stop re-checking cells
From a fixed top-left `(r1, c1)`, go DOWN one row at a time and keep the
largest width still available: the run of "1"s starting at `c1` shrinks as
soon as a row has a "0" earlier. Each row gives a rectangle of area
`(rows so far) * (current width)`. O(R^2 * C^2) total.

### The key insight: stack the rows into a histogram
For each row, count how many consecutive "1"s sit directly above (and
including) each cell. Those counts form a histogram of bar heights. Any
all-ones rectangle ending on that row is a rectangle inside that histogram!
Use the O(C) monotonic-stack solution from LC 84 on every row.

### Step-by-step trace
```
matrix                      heights after row     best rectangle in histogram
row 0: 1 0 1 0 0   ->       [1, 0, 1, 0, 0]       1
row 1: 1 0 1 1 1   ->       [2, 0, 2, 1, 1]       3   (bars idx 2..4, min 1, width 3)
row 2: 1 1 1 1 1   ->       [3, 1, 3, 2, 2]       6   (bars idx 2..4, min 2, width 3)
row 3: 1 0 0 1 0   ->       [4, 0, 0, 3, 0]       4   (single bar of height 4)
answer = max(1, 3, 6, 4) = 6 ✅
```

Detail for row 2, heights = [3, 1, 3, 2, 2] (single-pass stack + sentinel 0):
```
i=0 cur=3: push 0                                   stack=[0]
i=1 cur=1: pop 0 (h=3), left=-1, width=1, area 3    push 1   stack=[1]
i=2 cur=3: push 2                                   stack=[1,2]
i=3 cur=2: pop 2 (h=3), left=1, width=1, area 3     push 3   stack=[1,3]
i=4 cur=2: top h=2 > 2? no                          push 4   stack=[1,3,4]
i=5 cur=0 (sentinel):
           pop 4 (h=2), left=3, width=1, area 2
           pop 3 (h=2), left=1, width=3, area 6  <- best
           pop 1 (h=1), left=-1, width=5, area 5
row 2 best = 6 ✅
```

### The "aha" moment to remember 🎯
"A binary-matrix rectangle problem is LC 84 in disguise: cumulative column
heights give a histogram per row; the largest rectangle with its bottom on
that row lives in the histogram."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (every corner pair + full check)
# ================================================================================
"""
### Thought Process 🧠
Enumerate every top-left `(r1, c1)` that is "1", every bottom-right
`(r2, c2)` with `r2 >= r1` and `c2 >= c1`, and verify that all cells in the
sub-rectangle are "1". Record the area of valid ones. This is literally the
definition of the problem.

### Complexity
- TC: O(R^3 * C^3) — O(R^2 * C^2) corner pairs, O(R * C) validation each
- SC: O(1) extra

### Pros
- Zero cleverness; trivially correct, perfect oracle for testing.
- Skipping start cells that are "0" prunes a little.

### Cons
- For 200 x 200 this is astronomically slow (~10^15 steps in the worst case).
- Validates overlapping rectangles from scratch over and over.
- The inner `break` only exits the innermost loop (`j`); the outer `i` loop
  keeps running even after a zero is found. The answer is still correct
  because `is_rect` stays `False`, but wasted work could be avoided with a
  flag/early return.

### Bottleneck
Re-verifying every cell of every candidate rectangle, although a bigger
rectangle's validity depends on a smaller one's. Ask: "can I grow rectangles
incrementally and remember what is already known to be all 1s?" -> Yes (next
approaches).
"""


class SolutionBruteForce:
    def maximalRectangle(self, matrix: list[list[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        rows = len(matrix)
        cols = len(matrix[0])
        max_area = 0

        for r1 in range(rows):
            for c1 in range(cols):
                if matrix[r1][c1] == "0":
                    continue

                for r2 in range(r1, rows):
                    for c2 in range(c1, cols):
                        is_rect = True
                        for i in range(r1, r2 + 1):
                            for j in range(c1, c2 + 1):
                                if matrix[i][j] == "0":
                                    is_rect = False
                                    break
                        if is_rect:
                            area = (r2 - r1 + 1) * (c2 - c1 + 1)
                            max_area = max(max_area, area)
        return max_area


# ================================================================================
# MY APPROACH — Fix Top-Left, Extend Down with a Shrinking Width (O(R^2 * C^2))
# ================================================================================
"""
### Idea
For each top-left corner `(r1, c1)`, start with the widest possible width
(`cols - c1`) and walk DOWN row by row (`r2`). In every row, scan columns from
`c1` while within the current `width`; the first "0" at column `c2` shrinks
the width to `c2 - c1`. If the width reaches 0, no taller rectangle from this
corner can exist -> stop going down. Otherwise the rectangle `(r2 - r1 + 1)
x width` is valid -> update the maximum.

### Complexity
- TC: O(R^2 * C^2) worst case — R*C corners, each scanning up to R rows x C
  columns (e.g. an all-"1" matrix). Far better than brute force's
  O(R^3 * C^3).
- SC: O(1) extra

### Pros
- Shares work between rectangles: the width only ever SHRINKS as you go down,
  so each corner never re-validates previously accepted cells' columns
  beyond the current width.
- Early termination (`width == 0 -> break`) prunes dead corners instantly
  (including "0" start cells: the scan hits the zero immediately).
- No extra memory, short, readable, and still easy to reason about.

### Cons
- Still quadratic in the number of cells: ~1.6 * 10^9 steps at 200 x 200 in
  the worst case (all "1"s) -> too slow in Python.
- Re-scans the same row segments for every top-left corner in the same row.
- Looks like it does a lot of redundant work, because it does: two corners in
  the same column ask almost the same question.

### DSA Buddy Point 🧠
"Fixing a corner and extending in one direction while keeping the minimum
extent in the other direction is the brute-force cousin of the histogram
idea — the running `width` is the 'min bar height so far'. Replace the nested
scans with precomputed per-column heights and a monotonic stack to reach O(R*C)."

### What can be improved?
Correctness is fine (verified against brute force below, including the
"first cell is 0" case and the "width becomes 0 mid-way" case). To reach the
optimal complexity, precompute the per-column consecutive-ones height row by
row and run the LC 84 monotonic-stack solution on each row — O(R * C).
"""


class Solution:
    def maximalRectangle(self, matrix: list[list[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        rows = len(matrix)
        cols = len(matrix[0])
        max_area = 0

        for r1 in range(rows):
            for c1 in range(cols):
                width = cols - c1

                for r2 in range(r1, rows):
                    for c2 in range(c1, c1 + width):
                        if matrix[r2][c2] == "0":
                            width = c2 - c1
                            break

                    if width == 0:
                        break

                    area = (r2 - r1 + 1) * width
                    max_area = max(max_area, area)

        return max_area


# ================================================================================
# ALTERNATIVE APPROACH 2 — Consecutive-Ones Width per Cell + Walk Up (O(R^2 * C))
# ================================================================================
"""
### Thought Process 🧠
Precompute `width[r][c]` = number of consecutive "1"s ending at `(r, c)` in
row `r` (reset to 0 at a "0"). Now fix the BOTTOM-RIGHT corner `(r, c)` and
walk UP: for `k = r, r-1, ...`, keep `min_w = min(min_w, width[k][c])`; the
rectangle spanning rows `k..r` with right edge at column `c` can be at most
`min_w` wide, so its area is `min_w * (r - k + 1)`. Stop when `min_w == 0`.

### Complexity
- TC: O(R^2 * C) — for each of R*C cells, walk up at most R rows
- SC: O(R * C) — the `width` table

### Pros
- A big step down from O(R^2 * C^2): the inner row scans become O(1) lookups
  thanks to the precomputed widths.
- Easy to explain as "brute force + prefix counts"; a good intermediate answer
  if the stack idea doesn't come to mind.

### Cons
- Still O(R^2 * C) — about 8 * 10^6 steps at 200 x 200, fine here but not
  optimal; and uses O(R * C) extra memory.
- Not obviously generalizable to larger matrices.

### DSA Buddy Point 🧠
"Prefix counts (consecutive ones per row) turn 'check a whole row segment'
into an O(1) lookup — a general trick for rectangle problems."
"""


def maximal_rectangle_walk_up(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    width = [[0] * cols for _ in range(rows)]
    best = 0
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == "1":
                width[r][c] = (width[r][c - 1] if c > 0 else 0) + 1
                min_w = width[r][c]
                for k in range(r, -1, -1):
                    min_w = min(min_w, width[k][c])
                    if min_w == 0:
                        break
                    best = max(best, min_w * (r - k + 1))
    return best


# ================================================================================
# ALTERNATIVE APPROACH 3 — Histogram per Row + Monotonic Stack (optimal, canonical)
# ================================================================================
"""
### Thought Process 🧠
Maintain `heights[j]` = consecutive "1"s ending at the current row in column
`j`. After updating `heights` for each row, compute the largest rectangle in
the histogram `heights` with the single-pass monotonic stack from LC 84
(sentinel bar of height 0 at the end). The overall answer is the maximum over
all rows.

### Complexity
- TC: O(R * C) — per row: O(C) to update + O(C) for the stack pass
- SC: O(C) — one `heights` array and the stack

### Pros
- Optimal time and the standard interview answer.
- O(C) space — only the current histogram is stored.
- Reuses a known sub-solution (LC 84) — a textbook "reduce to a solved
  problem" move that interviewers love to see.

### Cons
- Requires knowing/deriving the LC 84 stack technique first (width =
  `i - new_top - 1`, sentinel flush) — easy to slip on off-by-ones.
- Two-step reasoning (matrix -> histogram -> stack) is harder to explain than
  brute force.
- Remember the matrix holds STRINGS: compare with `"1"`, not `1`.

### DSA Buddy Point 🧠
"2-D 'largest all-ones rectangle' = row-by-row histogram + LC 84. The
incremental `heights` update is the bridge between the two problems."
"""


def _largest_in_histogram(heights: list[int]) -> int:
    n = len(heights)
    stack: list[int] = []
    best = 0
    for i in range(n + 1):
        cur = heights[i] if i < n else 0
        while stack and heights[stack[-1]] > cur:
            h = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, h * (i - left - 1))
        stack.append(i)
    return best


def maximal_rectangle_histogram(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    cols = len(matrix[0])
    heights = [0] * cols
    best = 0
    for row in matrix:
        for j in range(cols):
            heights[j] = heights[j] + 1 if row[j] == "1" else 0
        best = max(best, _largest_in_histogram(heights))
    return best


# ================================================================================
# ALTERNATIVE APPROACH 4 — DP with height / left / right Arrays (no stack)
# ================================================================================
"""
### Thought Process 🧠
For each column `j` keep three values describing the tallest rectangle that
has its BOTTOM on the current row and contains column `j`:
- `height[j]`: consecutive "1"s above (including this row);
- `left[j]`: leftmost column of the contiguous span where every column has
  height >= `height[j]` (computed as `max(left[j] from the previous row,
  start of the current run of 1s)`);
- `right[j]`: one past the rightmost such column (`min(right[j] from the
  previous row, end of the current run of 1s)`).
Area = `(right[j] - left[j]) * height[j]`. On a "0" cell reset `height = 0`,
`left = 0`, `right = cols` so the neutral values don't constrain the next row.

### Complexity
- TC: O(R * C) — three linear passes per row
- SC: O(C) — three arrays of length `cols`

### Pros
- Optimal time and space; NO monotonic stack — only simple loops and
  `max`/`min` updates.
- Nice alternative if you don't remember the LC 84 stack solution.

### Cons
- The `left`/`right` update rules and their reset values are subtle and easy
  to get wrong (`left` resets to 0, `right` resets to `cols`).
- Harder to prove correct than the stack; unfamiliar to many interviewers.
- Three separate passes per row make the code longer.

### DSA Buddy Point 🧠
"The span of a column's rectangle only SHRINKS as you keep a column's height:
carry `left`/`right` from the previous row and clip them with the current
row's run of 1s."
"""


def maximal_rectangle_dp(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    cols = len(matrix[0])
    height = [0] * cols
    left = [0] * cols
    right = [cols] * cols
    best = 0

    for row in matrix:
        cur_left = 0
        for j in range(cols):
            if row[j] == "1":
                height[j] += 1
                left[j] = max(left[j], cur_left)
            else:
                height[j] = 0
                left[j] = 0
                cur_left = j + 1

        cur_right = cols
        for j in range(cols - 1, -1, -1):
            if row[j] == "1":
                right[j] = min(right[j], cur_right)
            else:
                right[j] = cols
                cur_right = j

        for j in range(cols):
            best = max(best, (right[j] - left[j]) * height[j])
    return best


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MAXIMAL RECTANGLE (binary matrix)
│
├── Brute Force
│   └── Every (top-left, bottom-right) pair + full validation
│       -> O(R^3 * C^3) time, O(1) space
│
├── Bottleneck
│   └── Re-validates overlapping rectangles from scratch; rows of 1s that
│       were already known are re-scanned over and over
│
├── Key Insight
│   └── Fix the BOTTOM row; consecutive 1s above each column form a HISTOGRAM
│       -> largest rectangle with that bottom = LC 84 on the histogram
│
├── My Approach — Top-Left + Extend Down, Shrinking Width
│   └── width = cols - c1; for each row down, shrink width at the first "0";
│       area = (rows) * width -> O(R^2 * C^2) time, O(1) space
│
├── Width Table + Walk Up
│   └── width[r][c] = consecutive 1s ending at (r, c); walk up keeping min
│       -> O(R^2 * C) time, O(R * C) space
│
├── Histogram + Monotonic Stack (OPTIMAL, canonical)
│   └── heights[j] += 1 or reset to 0; run LC 84 stack on each row
│       -> O(R * C) time, O(C) space
│
└── DP: height / left / right arrays (OPTIMAL, no stack)
    └── clip left/right with the current run of 1s; area = (right - left) * height
        -> O(R * C) time, O(C) space
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Matrix rectangle of 1s => per-row HISTOGRAM of consecutive-1s heights +
  Largest Rectangle in Histogram (LC 84). That reduction is the whole problem."
- "`heights[j] = heights[j] + 1 if cell == '1' else 0` — a 0 cell RESETS the
  column; everything above it no longer counts."
- "Cells are STRINGS ('0'/'1'), not ints — compare against '1'."
- "Fix the BOTTOM edge: every all-ones rectangle has a bottom row, and in that
  row it is a rectangle inside the histogram."
- "Total O(R * C): O(C) update + O(C) stack pass per row; space O(C)."
- "Single-pass LC 84 stack: width = `i - new_top - 1` after popping, sentinel
  height 0 at the end to flush."
- "No-stack alternative: DP with `left`/`right`/`height` arrays; reset values
  on '0' are `left = 0`, `right = cols`, `height = 0`."
- "Early exit in corner-based solutions: once the available width hits 0, no
  taller rectangle from that corner exists."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                      | Core Idea                                                   | TC               | SC        | Pros                                              | Cons                                                    | When to Use                              |
|-------------------------------|-------------------------------------------------------------|------------------|-----------|---------------------------------------------------|---------------------------------------------------------|------------------------------------------|
| Brute Force                   | Every corner pair + full validation                         | O(R^3 * C^3)     | O(1)      | Trivially correct, great oracle                   | Astronomically slow, redundant checks                   | Baseline / correctness check (your 1st)  |
| Top-Left + Extend Down        | Shrinking width as rows go down; stop at width 0            | O(R^2 * C^2)     | O(1)      | Shares work, early exit, no extra memory          | Still quadratic in cells, TLE at 200 x 200 in Python    | Better brute force (your 2nd code)       |
| Width Table + Walk Up         | Precompute consecutive-ones per row; walk up w/ running min | O(R^2 * C)       | O(R * C)  | Big speedup, simple idea                          | Not optimal, extra O(R * C) memory                      | Intermediate answer                      |
| Histogram + Monotonic Stack   | heights per row + LC 84 single-pass stack                   | O(R * C)         | O(C)      | Canonical optimal, reuses LC 84                   | Needs the stack solution; off-by-one prone              | Best answer to write in an interview     |
| DP height / left / right      | Carry left/right bounds from previous row, clip with runs   | O(R * C)         | O(C)      | Optimal, no stack                                 | Subtle reset rules, harder to prove                     | When the stack solution isn't top of mind|

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Reduction to Largest Rectangle in Histogram (monotonic stack) —
  per-row cumulative column heights. Cousins: LC 84 (Largest Rectangle in
  Histogram), LC 221 (Maximal Square), LC 1504 (Count Submatrices With All
  Ones), LC 739/901/503 (monotonic stack family).
- Go-to answer: "For every row, maintain `heights[j]` = consecutive 1s ending
  at that row in column j (reset to 0 on a '0'). The largest all-ones
  rectangle whose bottom edge is on this row is the largest rectangle in that
  histogram, which I find in O(C) with a monotonic stack. Take the maximum
  over all rows: O(R * C) time, O(C) space."
- Good to call out: that cells are strings, why fixing the bottom row makes
  it a histogram, the zero-reset, and the sentinel/width formula of the stack.
- Common follow-ups:
  * "Largest SQUARE of 1s?" -> LC 221: `dp[i][j] = 1 + min(up, left, diag)`
    in O(R * C), or use the same histogram with side = min(height, width).
  * "Count ALL all-ones rectangles?" -> LC 1504: same row histogram with a
    monotonic stack that accumulates counts.
  * "Streaming rows, can't store the matrix?" -> `heights` is only O(C), so
    the histogram/stack solution already works online row by row.
  * "Can you do it without a stack?" -> The DP with left/right/height arrays.
"""
