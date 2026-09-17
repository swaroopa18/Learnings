"""
================================================================================
 PROBLEM: Matrix Block Sum (LeetCode 1314)
================================================================================
Given: an `row_len x col_len` matrix `mat` and an integer `k`.
Task: for each cell (i, j), compute the sum of all elements
`mat[r][c]` where `|r - i| <= k` and `|c - j| <= k` — i.e. the sum of the
square block of "radius" k centered at (i, j), clipped to the matrix
bounds. Return a matrix of these sums.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Should the block clip at the matrix edges, or wrap/pad? (Clip — matches
  the given solutions' `max(0, ...)` / `min(..., len-1)` clamping)
- Can k be 0? (Then each cell's block is just itself)
- Can k be larger than the matrix dimensions? (Then the block is the
  entire matrix for every cell — clamping handles this automatically)
- Is mat guaranteed non-empty / rectangular? (Usually yes — confirm)
"""

# ================================================================================
# MY APPROACH #1 — Brute Force (direct block summation)
# ================================================================================
"""
### Idea
For every cell (i, j), directly compute the clipped block boundaries
(row_start, row_end, col_start, col_end), then sum every element inside
that block with a nested loop.

### Complexity
- TC: O(rows * cols * k^2) — for each of the rows*cols cells, we sum up to
  a (2k+1) x (2k+1) block, which is O(k^2) work
- SC: O(rows * cols) — for the output matrix (ignoring the O(1) extra
  scratch variables)

### Pros
- Directly mirrors the problem statement — very easy to verify correct.
- No preprocessing step; simple to write under time pressure.

### Cons
- For large k (close to matrix size), this degrades toward
  O(rows^2 * cols^2) — quadratic in k on top of the matrix size, which is
  the real cost driver here.
- Massive redundant work: adjacent cells' blocks overlap heavily (a block
  centered at (i, j) and one at (i, j+1) share almost the entire block),
  but each is summed completely from scratch.

### Bottleneck
Every cell re-sums a whole rectangular region, even though neighboring
cells' regions overlap by up to (2k) x (2k+1) elements. Ask: "is there a
way to get ANY rectangular sum in O(1) after some preprocessing?" -> Yes:
2D prefix sums (below), which is the textbook fix for "many rectangular
range-sum queries on a fixed matrix."
"""


def matrix_block_sum_brute(mat: list[list[int]], k: int) -> list[list[int]]:
    col_len, row_len = len(mat[0]), len(mat)
    result = [[0] * col_len for _ in range(row_len)]

    for i in range(row_len):
        for j in range(col_len):
            row_start = i - k if i - k >= 0 else 0
            col_start = j - k if j - k >= 0 else 0
            row_end = i + k + 1 if i + k + 1 <= row_len else row_len
            col_end = j + k + 1 if j + k + 1 <= col_len else col_len
            total = 0
            for r in range(row_start, row_end):
                for c in range(col_start, col_end):
                    total += mat[r][c]
            result[i][j] = total
    return result


# ================================================================================
# MY APPROACH #2 — 2D Prefix Sum (optimal)
# ================================================================================
"""
### Idea
Precompute a 2D prefix-sum matrix `prefix`, where `prefix[i][j]` = sum of
ALL elements in the rectangle from (0,0) to (i-1, j-1) (using a 1-indexed
padded border to avoid special-casing row/col 0). Once built, the sum of
ANY axis-aligned rectangle can be computed in O(1) via inclusion-exclusion:

    rect_sum(r1..r2, c1..c2) = prefix[r2+1][c2+1]
                              - prefix[r1][c2+1]
                              - prefix[r2+1][c1]
                              + prefix[r1][c1]

(The `+ prefix[r1][c1]` term corrects for double-subtracting the
top-left overlap region — classic 2D inclusion-exclusion, the matrix
analog of 1D prefix sums.)

For each cell (i, j), clamp the block's corners to the matrix bounds
(r1, c1, r2, c2), then look up that rectangle's sum in O(1).

### Why does it work?
Building the prefix matrix is itself just 1D prefix-sum logic applied
along both axes simultaneously — each cell adds its own value to the
running sums accumulated from above and to the left, correcting for
double-counted overlap. Once built, every rectangle query becomes pure
arithmetic on 4 lookups, regardless of the rectangle's size.

### Complexity
- TC: O(rows * cols) — O(rows*cols) to build the prefix matrix, then
  O(rows*cols) to answer all queries at O(1) each — no dependence on k!
- SC: O(rows * cols) — for the (rows+1) x (cols+1) prefix matrix

### Pros
- Completely removes k from the time complexity — huge win when k is
  large relative to the matrix.
- Standard, reusable technique: any "give me the sum of many rectangular
  regions in a fixed matrix" problem reaches for 2D prefix sums.

### DSA Buddy Point 🧠
"Many overlapping rectangle-sum queries on a FIXED matrix -> build a 2D
prefix sum once, then answer each query in O(1) via inclusion-exclusion:
bottom-right minus the two overlapping strips, plus back the
double-subtracted corner."

### What can be improved?
Nothing further — O(rows*cols) is optimal here, since you must at least
read every input cell once, and this solution does exactly that (plus a
second O(rows*cols) pass for the O(1) queries). This is the accepted
optimal solution.
"""


def matrix_block_sum(mat: list[list[int]], k: int) -> list[list[int]]:
    col_len, row_len = len(mat[0]), len(mat)
    prefix = [[0] * (col_len + 1) for _ in range(row_len + 1)]
    result = [[0] * col_len for _ in range(row_len)]

    for i in range(row_len):
        for j in range(col_len):
            prefix[i + 1][j + 1] = (
                mat[i][j] + prefix[i][j + 1] + prefix[i + 1][j] - prefix[i][j]
            )

    for i in range(row_len):
        for j in range(col_len):
            r1 = max(0, i - k)
            c1 = max(0, j - k)
            r2 = min(i + k, row_len - 1)
            c2 = min(j + k, col_len - 1)

            result[i][j] = (
                prefix[r2 + 1][c2 + 1]
                - prefix[r1][c2 + 1]
                - prefix[r2 + 1][c1]
                + prefix[r1][c1]
            )
    return result


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MATRIX BLOCK SUM
│
├── Brute Force
│   └── For each cell, sum its clipped (2k+1) x (2k+1) block directly
│       └── O(rows * cols * k^2)
│
├── Bottleneck
│   └── Adjacent cells' blocks overlap heavily but are re-summed from
│       scratch every time — k appears as a squared cost factor
│
├── Key Observation
│   └── This is "many rectangular range-sum queries on a fixed matrix"
│       -> the textbook use case for 2D prefix sums
│
└── Optimization — 2D Prefix Sum
    ├── Build prefix[i+1][j+1] = mat[i][j] + prefix[i][j+1] + prefix[i+1][j]
    │                             - prefix[i][j]   (1D prefix sum, both axes)
    ├── Clamp each cell's block to matrix bounds -> (r1, c1, r2, c2)
    └── rect_sum = prefix[r2+1][c2+1] - prefix[r1][c2+1]
                    - prefix[r2+1][c1] + prefix[r1][c1]
        └── O(rows * cols) total, k no longer affects complexity
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Many overlapping rectangle-sum queries on a fixed matrix -> 2D prefix
  sums, always. This is the matrix generalization of 1D prefix sums for
  'many subarray sum queries.'"
- "2D prefix sum formula = inclusion-exclusion: bottom-right corner, minus
  the top strip, minus the left strip, PLUS the top-left corner back (it
  was subtracted twice)."
- "Padding the prefix matrix with an extra row/col of zeros (1-indexed
  lookup) avoids special-casing row 0 / col 0 boundaries."
- "Once the prefix matrix is built, k completely disappears from the time
  complexity — each query becomes O(1) regardless of block size."
- "Clamp block corners to matrix bounds with max(0, ...) / min(..., len-1)
  — this handles k larger than the matrix and edge cells uniformly."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach          | Core Idea                                         | TC                     | SC             | Pros                                  | Cons                                       | When to Use                     |
|----------------------|--------------------------------------------------------|------------------------|----------------|-------------------------------------------|-----------------------------------------------|-------------------------------------|
| Brute Force          | Sum each cell's block directly, nested loops              | O(rows*cols*k^2)       | O(rows*cols)   | Simple, directly matches problem statement | Degrades badly as k grows — huge redundant work | Small k, or as a first-pass baseline |
| 2D Prefix Sum        | Precompute prefix matrix, O(1) rectangle sum per cell      | O(rows*cols)           | O(rows*cols)   | k has NO effect on time complexity          | Needs the extra prefix matrix + inclusion-exclusion setup | Default optimal choice (your code)  |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: 2D Prefix Sum / Inclusion-Exclusion (matrix generalization of
  1D prefix sums — same family as "range sum query 2D - immutable").
- Go-to answer: "Precompute a 2D prefix-sum matrix so any rectangle's sum
  is a 4-lookup O(1) inclusion-exclusion query. For each cell, clamp its
  k-radius block to the matrix bounds and look up that rectangle's sum.
  O(rows*cols) time and space, completely independent of k."
- Good to mention the brute force first (and why it's O(k^2) per cell) to
  show you recognize WHY prefix sums are the fix — the "adjacent blocks
  overlap heavily" observation is the key insight interviewers want to
  hear.
- Common follow-up: "What if the matrix were mutable (updates between
  queries)?" -> Prefix sums don't support efficient updates; you'd need a
  2D Binary Indexed Tree (Fenwick Tree) or 2D segment tree instead.
"""