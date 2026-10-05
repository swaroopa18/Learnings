"""
================================================================================
 PROBLEM: Largest Rectangle in Histogram (LeetCode 84)
================================================================================
Given an array of integers `heights` representing the bar heights of a
histogram where the WIDTH of every bar is 1, return the AREA of the LARGEST
rectangle that fits entirely inside the histogram.

Example: heights = [2, 1, 5, 6, 2, 3] -> 10  (the bars of height 5 and 6,
         rectangle of height 5 and width 2).
Example: heights = [2, 4]            -> 4

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Must the rectangle be made of CONTIGUOUS bars? (Yes — it spans a run of
  adjacent bars, and its height is limited by the SHORTEST bar in that run.
  That "limited by the shortest" fact is the entire insight of the problem.)
- Can heights be 0? (Yes — a 0-height bar contributes area 0 and acts as a
  hard wall that no rectangle of positive area can cross.)
- Can heights be equal / repeated? (Yes — equal neighbours must be treated
  consistently (either both extend over each other or are handled by the
  last one); this decides `>=` vs `>` in the comparisons.)
- How large can `n` be? (Up to 10^5 -> an O(n^2) solution is ~10^10 steps in
  the worst case and will TLE; the intended solution is O(n).)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "LARGEST RECTANGLE / NEAREST SMALLER" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Treat EVERY bar as the SHORTEST bar of the best rectangle.        │
    │   That rectangle extends left and right until it hits a STRICTLY    │
    │   SMALLER bar:                                                      │
    │       area(i) = heights[i] * (right_smaller(i) - left_smaller(i) - 1)│
    │   => "previous smaller" + "next smaller" element = MONOTONIC STACK  │
    │   (increasing heights). Answer = max over all bars.                 │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the CAPSTONE of the monotonic-stack family (Daily Temperatures, Next
Greater Element, Stock Span): same stack, but now you need BOTH boundaries of
each element and you turn them into an area. Key ideas:

1. **Fix the height, maximize the width.** For a candidate rectangle with
   height `heights[i]`, the widest it can be is the maximal run of bars around
   `i` that are all `>= heights[i]`. So the best rectangle containing bar `i`
   as its limiting bar has an exactly computable width.

2. **Boundaries = nearest strictly smaller bar on each side.** `left[i]` =
   index of the previous bar with height `< heights[i]` (or -1), `right[i]` =
   index of the next bar with height `< heights[i]` (or n).
   `width = right[i] - left[i] - 1`.

3. **A monotonic INCREASING stack finds those boundaries in O(n).** When a bar
   shorter than the stack top arrives, it is the top's RIGHT boundary; the
   element just below the top on the stack is its LEFT boundary. So each bar
   gets both boundaries at the moment it is popped.

4. **Sentinel trick:** process one extra "bar" of height 0 at index `n` to
   flush every remaining stack entry, so you don't need a second cleanup loop.

5. **Equal heights:** popping on strict `>` leaves equal bars on the stack; an
   earlier equal bar gets a too-small width, but the LAST equal bar computes
   the full width, so the maximum is still correct. (The two-pass version
   below uses `>` too and defaults unresolved boundaries to the array ends.)

6. **Why O(n^2) expand-around-each-bar is the natural first answer:** it is
   the same formula with the boundaries found by walking; the stack just
   finds them without re-walking.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Pick every pair of bars `(i, j)` as the left and right ends, take the SHORTEST
bar between them as the height, multiply by the width `j - i + 1`, and keep
the maximum. O(n^2) with a running minimum. Works, but far too slow for 10^5.

### A smarter first step: fix the limiting bar
Instead of choosing ends, choose the SHORTEST bar `i` of the rectangle. Then
the rectangle grows left while bars are `>= heights[i]` and right while bars
are `>= heights[i]`. Compute `heights[i] * width`. Max over `i`. Same O(n^2)
worst case (a long flat or increasing histogram), but the idea is exactly
what the O(n) solution optimizes.

### The key insight: nearest-smaller boundaries via a monotonic stack
"Walk left/right until a smaller bar" = "previous/next smaller element". A
monotonic increasing stack of indices answers it for ALL bars in one pass:
- when a smaller bar arrives, it is the RIGHT boundary of everything taller
  that is on top of the stack;
- the bar left on the stack right below a popped bar is its LEFT boundary.

### Step-by-step trace (single pass + sentinel): heights = [2, 1, 5, 6, 2, 3]
Stack holds indices; `cur` is the height of the incoming bar (0 at i = 6).
```
i=0 cur=2: stack empty                         -> push 0     stack=[0]
i=1 cur=1: top h=2 > 1 -> pop 0
           left = -1 (empty) -> width = 1-(-1)-1 = 1, area = 2*1 = 2
           push 1                                          stack=[1]
i=2 cur=5: top h=1 > 5? no                     -> push 2     stack=[1,2]
i=3 cur=6: top h=5 > 6? no                     -> push 3     stack=[1,2,3]
i=4 cur=2: top h=6 > 2 -> pop 3
           left = 2 -> width = 4-2-1 = 1, area = 6*1 = 6
           top h=5 > 2 -> pop 2
           left = 1 -> width = 4-1-1 = 2, area = 5*2 = 10   <- best so far
           top h=1 > 2? no                     -> push 4     stack=[1,4]
i=5 cur=3: top h=2 > 3? no                     -> push 5     stack=[1,4,5]
i=6 cur=0 (sentinel): top h=3 > 0 -> pop 5
           left = 4 -> width = 6-4-1 = 1, area = 3
           top h=2 > 0 -> pop 4
           left = 1 -> width = 6-1-1 = 4, area = 8
           top h=1 > 0 -> pop 1
           left = -1 -> width = 6-(-1)-1 = 6, area = 6
max area = 10 ✅
```

### The "aha" moment to remember 🎯
"Every bar is the limiting bar of some rectangle. Its widest rectangle is
bounded by the nearest strictly smaller bar on each side. A monotonic
increasing stack gives both boundaries for every bar in one pass — add a
height-0 sentinel at the end to flush the stack."
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (all pairs with a running minimum)
# ================================================================================
"""
### Thought Process 🧠
For every left end `i`, extend the right end `j` from `i` to `n - 1`,
maintaining `min_h = min(heights[i..j])`. The candidate area is
`min_h * (j - i + 1)`. Track the maximum.

### Complexity
- TC: O(n^2) — two nested loops; the running minimum makes each step O(1)
  (without it, recomputing the min makes it O(n^3))
- SC: O(1) extra

### Pros
- Obviously correct, almost impossible to get wrong.
- Perfect oracle for validating the optimized solutions.

### Cons
- n up to 10^5 -> ~5*10^9 steps; guaranteed TLE.
- Examines every pair of ends even though most pairs can never be optimal.

### Bottleneck
Enumerates `(left, right)` pairs, but the best rectangle is determined by its
SHORTEST bar alone. Ask: "can I enumerate only n candidates (one per bar as
the limiting bar) and find their widths fast?" -> Yes (next approaches).
"""


def largest_rectangle_brute(heights: list[int]) -> int:
    n = len(heights)
    best = 0
    for i in range(n):
        min_h = heights[i]
        for j in range(i, n):
            min_h = min(min_h, heights[j])
            best = max(best, min_h * (j - i + 1))
    return best


# ================================================================================
# MY APPROACH 1 — Expand Left/Right Around Each Bar (O(n^2), O(1) space)
# ================================================================================
"""
### Idea
Treat each bar `h` as the limiting (shortest) bar. Walk `l` left while
`heights[l] >= height` and `r` right while `heights[r] >= height`. The width
is `r - l - 1` (both pointers stop ON the first shorter bar or out of range).
Area = `width * height`; keep the maximum.

### Complexity
- TC: O(n^2) worst case — e.g. an all-equal or monotone histogram makes every
  bar walk across (almost) the whole array; O(n) for typical "spiky" data
- SC: O(1) extra

### Pros
- Directly encodes the key insight (limiting bar + nearest smaller bar on
  each side); excellent stepping stone to the stack solution.
- No extra memory; very short and readable.
- Using `>=` while walking correctly extends over EQUAL bars, so a run of
  equal heights is measured in full.

### Cons
- Quadratic worst case -> TLE at n = 10^5 (flat input like [5, 5, 5, ..., 5]).
- Re-walks the same stretches for neighbouring bars instead of reusing
  boundaries already discovered.

### DSA Buddy Point 🧠
"Express the answer per element as `value * span`, where the span is bounded
by the nearest smaller elements — then find those boundaries with a monotonic
stack instead of walking."

### What can be improved?
Correctness-wise your code is fine: `>=` is the right comparison, and
`width = r - l - 1` is exact. To speed it up, REUSE earlier answers while
walking — see the jump-pointer approach below — or compute both boundaries
with a monotonic stack (your second solution), which is O(n).
"""


class SolutionExpandAroundBar:
    def largestRectangleArea(self, heights: list[int]) -> int:
        n = len(heights)
        max_area = 0

        for h, height in enumerate(heights):
            l, r = h - 1, h + 1

            while l >= 0 and heights[l] >= height:
                l -= 1
            while r < n and heights[r] >= height:
                r += 1

            width = r - l - 1
            max_area = max(max_area, width * height)
        return max_area


# ================================================================================
# MY APPROACH 2 — Two Monotonic-Stack Passes (forward/backward boundaries, optimal)
# ================================================================================
"""
### Idea
Compute, for every bar, how far its rectangle can extend:
- Left-to-right pass with a monotonic stack: when a shorter bar `h` arrives, it
  is the right boundary for every taller bar it pops -> set
  `forward[popped] = h - 1` (last index the popped bar's rectangle reaches).
  Bars never popped can reach the end: default `forward = n - 1`.
- Right-to-left pass, mirrored: set `backward[popped] = h + 1` (first index
  reached); default `backward = 0`.
Then `width = forward[i] - backward[i] + 1` and
`area = width * heights[i]`. Take the max.

### Complexity
- TC: O(n) — each index is pushed/popped at most once per pass, plus one final
  linear scan
- SC: O(n) — two boundary arrays and a stack

### Pros
- O(n) and conceptually clean: "compute left boundary array, right boundary
  array, then combine" — each pass is the familiar next-smaller stack.
- Strict `>` pop keeps equal bars in the stack so their rectangles correctly
  extend across equal neighbours (boundaries stop only at STRICTLY shorter
  bars).
- Separating boundary computation from area computation makes it easy to
  debug and to reuse for LC 85 (Maximal Rectangle) or LC 907.

### Cons
- Three passes and 2 extra arrays; more memory/time than the single-pass
  stack with a sentinel.
- Defaults (`n - 1`, `0`) for never-popped entries are easy to forget or
  get off by one.
- Slightly more code than needed — the single-pass version gets both
  boundaries at once.

### DSA Buddy Point 🧠
"Previous-smaller and next-smaller are two separate monotonic-stack passes;
combine them as `right - left - 1`. The single-pass version fuses the two
by reading the LEFT boundary off the stack when popping."

### What can be improved?
Your code is correct (it matches brute force on the test run below). The
only improvement is structural: a single pass with a sentinel computes the
same widths using just one stack and no boundary arrays, so one pass and
O(n) space become one pass and O(n) stack only.
"""


class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        n = len(heights)

        forward = [n - 1] * n
        backward = [0] * n

        stack = []
        for h, height in enumerate(heights):
            while stack and heights[stack[-1]] > height:
                forward[stack.pop()] = h - 1
            stack.append(h)

        stack = []
        for h in range(n - 1, -1, -1):
            while stack and heights[stack[-1]] > heights[h]:
                backward[stack.pop()] = h + 1
            stack.append(h)

        max_area = 0

        for h, height in enumerate(heights):
            width = forward[h] - backward[h] + 1
            max_area = max(max_area, width * height)
        return max_area


# ================================================================================
# ALTERNATIVE APPROACH 2 — Single-Pass Monotonic Stack with Sentinel (canonical)
# ================================================================================
"""
### Thought Process 🧠
Keep a stack of indices with non-decreasing heights. Iterate `i` from 0 to `n`
inclusive, treating `i = n` as a sentinel bar of height 0. While the incoming
height is strictly less than the top's height, pop the top: its HEIGHT is
`heights[popped]`, its RIGHT boundary is `i` (exclusive) and its LEFT boundary
is the new top of the stack (or -1 if empty), so
`width = i - left - 1`. Update the max, then push `i`.

### Complexity
- TC: O(n) — each index pushed once, popped at most once
- SC: O(n) — the stack

### Pros
- THE standard interview solution: one pass, one stack, no boundary arrays.
- The sentinel removes the separate "flush the stack" loop.
- Each popped bar's area is computed at the exact moment its right boundary
  becomes known.

### Cons
- Width formula depends on peeking at the stack AFTER popping (`stack[-1]` or
  -1) — easy to get off by one.
- Hardest to explain from scratch: boundaries are implicit rather than stored.
- Using `>=` instead of `>` changes which equal bar computes the full width
  (both work if applied consistently).

### DSA Buddy Point 🧠
"One pass + sentinel: when you pop, you know the height (popped bar), the
right boundary (current `i`) and the left boundary (new top) — the area is
ready right there."
"""


def largest_rectangle_single_pass(heights: list[int]) -> int:
    n = len(heights)
    stack: list[int] = []
    best = 0
    for i in range(n + 1):
        cur = heights[i] if i < n else 0  # sentinel flushes the stack
        while stack and heights[stack[-1]] > cur:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best


# ================================================================================
# ALTERNATIVE APPROACH 3 — Jump Pointers (reuse boundaries instead of a stack)
# ================================================================================
"""
### Thought Process 🧠
Upgrade the expand-around-each-bar idea by REUSING boundaries. Let
`left[i]` be the leftmost index of the run of bars `>= heights[i]` that ends at
`i`. To compute it, start at `l = i - 1`; while `heights[l] >= heights[i]`, the
whole block `[left[l], l]` is also `>= heights[i]`, so JUMP: `l = left[l] - 1`.
Mirror for `right[i]` from the right. Area = `heights[i] * (right[i] - left[i] +
1)`.

### Complexity
- TC: O(n) amortized — each jump skips an entire already-processed block
- SC: O(n) — `left` and `right` arrays

### Pros
- Same code shape as the O(n^2) expansion, with one line changed — an elegant
  optimization story for interviews.
- No explicit stack.

### Cons
- The amortized-O(n) argument is subtler than the stack's push/pop counting.
- Still needs two arrays and two passes.

### DSA Buddy Point 🧠
"Previously computed boundaries describe whole blocks — jump over them
(`l = left[l] - 1`) instead of stepping one bar at a time. It's the same trick
as `j += ans[j]` in Daily Temperatures and `j -= spans[j]` in Stock Span."
"""


def largest_rectangle_jump(heights: list[int]) -> int:
    n = len(heights)
    left = [0] * n  # leftmost index of the >= run ending at i
    right = [0] * n  # rightmost index of the >= run starting at i

    for i in range(n):
        l = i - 1
        while l >= 0 and heights[l] >= heights[i]:
            l = left[l] - 1
        left[i] = l + 1

    for i in range(n - 1, -1, -1):
        r = i + 1
        while r < n and heights[r] >= heights[i]:
            r = right[r] + 1
        right[i] = r - 1

    return max((heights[i] * (right[i] - left[i] + 1) for i in range(n)), default=0)


# ================================================================================
# ALTERNATIVE APPROACH 4 — Divide and Conquer on the Minimum Bar
# ================================================================================
"""
### Thought Process 🧠
The tallest rectangle in `heights[lo..hi]` is one of three things: (a) the
rectangle using the WHOLE range at the height of the minimum bar
(`min_h * (hi - lo + 1)`), (b) the best rectangle entirely LEFT of the minimum
bar, or (c) the best rectangle entirely RIGHT of it (no rectangle can cross the
minimum bar and be taller than option (a)). Find the minimum, recurse on both
sides.

### Complexity
- TC: O(n log n) on average / balanced splits (with an O(1) range-minimum
  structure such as a segment tree or sparse table it is O(n log n) worst
  case); O(n^2) worst case when using a plain linear scan to find the minimum
  on sorted input (every split peels off one bar)
- SC: O(log n) recursion depth on balanced input; O(n) on sorted input
  (Python's default recursion limit of 1000 would be exceeded for large
  sorted inputs)

### Pros
- A genuinely different paradigm (recursion on the minimum) — a good
  "do you know another way?" answer.
- Easy to prove correct: the global-minimum bar splits the problem cleanly.

### Cons
- Worst case O(n^2) with a naive minimum search, plus recursion-depth risk in
  Python for n = 10^5 sorted input.
- Needs a segment tree / sparse table to make it truly O(n log n).
- More code and more overhead than the stack solution.

### DSA Buddy Point 🧠
"No rectangle can span the minimum bar and beat 'whole range x min height',
so split at the minimum and recurse."
"""


def largest_rectangle_divide_conquer(heights: list[int]) -> int:
    def solve(lo: int, hi: int) -> int:
        if lo > hi:
            return 0
        min_idx = lo
        for k in range(lo, hi + 1):
            if heights[k] < heights[min_idx]:
                min_idx = k
        whole = heights[min_idx] * (hi - lo + 1)
        return max(whole, solve(lo, min_idx - 1), solve(min_idx + 1, hi))

    return solve(0, len(heights) - 1)


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
LARGEST RECTANGLE IN HISTOGRAM
│
├── Brute Force
│   └── Every (i, j) pair with a running minimum -> O(n^2) time, O(1) space
│
├── Bottleneck
│   └── The rectangle's height is decided by its SHORTEST bar, so only n
│       candidates exist (one per bar); pairs are wasted work
│
├── Key Insight
│   └── For each bar as the limiting bar: width = nearest strictly smaller
│       bar on the right − nearest strictly smaller bar on the left − 1
│       -> previous/next smaller element -> MONOTONIC (increasing) STACK
│
├── My Approach 1 — Expand Around Each Bar
│   └── walk l/r while heights >= height; area = width * height
│       -> O(n^2) time worst case, O(1) space
│
├── My Approach 2 — Two Stack Passes (OPTIMAL)
│   └── forward[i] / backward[i] from next-/previous-smaller stacks
│       width = forward - backward + 1 -> O(n) time, O(n) space
│
├── Single-Pass Stack + Sentinel (canonical optimal)
│   └── pop when cur < top; width = i - new_top - 1; sentinel height 0
│       -> O(n) time, O(n) space, one stack and no boundary arrays
│
├── Jump Pointers
│   └── l = left[l] - 1 / r = right[r] + 1 reuses boundaries
│       -> O(n) amortized time, O(n) space, no stack
│
└── Divide and Conquer on Minimum
    └── best = max(min*width, solve(left), solve(right))
        -> O(n log n) average / O(n^2) worst, recursion-depth risk
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Every bar can be the LIMITING (shortest) bar of a rectangle. Its widest
  rectangle stretches to the nearest STRICTLY SMALLER bar on each side:
  width = right_smaller - left_smaller - 1."
- "Previous-smaller + next-smaller = monotonic increasing stack. This is the
  capstone of the Daily Temperatures / Next Greater / Stock Span stack
  family — same stack, two boundaries, area at the end."
- "Single-pass trick: when you POP a bar, its right boundary is the current
  index and its left boundary is the NEW stack top (or -1) — the area is
  computable right there."
- "Append a sentinel bar of height 0 to flush all remaining bars; no
  separate cleanup loop."
- "Equal heights: with `>` pop, the LAST equal bar computes the full width;
  with the expansion approach use `>=` so equal neighbours are included."
- "O(n^2) expand-around-each-bar is the natural first answer; reusing the
  boundaries (stack or jump pointers) is what makes it O(n)."
- "Width bug alert: `width = i - left - 1` where `left` is the stack top AFTER
  popping, NOT the popped index."
- "The same stack powers LC 85 (Maximal Rectangle: run this on each row's
  histogram), LC 907 (Sum of Subarray Minimums), LC 42 (Trapping Rain
  Water)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                      | Core Idea                                                  | TC               | SC     | Pros                                              | Cons                                                    | When to Use                              |
|-------------------------------|------------------------------------------------------------|------------------|--------|---------------------------------------------------|---------------------------------------------------------|------------------------------------------|
| Brute Force (all pairs)       | min of range * width for every (i, j)                      | O(n^2)           | O(1)   | Trivially correct, great oracle                   | TLE at n = 10^5                                         | Baseline / correctness check             |
| Expand Around Each Bar        | Walk l/r while >= height; area = width * height            | O(n^2) worst     | O(1)   | Encodes the key insight, tiny code                | Quadratic on flat/monotone data                         | First idea (your first code)             |
| Two Stack Passes              | forward/backward boundary arrays from two stack passes     | O(n)             | O(n)   | Clean, optimal, easy to debug each pass           | Three passes + two arrays, default-value pitfalls       | Optimal & explicit (your second code)    |
| Single-Pass Stack + Sentinel  | Pop on shorter bar; width = i - new_top - 1                | O(n)             | O(n)   | Canonical interview answer, one stack, one pass   | Implicit boundaries, off-by-one prone                   | Best answer to write in an interview     |
| Jump Pointers                 | Reuse left/right arrays to skip blocks                     | O(n) amortized   | O(n)   | Direct upgrade of the expansion idea, no stack    | Subtler amortized proof, two arrays                     | Follow-up: "optimize the expansion?"     |
| Divide & Conquer on Minimum   | Split at the minimum bar and recurse                       | O(n log n) avg   | O(log n)| Different paradigm, simple correctness proof     | O(n^2) worst & deep recursion without an RMQ structure  | "Another way?" discussion                |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Monotonic Stack — previous/next SMALLER element, converted into a
  max-area. Cousins: LC 739 (Daily Temperatures), LC 503/496 (Next Greater
  Element), LC 901 (Online Stock Span), LC 85 (Maximal Rectangle), LC 907
  (Sum of Subarray Minimums), LC 42 (Trapping Rain Water).
- Go-to answer: "Every bar is the limiting bar of some rectangle, whose width
  extends to the nearest strictly smaller bar on each side. Use a monotonic
  increasing stack: when a shorter bar arrives, pop taller bars — each popped
  bar's height is known, its right boundary is the current index, and its left
  boundary is the new stack top. Add a sentinel height 0 at the end to flush
  the stack. O(n) time, O(n) space."
- Good to call out: why only n candidates exist (one per limiting bar), why
  the width formula is `i - new_top - 1`, the sentinel, and how equal
  heights are handled.
- Common follow-ups:
  * "Largest rectangle of 1s in a binary matrix?" -> LC 85: build a histogram
    per row (heights[j] += 1 or reset to 0) and run this algorithm on each
    row -> O(rows * cols).
  * "Can you avoid the stack?" -> Jump-pointer boundaries (`l = left[l] - 1`).
  * "Make it work if bar widths differ?" -> Same stack; width becomes a
    difference of prefix sums of widths instead of index difference.
  * "Largest SQUARE in the histogram?" -> For each bar candidate, the best
    square side is `min(height, width)` using the same boundaries.
"""
