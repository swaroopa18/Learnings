"""
================================================================================
 PROBLEM: Range Sum Query 2D - Immutable (LeetCode 304)
================================================================================
Given: a fixed (immutable — never updated after construction) 2D matrix.
Task: support many `sumRegion(row1, col1, row2, col2)` queries, each asking
for the sum of the rectangle from (row1, col1) to (row2, col2) inclusive,
as efficiently as possible per query.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is the matrix guaranteed to stay immutable (no update() calls)? (Yes —
  that's the whole point of this variant vs. LC 308's mutable version)
- How many queries should we expect? (Many — this signals "pay
  preprocessing cost once, make each query cheap")
- Are row1<=row2 and col1<=col2 always valid, in-bounds inputs? (Usually
  yes — confirm before skipping bounds checks)
"""

# ================================================================================
# MY APPROACH — 2D Prefix Sum, Precomputed Once in __init__
# ================================================================================
"""
### Idea
This is the constructor/query (amortized) version of the same 2D prefix
sum idea used for "Matrix Block Sum": build `prefix[i+1][j+1]` = sum of
the rectangle from (0,0) to (i,j) ONCE in `__init__`, using a padded
(rows+1) x (cols+1) grid to avoid special-casing row/col 0. Then every
`sumRegion` call is a pure O(1) inclusion-exclusion lookup:

    sumRegion(r1,c1,r2,c2) = prefix[r2+1][c2+1]
                            - prefix[r1][c2+1]
                            - prefix[r2+1][c1]
                            + prefix[r1][c1]

### Why does it work?
`prefix[r2+1][c2+1]` covers everything from the origin down to (r2,c2).
Subtracting `prefix[r1][c2+1]` removes everything above row r1; subtracting
`prefix[r2+1][c1]` removes everything left of column c1. But the top-left
corner rectangle (above r1 AND left of c1) got subtracted twice by those
two operations, so it's added back once via `+ prefix[r1][c1]` — classic
inclusion-exclusion.

### Complexity
- TC:
  - `__init__`: O(rows * cols) — one pass to build the prefix matrix
  - `sumRegion`: O(1) per call — just 4 array lookups and arithmetic
- SC: O(rows * cols) — for the padded prefix matrix

### Pros
- Query cost is O(1) regardless of how many times `sumRegion` is called —
  the O(rows*cols) cost is paid exactly once, up front, in `__init__`.
- This is precisely the right trade for an "immutable + many queries"
  API design — most of the total work amortizes away as query count grows.

### DSA Buddy Point 🧠
"'Immutable matrix + many range-sum queries' is the textbook signal for
2D prefix sums: pay O(rows*cols) once in the constructor, then answer
every future query in O(1)."

### What can be improved?
Nothing for this exact API shape — O(1) per query after O(rows*cols)
preprocessing is optimal, since you can't answer even a single query
without having looked at the matrix at least once overall. This class of
problem changes ONLY if updates re-enter the picture (see the "mutable"
follow-up below), at which point prefix sums stop being the right tool.
"""


class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        self.matrix = matrix
        cols, rows = len(matrix[0]), len(matrix)

        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]

        for i in range(rows):
            for j in range(cols):
                self.prefix[i + 1][j + 1] = (
                    matrix[i][j]
                    + self.prefix[i][j + 1]
                    + self.prefix[i + 1][j]
                    - self.prefix[i][j]
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.prefix[row2 + 1][col2 + 1]
            - self.prefix[row1][col2 + 1]
            - self.prefix[row2 + 1][col1]
            + self.prefix[row1][col1]
        )


# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (no preprocessing)
# ================================================================================
"""
### Thought Process 🧠
Skip preprocessing entirely — just store the raw matrix, and for every
`sumRegion` call, sum the requested rectangle directly with nested loops.

### Idea
`__init__` does O(1) work (just stores a reference). `sumRegion` walks
every cell in [row1..row2] x [col1..col2] and adds it up.

### Complexity
- TC:
  - `__init__`: O(1)
  - `sumRegion`: O((row2-row1) * (col2-col1)) — worst case O(rows*cols)
    per query if the region spans the whole matrix
- SC: O(1) extra (just stores the matrix reference)

### Pros
- Zero preprocessing cost — great if `sumRegion` is called rarely or never.
- Trivially simple, easy to get right immediately.

### Cons
- Falls apart under "many queries" — if `sumRegion` is called Q times on
  large regions, total cost is O(Q * rows * cols), which is exactly the
  scenario 2D prefix sums are designed to avoid.

### Bottleneck
Every query re-walks its rectangle from scratch, even though the SAME
underlying matrix never changes between calls — there's no reuse of work
across queries at all. Ask: "since the matrix never changes, can I do
some one-time preprocessing that makes each query cheap regardless of how
many times it's asked?" -> Yes: 2D prefix sums (main approach above).
"""


class NumMatrixBrute:
    def __init__(self, matrix: list[list[int]]):
        self.matrix = matrix

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        total = 0
        for r in range(row1, row2 + 1):
            for c in range(col1, col2 + 1):
                total += self.matrix[r][c]
        return total


# ================================================================================
# ALTERNATIVE APPROACH — Row-wise 1D Prefix Sums (partial optimization)
# ================================================================================
"""
### Thought Process 🧠
A middle-ground between brute force and full 2D prefix sums: precompute a
1D prefix sum for EACH ROW independently, so a query can sum each row's
slice in O(1), but still has to loop over the rows in the query range.

### Idea
`row_prefix[i][j]` = sum of `matrix[i][0..j-1]` (a 1D prefix sum per row).
For `sumRegion(r1,c1,r2,c2)`, loop `r` from r1 to r2 and add
`row_prefix[r][c2+1] - row_prefix[r][c1]` (an O(1) row-slice sum) each time.

### Complexity
- TC:
  - `__init__`: O(rows * cols) — build one 1D prefix sum per row
  - `sumRegion`: O(row2 - row1) — one O(1) lookup per row in range,
    instead of O((row2-row1) * (col2-col1)) for brute force
- SC: O(rows * cols) — same space as full prefix sums

### Pros
- Strictly better than brute force for wide queries (many columns, few
  rows) — column-summing is now O(1) per row instead of per cell.
- A natural stepping stone: shows the reasoning that leads to full 2D
  prefix sums, if you're deriving the solution live in an interview.

### Cons
- Still O(row2 - row1) per query in the worst case (a region spanning
  many rows), unlike full 2D prefix sums' true O(1) — this is only a
  partial fix, not the optimal one.

### DSA Buddy Point 🧠
"1D prefix sums collapse a row's range-sum to O(1). Doing that PER ROW
still leaves you iterating over rows per query — the full 2D prefix sum
takes the same collapsing idea and applies it along BOTH axes at once,
getting you all the way to O(1) per query."
"""


class NumMatrixRowPrefix:
    def __init__(self, matrix: list[list[int]]):
        rows, cols = len(matrix), len(matrix[0])
        self.row_prefix = [[0] * (cols + 1) for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                self.row_prefix[i][j + 1] = self.row_prefix[i][j] + matrix[i][j]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        total = 0
        for r in range(row1, row2 + 1):
            total += self.row_prefix[r][col2 + 1] - self.row_prefix[r][col1]
        return total


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
RANGE SUM QUERY 2D - IMMUTABLE
│
├── Brute Force
│   └── No preprocessing; sum the rectangle directly per query
│       └── init: O(1), query: O(rows*cols) worst case
│
├── Bottleneck
│   └── Matrix NEVER changes between queries, but every query redoes
│       full work from scratch — zero reuse across calls
│
├── Partial Fix — Row-wise 1D Prefix Sums
│   └── Precompute per-row prefix sums -> O(1) per row slice
│       └── init: O(rows*cols), query: O(row2-row1)  [still loops rows]
│
└── Full Fix — 2D Prefix Sum
    ├── Build prefix[i+1][j+1] once in __init__ (inclusion-exclusion build)
    └── sumRegion = 4-lookup inclusion-exclusion formula
        └── init: O(rows*cols), query: O(1)  <-- optimal, your code
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'Immutable data structure + many queries' -> pay preprocessing cost
  ONCE upfront (constructor), make each query as cheap as possible."
- "2D prefix sum = 1D prefix sum applied along both axes — the
  inclusion-exclusion correction (+ prefix[r1][c1]) exists because
  subtracting the top strip AND the left strip double-removes their
  shared top-left corner."
- "Row-wise 1D prefix sums are a natural, valid stepping stone toward the
  full 2D version — useful to mention if deriving the solution out loud."
- "This exact technique breaks the moment `update()` re-enters the
  picture — an immutable-only optimization."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                  | init TC       | query TC        | SC             | Pros                                   | Cons                                    | When to Use                          |
|------------------------------|-----------------|--------------------|----------------|---------------------------------------------|----------------------------------------------|-------------------------------------------|
| Brute Force                   | O(1)            | O(rows*cols)        | O(1)           | Zero setup cost                              | Terrible under many/large queries             | sumRegion called rarely, or never          |
| Row-wise 1D Prefix Sums       | O(rows*cols)    | O(row2-row1)        | O(rows*cols)   | Better than brute for wide, short queries    | Still scales with row-range per query          | Stepping-stone / partial optimization      |
| 2D Prefix Sum                 | O(rows*cols)    | O(1)                | O(rows*cols)   | True O(1) per query, regardless of region size | None significant for the immutable case       | Default optimal choice (your code)         |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: 2D Prefix Sum / Inclusion-Exclusion, amortized across a
  constructor + many queries (same family as "Matrix Block Sum," but
  framed as a reusable class instead of a one-shot function).
- Go-to answer: "Since the matrix is immutable, precompute a 2D prefix
  sum once in the constructor — O(rows*cols). Every sumRegion call then
  becomes a 4-term inclusion-exclusion lookup in O(1), independent of the
  query count or region size."
- If asked to think out loud, brute force -> row-wise prefix sums -> full
  2D prefix sums is a clean narrative showing the "collapse a range to
  O(1) via prefix sums" idea being extended from 1 axis to 2.
- Common follow-up: "What if update(row, col, val) were added?" -> That's
  LC 308 (mutable version) — plain prefix sums can't support O(1) updates
  efficiently (an update would require recomputing a huge chunk of the
  prefix matrix), so you'd switch to a 2D Binary Indexed Tree (Fenwick
  Tree) or 2D segment tree, both offering O(log rows * log cols) update
  and query.
"""