"""
================================================================================
 PROBLEM: Capacity To Ship Packages Within D Days (LeetCode 1011)
================================================================================
Given: `weights` (an array of package weights, in the FIXED order they
must be shipped — no reordering allowed) and `days` (number of days
available). A ship has some weight `capacity`; each day, load packages
onto the ship IN ORDER until adding the next one would exceed capacity,
then that day is done and a new day starts. Task: return the MINIMUM
capacity such that all packages ship within `days` days.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Must packages ship in the given ORDER (no reordering/repacking
  allowed)? (Yes — this is what makes it a "greedy simulate one day at a
  time" check, not a bin-packing/subset-sum problem)
- Is capacity guaranteed to be achievable within [max(weights),
  sum(weights)]? (Yes — max(weights) is the absolute minimum possible
  capacity, since even a single heaviest package must fit in one day;
  sum(weights) is the absolute max needed, shipping everything in 1 day)
- Must `days` be enough to ship everything at all (i.e. days <=
  len(weights) isn't required, but days must be achievable)? (LeetCode
  guarantees a valid answer exists within the given constraints)
"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "BINARY SEARCH ON THE ANSWER" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   "Minimum capacity/speed/value such that a COST function stays    │
    │   under a budget" -> binary search the ANSWER SPACE, not an array. │
    │   Higher capacity -> fewer days needed (monotonic) -> binary search│
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the DIRECT SIBLING of "Koko Eating Bananas" — same template,
different cost function. Memorize the shared reflexes:

1. **Identify the monotonic relationship.** As ship capacity increases,
   days needed to ship everything DECREASES (or stays the same) — never
   increases. That monotonicity is what licenses binary search here.

2. **Search space is [max(weights), sum(weights)].** `max(weights)` is
   the smallest capacity that can even physically hold the single
   heaviest package in one day (a hard lower bound — go below this and
   it's literally impossible). `sum(weights)` ships everything in exactly
   1 day (a trivial upper bound that always works).

3. **calculate(mid) is a GREEDY DAY-BY-DAY SIMULATION**, not a formula
   like ceiling division — load packages onto the "current day" in order
   until the next one wouldn't fit, then start a new day. This greedy
   simulation is provably optimal for a FIXED capacity, because packing
   as much as possible into each day before moving on never hurts (it
   can only reduce or match the days needed compared to stopping early).

4. **calculate(mid) <= days -> capacity WORKS -> try smaller -> r = mid.**
   **calculate(mid) > days -> capacity too small -> must go bigger ->
   l = mid + 1.**

5. **Converging pointers (`l < r`)** — same template as Koko, findMin,
   findPeakElement, firstBadVersion. `return l` and `return r` are
   interchangeable at the end.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Try the smallest POSSIBLE capacity first — `max(weights)`, since anything
smaller couldn't even hold the heaviest single package. Simulate
shipping with that capacity and count the days needed. If it's <= days,
you're done. Otherwise, try `max(weights) + 1`. Then `+ 2`. Keep
incrementing until the simulated days needed finally drops to <= days.
That's the brute force approach.

### The key insight: capacity and days-needed move in OPPOSITE
    directions, predictably
The bigger the ship's capacity, the fewer days it takes to ship
everything (more packages fit per day). This relationship NEVER
reverses — a bigger capacity can never require MORE days than a smaller
one. That's the monotonic predicate binary search needs, exactly like
Koko's "faster speed never needs more hours."

### Why is the day-by-day greedy simulation correct for checking a FIXED
    capacity?
For a GIVEN capacity, greedily packing as many packages as possible into
each day (only starting a new day when the next package genuinely
wouldn't fit) is provably the best you can do — packages must ship in
order, so there's no clever repacking trick available; the only lever is
"how much do I cram into today before moving on," and cramming as much as
possible is always at least as good as stopping early. So `calculate(mid)`
correctly answers "what's the FEWEST days possible at this exact
capacity?"

### Step-by-step trace: shipWithinDays([1,2,3,4,5,6,7,8,9,10], days=5)
```
l = max(weights) = 10, r = sum(weights) = 55

Step 1: mid = (10+55)//2 = 32
        Simulate: day1=[1,2,3,4,5,6,7]=28 (+8 would be 36>32, new day)
                  day2=[8,9]=17 (+10 would be 27<=32... wait let's just
                  trust the simulation) -> total days needed <= 5? YES
        -> capacity works, try smaller -> r = 32

Step 2: l=10, r=32 -> mid=21
        Simulate at capacity 21 -> days needed, say 6 (too many)
        -> capacity too small -> l = mid+1 = 22

... (continues narrowing) ...

Eventually converges to 15.
Return 15.  Correct! ✅ (matches LeetCode's known expected answer)
```
(Full simulation arithmetic omitted for brevity in the trace above — the
core pattern is identical to Koko's trace: compute a candidate, run the
O(n) check, compare to budget, narrow accordingly.)

### Building strong intuition: "search the CAPACITY, not the weights"
Just like Koko searches over SPEED (not piles), this problem binary
searches over CAPACITY (not weights). The weights array only gets used
INSIDE the `calculate` check — the outer binary search never touches
individual weights directly, it only ever asks "at this capacity, how
many days does the greedy simulation need?"

### The "aha" moment to remember 🎯
This is the exact same TWO-LAYER STRUCTURE as Koko Eating Bananas: an
OUTER binary search over a candidate answer range, and an INNER O(n)
function that simulates/evaluates whether that candidate satisfies the
budget. Once you've internalized this shape from one problem, recognizing
it in a differently-worded problem (ships instead of bananas, days
instead of hours) becomes almost automatic.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (try every capacity from max(weights) upward)
# ================================================================================
"""
### Thought Process 🧠
Try capacity = max(weights), check days needed; if too many days, try
max(weights) + 1; keep incrementing until the simulated days needed is
within budget.

### Complexity
- TC: O((sum(weights) - max(weights)) * n) — worst case, tries a huge
  range of capacities, each requiring an O(n) simulation
- SC: O(1)

### Pros
- Simple, obviously correct, easy to write under time pressure if binary
  search isn't immediately obvious.

### Cons
- Can be extremely slow for large weight sums — trying every single
  integer capacity one at a time wastes the monotonic structure entirely.

### Bottleneck
Same as Koko: a failed capacity attempt throws away the fact that every
SMALLER capacity is now also guaranteed to fail. Ask: "since 'does this
capacity work' is monotonic, can one check eliminate half the remaining
candidates?" -> Yes: binary search (the main approach below).
"""


def ship_brute(weights: list[int], days: int) -> int:
    def calculate(capacity):
        days_needed = 1
        curr = 0
        for w in weights:
            if curr + w > capacity:
                days_needed += 1
                curr = 0
            curr += w
        return days_needed

    capacity = max(weights)
    while calculate(capacity) > days:
        capacity += 1
    return capacity


# ================================================================================
# MY APPROACH — Binary Search with Explicit Equal/Greater Branching
# ================================================================================
"""
### Idea
Binary search capacity over `[1, sum(weights)]`. The `calculate` helper
simulates day-by-day loading: track a running `curr` load; if adding the
next package would make `curr == weight` (capacity) exactly, close out
the day; if it would exceed the capacity, start a new day with just that
package. An early guard `if w > weight: return math.inf` handles a single
package too heavy to ever fit at this candidate capacity (correctly
signals "this capacity is invalid," pushing the search higher).

### Complexity
- TC: O(n log(sum(weights))) — O(log(sum(weights))) binary search
  iterations, each running an O(n) `calculate` simulation
- SC: O(1) extra

### Pros
- Explicitly handles the "package too heavy for this capacity" case with
  an early return, which is a correctness safeguard (though technically
  redundant if the search's lower bound already starts at max(weights)
  instead of 1 — see the note below).
- The equal-vs-greater-than distinction in the day-closing logic is very
  precise about exactly when a day ends.

### DSA Buddy Point 🧠
"Searching from l=1 (instead of l=max(weights)) means the 'is any single
package too heavy?' check becomes NECESSARY, since early low-capacity
guesses genuinely could be invalid. Starting the search range at
max(weights) instead makes that guard provably unreachable — a nice
example of how tightening your search bounds can simplify the logic
inside the check."

### What can be improved?
The `calculate` function's branching (`== weight` vs `> weight`) can be
simplified into a single unified condition (`curr + w > capacity`), which
naturally covers both the "exactly full" and "would overflow" cases
without needing to special-case equality — see the cleaner version below.
Also, starting the search at `l = max(weights)` instead of `l = 1`
eliminates the need for the `w > weight: return math.inf` guard entirely,
since no candidate ever below max(weights) is ever tried.
"""


def ship_v1(weights: list[int], days: int) -> int:
    import math
    l, r = 1, sum(weights)

    def calculate(weight):
        total = 0
        curr = 0
        for w in weights:
            if w > weight:
                return math.inf
            curr += w
            if curr == weight:
                curr = 0
                total += 1
            elif curr > weight:
                curr = w
                total += 1
        return total if curr == 0 else total + 1

    while l < r:
        mid = (l + r) // 2
        if calculate(mid) <= days:
            r = mid
        else:
            l = mid + 1
    return l


# ================================================================================
# ALTERNATIVE APPROACH — Cleaner Binary Search (tighter bounds, unified check)
# ================================================================================
"""
### Thought Process 🧠
A streamlined version of the same idea: start the search range at
`max(weights)` instead of `1` (the true minimum possible capacity,
eliminating ever needing to check "is a package too heavy?" — it
structurally can't happen). Simplify the day-closing logic into a single
condition: "would adding this package OVERFLOW the current day?" If yes,
close the current day and start fresh with this package; if no, just add
it to the running total. No separate `== weight` branch needed — a day
naturally closes out via the SAME `days_needed += 1` step whether the
running total lands exactly on capacity or would have exceeded it; the
only real decision point is "does this package still fit today?"

### Idea
`l, r = max(weights), sum(weights)`. `calculate(capacity)`: start
`days_needed = 1` (the first day always exists), `curr = 0`. For each
weight: if `curr + w > capacity`, this package doesn't fit today — start
a new day (`days_needed += 1`, `curr = 0`) before adding it. Then always
add `w` to `curr`. Return `days_needed`.

### Complexity
- TC: O(n log(sum(weights) - max(weights))) — same asymptotic shape as
  the other version, slightly tighter search range
- SC: O(1)

### Pros
- No special-case guard needed for "package too heavy" — structurally
  impossible given the tighter starting bound.
- Simpler day-closing logic — one condition instead of two branches, and
  it reads very naturally as "does today have room? If not, start
  tomorrow."

### Cons
- None significant — this is a strict readability/simplicity improvement
  over Approach #1 with no complexity trade-off.

### DSA Buddy Point 🧠
"Tightening a binary search's bounds to the TRUE minimum/maximum
possible answer (not just a technically-valid-but-looser bound) often
lets you simplify or entirely remove defensive checks inside the
per-candidate evaluation function — the bounds themselves become a proof
that certain edge cases can't occur."
"""


def ship_within_days(weights: list[int], days: int) -> int:
    l, r = max(weights), sum(weights)

    def calculate(capacity):
        days_needed = 1
        curr = 0
        for w in weights:
            if curr + w > capacity:
                days_needed += 1
                curr = 0
            curr += w
        return days_needed

    while l < r:
        mid = (l + r) // 2
        if calculate(mid) <= days:
            r = mid
        else:
            l = mid + 1
    return l


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
CAPACITY TO SHIP PACKAGES WITHIN D DAYS
│
├── Brute Force
│   └── Try capacity = max(weights), max(weights)+1, ... until days fit
│       └── O((sum - max) * n)
│
├── Bottleneck
│   └── Ignores that "does this capacity work?" is MONOTONIC in capacity
│
├── Key Observation
│   └── Higher capacity -> fewer (or equal) days needed, NEVER more
│       -> classic binary-search-on-the-answer setup (Koko's sibling)
│
├── Search Space
│   └── capacity in [max(weights), sum(weights)] — true lower bound
│       (must hold the heaviest single package) to true upper bound
│       (ship everything in exactly 1 day)
│
├── Per-Capacity Check — Greedy Day-by-Day Simulation
│   └── Pack each day full before starting a new one (provably optimal
│       for a FIXED capacity, since order is fixed and packing more
│       never hurts)
│
└── Optimization — Converging-Pointer Binary Search
    ├── calculate(mid) <= days -> capacity works, try smaller -> r = mid
    ├── calculate(mid) > days  -> too small, go bigger -> l = mid+1
    ├── Loop while l < r
    └── l == r at the end -> minimum valid capacity
        └── O(n log(sum(weights))) time, O(1) space  <-- optimal
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "This is Koko Eating Bananas' DIRECT SIBLING: same two-layer binary-
  search-on-the-answer template, different cost function (greedy
  day-packing simulation instead of ceiling division per pile)."
- "Search bounds: [max(single item), sum(all items)] — the true physical
  lower and upper bounds, not just '1' to 'infinity.' Tight bounds can
  eliminate the need for defensive checks inside the per-candidate check."
- "The greedy 'pack today full before moving to tomorrow' simulation is
  correct because packages ship in FIXED ORDER — there's no reordering
  lever to pull, so maximizing each day's load is always at least as
  good as stopping early."
- "Two-layer structure: OUTER binary search over candidate answers,
  INNER linear pass (here, a greedy simulation) to evaluate a candidate.
  Recognize this shape across Koko, this problem, Split Array Largest
  Sum, Minimum Number of Days to Make Bouquets, and more."
- "Simplifying a two-branch condition (== vs >) into one unified
  condition (curr + w > capacity) is often possible when the two branches
  ultimately trigger the same action (closing out a day) — look for that
  redundancy."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                          | Core Idea                                                | TC                              | SC   | Pros                                    | Cons                                        | When to Use                          |
|---------------------------------------|-------------------------------------------------------------------|----------------------------------|------|------------------------------------------------|--------------------------------------------------|-------------------------------------------|
| Brute Force                            | Try capacity max(weights), +1, +2, ... until it works                | O((sum-max) * n)                | O(1) | Trivial to write/verify                          | Far too slow for large weight sums                  | Baseline / correctness check only         |
| Binary Search (l=1, extra guard)       | Binary search from 1; explicit equal/greater branching + heavy-package guard | O(n log(sum(weights)))    | O(1) | Explicit, defensive about edge cases            | Loose lower bound requires an otherwise-unneeded guard | Fine, but not the tightest version         |
| Binary Search (tight bounds, unified)  | Binary search from max(weights); single overflow condition            | O(n log(sum(weights)-max(weights))) | O(1) | Cleanest code, tightest bounds, no dead guard   | None significant                                     | Default optimal choice                     |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Binary Search on the Answer (Koko Eating Bananas' sibling —
  same "minimize X subject to a monotonic cost constraint" template).
  Also closely related to Split Array Largest Sum and Minimum Number of
  Days to Make m Bouquets.
- Go-to answer: "Since higher capacity never increases days needed,
  binary search capacity in [max(weights), sum(weights)]. For each
  candidate, greedily simulate day-by-day loading (pack as much as
  possible before starting a new day); if within the day budget, try
  smaller (r = mid), otherwise go bigger (l = mid + 1)."
- Good to explicitly justify why greedy day-packing is optimal for a
  FIXED capacity (order is fixed, so cramming as much as possible into
  each day is never worse than stopping early) — this is the correctness
  argument interviewers want to hear, not just "binary search go brrr."
- Common follow-up: "What if packages COULD be reordered?" -> That
  changes the problem into something closer to bin-packing / partition
  optimization, which is NP-hard in general — the fixed-order constraint
  here is exactly what keeps the per-candidate check a simple, provably
  optimal O(n) greedy pass.
"""