"""
================================================================================
 PROBLEM: Search a 2D Matrix II (LeetCode 240)
================================================================================
Given: an m x n `matrix` where every ROW is sorted ascending left-to-
right AND every COLUMN is sorted ascending top-to-bottom — but, UNLIKE
LC 74, there is NO guarantee that rows chain together (row i+1's first
element does NOT need to exceed row i's last element). Given a `target`,
return True if it exists anywhere in the matrix, else False.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is this the "rows AND columns independently sorted" version, or the
  "whole matrix is one chained sorted sequence" version (LC 74)? (This
  is THE critical distinguishing question — confusing the two leads
  straight to reaching for a flat-index binary search that doesn't
  work here, since there's no global ordering to flatten)
- Can the matrix be empty, or contain empty rows? (Guard for
  `len(matrix) == 0` or `len(matrix[0]) == 0` -> return False)
- Are duplicate values allowed? (Doesn't affect an existence check)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "STAIRCASE SEARCH" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Rows sorted + columns sorted, but NO global chaining across      │
    │   rows -> you CANNOT flatten this into one sorted 1-D array, so    │
    │   binary search (in the classic sense) doesn't directly apply.     │
    │   Instead: start at a CORNER where one direction increases and     │
    │   the other decreases (top-right or bottom-left), and let each     │
    │   comparison eliminate a whole ROW or a whole COLUMN at once.      │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the natural follow-up to LC 74 "Search a 2D Matrix" and is
explicitly flagged there as needing a DIFFERENT technique — here's why,
and what's new:

1. **Why flattening breaks here.** LC 74's trick relied on
   `matrix[i+1][0] > matrix[i][-1]` so reading row-by-row produced one
   ascending sequence. Here that guarantee is GONE — row 2 might start
   smaller than row 1 ends. So `idx // n, idx % n` no longer maps a flat
   sorted position to the right cell; the "flat array" isn't sorted at
   all anymore. Classic binary search needs a single monotonic sequence
   to eliminate half the search space per step — this matrix doesn't
   offer one globally, only along each row and each column separately.

2. **The corner trick: pick a starting cell where "up/down" and
   "left/right" move in OPPOSITE value directions.** At the top-right
   corner `(0, cols-1)`: moving LEFT (decreasing column) only ever
   DECREASES the value (row sorted ascending L->R), while moving DOWN
   (increasing row) only ever INCREASES the value (column sorted
   ascending top->bottom). That's exactly the property needed to prune
   correctly: if `matrix[r][c] > target`, target can't be anywhere in
   column `c` (everything below `matrix[r][c]` in that column is even
   bigger) -> eliminate the WHOLE column, move left. If
   `matrix[r][c] < target`, target can't be anywhere in row `r`
   (everything left of `matrix[r][c]` in that row is even smaller) ->
   eliminate the WHOLE row, move down. The bottom-left corner works
   symmetrically (swap the roles of left/right and up/down).

3. **Why NOT the top-left or bottom-right corner?** At the top-left
   corner, moving right AND moving down both INCREASE the value — two
   directions that agree in sign give you no way to decide which one to
   eliminate when `matrix[r][c] != target`. You'd have to try both,
   losing the "eliminate a whole row/column per step" guarantee. Same
   problem (values only decrease in both directions) at bottom-right.
   Only the two ANTI-diagonal corners work.

4. **Each step eliminates one full row OR one full column — not half
   the remaining cells like binary search does.** So the total work is
   bounded by `(rows - 1) + (cols - 1)` steps in the worst case (you can
   move down at most `rows-1` times and left at most `cols-1` times
   before falling off the matrix) -> O(m + n), not O(log(m*n)). Slower
   per-step progress than true binary search, but still linear rather
   than the brute force's O(m*n) — a real win, just a different shape of
   win.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Scan every cell and compare to target — O(m*n), ignores all structure.

### The key insight: find a corner with "opposite" monotonicity
Picture:
```
matrix = [
  [ 1,  4,  7, 11, 15],
  [ 2,  5,  8, 12, 19],
  [ 3,  6,  9, 16, 22],
  [10, 13, 14, 17, 24],
  [18, 21, 23, 26, 30],
]
```
Start at top-right corner, value 15 (row 0, col 4):
- Moving LEFT along row 0: 15, 11, 7, 4, 1 -> strictly DECREASING.
- Moving DOWN along col 4: 15, 19, 22, 24, 30 -> strictly INCREASING.
So at `(0, 4)`, "left" and "down" point in opposite value directions —
exactly the leverage needed: one comparison tells you definitively
whether to eliminate the current ROW (move down) or the current COLUMN
(move left).

### Step-by-step trace: search(matrix above, target=5)
```
r=0, c=4 -> matrix[0][4]=15 -> 15 > 5 -> eliminate column 4 -> c=3
r=0, c=3 -> matrix[0][3]=11 -> 11 > 5 -> eliminate column 3 -> c=2
r=0, c=2 -> matrix[0][2]=7  -> 7 > 5  -> eliminate column 2 -> c=1
r=0, c=1 -> matrix[0][1]=4  -> 4 < 5  -> eliminate row 0    -> r=1
r=1, c=1 -> matrix[1][1]=5  -> MATCH -> True ✅
```
5 steps total, each eliminating a whole row or column — never re-checked.

### The "aha" moment to remember 🎯
LC 74 and LC 240 LOOK like the same problem (sorted rows, sorted
columns) but need genuinely different algorithms because LC 74 has one
extra guarantee (global chaining) that LC 240 lacks. When you see "rows
and columns are sorted" in a problem statement, always ask: "do rows
ALSO chain together into one global order?" If yes -> flatten and binary
search (LC 74 style). If no -> staircase search from an anti-diagonal
corner (this problem).
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (scan every cell)
# ================================================================================
"""
### Thought Process 🧠
Nested loop over every row and column, check for equality.

### Complexity
- TC: O(m * n)
- SC: O(1)

### Pros
- Always correct, no assumptions about structure required.

### Cons
- Ignores both sortedness guarantees entirely.

### Bottleneck
Doesn't use row/column sortedness to eliminate anything. Ask: "is there
a starting point from which one comparison reliably tells me to discard
an entire row or column?" -> Yes: the anti-diagonal corners -> staircase
search (main approach below).
"""


class SolutionBruteForce:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == target:
                    return True
        return False


# ================================================================================
# ALTERNATIVE APPROACH — Per-Row Binary Search
# ================================================================================
"""
### Thought Process 🧠
Since each row IS individually sorted (even without cross-row chaining),
binary search each row for `target`, same as LC 74's Approach #1.

### Complexity
- TC: O(m log n) — one O(log n) binary search per row
- SC: O(1)

### Pros
- Correct, and still a real improvement over brute force.
- Simple: reuses ordinary binary search, no new logic needed.

### Cons
- Doesn't use column-sortedness at all -> strictly worse than the
  staircase approach, which is O(m + n) and beats O(m log n) whenever
  `n` is reasonably large (log n > 1, i.e. basically always for n > 2).
- Feels like it "should" be optimal by analogy to LC 74, but LC 74's
  extra chaining guarantee is exactly what made per-row/per-column
  binary search near-optimal there — that edge is gone here.

### DSA Buddy Point 🧠
"Don't assume a technique that worked on a 'twin' problem (LC 74) ports
over directly — always re-check which specific guarantees the new
problem does or doesn't retain (here: cross-row chaining is dropped),
since that's usually exactly what determines the right algorithm."

### What can be improved?
Use BOTH sortedness directions at once via a corner-based staircase
search — O(m + n), and no per-row search needed at all.
"""


class SolutionPerRowBinarySearch:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        for r in range(len(matrix)):
            l, hi = 0, len(matrix[0]) - 1
            while l <= hi:
                mid = (l + hi) // 2
                if matrix[r][mid] == target:
                    return True
                elif matrix[r][mid] < target:
                    l = mid + 1
                else:
                    hi = mid - 1
        return False


# ================================================================================
# MY APPROACH — Staircase Search from the Top-Right Corner (optimal)
# ================================================================================
"""
### Idea
Start at `(row=0, col=cols-1)` — the top-right corner. At each step:
- If `matrix[r][c] == target` -> found it, return True.
- If `matrix[r][c] > target` -> everything below in this column is even
  bigger (column sorted ascending downward), so target can't be in this
  column -> move left (`c -= 1`), eliminating the whole column.
- If `matrix[r][c] < target` -> everything to the left in this row is
  even smaller (row sorted ascending rightward), so target can't be in
  this row -> move down (`r += 1`), eliminating the whole row.
Stop when the pointers walk off the matrix (`r >= rows or c < 0`) ->
target isn't present -> False.

### Complexity
- TC: O(m + n) — `r` can only increase up to `rows` times and `c` can
  only decrease up to `cols` times before the loop must terminate; each
  iteration does O(1) work
- SC: O(1) — just two pointers

### Pros
- Uses BOTH sortedness guarantees simultaneously — no wasted structure.
- Single loop, no nested search, minimal code and minimal edge cases.
- Optimal for this problem's guarantees: you cannot do better than
  O(m + n) here in general, since (unlike LC 74) there's no global order
  to exploit for a logarithmic algorithm — a classic adversarial matrix
  can force you to touch this many rows/columns.

### Cons
- Slower per-step progress than true binary search (eliminates one
  row/column per step, not half the remaining search space) — but this
  is a genuine consequence of the weaker sortedness guarantee, not a
  flaw in the algorithm; O(m + n) is the best achievable here.

### DSA Buddy Point 🧠
"When two sorted directions in a grid don't globally chain into one
order, look for a STARTING CORNER where the two directions move in
OPPOSITE senses (one increasing, one decreasing) — that's what lets a
single comparison eliminate an entire row or column, turning O(m*n) into
O(m + n) without needing true binary search at all."

### What can be improved?
Nothing asymptotically — O(m+n) is optimal for this problem's
guarantees. (Symmetric variant: start bottom-left instead of top-right —
same complexity, mirrored logic.)
"""


class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        rows, cols = len(matrix), len(matrix[0])

        r, c = 0, cols - 1

        while r < rows and c >= 0:
            if matrix[r][c] == target:
                return True
            elif matrix[r][c] > target:
                c -= 1
            else:
                r += 1
        return False


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
SEARCH A 2D MATRIX II (LC 240)
│
├── Brute Force
│   └── Scan every cell -> O(m*n)
│
├── Bottleneck
│   └── Ignores both row- and column-sortedness
│
├── Key Difference from LC 74
│   └── NO global chaining across rows -> matrix does NOT flatten into
│       one sorted 1-D array -> classic/flat-index binary search
│       does NOT apply here
│
├── Per-Row Binary Search
│   └── Uses row-sortedness only -> O(m log n)
│       (misses column-sortedness entirely; worse than staircase)
│
└── Staircase Search from Anti-Diagonal Corner (BEST)
    └── Start top-right (or bottom-left): one direction increases,
        the other decreases -> each comparison eliminates a whole
        row OR column -> O(m + n) time, O(1) space
        (top-left / bottom-right corners DON'T work: both directions
         move the same way there, giving no basis to choose)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "LC 74 vs LC 240: the deciding question is always 'does the sortedness
  chain GLOBALLY across rows, or only WITHIN each row/column
  independently?' Global chaining -> flatten + binary search,
  O(log(m*n)). Independent only -> staircase search, O(m + n). Mixing
  these up is the single most common mistake on this problem pair."
- "The staircase search's starting corner MUST be one of the two
  ANTI-diagonal corners (top-right or bottom-left) — only there do the
  two movement directions (row-wise, column-wise) point in opposite
  value directions, which is what lets one comparison eliminate an
  entire row or column. Top-left and bottom-right corners don't work:
  both directions increase (or both decrease) the value there."
- "O(m + n) here is NOT a weaker/lazier answer than O(log(m*n)) — it's
  the best possible complexity given this problem's guarantees. Don't
  try to force a binary-search-flavored solution onto a matrix that
  doesn't have the global ordering binary search needs."
- "Each staircase step eliminates one full row OR one full column —
  never re-visits a cell — which is why the total steps are bounded by
  `(rows - 1) + (cols - 1)`, giving the O(m + n) bound directly from the
  loop's own termination condition."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                                          | TC           | SC   | Pros                                               | Cons                                                        | When to Use                              |
|--------------------------------|-----------------------------------------------------------------------|---------------|------|-------------------------------------------------------|------------------------------------------------------------------|---------------------------------------------|
| Brute Force                    | Scan every cell                                                        | O(m*n)        | O(1) | Trivial, no structure assumptions needed                | Ignores both sortedness guarantees -> far too slow                 | Baseline / correctness check only            |
| Per-Row Binary Search          | Standard binary search within each row, loop over rows                  | O(m log n)    | O(1) | Simple, exploits row-sortedness                         | Ignores column-sortedness -> worse than staircase for large n        | If only row-sortedness is guaranteed          |
| Staircase Search (corner)      | Start at top-right (or bottom-left); eliminate a row or column per step | O(m + n)      | O(1) | Optimal for this problem, single loop, minimal edge cases | Slower per-step progress than true binary search (but that's optimal)| Default optimal choice for LC 240             |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Staircase / Corner-Elimination Search — a distinct technique
  from classic binary search, used when a grid is sorted along both
  axes independently but does NOT globally chain into one sorted
  sequence (contrast with LC 74's flat-index binary search).
- Go-to answer: "Start at the top-right corner. If the current value is
  bigger than target, the whole column below it is even bigger, so move
  left, eliminating that column. If it's smaller, the whole row to the
  left is even smaller, so move down, eliminating that row. Repeat until
  found or the pointers walk off the matrix — O(m + n) time, O(1)
  space."
- Good to explicitly contrast this with LC 74 "Search a 2D Matrix" if
  discussing both — the surface-level problem statements look almost
  identical, but the missing cross-row chaining guarantee here means
  the flat-index binary search trick from LC 74 is NOT valid and would
  silently give wrong answers if applied to this matrix shape.
- Common follow-up: "Can you do better than O(m + n)?" -> Not in
  general, for an arbitrary matrix satisfying only these two
  guarantees — an adversarial matrix can be constructed to force the
  staircase to visit close to `m + n` cells, so this is asymptotically
  tight for this problem's guarantees.
"""