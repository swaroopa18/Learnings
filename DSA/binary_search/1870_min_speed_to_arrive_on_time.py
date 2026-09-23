"""
================================================================================
 PROBLEM: Minimum Speed to Arrive on Time (LeetCode 1870)
================================================================================
Given: `dist` (distances of each train segment) and `hour` (a FLOATING
POINT time budget, with at most 2 decimal digits). You travel each
segment at a constant integer speed. For every segment EXCEPT the last,
you must wait for the next whole hour to catch the next train if you
don't arrive exactly on an hour mark (i.e. arrival time rounds UP to the
next integer hour). The LAST segment has no such rounding — you just need
to arrive by the exact time budget. Task: return the MINIMUM integer
speed to arrive within `hour`, or -1 if impossible.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Why would -1 ever be the answer? (If there are n segments, the FIRST
  n-1 each force at least 1 full hour of waiting/rounding regardless of
  speed — so if `hour <= n - 1`, it's mathematically impossible to make
  it in time no matter how fast you go)
- Is there an upper bound on speed to search up to? (LeetCode constraints
  cap dist[i] and hour such that speed never needs to exceed 10^7 —
  worth confirming/deriving this bound rather than guessing it)
- Does `hour` having at most 2 decimal digits matter for implementation?
  (Yes — floating point comparisons can be imprecise; an integer-based
  approach, working in hundredths, sidesteps this entirely — see the
  alternative below)
"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "BINARY SEARCH ON THE ANSWER" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   "Minimum speed/capacity/value such that a COST function stays    │
    │   under a budget" -> binary search the ANSWER SPACE, not an array. │
    │   Higher speed -> less time needed (monotonic) -> binary search.   │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the THIRD member of the "Koko Eating Bananas" family you've seen
(after Koko itself and Capacity To Ship Packages) — same template, a
different (and slightly trickier) cost function. Shared reflexes:

1. **Identify the monotonic relationship.** Faster speed -> less (or
   equal) total travel time, never more. Standard monotonic predicate.

2. **Search space is [1, some safe upper bound]** (here, 10^7, derived
   from the problem's constraints on dist[i] and hour — always worth
   asking "what's the largest speed that could EVER be necessary?"
   rather than picking a bound arbitrarily).

3. **The cost function has an asymmetry: ALL segments except the LAST
   round UP to the next integer hour; the LAST segment does NOT round.**
   This is the one genuinely new wrinkle in this problem compared to
   Koko/Ship — most of the "two-layer binary search" skeleton is
   identical, but the per-segment cost logic needs special handling for
   the final segment.

4. **-1 is possible here** (unlike Koko/Ship, where a valid answer always
   exists within the search bounds) — check for it FIRST, before running
   binary search at all: if `len(dist) - 1 >= hour`, it's impossible,
   since the first n-1 segments alone force at least n-1 full hours of
   rounding-up, regardless of how fast you go.

5. **Converging pointers (`l < r`)** — same template as Koko, Ship,
   findMin, findPeakElement, firstBadVersion.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Try speed 1. Compute the total time needed (with the special last-segment
rule). If it's <= hour, done. Otherwise try speed 2, then 3, and so on,
until you find a speed that works. Brute force, as always.

### The key insight: same monotonic binary search as Koko/Ship, plus one
    new wrinkle
Everything about the OUTER binary search structure is identical to Koko
Eating Bananas and Capacity To Ship Packages — faster speed can only
help, never hurt, so binary search over candidate speeds applies exactly
the same way. The one NEW thing to get right is the INNER cost function:
for every segment except the very last one, you must round UP to the
next whole hour (you can't catch a train "partway" through an hour), but
the LAST segment has no such constraint — you just need to physically
arrive by the deadline, partial hours and all.

### Why check for -1 FIRST, before binary searching at all?
If there are `n` segments, the first `n-1` of them EACH force at least 1
full hour of rounding-up, no matter how absurdly fast you travel (even at
speed 10^7, `math.ceil(tiny_number)` is still 1, never 0). So the
absolute minimum possible total time, regardless of speed, is at least
`n - 1` hours (from rounding alone) plus whatever time the last segment
takes (which can be made arbitrarily small with high enough speed, but
never negative). So if `hour <= n - 1`, no speed — not even an
infinitely fast one — could ever satisfy the budget. This is a hard
mathematical impossibility, not something binary search could "find" by
searching harder; it must be checked as a precondition.

### Step-by-step trace: minSpeedOnTime([1,3,2], hour=2.7)
```
n=3, is 2 (n-1) >= 2.7 (hour)? NO -> proceed with binary search
l=1, r=10^7

(binary search narrows down, evaluating calculate(mid) each step,
 where the first n-1=2 segments round up and the last does not)

At speed=3: calculate = ceil(1/3) + ceil(3/3) + 2/3
                       = 1        + 1        + 0.667 = 2.667
            2.667 <= 2.7? YES -> works, try smaller

At speed=2: calculate = ceil(1/2) + ceil(3/2) + 2/2
                       = 1        + 2        + 1     = 4
            4 <= 2.7? NO -> too slow, need faster

... narrows down to speed=3 as the minimum working speed ...

Return 3.  Correct! ✅ (matches LeetCode's known expected answer)
```

### Building strong intuition: "the last segment is special, everything
    else is just Koko/Ship again"
If you already understand Koko's and Ship's binary-search-on-the-answer
template, 95% of this problem is "nothing new." The genuinely new
learning here is narrow and specific: identify the LAST segment inside
your cost function and give it different treatment (no ceiling) than
every other segment (ceiling). Everything else — the monotonicity
argument, the converging-pointer binary search, the two-layer structure —
transfers directly.

### The "aha" moment to remember 🎯
When a new problem "smells like" one you've already solved (same
monotonic-cost-under-a-budget shape), don't re-derive the whole solution
from scratch — instead, ask "what's DIFFERENT about this cost function
compared to the one I already know?" Here, that's exactly two things:
(1) the last-segment special case, and (2) the possibility of a genuine
"impossible" answer that must be checked as a precondition rather than
discovered via the search itself.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (try every speed from 1 upward)
# ================================================================================
"""
### Thought Process 🧠
Try speed 1, 2, 3, ... in order, computing total time (with the
last-segment special case) at each, until one satisfies the budget.

### Complexity
- TC: O(upper_bound * n) — worst case, tries up to the full speed range,
  each check being O(n)
- SC: O(1)

### Pros
- Simple, obviously correct.

### Cons
- Far too slow if the answer speed is large (up to 10^7 in this
  problem's constraints) — exactly the scenario binary search exists to
  avoid.

### Bottleneck
Same monotonicity-ignoring issue as Koko/Ship: a failed speed doesn't
inform the search that every smaller speed is now also guaranteed to
fail. Ask: "can one check eliminate half the remaining candidates?" ->
Yes: binary search (the main approach below).
"""


def min_speed_brute(dist: list[int], hour: float) -> int:
    import math
    n = len(dist)
    if n - 1 >= hour:
        return -1

    def calculate(speed):
        hours = 0
        for idx, d in enumerate(dist):
            if idx == n - 1:
                hours += d / speed
            else:
                hours += math.ceil(d / speed)
        return hours

    for speed in range(1, 10**7 + 1):
        if calculate(speed) <= hour:
            return speed
    return -1


# ================================================================================
# MY APPROACH — Binary Search with Impossibility Pre-check
# ================================================================================
"""
### Idea
First, check the impossibility condition: if `len(dist) - 1 >= hour`,
return -1 immediately (see the walkthrough above for why this is a hard
mathematical guarantee, not just a heuristic). Otherwise, binary search
speed over `[1, 10^7]`. The `calculate` helper sums travel time per
segment: `math.ceil(d / speed)` for every segment except the last, and
plain float division `d / speed` for the last segment (no rounding).

### Complexity
- TC: O(n log(10^7)) — O(log(10^7)) ≈ 24 binary search iterations, each
  doing an O(n) `calculate` pass
- SC: O(1) extra

### Pros
- Correctly captures the problem's core asymmetry (last segment treated
  differently) in a compact, readable `calculate` function.
- The upfront impossibility check cleanly separates "can this even be
  done?" from "what's the minimum speed if it CAN be done?" — good
  separation of concerns.

### DSA Buddy Point 🧠
"When a problem can have a genuine 'no valid answer exists' case,
check for it EXPLICITLY and UP FRONT, using the problem's own structure
to prove impossibility — don't rely on the binary search's bounds or
behavior to somehow 'discover' infeasibility; that's fragile and can lead
to wrong or index-out-of-range results if you get the bounds even
slightly wrong."

### What can be improved?
The one legitimate concern with this version is FLOATING-POINT
PRECISION: comparing `hours <= hour` where `hours` accumulates from
several floating-point divisions and `hour` itself is a float with up to
2 decimal digits can, in rare edge cases, suffer from tiny rounding
errors that flip a comparison the wrong way. See the integer-arithmetic
alternative below for a version that sidesteps this entirely.
"""


def min_speed_on_time_v1(dist: list[int], hour: float) -> int:
    import math
    if (len(dist) - 1) >= hour:
        return -1

    l, r = 1, 10**7

    def calculate(speed):
        hours = 0
        for idx, d in enumerate(dist):
            if idx == len(dist) - 1:
                hours += d / speed
            else:
                hours += math.ceil(d / speed)
        return hours

    while l < r:
        mid = (l + r) // 2
        if calculate(mid) <= hour:
            r = mid
        else:
            l = mid + 1
    return l


# ================================================================================
# ALTERNATIVE APPROACH — Integer Arithmetic (avoid floating-point precision issues)
# ================================================================================
"""
### Thought Process 🧠
Since `hour` is guaranteed to have AT MOST 2 decimal digits, we can
sidestep all floating-point precision concerns entirely by working in
HUNDREDTHS OF AN HOUR as integers instead of raw floats. Multiply `hour`
by 100 and round to the nearest integer once, up front; inside
`calculate`, compute every segment's contribution in hundredths using
pure integer ceiling-division arithmetic (the same `(a + b - 1) // b`
trick from Koko Eating Bananas), including the last segment's
non-rounded time — the only difference is WHICH formula is used per
segment, not whether floats are involved at all.

### Idea
`hour_hundredths = round(hour * 100)`. For every segment except the
last: `math.ceil(d / speed) * 100` (an integer number of full hours,
converted to hundredths). For the last segment: `(d * 100 + speed - 1)
// speed` — this computes `ceil((d * 100) / speed)`, which is exactly
`d / speed` expressed in hundredths, rounded UP to the nearest hundredth
(a reasonable, precision-safe way to represent a fractional hour amount
without ever touching a float inside the hot loop).

### Complexity
- TC: O(n log(10^7)) — same as the main approach
- SC: O(1)

### Pros
- Completely immune to floating-point comparison bugs — everything is
  integer arithmetic from `calculate` onward.
- Reuses the same ceiling-division trick from Koko Eating Bananas,
  reinforcing that shared technique across the problem family.

### Cons
- Slightly more setup complexity (converting to hundredths, and
  reasoning through why that conversion is safe given the "at most 2
  decimal digits" guarantee) than just comparing floats directly.
- If the problem DIDN'T guarantee a bounded number of decimal digits,
  this exact hundredths-based trick wouldn't cleanly apply — worth
  recognizing this technique is enabled specifically by that constraint.

### DSA Buddy Point 🧠
"Whenever a problem gives you a bounded number of decimal digits (e.g.
'at most 2 decimal digits'), that's often a signal you can safely scale
everything into integers and avoid floating-point precision pitfalls
entirely — a broadly useful trick beyond just this problem."
"""


def min_speed_on_time(dist: list[int], hour: float) -> int:
    n = len(dist)
    if n - 1 >= hour:
        return -1

    hour_hundredths = round(hour * 100)

    def calculate(speed):
        total_hundredths = 0
        for idx, d in enumerate(dist):
            if idx == n - 1:
                total_hundredths += (d * 100 + speed - 1) // speed
            else:
                total_hundredths += -(-d // speed) * 100  # ceil(d/speed) * 100
        return total_hundredths

    l, r = 1, 10**7
    while l < r:
        mid = (l + r) // 2
        if calculate(mid) <= hour_hundredths:
            r = mid
        else:
            l = mid + 1
    return l


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MINIMUM SPEED TO ARRIVE ON TIME
│
├── Brute Force
│   └── Try speed 1, 2, 3, ... until total time <= hour -> O(bound * n)
│
├── Bottleneck
│   └── Ignores that "does this speed work?" is MONOTONIC in speed
│
├── Same Family As: Koko Eating Bananas, Capacity To Ship Packages
│   └── Two-layer binary-search-on-the-answer template — what's NEW here:
│
├── New Wrinkle #1 — Impossibility Check
│   └── If len(dist)-1 >= hour -> return -1 immediately (hard
│       mathematical impossibility, not something to "search" for)
│
├── New Wrinkle #2 — Last-Segment Asymmetry
│   └── All segments except the last: ceil(d/speed) (must round up)
│       Last segment: d/speed exactly (no rounding, exact arrival time)
│
├── Path A — Float Comparison (straightforward)
│   └── O(n log(10^7)) time, O(1) space  <-- your code, simple, but
│       theoretically float-precision-sensitive
│
└── Path B — Integer Arithmetic (hundredths of an hour)
    └── Same complexity, but immune to floating-point comparison bugs
        by scaling everything into integers up front
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "This is Koko Eating Bananas' and Capacity To Ship Packages' THIRD
  sibling — same binary-search-on-the-answer template; the only genuinely
  new material is the last-segment asymmetry and the -1 impossibility
  case."
- "Check for impossibility EXPLICITLY and FIRST, using the problem's own
  structure to prove it mathematically (here: n-1 segments each force at
  least 1 hour of rounding, regardless of speed) — don't rely on the
  search itself to somehow reveal infeasibility."
- "All-but-last-segment rounds UP (ceil); the LAST segment doesn't round
  at all — get this asymmetry right and the rest of the solution is
  identical to problems you've already solved."
- "A bounded number of decimal digits in the input (e.g. 'at most 2
  decimal places') is a signal you can scale into integers and avoid
  floating-point precision issues — reuse the (a + b - 1) // b ceiling
  trick from Koko in the process."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                                | TC                    | SC   | Pros                                    | Cons                                          | When to Use                          |
|----------------------------------|-------------------------------------------------------------------|------------------------|------|------------------------------------------------|----------------------------------------------------|-------------------------------------------|
| Brute Force                       | Try speed 1, 2, 3, ... until total time fits                          | O(bound * n)            | O(1) | Trivial to write/verify                          | Far too slow for large speed bounds                   | Baseline / correctness check only         |
| Binary Search (float comparison)  | Standard binary search; ceil for all-but-last, exact division for last | O(n log(10^7))          | O(1) | Simple, readable, directly matches problem wording | Theoretically float-precision-sensitive                | Fine for this problem's constraints (your code) |
| Binary Search (integer arithmetic)| Same structure, scaled into hundredths to avoid float precision issues | O(n log(10^7))          | O(1) | Immune to floating-point comparison bugs           | Slightly more setup / conceptual overhead              | When precision safety matters most         |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Binary Search on the Answer (third sibling in the Koko Eating
  Bananas / Capacity To Ship Packages family — recognizing the shared
  shape across all three is the real skill being tested here).
- Go-to answer: "First check impossibility: if there are n segments, the
  first n-1 force at least n-1 hours of rounding no matter the speed, so
  if hour <= n-1, return -1. Otherwise, binary search speed; for each
  candidate, sum ceil(d/speed) for all but the last segment, plus exact
  d/speed for the last segment, and compare to the budget."
- Good to explicitly connect this to Koko/Ship if you've already
  discussed them — showing you recognize the shared template (rather
  than treating this as a brand new problem from scratch) is exactly the
  kind of pattern recognition interviewers want to see.
- Common follow-up: "How would you handle floating-point precision
  concerns?" -> Scale into integers using the guaranteed decimal-digit
  bound (see the integer-arithmetic alternative) — a great opportunity to
  show awareness of a subtle correctness pitfall beyond just the
  algorithm's asymptotic complexity.
"""
