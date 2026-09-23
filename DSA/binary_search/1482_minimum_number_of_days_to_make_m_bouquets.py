"""
================================================================================
 PROBLEM: Minimum Number of Days to Make m Bouquets (LeetCode 1482)
================================================================================
Given: `bloomDay[i]` (the day flower `i` blooms), `m` (bouquets needed),
and `k` (ADJACENT flowers required per bouquet — each bouquet must use k
flowers that are consecutive in the garden row, all already bloomed).
Task: return the MINIMUM day on which you can make m bouquets, or -1 if
it's impossible no matter how long you wait.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Must the k flowers per bouquet be ADJACENT in the array (not just any k
  bloomed flowers)? (Yes — this is the key structural detail; it's why
  `calculate` resets its running `flowers` counter to 0 whenever it hits
  an unbloomed flower, breaking the current streak of adjacency)
- When is it impossible? (When `m * k > len(bloomDay)` — you simply don't
  have enough flowers in total to ever form m bouquets of k adjacent
  flowers each, regardless of how long you wait)
- Can a flower be reused across multiple bouquets? (No — implicitly, once
  k adjacent flowers form a bouquet, `calculate` resets the counter,
  meaning those flowers aren't double-counted toward another bouquet)
"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "BINARY SEARCH ON THE ANSWER" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   "Minimum day/speed/capacity such that a COUNT function reaches   │
    │   a target" -> binary search the ANSWER SPACE, not an array.       │
    │   More days -> more bouquets possible (monotonic) -> binary search.│
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the FOURTH member of the Koko/Ship/MinSpeed family you've built
notes for — same two-layer template, a different (adjacency-based) cost
function. Shared reflexes, plus what's new here:

1. **Monotonicity direction is slightly different from Koko/Ship.** In
   Koko/Ship, a LARGER candidate (speed/capacity) makes the cost
   function's OUTPUT SMALLER (fewer hours/days needed) — so you compare
   with `<=` and shrink toward smaller). HERE, a LARGER candidate (day)
   makes the cost function's output LARGER (more bouquets possible as
   more time passes) — you're searching for when it first REACHES `m`,
   not when it first drops BELOW a budget. Recognize this as the same
   template with the inequality direction flipped, based on which way
   "more" moves the cost.

2. **Impossibility check: `m * k > len(bloomDay)`.** If you need m
   bouquets of k flowers each, that's `m * k` total flowers required —
   if the garden doesn't even have that many flowers, no amount of
   waiting helps. Check this FIRST, exactly like MinSpeedOnTime's
   impossibility precondition.

3. **The cost function tracks a running STREAK of adjacent bloomed
   flowers**, resetting to 0 the moment it hits an unbloomed one — this
   is what enforces the "k adjacent flowers" requirement structurally.

4. **calculate(mid) == m -> reachable at this day -> try earlier ->
   r = mid.** **calculate(mid) != m (which given the early-return means
   < m) -> not enough bouquets yet -> need more time -> l = mid + 1.**

5. **Converging pointers (`l < r`)** — same template as the rest of the
   family.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Try day 1. Simulate: which flowers have bloomed by day 1? Walk through
the garden, counting consecutive runs of bloomed flowers, forming a
bouquet every time you accumulate k adjacent bloomed ones. Count total
bouquets formed. If >= m, day 1 works! Otherwise try day 2, then day 3,
and so on. Brute force, as always.

### The key insight: MORE days can only HELP, never hurt
As days pass, MORE flowers bloom (bloomDay values only need to be <= the
current day, and that set only grows as days increase) — flowers never
"un-bloom." So the number of possible bouquets on day X is always >= the
number possible on any earlier day. This one-directional monotonicity is
exactly what licenses binary search — just note that here, "more"
INCREASES the cost function's output (bouquets possible), the opposite
direction from Koko/Ship where "more" (speed/capacity) DECREASED the cost
function's output (hours/days needed). Same template, flipped direction.

### Why does the cost function reset on an unbloomed flower?
Bouquets require ADJACENT bloomed flowers. Picture the garden as a row:
[bloomed, bloomed, NOT bloomed, bloomed, bloomed, bloomed]. Even though
there are 5 bloomed flowers total, they're not all adjacent — the
unbloomed one in the middle breaks the run. If k=3, you could NOT form a
bouquet from the first two bloomed flowers (only 2 adjacent, need 3), but
you COULD form one from the last three (3 adjacent bloomed flowers in a
row). The `flowers = 0` reset the moment an unbloomed flower is hit is
exactly what captures this adjacency requirement.

### Step-by-step trace: minDays([1,10,3,10,2], m=3, k=1)
```
m*k = 3, len(bloomDay) = 5 -> 3 <= 5, possible, proceed
l=0, r=max(bloomDay)+1=11

(k=1 means each bouquet needs just 1 bloomed flower — adjacency is
 trivially satisfied since a single flower is always "adjacent to itself")

Step-by-step binary search narrows down to day=3:
  At day=3: bloomed flowers are those with bloomDay <= 3: indices 0(day1),
            2(day3), 4(day2) -> 3 bloomed flowers -> with k=1, that's
            3 bouquets (one per bloomed flower) -> calculate(3) == 3 == m
            -> works! try earlier.
  At day=2: bloomed: indices 0(day1), 4(day2) -> 2 bloomed -> 2 bouquets
            -> calculate(2) == 2 != m(3) -> not enough, need more time.

Converges to day=3.  Correct! ✅ (matches LeetCode's known expected answer)
```

### Building strong intuition: "search the DAY, not the flowers"
Just like Koko searches SPEED and Ship searches CAPACITY, this problem
binary searches the DAY NUMBER — the `bloomDay` array only gets consulted
INSIDE the `calculate` check. The outer binary search never looks at
individual bloom days directly; it only asks "by this candidate day, can
I form m bouquets?"

### The "aha" moment to remember 🎯
This problem is 90% identical in STRUCTURE to Koko/Ship/MinSpeed — same
two-layer binary search on the answer. The two things that make it feel
different are (1) the inequality direction (searching for when a growing
count first REACHES a target, rather than when a shrinking cost first
DROPS to a budget) and (2) the adjacency-tracking logic inside
`calculate`. Once you see past those surface differences, it's the same
template you've now seen four times.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (try every day from 1 upward)
# ================================================================================
"""
### Thought Process 🧠
Try day 1, 2, 3, ... in order, simulating bouquet formation each time,
until the count reaches m.

### Complexity
- TC: O(max(bloomDay) * n) — worst case, tries every day up to the
  latest bloom day, each simulation being O(n)
- SC: O(1)

### Pros
- Simple, obviously correct.

### Cons
- Far too slow if `max(bloomDay)` is large (up to 10^9 in this problem's
  constraints) — exactly what binary search exists to avoid.

### Bottleneck
Ignores that "can I form m bouquets by this day?" is monotonic in day —
the same wasted-work pattern as every problem in this family. Ask: "can
one simulation eliminate half the remaining candidate days?" -> Yes:
binary search (the main approach below).
"""


def min_days_brute(bloomDay: list[int], m: int, k: int) -> int:
    if m * k > len(bloomDay):
        return -1

    def calculate(days):
        bouquets = 0
        flowers = 0
        for b_day in bloomDay:
            if b_day <= days:
                flowers += 1
                if flowers == k:
                    bouquets += 1
                    flowers = 0
            else:
                flowers = 0
        return bouquets

    for day in range(1, max(bloomDay) + 1):
        if calculate(day) >= m:
            return day
    return -1


# ================================================================================
# MY APPROACH #1 — Binary Search with a "Found" Flag
# ================================================================================
"""
### Idea
Binary search day over `[0, max(bloomDay) + 1]`. Track a separate
`bouquets_found` boolean, set to True the first time `calculate(mid) ==
m` is observed during the search, and return -1 at the end if that flag
was never set (meaning no candidate day in the ENTIRE search range ever
reached m bouquets).

### Complexity
- TC: O(n log(max(bloomDay))) — standard binary search over this family
- SC: O(1) extra

### Pros
- Doesn't require a separate upfront mathematical proof of impossibility
  — instead, it discovers infeasibility empirically by tracking whether
  the target was ever reached during the search.

### Cons
- Relies on the flag being set correctly at every point the condition
  becomes true — an easy-to-forget detail if you refactor the loop later
  without noticing the flag needs updating too.
- Slightly more state to track than a clean upfront impossibility check.

### DSA Buddy Point 🧠
"Detecting infeasibility via 'did the target condition ever trigger
during the search?' works, but a precomputed impossibility check (like
MinSpeedOnTime's `n-1 >= hour`, or this problem's `m*k > len(bloomDay)`)
is usually cleaner — it separates 'can this be done at all?' from 'what's
the minimum answer if it can?' as two distinct, independently-verifiable
steps, rather than tangling them into one search with extra state."

### What can be improved?
The impossibility check can be computed directly and cheaply UP FRONT
(`m * k > len(bloomDay)`), removing the need for the `bouquets_found`
flag entirely — see Approach #2 below, which is functionally identical
but cleaner.
"""


def min_days_v1(bloomDay: list[int], m: int, k: int) -> int:
    l, r = 0, max(bloomDay) + 1

    def calculate(days):
        bouquets = 0
        flowers = 0

        for idx, b_day in enumerate(bloomDay):
            if b_day <= days:
                flowers += 1
                if flowers == k:
                    bouquets += 1
                    flowers = 0
                    if bouquets == m:
                        return bouquets
            else:
                flowers = 0
        return bouquets

    bouquets_found = False
    while l < r:
        mid = (l + r) // 2

        if calculate(mid) == m:
            bouquets_found = True
            r = mid
        else:
            l = mid + 1
    return l if bouquets_found else -1


# ================================================================================
# MY APPROACH #2 — Binary Search with Upfront Impossibility Check (cleanest)
# ================================================================================
"""
### Idea
Check `m * k > len(bloomDay)` FIRST — if true, immediately return -1
(mathematically proven impossible, no search needed). Otherwise, the
binary search is guaranteed to find a valid day, so the loop can be
simplified: no flag needed, just return `l` directly at the end.

### Complexity
- TC: O(n log(max(bloomDay))) — same as Approach #1
- SC: O(1)

### Pros
- Cleaner: separates "is this even possible?" from "find the minimum
  day," exactly mirroring the pattern from MinSpeedOnTime.
- No extra state (`bouquets_found`) to maintain or risk forgetting to
  update correctly.
- Once the impossibility check passes, the search is GUARANTEED to
  succeed — this is a provable invariant, not something you need to
  empirically verify during the loop.

### DSA Buddy Point 🧠
"Proving impossibility mathematically upfront (m*k > total flowers) is
strictly better than discovering it via a search-time flag — it's a hard
guarantee, checkable in O(1), rather than something the search has to
'stumble into' finding out."

### What can be improved?
Nothing — this is the accepted clean, optimal solution:
O(n log(max(bloomDay))) time, O(1) space, no unnecessary state.
"""


def min_days(bloomDay: list[int], m: int, k: int) -> int:
    if m * k > len(bloomDay):
        return -1

    l, r = 0, max(bloomDay) + 1

    def calculate(days):
        bouquets = 0
        flowers = 0

        for idx, b_day in enumerate(bloomDay):
            if b_day <= days:
                flowers += 1
                if flowers == k:
                    bouquets += 1
                    flowers = 0
                    if bouquets == m:
                        return bouquets
            else:
                flowers = 0
        return bouquets

    while l < r:
        mid = (l + r) // 2

        if calculate(mid) == m:
            r = mid
        else:
            l = mid + 1
    return l


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MINIMUM DAYS TO MAKE M BOUQUETS
│
├── Brute Force
│   └── Try day 1, 2, 3, ... until bouquets formed >= m -> O(max(bloomDay) * n)
│
├── Bottleneck
│   └── Ignores that "bouquets possible by this day" is MONOTONIC in day
│
├── Same Family As: Koko Eating Bananas, Ship Packages, Min Speed On Time
│   └── Two-layer binary-search-on-the-answer template — what's DIFFERENT:
│
├── Difference #1 — Inequality Direction Flipped
│   └── Koko/Ship: larger candidate -> SMALLER cost (hours/days) -> <=
│       This problem: larger candidate (day) -> LARGER cost (bouquets) ->
│       searching for when it first REACHES the target, not drops below it
│
├── Difference #2 — Adjacency-Tracking Cost Function
│   └── Running `flowers` streak counter, RESET on any unbloomed flower
│       -> structurally enforces "k ADJACENT bloomed flowers per bouquet"
│
├── Impossibility Check
│   └── m * k > len(bloomDay) -> not enough total flowers, ever -> -1
│
├── Path A — Found-Flag Version
│   └── Discovers infeasibility empirically via a boolean during the search
│       └── O(n log(max(bloomDay))) time, O(1) space
│
└── Path B — Upfront Impossibility Check (cleaner)
    └── Proves infeasibility mathematically before searching at all
        └── O(n log(max(bloomDay))) time, O(1) space  <-- cleanest
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "This is the FOURTH sibling in the binary-search-on-the-answer family
  (after Koko, Ship, MinSpeedOnTime) — recognize the shared two-layer
  shape, then focus your attention only on what's genuinely NEW."
- "Watch the inequality DIRECTION: does a larger candidate make the cost
  function's output go UP or DOWN? That determines whether you're
  searching for 'first time it drops below budget' (Koko/Ship style) or
  'first time it reaches/exceeds a target' (this problem's style)."
- "Adjacency requirements in a cost function usually mean tracking a
  running STREAK that RESETS whenever the adjacency condition breaks —
  a broadly reusable technique beyond just this problem."
- "Prove impossibility mathematically and check it UP FRONT (m*k > total
  flowers) rather than discovering it empirically via a search-time flag
  — cleaner, and removes state you could forget to maintain correctly."
- "calculate() returning early once it hits the target (bouquets == m)
  is a nice micro-optimization — no need to keep scanning once you've
  already proven the day works."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                        | Core Idea                                                  | TC                        | SC   | Pros                                     | Cons                                        | When to Use                          |
|-------------------------------------|-----------------------------------------------------------------|----------------------------|------|-----------------------------------------------|--------------------------------------------------|-------------------------------------------|
| Brute Force                          | Try day 1, 2, 3, ... until bouquets formed >= m                     | O(max(bloomDay) * n)      | O(1) | Trivial to write/verify                        | Far too slow for large bloom day values             | Baseline / correctness check only         |
| Binary Search + Found Flag           | Track boolean during search; -1 if target never reached              | O(n log(max(bloomDay)))   | O(1) | Doesn't require an upfront math proof            | Extra state to maintain, less clean separation      | Fine, but not the cleanest version         |
| Binary Search + Upfront Check        | Prove impossibility first (m*k > len), then clean binary search      | O(n log(max(bloomDay)))   | O(1) | Cleanest, no extra state, provable invariant      | None significant                                     | Default optimal choice (your second code) |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Binary Search on the Answer (fourth sibling in the Koko Eating
  Bananas / Capacity To Ship Packages / Min Speed On Time family — the
  inequality direction is flipped compared to those two, matching
  MinSpeedOnTime's "impossibility precondition" style instead).
- Go-to answer: "Since more days can only increase (never decrease) the
  number of formable bouquets, binary search the day. If m*k exceeds the
  total flower count, it's impossible — return -1 immediately. Otherwise,
  for each candidate day, count bouquets via a running adjacency streak
  that resets on unbloomed flowers; if it reaches m, try an earlier day,
  otherwise a later one."
- Good to explicitly connect this to the Koko/Ship/MinSpeed family you've
  already built if discussing multiple problems — and to call out the
  flipped inequality direction as the one thing that's genuinely
  different in the search logic itself.
- Common follow-up: "What if bouquets DIDN'T need adjacent flowers (any k
  bloomed flowers count)?" -> The cost function simplifies dramatically —
  just count total bloomed flowers by day X and divide by k — no running
  streak or reset logic needed at all, since adjacency no longer matters.
"""