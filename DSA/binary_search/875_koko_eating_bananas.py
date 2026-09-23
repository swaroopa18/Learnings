"""
================================================================================
 PROBLEM: Koko Eating Bananas (LeetCode 875)
================================================================================
Given: `piles` (an array of banana pile sizes) and `h` (hours available).
Koko eats at a constant integer speed `k` bananas/hour. Each hour she
picks one pile and eats up to `k` bananas from it — if the pile has fewer
than `k` bananas left, she eats them all and does NOT continue to another
pile that same hour (any "spare capacity" left in the hour is wasted).
Task: return the MINIMUM integer speed `k` such that she can eat all
piles within `h` hours.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is `h` guaranteed >= len(piles)? (Yes — otherwise it would be
  impossible to even visit every pile once, one pile per hour minimum)
- Must speed be a positive integer? (Yes — k >= 1)
- If a pile is exactly divisible by k, does she finish that pile in
  exactly pile/k hours with no leftover hour wasted? (Yes)
- What if she finishes a pile with time "left over" in that hour — can
  she start another pile? (No — each hour is dedicated to at most one
  pile; this is what makes it a per-pile CEILING division problem, not a
  continuous-rate problem)
"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "BINARY SEARCH ON THE ANSWER" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   "Minimum speed/capacity/value such that a COST function stays    │
    │   under a budget" -> binary search the ANSWER SPACE, not an array. │
    │   Higher speed -> fewer hours needed (monotonic) -> binary search. │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

Memorize these as REFLEXES for this very common problem family (Koko
Eating Bananas, Capacity To Ship Packages, Split Array Largest Sum, etc.):

1. **Identify the monotonic relationship.** As speed `k` increases, hours
   needed to finish DECREASES (or stays the same) — never increases. This
   monotonicity is what makes binary search valid here, exactly like
   "mid*mid <= x" was monotonic in mySqrt.

2. **The search space is [1, max(piles)].** Speed 1 is the slowest
   possible (guaranteed valid answer if h is large enough); speed
   max(piles) means finishing the single biggest pile in exactly 1 hour —
   no speed faster than that is ever NEEDED, since one pile can only take
   1 hour minimum regardless of how high k goes beyond its size.

3. **Per-pile hours = CEILING division: `(pile + k - 1) // k`,** NOT
   floor division. A pile of 7 bananas at speed 3 takes 3 hours (3+3+1),
   not 2 — she can't "roll over" leftover time into another pile mid-hour.
   Manually branching on `pile % k == 0` is equivalent but unnecessary;
   the ceiling-division formula folds that check away for free.

4. **calculate(mid) <= h -> this speed WORKS -> try going SLOWER ->
   r = mid** (keep mid, it might be the minimum valid speed).
   **calculate(mid) > h -> this speed is TOO SLOW -> must go FASTER ->
   l = mid + 1.**

5. **Converging pointers (`l < r`)** — same template as findPeakElement,
   findMin, and firstBadVersion. `return l` and `return r` are
   interchangeable at the end, since they converge to the same value.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Just try speed = 1. Compute how many hours that takes. If it's <= h,
great, that's your answer (the slowest possible speed already works). If
not, try speed = 2. Then 3. Then 4. Keep increasing by 1 until the hours
needed finally drops to <= h. That's the brute force approach — simple,
correct, but potentially very slow if the needed speed is large.

### The key insight: speed and hours-needed move in OPPOSITE directions,
    predictably
As Koko eats faster, she obviously needs FEWER (or equal) hours to finish
everything — this relationship never reverses. Faster speed literally
cannot make her need MORE time. This "if X works, everything bigger than
X also works; if X doesn't work, everything smaller than X also doesn't
work" property is EXACTLY the monotonic predicate that binary search
needs — just like mySqrt's `mid*mid <= x`, except now the "predicate
function" is "can she finish in <= h hours at this speed," which
requires actually SIMULATING her eating at that speed to evaluate.

### Why ceiling division for hours-per-pile?
If a pile has 7 bananas and she eats at speed 3: hour 1 she eats 3
(4 left), hour 2 she eats 3 (1 left), hour 3 she eats the last 1 (even
though her "capacity" was 3, only 1 banana was left) — that's 3 hours
total, not 7/3 = 2.33 rounded down to 2. She always needs to "round up"
to a whole extra hour for any leftover, which is exactly what ceiling
division computes: `(7 + 3 - 1) // 3 = 9 // 3 = 3`. ✅

### Step-by-step trace: minEatingSpeed([3,6,7,11], h=8)
```
l=1, r=11 (max pile)

Step 1: mid=6 -> hours needed: ceil(3/6)+ceil(6/6)+ceil(7/6)+ceil(11/6)
                              = 1 + 1 + 2 + 2 = 6
        6 <= 8 (h)? YES -> speed 6 WORKS, try slower -> r = mid = 6

Step 2: l=1, r=6 -> mid=3 -> hours: ceil(3/3)+ceil(6/3)+ceil(7/3)+ceil(11/3)
                                   = 1 + 2 + 3 + 4 = 10
        10 <= 8? NO -> speed 3 too slow, must go faster -> l = mid+1 = 4

Step 3: l=4, r=6 -> mid=5 -> hours: ceil(3/5)+ceil(6/5)+ceil(7/5)+ceil(11/5)
                                   = 1 + 2 + 2 + 3 = 8
        8 <= 8? YES -> speed 5 WORKS, try slower -> r = mid = 5

Step 4: l=4, r=5 -> mid=4 -> hours: ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4)
                                   = 1 + 2 + 2 + 3 = 8
        8 <= 8? YES -> speed 4 WORKS, try slower -> r = mid = 4

Step 5: l=4, r=4 -> l == r, loop ends!

Return 4.  Correct! ✅ (matches LeetCode's known expected answer)
```

### Building strong intuition: "search the SPEED, not the piles"
The array `piles` isn't what you're binary searching OVER — you're
binary searching over the space of POSSIBLE SPEEDS, from 1 to
max(piles). At each candidate speed, you run a full O(n) simulation
(`calculate`) to check "does this speed satisfy the hour budget?" This
two-layer structure — binary search on the OUTSIDE, a full linear check
on the INSIDE — is extremely common in "minimize X such that Y stays
within a budget" problems, and is worth recognizing as its own template.

### The "aha" moment to remember 🎯
Binary search doesn't require the thing you're searching over to be an
array at all — it just needs a MONOTONIC predicate over an ordered range
of candidate answers. Here, that range is [1, max(piles)], and the
predicate ("can she finish in time at this speed") happens to require an
O(n) simulation to evaluate, but that doesn't change the fact that the
OUTER search is still classic O(log(max(piles))) binary search.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (try every speed from 1 upward)
# ================================================================================
"""
### Thought Process 🧠
Try speed 1, check if it works; if not, try 2; if not, try 3; ... keep
incrementing until you find the first speed that satisfies the hour
budget.

### Idea
`speed = 1; while calculate(speed) > h: speed += 1; return speed`

### Complexity
- TC: O(max(piles) * n) — worst case, you try up to max(piles) different
  speeds, and each `calculate` call is O(n) (n = number of piles)
- SC: O(1)

### Pros
- Very intuitive, directly matches "just try increasing speeds."

### Cons
- Can be extremely slow if the answer speed is large and piles are huge
  (pile sizes can be up to 10^9 on LeetCide's constraints) — trying every
  single integer speed one at a time is far too slow in the worst case.

### Bottleneck
Each failed speed attempt throws away almost all the information we
learned — we know that speed didn't work, but linear scanning doesn't
exploit the fact that EVERY smaller speed is now also guaranteed to fail
too (monotonicity). Ask: "since 'does this speed work' is monotonic, can
I eliminate half the remaining candidate speeds with one check?" -> Yes:
binary search over the speed range (the main approach below).
"""


def min_eating_speed_brute(piles: list[int], h: int) -> int:
    def calculate(speed):
        return sum((pile + speed - 1) // speed for pile in piles)

    speed = 1
    while calculate(speed) > h:
        speed += 1
    return speed


# ================================================================================
# MY APPROACH #1 — Binary Search with Manual Remainder Check (+ unneeded special case)
# ================================================================================
"""
### Idea
Binary search over speed in [1, max(piles)]. For each candidate speed,
`calculate` computes total hours needed by manually checking each pile's
remainder: if `pile % speed == 0`, it divides evenly (`pile // speed`
hours); otherwise, add one extra hour for the leftover
(`pile // speed + 1`).

### A closer look: the `if len(piles) == 1` special case ⚠️
This version adds an early return for single-pile inputs, calling
`calculate(h)` directly instead of running the binary search. Tracing
through it: this special case is actually UNNECESSARY — the general
binary search logic already produces the correct answer for single-pile
inputs without it (verified: removing this branch entirely still gives
correct results on single-pile test cases). It's a classic example of a
"just in case" special case added out of uncertainty about whether the
general logic covers an edge case that, in fact, it already does.

### Complexity
- TC: O(n log(max(piles))) — O(log(max(piles))) binary search iterations,
  each doing an O(n) `calculate` pass
- SC: O(1) extra

### Pros
- The manual remainder check is very explicit about WHY ceiling division
  is needed — good for building initial intuition even if the formula
  version (below) is more concise.

### DSA Buddy Point 🧠
"When you're not sure if a special case is needed, it's worth actually
testing the general logic WITHOUT it first — unnecessary special-casing
adds code surface area and cognitive load without adding correctness."

### What can be improved?
The manual `if rem == 0: ... else: ... + 1` branching is exactly what
ceiling division (`(pile + speed - 1) // speed`) computes in a single
expression, with no branching needed — see Approach #2 below. Also, the
`len(piles) == 1` special case can be safely removed.
"""


def min_eating_speed_v1(piles: list[int], h: int) -> int:
    l, r = 1, max(piles)

    def calculate(speed):
        total = 0
        for pile in piles:
            curr = pile // speed
            rem = pile % speed
            if rem == 0:
                total += curr
            else:
                total += curr + 1
        return total

    if len(piles) == 1:
        return calculate(h)

    while l < r:
        mid = (l + r) // 2
        if calculate(mid) <= h:
            r = mid
        else:
            l = mid + 1
    return l


# ================================================================================
# MY APPROACH #2 — Binary Search with Ceiling Division Formula (cleanest)
# ================================================================================
"""
### Idea
Identical binary search structure, but `calculate` uses the ceiling
division FORMULA `(pile + speed - 1) // speed` instead of manual
remainder branching. This single expression correctly rounds up whether
or not `pile` divides evenly by `speed`, with no `if/else` needed.

### Why does the formula work?
Adding `speed - 1` before floor-dividing pushes any nonzero remainder
just far enough to "spill over" into an extra whole unit when floor
division truncates, while a PERFECTLY divisible pile is pushed by less
than a full `speed` unit and truncates right back down to the exact same
quotient. It's a standard integer-ceiling-division trick:
`ceil(a / b) == (a + b - 1) // b` for positive integers.

### Complexity
- TC: O(n log(max(piles))) — same as Approach #1
- SC: O(1) extra

### Pros
- More concise — one expression instead of a branch.
- No unneeded special case — the general binary search logic handles
  every input size correctly, including single-pile arrays.
- The ceiling-division-via-formula trick is broadly reusable across many
  "round up per-item cost" problems, worth having memorized.

### What can be improved?
Nothing — this is the accepted clean, optimal solution:
O(n log(max(piles))) time, O(1) space, with no unnecessary branching or
special-casing.
"""


def min_eating_speed(piles: list[int], h: int) -> int:
    l, r = 1, max(piles)

    def calculate(speed):
        total = 0
        for pile in piles:
            total += (pile + speed - 1) // speed
        return total

    while l < r:
        mid = (l + r) // 2
        if calculate(mid) <= h:
            r = mid
        else:
            l = mid + 1
    return l


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
KOKO EATING BANANAS
│
├── Brute Force
│   └── Try speed 1, 2, 3, ... until hours needed <= h -> O(max(piles) * n)
│
├── Bottleneck
│   └── Ignores that "does this speed work?" is MONOTONIC in speed
│
├── Key Observation
│   └── Higher speed -> fewer (or equal) hours needed, NEVER more
│       -> classic binary-search-on-the-answer setup
│
├── Search Space
│   └── speed in [1, max(piles)] — no speed beyond the biggest pile is
│       ever necessary (one pile takes at least 1 hour regardless)
│
├── Per-Pile Cost — Two Equivalent Ways to Compute
│   ├── Manual remainder check: pile//speed, +1 if pile % speed != 0
│   └── Ceiling division formula: (pile + speed - 1) // speed  <-- cleaner
│
└── Optimization — Converging-Pointer Binary Search
    ├── calculate(mid) <= h  -> speed works, try slower -> r = mid
    ├── calculate(mid) > h   -> speed too slow, go faster -> l = mid+1
    ├── Loop while l < r
    └── l == r at the end -> minimum valid speed
        └── O(n log(max(piles))) time, O(1) space  <-- optimal
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'Minimum speed/capacity such that a cost stays under budget' -> binary
  search the ANSWER SPACE. Check monotonicity first: does increasing the
  candidate answer make the cost go down (or stay the same), never up?"
- "Search space bound: [1, max(single item)] — no candidate speed beyond
  the largest single item is ever needed, since that item alone caps the
  minimum possible time to 1 unit regardless of how much faster you go."
- "Per-item 'rounding up' cost -> ceiling division: (value + divisor - 1)
  // divisor. Memorize this formula; it replaces manual remainder
  branching in one line."
- "Two-layer structure: OUTER binary search over candidate answers,
  INNER linear pass to evaluate whether a candidate works. This shape
  recurs across an entire family of problems (Capacity To Ship Packages,
  Split Array Largest Sum, Minimum Number of Days to Make Bouquets, etc.)."
- "Don't add special cases 'just in case' — test whether the general
  logic already handles the edge case before adding a branch for it."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                          | Core Idea                                               | TC                        | SC   | Pros                                   | Cons                                          | When to Use                          |
|---------------------------------------|------------------------------------------------------------------|---------------------------|------|-----------------------------------------------|----------------------------------------------------|-------------------------------------------|
| Brute Force                            | Try speed 1, 2, 3, ... until it works                              | O(max(piles) * n)         | O(1) | Trivial to write/verify                        | Far too slow for large pile sizes                   | Baseline / correctness check only         |
| Binary Search + Manual Remainder       | Binary search speed; per-pile if/else for leftover hour             | O(n log(max(piles)))      | O(1) | Explicit about WHY ceiling rounding is needed  | More verbose; had an unneeded special case          | Good for first-pass intuition building     |
| Binary Search + Ceiling Division       | Binary search speed; (pile+speed-1)//speed formula, no branching     | O(n log(max(piles)))      | O(1) | Cleanest code, no unnecessary special-casing    | None significant                                     | Default optimal choice (your second code) |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Binary Search on the Answer (same family as mySqrt, and the
  broader "minimize X subject to a monotonic cost constraint" template —
  Capacity To Ship Packages Within D Days, Split Array Largest Sum, etc.
  are near-identical in structure).
- Go-to answer: "Since a faster speed never increases hours needed,
  binary search speed in [1, max(piles)]. For each candidate, compute
  total hours via ceiling division per pile; if within budget, try
  slower (r = mid); otherwise go faster (l = mid + 1). O(n log(max(piles)))
  time."
- Good to explicitly name the search space bound (1 to max(piles)) and
  WHY it's sufficient — shows you're not just pattern-matching binary
  search blindly.
- Common follow-up: "What if `h` were guaranteed less than len(piles)?" ->
  The problem would become unsolvable (impossible to visit every pile
  even once), so the answer wouldn't exist — worth flagging as a
  precondition rather than something the code needs to defensively
  handle, per this problem's stated constraints.
"""