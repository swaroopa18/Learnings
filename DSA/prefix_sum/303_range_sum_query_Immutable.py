"""
================================================================================
 PROBLEM: Range Sum Query - Immutable (LeetCode 303)
================================================================================
Given: a fixed (immutable — never updated) integer array `nums`.
Task: support many `sumRange(left, right)` queries, each asking for the
sum of `nums[left..right]` inclusive, as efficiently as possible per query.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is nums guaranteed to stay immutable (no update() calls)? (Yes — that's
  the defining constraint of this variant vs. LC 307's mutable version)
- How many sumRange calls should we expect? (Many — this is the signal
  that preprocessing cost in __init__ is worth paying)
- Are left <= right always valid, in-bounds indices? (Usually yes)
"""

# ================================================================================
# VERSION 1 (your first solution) — Recompute Prefix Sum Inside sumRange
# ================================================================================
"""
### What it does
Builds a fresh prefix-sum array FROM SCRATCH, every single time
`sumRange` is called, then does the lookup.

### Why this is a real problem, not just a style choice ⚠️
This completely defeats the purpose of an "immutable" data structure API!
The whole reason LC 303 separates construction from querying is to let you
pay preprocessing cost ONCE and amortize it across many queries. Rebuilding
the prefix array inside `sumRange` means EVERY query pays the full
O(n) preprocessing cost again — there's zero reuse of work between calls,
even though `nums` never changes.

### Complexity
- TC:
  - `__init__`: O(1) — just stores a reference
  - `sumRange`: O(n) — rebuilds the full prefix array every call
  - If called Q times: O(Q * n) total — no better than brute-force
    re-summing the range directly each time!
- SC: O(n) — new prefix array allocated on every call (transient, but
  still real work and garbage-collection pressure)

### DSA Buddy Point 🧠
"If your class has both `__init__` and per-query methods, ask yourself:
'what work here doesn't depend on the QUERY, only on the DATA?' That work
belongs in `__init__`, done once — not inside the query method, done
every time."

### Verdict
This is a common trap: recognizing "prefix sums help here" but putting the
precompute step in the wrong place. It's still correct, but it throws away
the entire point of the immutable-data-structure pattern.
"""


class NumArraySlow:
    def __init__(self, nums: list[int]):
        self.nums = nums

    def sumRange(self, left: int, right: int) -> int:
        nums = self.nums[:]
        for i in range(1, len(nums)):
            nums[i] += nums[i - 1]
        if left == 0:
            return nums[right]
        return nums[right] - nums[left - 1]


# ================================================================================
# VERSION 2 (your second solution) — Precompute Prefix Sum Once in __init__
# ================================================================================
"""
### Idea
Build the prefix-sum array ONCE, in the constructor, using a padded
(len(nums)+1)-sized array so `prefix[i]` = sum of `nums[0..i-1]`. This
avoids the `if left == 0` special case entirely — `prefix[0]` is just 0
by construction. Then `sumRange(left, right)` is a single O(1) subtraction:

    sumRange(left, right) = prefix[right + 1] - prefix[left]

### Why the padding matters
Without padding (0-indexed prefix aligned directly to nums), you need a
special case for `left == 0` (nothing to subtract). WITH a 1-indexed
padded array, `prefix[left]` naturally represents "sum before index left"
even when `left == 0` (since `prefix[0] == 0`), eliminating the branch
entirely — this is exactly why Version 1 needed its `if` check and this
version doesn't.

### Complexity
- TC:
  - `__init__`: O(n) — one pass to build the prefix array
  - `sumRange`: O(1) — a single lookup + subtraction
  - If called Q times: O(n + Q) total — preprocessing paid once, ever
- SC: O(n) — one persistent prefix array, built once

### Pros
- True O(1) per query, completely decoupled from query count.
- No branching needed in `sumRange` — the padded array design eliminates
  the edge case cleanly.

### DSA Buddy Point 🧠
"Padding a prefix-sum array with a leading 0 (making it size n+1 instead
of n) isn't just cosmetic — it removes the need for an `if index == 0`
special case at every query site. Small design choice, real simplification."

### What can be improved?
Nothing — O(n) preprocessing once, O(1) per query forever after, is
optimal for this problem. You cannot answer even a single sumRange query
without having looked at the relevant elements of nums at least once
overall, and this solution does exactly the minimum necessary work.
"""


class NumArray:
    def __init__(self, nums: list[int]):
        self.prefix = [0] * (len(nums) + 1)

        for i in range(len(nums)):
            self.prefix[i + 1] = nums[i] + self.prefix[i]

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
RANGE SUM QUERY - IMMUTABLE
│
├── The Core Question
│   └── "What work depends only on the DATA (do once), vs. what depends
│        on the QUERY (do every call)?"
│
├── The Trap — Version 1
│   └── Prefix sum built INSIDE sumRange -> recomputed every call
│       └── init: O(1), query: O(n) -> Q queries cost O(Q*n) total
│       └── No better than brute-force summing the range directly!
│
├── The Fix — Version 2
│   └── Prefix sum built ONCE in __init__, padded with a leading 0
│       └── init: O(n), query: O(1) -> Q queries cost O(n + Q) total
│       └── Padding removes the `left == 0` special case entirely
│
└── General Principle
    └── "Immutable data structure + many queries" ALWAYS means:
        push work into __init__, keep query methods O(1) or as cheap
        as the problem allows
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Constructor vs. query method split is a DESIGN SIGNAL — anything that
  doesn't change between queries belongs in __init__, not in the query."
- "Recomputing a prefix sum inside every query call defeats the entire
  purpose of prefix sums — you've just moved the O(n) cost around, not
  eliminated it."
- "A padded (size n+1) prefix array with a leading 0 removes edge-case
  branching (`if left == 0`) that an unpadded version requires."
- "sumRange(left, right) = prefix[right+1] - prefix[left] — memorize this
  exact formula shape; it recurs in every 1D prefix-sum problem."
- "If you see `__init__` AND a query method both doing O(n) work, that's
  almost always a sign the preprocessing landed in the wrong place."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Version              | init TC | query TC | SC   | Pros                          | Cons                                          | When to Use                    |
|-------------------------|---------|----------|------|-------------------------------------|--------------------------------------------------|-------------------------------------|
| V1 — Recompute per query| O(1)    | O(n)     | O(n) transient | Looks like it "uses prefix sums" | Defeats the purpose — no cheaper than brute force per query | Never — this is an anti-pattern here |
| V2 — Precompute once    | O(n)    | O(1)     | O(n) persistent| True O(1) query, amortizes over many calls | None significant                                | Default optimal choice (your second code) |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: 1D Prefix Sum, precomputed once in a constructor (the 1D
  sibling of "Range Sum Query 2D - Immutable" — same amortization idea,
  one axis instead of two).
- Go-to answer: "Since nums never changes, build a prefix-sum array once
  in __init__ — O(n). Every sumRange call then becomes a single O(1)
  subtraction: prefix[right+1] - prefix[left]."
- If you catch yourself building or modifying a prefix array INSIDE a
  query method on an immutable structure, that's worth flagging out loud
  in an interview — recognizing the anti-pattern shows real understanding,
  not just pattern-matching "prefix sum -> done."
- Common follow-up: "What if nums could be updated between queries?" ->
  That's LC 307 (mutable version); plain prefix sums can't support O(1)
  or even fast updates (a single update can shift many prefix values), so
  you'd switch to a Binary Indexed Tree (Fenwick Tree) or segment tree,
  both giving O(log n) update and O(log n) query.
"""