"""
================================================================================
 PROBLEM: Maximum Sum of Distinct Subarrays With Length K (LeetCode 2461)
================================================================================
Given: an integer array `nums` and an integer `k`.
Task: find the maximum sum of a contiguous subarray of length exactly k
whose elements are all DISTINCT (no duplicates within that window). If no
such subarray exists, return 0.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can nums contain negative numbers? (If yes, same max_sum=0 caveat as the
  plain "max sum subarray of size k" problem applies)
- What if no valid distinct-window of size k exists? (Return 0 — matches
  the given default)
- Is k guaranteed <= len(nums)? (If not, add a length guard)
- "Distinct" means all k elements pairwise different, not just adjacent
  ones different — confirm this before coding.
"""

# ================================================================================
# MY APPROACH — Sliding Window + Hash Set (for distinctness)
# ================================================================================
"""
### Idea
This is "max sum subarray of size k" PLUS one new constraint: no duplicate
values inside the window. So on top of the running-sum sliding window, we
track which values currently live in the window via a hash set.

Two different reasons can push `start` forward:
1. The incoming `num` is already in the window (`while num in hset`) ->
   shrink from the left until it's gone, before adding `num`. This handles
   duplicates immediately, even if that means the window shrinks below k.
2. The window has reached exactly size k (`end - start + 1 == k`) -> record
   the sum, then slide forward by one as usual.

### Why does it work?
Any window containing a duplicate is invalid by definition, so as soon as
we detect the incoming number already exists in the window, we must evict
elements from the left until that duplicate is gone — otherwise we'd be
counting an illegal window as "still forming." Once we pass that dedup
check, the logic collapses back into the standard fixed-size sliding
window: add new element, check if size == k, record, then evict the
oldest element to keep the window sliding.

### Complexity
- TC: O(n) — each element is added to the hash set once and removed once
  (amortized), `start` only ever moves forward, never backward
- SC: O(k) — the hash set holds at most k distinct values at a time

### Pros
- Handles both constraints (fixed size AND distinctness) in a single pass.
- Amortized O(n): even though there's a `while` loop, `start` is bounded by
  `end`, so total start-advances across the whole run is O(n).

### DSA Buddy Point 🧠
"Fixed-size sliding window + 'no duplicates allowed' -> add a hash set as
a membership tracker, and let a `while` loop shrink the window from the
left whenever the incoming element would violate distinctness."

### Edge Case ⚠️
Same as plain max-sum-subarray-of-k: `max_sum` starts at 0, which is only
safe if elements are non-negative or 0 is an acceptable "no valid window"
sentinel. If negatives are allowed and a distinct window must always be
compared honestly, consider `float('-inf')` — but here the problem spec
explicitly wants 0 when no valid window exists, so 0 as the default is
actually correct per the problem statement (not just a lucky default).

### What can be improved?
Nothing algorithmically — O(n) time is optimal since every element must be
inspected at least once, and O(k) space is required to track distinctness
within a window of size k. This is the accepted optimal solution.
"""


def maximum_subarray_sum(nums: list[int], k: int) -> int:
    hset = set()
    start, max_sum, curr_sum = 0, 0, 0

    for end, num in enumerate(nums):
        while num in hset:
            hset.remove(nums[start])
            curr_sum -= nums[start]
            start += 1

        hset.add(num)
        curr_sum += num

        if end - start + 1 == k:
            max_sum = max(max_sum, curr_sum)
            curr_sum -= nums[start]
            hset.remove(nums[start])
            start += 1

    return max_sum


# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (check every window with a fresh set)
# ================================================================================
"""
### Thought Process 🧠
The most direct reading of the problem: for every possible starting index,
look at the next k elements, check if they're all distinct, and if so sum
them and compare to the running max.

### Idea
For each start index i (where a full window of size k fits), build a fresh
set from nums[i:i+k]. If `len(set) == k`, all elements are distinct, so
sum the window and update max_sum.

### Complexity
- TC: O(n*k) — n-k+1 windows, each costs O(k) to slice, set-build, and sum
- SC: O(k) — one window's worth of elements in the set at a time

### Pros
- Very easy to write and verify correctness against.
- No tricky two-pointer/eviction logic to get wrong.

### Cons
- O(n*k) — re-does all the work for overlapping windows from scratch,
  same wasted-work problem as the naive "max sum subarray of size k."

### Bottleneck
Every window shares (k-1) elements with its neighbor, but we throw all of
that away and rebuild from scratch each time. Ask: "can I incrementally
update the sum AND the distinctness check as the window slides by one?"
-> Yes: sliding window + hash set (the main approach above).
"""


def maximum_subarray_sum_brute(nums: list[int], k: int) -> int:
    n = len(nums)
    max_sum = 0
    for i in range(n - k + 1):
        window = nums[i:i + k]
        if len(set(window)) == k:
            max_sum = max(max_sum, sum(window))
    return max_sum


# ================================================================================
# ALTERNATIVE APPROACH — Hash Map with Last-Seen Index (direct jump)
# ================================================================================
"""
### Thought Process 🧠
The main approach evicts duplicates one element at a time via a `while`
loop. A common refinement (seen in "Longest Substring Without Repeating
Characters") is to remember the LAST INDEX each value was seen at, so when
a duplicate shows up we can jump `start` directly past it in O(1), instead
of removing elements one by one.

### Idea
Keep a dict `last_seen: value -> most recent index`. When `num` at index
`end` was last seen at an index >= `start`, jump `start` to
`last_seen[num] + 1` immediately (no loop needed). Maintain `curr_sum` by
re-deriving it from a prefix-sum array (or recompute the window sum
directly) since a direct jump skips the one-by-one subtraction the
eviction loop used to do for us.

### Complexity
- TC: O(n) — single pass; prefix sums make window-sum lookups O(1)
- SC: O(n) for prefix sums + O(k) for last_seen -> O(n) overall (or O(k)
  for last_seen alone if you recompute sums differently)

### Pros
- No `while` loop — `start` jumps directly, conceptually simpler to trace.
- Reuses a very well-known pattern (last-seen-index dedup), transferable
  to substring/subarray uniqueness problems generally.

### Cons
- Needs a prefix-sum array (or equivalent) to get O(1) window sums after a
  jump, since we can no longer rely on incrementally subtracting evicted
  elements one at a time -> slightly more setup, more space than the
  hash-set + running-sum version.
- Same Big-O as the main approach — this is a stylistic/pattern trade, not
  a complexity improvement.

### DSA Buddy Point 🧠
"'Evict one by one with a while loop' and 'jump directly via last-seen
index' are two flavors of the same idea — both are O(n) amortized. Pick
whichever is easier to reason about for the problem at hand; last-seen
index shines when the eviction target could be far away and iterating one
step at a time would be wasteful for OTHER problems (here, eviction is
already O(1) amortized, so this is mostly for pattern familiarity)."
"""


def maximum_subarray_sum_last_seen(nums: list[int], k: int) -> int:
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, num in enumerate(nums):
        prefix[i + 1] = prefix[i] + num

    last_seen = {}
    start = 0
    max_sum = 0

    for end, num in enumerate(nums):
        if num in last_seen and last_seen[num] >= start:
            start = last_seen[num] + 1
        last_seen[num] = end

        if end - start + 1 == k:
            window_sum = prefix[end + 1] - prefix[start]
            max_sum = max(max_sum, window_sum)
            start += 1  # slide forward by one for the next window

    return max_sum


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MAX SUM OF DISTINCT SUBARRAYS OF SIZE K
│
├── Brute Force
│   └── Fresh set + sum per window -> O(n*k)
│
├── Base Pattern (fix the waste)
│   └── Fixed-size sliding window (running sum, add right / drop left)
│       [same as plain "max sum subarray of size k"]
│
├── New Constraint
│   └── No duplicates allowed inside the window
│
├── How to Enforce It — Two Flavors
│   ├── Hash Set + while-loop eviction (one element at a time) -> O(n)
│   └── Hash Map of last-seen index + direct jump + prefix sums -> O(n)
│
├── After Dedup Check Passes
│   └── Same as base pattern: add num, check size == k, record max,
│       evict oldest / slide forward
│
└── Complexity (optimal versions)
    └── O(n) time (amortized — start only moves forward)
    └── O(k) space (hash set flavor) or O(n) space (prefix-sum flavor)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Fixed window + uniqueness constraint -> sliding window + hash set for
  membership tracking."
- "A `while` loop shrinking the window is still O(n) amortized as long as
  `start` never moves backward — each element is added/removed at most once."
- "Two separate reasons to shrink the window: (1) duplicate incoming
  element, (2) window reached target size k — don't conflate them."
- "This is 'max sum subarray of size k' with one extra guard clause, not a
  fundamentally different algorithm."
- "One-by-one eviction (while loop) and direct-jump (last-seen index) are
  both O(n) amortized — same complexity class, different bookkeeping style."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                       | Core Idea                                          | TC     | SC   | Pros                                  | Cons                                       | When to Use                        |
|-----------------------------------|-------------------------------------------------------|--------|------|------------------------------------------|-----------------------------------------------|----------------------------------------|
| Brute Force                       | Fresh set + sum per window                             | O(n*k) | O(k) | Trivial to write and verify              | Redoes overlapping work every window            | Baseline / correctness check only     |
| Sliding Window + Hash Set         | Running sum, while-loop evicts on duplicate            | O(n)   | O(k) | Simple, no extra prefix array needed     | While loop can look like it's not O(n) at a glance | Default optimal choice (your code)    |
| Hash Map (Last-Seen Index) + Prefix Sum | Jump start directly, O(1) window sum via prefix sums | O(n)   | O(n) | No while loop, transfers to other "distinct window" problems | Needs prefix-sum array, more setup/space | When you want the last-seen-index pattern for a related problem |
"""

# ================================================================================
# INTERVIEW SNAPSHOT
# ================================================================================
"""
- Pattern: Fixed-Size Sliding Window + Hash Set for distinctness (same
  family as "longest substring without repeating characters," but with a
  fixed window size instead of a growing one).
- Go-to answer: "Maintain a sliding window of running sum and a set of
  values currently in the window. Before adding a new element, shrink the
  window from the left while it already contains that value. Once the
  window is exactly size k, record the sum and slide forward as usual.
  O(n) time, O(k) space."
- Common follow-up: "What if k could vary, or we wanted the longest
  distinct-window instead of a fixed size?" -> That's the classic
  "longest substring without repeating characters" variable-window version.
"""