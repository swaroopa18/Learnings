"""
================================================================================
 PROBLEM: Search a 2D Matrix (LeetCode 74)
================================================================================
Given: an m x n `matrix` with two properties — (1) each ROW is sorted in
ascending order left-to-right, and (2) the first integer of each row is
GREATER than the last integer of the PREVIOUS row (so the whole matrix,
read row by row, is one single ascending sequence). Given a `target`,
return True if it exists anywhere in the matrix, else False.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is EVERY row sorted AND does the matrix behave like one big sorted
  1-D array when flattened (first-of-row > last-of-previous-row)? (Yes —
  this is the detail that separates LC 74 from LC 240 "Search a 2D
  Matrix II," where only rows+columns are sorted independently and rows
  don't chain together — that variant needs a totally different
  staircase-search approach, not binary search)
- Can the matrix be empty, or contain empty rows? (Should guard for this
  — `len(matrix) == 0` or `len(matrix[0]) == 0` -> return False)
- Are there duplicate values? (Doesn't matter for existence-check binary
  search — just find any match)
- What are the value ranges / do I need to worry about overflow? (Not in
  Python, but worth mentioning in a language where fixed-width ints are
  a concern — use `l + (r - l) // 2` for the midpoint)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "MATRIX AS A DISGUISED 1-D SORTED ARRAY"  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Whenever a 2-D structure is secretly just a 1-D SORTED sequence  │
    │   wrapped onto multiple rows, don't binary search it TWICE —       │
    │   binary search it ONCE by mapping a single flat index `mid` to    │
    │   `(mid // n, mid % n)`. One search beats two nested searches.     │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is a DIFFERENT shape of problem than the Koko/Ship/MinSpeed/Bouquets
family (those binary-search an abstract ANSWER SPACE via a monotonic cost
function). Here, binary search is applied directly to an array-like
structure to find a value — the classic "vanilla" binary search, just
with one extra layer of indexing math because the array is drawn as a
grid. Key ideas:

1. **The matrix is really one sorted array wearing a grid costume.**
   Because row i+1's first element > row i's last element, reading the
   matrix left-to-right, top-to-bottom produces a single non-decreasing
   sequence of length `m * n`. Any algorithm that works on a sorted 1-D
   array — binary search, in particular — works here once you translate
   a flat index back into `(row, col)`.

2. **Flat-index <-> (row, col) conversion is the whole trick.**
   For an n-column matrix: `row = idx // n`, `col = idx % n`. This is
   the ONE piece of new machinery vanilla binary search needs to handle
   the grid shape — everything else is identical to searching a plain
   list.

3. **Two-stage binary search (search rows, then search the found row)
   also works and is asymptotically the same, O(log m + log n) ==
   O(log(m*n))**, but does two separate binary searches with two sets of
   pointers instead of one — more code, more edge cases (what if the
   target's row is never "found" as containing it because of a boundary
   check?), no efficiency gain.

4. **Per-row binary search (search every row) is asymptotically worse**
   — O(m log n) instead of O(log(m*n)) — because it doesn't exploit the
   fact that rows are chained together in sorted order; it treats each
   row as an independent sorted array and searches all of them.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Scan every cell, one at a time, checking if it equals `target`. Works,
but ignores all the sorted structure the problem hands you for free.

### The key insight: "chained rows" == one long sorted line
Picture the matrix rows laid end-to-end instead of stacked:
`matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]`
becomes the flat array:
`[1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60]`
This is possible ONLY because `matrix[i+1][0] > matrix[i][-1]` for every
row — that guarantee is what "stitches" the rows into one ascending run.
Once you see this, "find target in the matrix" IS "find target in a
sorted array" — just apply standard binary search to the flat version.

### Why `row = idx // n`, `col = idx % n`?
If each row has `n` columns, then flat index `idx` skips over
`idx // n` COMPLETE rows to get to the right row, and lands `idx % n`
positions into that row. E.g. with n=4, flat idx=5 -> row = 5//4 = 1,
col = 5%4 = 1 -> `matrix[1][1]` = 11, which matches position 5 (0-
indexed) in the flattened array `[1,3,5,7,10,11,...]`. ✅

### Step-by-step trace: search([[1,3,5,7],[10,11,16,20],[23,30,34,60]], target=16)
```
m=3, n=4 -> flat length = 12
l=0, r=11

mid=5  -> row=5//4=1, col=5%4=1 -> matrix[1][1]=11 -> 11 < 16 -> l=6
mid=8  -> row=8//4=2, col=8%4=0 -> matrix[2][0]=23 -> 23 > 16 -> r=7
mid=6  -> row=6//4=1, col=6%4=2 -> matrix[1][2]=16 -> MATCH -> True ✅
```

### The "aha" moment to remember 🎯
Don't reach for a two-layer search (row search, then column search) out
of habit just because the input LOOKS 2-D. First ask: "does this grid's
sortedness actually chain across rows into one flat sorted sequence?" If
yes (as here), a SINGLE binary search over the flat index space is both
simpler and doesn't lose anything — the two-stage version isn't wrong,
just redundant machinery for a problem that's secretly 1-D.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (scan every cell)
# ================================================================================
"""
### Thought Process 🧠
Nested loop over every row and column, check for equality, return True
on first match, False if the loops finish without finding it.

### Complexity
- TC: O(m * n) — visits every cell in the worst case (target absent, or
  in the last cell)
- SC: O(1)

### Pros
- Trivial to write, no assumptions about structure needed — works even
  if the sortedness guarantees didn't hold.

### Cons
- Completely ignores the sorted structure the problem guarantees,
  wasting the opportunity for a logarithmic algorithm.

### Bottleneck
Treats the matrix as unordered data. Ask: "is there ANY structure here
that lets me eliminate large chunks of the search space at once?" ->
Yes: full row + chained-row sortedness -> binary search (approaches
below).
"""


class SolutionBruteForce:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == target:
                    return True
        return False


# ================================================================================
# MY APPROACH #1 — Binary Search Every Row
# ================================================================================
"""
### Idea
For each row, run a standard binary search across its columns. Return
True the moment any row's search finds `target`; False if every row's
search comes up empty.

### Complexity
- TC: O(m log n) — one O(log n) binary search per row, m rows total
- SC: O(1)

### Pros
- Correct, and a clear step up from brute force — exploits per-row
  sortedness immediately.
- Simple to reason about: each row is an independent, ordinary binary
  search problem.

### Cons
- Doesn't exploit the CROSS-row sortedness guarantee at all (that row
  i+1 starts higher than row i ends) — it treats the rows as if they
  were unrelated sorted arrays, so it still pays the full `m` factor
  instead of collapsing rows and columns into one `log(m*n)` search.
- Wasteful when `target` is smaller/larger than most rows' ranges —
  still runs a full binary search on rows that can't possibly contain
  it.

### DSA Buddy Point 🧠
"Whenever you find yourself running the SAME sub-search m times in a
loop, and the loop variable itself is sorted, ask whether that outer
loop can become a binary search too — collapsing O(m log n) into
O(log m + log n), or even O(log(m*n)) with the right indexing trick."

### What can be improved?
Binary search the ROWS first to narrow down to the one row that could
possibly contain `target` (using each row's first/last values), THEN
binary search just that row — see Approach #2.
"""


class SolutionRowBinarySearch:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        for i in range(len(matrix)):
            l, r = 0, len(matrix[0]) - 1

            while l <= r:
                mid = (l + r) // 2

                if matrix[i][mid] == target:
                    return True
                elif matrix[i][mid] < target:
                    l = mid + 1
                else:
                    r = mid - 1

        return False


# ================================================================================
# MY APPROACH #2 — Two-Stage Binary Search (rows, then columns)
# ================================================================================
"""
### Idea
First binary search over ROW INDICES to find the (unique) row whose
value range `[matrix[mid1][0], matrix[mid1][-1]]` could contain
`target`. Once that row is found, run a second, ordinary binary search
across ITS columns.

### Complexity
- TC: O(log m + log n) == O(log(m*n)) — asymptotically identical to the
  single flat-index search (Approach #3 below), since
  log m + log n = log(m*n)
- SC: O(1)

### Pros
- Exploits BOTH sortedness guarantees (within-row and cross-row) — a
  real improvement over Approach #1.
- Conceptually easy to explain in two clean stages: "find the row,
  then find the column."

### Cons
- Two separate binary search loops with two separate pointer pairs —
  more code and more edge cases to get right (e.g. the row-search
  boundary condition `matrix[mid1][0] <= target <= matrix[mid1][-1]`
  has to be exactly right, or you can skip past the correct row).
- No asymptotic benefit over the single flat-index binary search below
  — it's strictly more code for the same Big-O.

### DSA Buddy Point 🧠
"Two nested binary searches over a structure that's secretly ONE sorted
sequence usually means you can collapse them into a single binary
search with an index-mapping trick — same complexity class, less code,
fewer places to introduce an off-by-one bug."

### What can be improved?
Collapse both stages into a SINGLE binary search over the flat index
space `[0, m*n)`, converting each candidate flat index to `(row, col)`
on the fly — see Approach #3, the cleanest version.
"""


class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        l1, r1 = 0, len(matrix) - 1

        while l1 <= r1:
            mid1 = (l1 + r1) // 2

            if matrix[mid1][0] <= target <= matrix[mid1][len(matrix[mid1]) - 1]:
                l, r = 0, len(matrix[mid1]) - 1

                while l <= r:
                    mid = (l + r) // 2

                    if matrix[mid1][mid] == target:
                        return True
                    elif matrix[mid1][mid] < target:
                        l = mid + 1
                    else:
                        r = mid - 1

                return False

            elif matrix[mid1][0] > target:
                r1 = mid1 - 1
            else:
                l1 = mid1 + 1

        return False


# ================================================================================
# BETTER APPROACH — Single Binary Search over the Flattened Index (cleanest, optimal)
# ================================================================================
"""
### Idea
Treat the matrix as one flat sorted array of length `m * n` without
actually flattening it in memory. Binary search flat indices
`[0, m*n - 1]`; for each candidate `mid`, convert to `(mid // n,
mid % n)` to read the real cell. Standard binary search from there.

### Complexity
- TC: O(log(m * n)) — a single binary search over the full flat space;
  same complexity class as Approach #2 but with one loop instead of two
- SC: O(1) — no actual flattening, just index math

### Pros
- Simplest possible code: ONE binary search loop, no special-casing for
  "find the row" vs. "find the column."
- Fewest edge cases / off-by-one opportunities — there's only one
  boundary condition to get right (`l <= r` on the flat range), not two.
- Directly reflects the real insight of the problem: this matrix *is* a
  sorted array, just displayed with line breaks.

### Cons
- Slightly less intuitive at first glance than "search rows, then
  columns" if you haven't seen the flat-index trick before — the
  `idx // n`, `idx % n` conversion needs a beat of explanation.

### DSA Buddy Point 🧠
"When a 2-D grid's sortedness guarantee lets you describe it as ONE
sorted sequence, prefer flattening the INDEX MATH over flattening the
DATA (which would cost O(m*n) space) or running nested searches (which
costs nothing extra in Big-O here, but does cost code complexity)."

### What can be improved?
Nothing significant — this is the accepted optimal solution:
O(log(m*n)) time, O(1) space, single loop, minimal edge cases.
"""


class SolutionOptimal:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        m, n = len(matrix), len(matrix[0])
        l, r = 0, m * n - 1

        while l <= r:
            mid = (l + r) // 2
            val = matrix[mid // n][mid % n]

            if val == target:
                return True
            elif val < target:
                l = mid + 1
            else:
                r = mid - 1

        return False


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
SEARCH A 2D MATRIX (LC 74)
│
├── Brute Force
│   └── Scan every cell -> O(m*n)
│
├── Bottleneck
│   └── Ignores BOTH sortedness guarantees (per-row AND cross-row)
│
├── Key Insight
│   └── first-of-row > last-of-previous-row -> whole matrix flattens
│       into ONE sorted 1-D sequence of length m*n
│
├── Approach A — Binary Search Every Row
│   └── Exploits per-row sortedness only -> O(m log n)
│       (misses the cross-row chaining entirely)
│
├── Approach B — Two-Stage Binary Search (rows, then columns)
│   └── Exploits BOTH guarantees, but as two separate searches
│       -> O(log m + log n) == O(log(m*n)), more code/edge cases
│
└── Approach C — Single Flat-Index Binary Search (BEST)
    └── Treats matrix as one sorted array via idx -> (idx//n, idx%n)
        -> O(log(m*n)) time, O(1) space, one loop, cleanest
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Before reaching for a two-layer search on a grid, ask: does this
  grid's sortedness actually CHAIN across rows into one flat sorted
  sequence? If yes, a single binary search over a flat index beats two
  nested searches — same Big-O, less code, fewer edge cases."
- "The conversion `row = idx // n`, `col = idx % n` is the one new piece
  of machinery needed to apply vanilla binary search to a grid that's
  secretly 1-D — memorize this pattern, it recurs any time a problem
  gives you a grid with a global (not just per-row/per-column) ordering
  guarantee."
- "This is a DIFFERENT flavor of binary search than the Koko/Ship/
  MinSpeed/Bouquets family: those binary-search an abstract ANSWER SPACE
  via a monotonic cost function; this one binary-searches an actual
  VALUE within a sorted data structure — the 'classic' use case."
- "Don't confuse this with LC 240 'Search a 2D Matrix II,' where rows
  and columns are each sorted independently but do NOT chain into one
  global sorted order — that variant needs a staircase search (start
  top-right or bottom-left), NOT this flattening trick."
- "log m + log n == log(m*n) — algebraically identical complexity class
  whether you do two searches or one; the win from flattening is code
  simplicity and fewer boundary conditions, not a Big-O improvement."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                          | Core Idea                                                        | TC                  | SC   | Pros                                              | Cons                                                    | When to Use                          |
|------------------------------------|-------------------------------------------------------------------|---------------------|------|----------------------------------------------------|------------------------------------------------------------|---------------------------------------|
| Brute Force                        | Scan every cell                                                    | O(m*n)              | O(1) | Trivial, no structure assumptions needed             | Ignores all sortedness -> far too slow for large inputs      | Baseline / correctness check only     |
| Binary Search Every Row            | Standard binary search within each row, loop over rows              | O(m log n)          | O(1) | Simple, exploits per-row sortedness                  | Ignores cross-row chaining -> pays full `m` factor            | Only if cross-row order isn't guaranteed |
| Two-Stage Binary Search             | Binary search rows to find candidate row, then binary search it     | O(log m + log n)    | O(1) | Exploits both guarantees                              | Two loops/pointer pairs -> more code, more edge cases          | Fine, but not the cleanest version    |
| Single Flat-Index Binary Search     | Binary search flat index [0, m*n), convert to (row, col) on the fly | O(log(m*n))         | O(1) | Cleanest, one loop, fewest edge cases, no extra space | Needs a beat to explain the idx//n, idx%n trick                | Default optimal choice                |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Classic Binary Search on a Sorted Structure (NOT the "binary
  search on the answer" pattern used by Koko/Ship/MinSpeed/Bouquets —
  here you're searching for an actual value inside sorted data, not
  probing a monotonic cost function over a candidate answer space).
- Go-to answer: "Because the matrix's rows chain together in sorted
  order (first element of each row exceeds the last element of the
  previous row), the whole matrix is really one sorted 1-D array in
  disguise. Binary search a flat index from 0 to m*n-1, converting each
  candidate index to (idx // n, idx % n) to read the actual cell —
  O(log(m*n)) time, O(1) space, single loop."
- Good to explicitly contrast this with LC 240 "Search a 2D Matrix II"
  if discussing matrix-search problems together — that variant looks
  similar but needs a totally different (staircase) approach since rows
  and columns are independently sorted without a global chain.
- Common follow-up: "What if only rows AND columns were sorted, without
  the global chaining guarantee (LC 240)?" -> The flattening trick
  breaks down entirely; instead, start at the top-right (or bottom-left)
  corner and move left when the current value is too big, down when it's
  too small — O(m + n) time, O(1) space.
"""