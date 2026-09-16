"""
================================================================================
 PROBLEM: Minimum Size Subarray Sum (LeetCode 209)
================================================================================
Given: a positive integer `target` and an array of POSITIVE integers `nums`.
Task: find the length of the shortest contiguous subarray whose sum is
>= target. Return 0 if no such subarray exists.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Are all elements of nums guaranteed positive? (Critical! The sliding
  window approach below ONLY works because sums are monotonically
  increasing as the window grows — negative numbers break that invariant)
- Is it "sum >= target" or "sum == target"? (This problem: >=, shortest
  qualifying subarray, not an exact match)
- What if no subarray reaches target? (Return 0, matches the given default)
- Can nums be empty? (Then answer is trivially 0)
"""

import math

# ================================================================================
# MY APPROACH — Variable-Size Sliding Window
# ================================================================================
"""
### Idea
Unlike a FIXED-size window (like "max sum subarray of size k"), this window
grows and shrinks based on a condition. Expand `end` to grow the window and
accumulate `curr`. Whenever `curr >= target`, the window is "valid" — record
its length, then GREEDILY shrink from the left (subtract `nums[start]`,
advance `start`) as long as it's still valid, since a shorter valid window
is always better than a longer one.

### Why does it work?
Because all elements are positive, `curr` only increases as `end` advances
and only decreases as `start` advances — there's no ambiguity about which
direction shrinks the sum. This monotonic property is exactly what allows
the `while` loop to safely shrink as far as possible every time the window
becomes valid, without ever needing to grow again to "recheck" a shrink.

### Complexity
- TC: O(n) — `start` and `end` each move forward at most n times total
  across the whole run (never backward), so total work is O(n) amortized
- SC: O(1) — just a few running scalars

### Pros
- Optimal time and space — single pass, no auxiliary structures.
- Greedy shrink-while-valid is a clean, provably-correct strategy here.

### DSA Buddy Point 🧠
"Variable-size window + 'shortest subarray satisfying a condition' ->
grow with `end`, and once valid, GREEDILY shrink from `start` while still
valid — you're looking for the tightest possible fit, so always try to
shrink whenever you can."

### What can be improved?
Nothing algorithmically for the general case — O(n) time is optimal since
every element must be inspected at least once. There IS an alternative
O(n log n) approach using prefix sums + binary search (see below) — it's
strictly worse here, but the underlying idea (binary search on a
monotonic prefix-sum array) generalizes to problems where a sliding
window WON'T work, e.g. if negative numbers were allowed.
"""


def min_sub_array_len(target: int, nums: list[int]) -> int:
    min_len = math.inf
    start, curr = 0, 0
    for end, num in enumerate(nums):
        curr += num
        while curr >= target:
            min_len = min(end - start + 1, min_len)
            curr -= nums[start]
            start += 1
    return 0 if min_len == math.inf else min_len


# ================================================================================
# ALTERNATIVE APPROACH — Brute Force
# ================================================================================
"""
### Thought Process 🧠
The most literal reading: try every possible starting index, and for each
one, keep extending the subarray rightward until the sum reaches target,
then record its length and move on.

### Idea
For each start index i, walk j from i onward, accumulating the sum. As
soon as the running sum >= target, record `j - i + 1` and break out — no
need to extend further for this particular start, since we already found
the shortest valid subarray starting at i.

### Complexity
- TC: O(n^2) — worst case, each of the n starting points scans up to n
  elements before finding a valid subarray (or hitting the end)
- SC: O(1) extra

### Pros
- Very easy to write and convince yourself of correctness.
- Good first-pass answer to show you understand the problem before
  optimizing.

### Cons
- Quadratic — re-scans overlapping elements across different starting
  points, doing no better than the naive complexity bound.

### Bottleneck
Every time `start` advances by one, we throw away all knowledge of what
the running sum was and rebuild it from scratch. Ask: "can I reuse the
work already done as the window slides, instead of restarting?" -> Yes:
maintain a running sum incrementally with a sliding window (the main
approach above), since elements are all positive.
"""


def min_sub_array_len_brute(target: int, nums: list[int]) -> int:
    n = len(nums)
    min_len = math.inf
    for i in range(n):
        curr = 0
        for j in range(i, n):
            curr += nums[j]
            if curr >= target:
                min_len = min(min_len, j - i + 1)
                break
    return 0 if min_len == math.inf else min_len


# ================================================================================
# ALTERNATIVE APPROACH — Prefix Sums + Binary Search
# ================================================================================
"""
### Thought Process 🧠
Since all elements are positive, the prefix-sum array is strictly
increasing — and a strictly increasing array is exactly what binary search
needs. This reframes "find the shortest valid subarray starting at i" into
"find the smallest index j such that prefix[j] >= prefix[i] + target",
which binary search answers in O(log n).

### Idea
1. Build `prefix[0..n]` where `prefix[i]` = sum of the first i elements.
2. For each start index i, we want the smallest j > i such that
   `prefix[j] - prefix[i] >= target`, i.e. `prefix[j] >= prefix[i] + target`.
   Binary search for that threshold in the prefix array (it's sorted since
   all elements are positive).
3. If found, candidate length is `j - i`; track the minimum across all i.

### Complexity
- TC: O(n log n) — n starting points, each doing an O(log n) binary search
- SC: O(n) — the prefix-sum array

### Pros
- Demonstrates the binary-search-on-monotonic-array pattern, which
  generalizes to variants where a two-pointer window doesn't directly
  apply (e.g. "shortest subarray with sum in a range" type problems, or
  once you've already built prefix sums for another part of a larger
  problem).
- No `while`-loop shrink logic to reason about — just a clean binary
  search call per index.

### Cons
- Strictly worse than the sliding window here: O(n log n) vs O(n), and
  O(n) space vs O(1). The two-pointer version is always the better choice
  when it applies (i.e. whenever monotonicity from positive-only elements
  holds).

### DSA Buddy Point 🧠
"Positive-only elements -> prefix sums are monotonic -> binary search
becomes an option. But if a sliding window ALSO applies (same positivity
requirement), the window is strictly cheaper — binary search here is
mostly useful as a technique to have in your pocket for problems where
the two-pointer trick breaks down."
"""


def min_sub_array_len_binary_search(target: int, nums: list[int]) -> int:
    from bisect import bisect_left
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, num in enumerate(nums):
        prefix[i + 1] = prefix[i] + num

    min_len = math.inf
    for i in range(n):
        needed = target + prefix[i]
        j = bisect_left(prefix, needed, i + 1)
        if j <= n:
            min_len = min(min_len, j - i)
    return 0 if min_len == math.inf else min_len


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MINIMUM SIZE SUBARRAY SUM
│
├── Brute Force
│   └── For each start, extend right until sum >= target -> O(n^2)
│
├── Bottleneck
│   └── Running sum rebuilt from scratch for every starting index
│
├── Key Observation
│   └── All elements POSITIVE -> running sum only grows as window grows,
│       only shrinks as window shrinks -> fully monotonic
│
├── Path A — Variable-Size Sliding Window
│   └── Grow with `end`; once sum >= target, GREEDILY shrink from `start`
│       while still valid, recording length each time
│       └── O(n) time, O(1) space  <-- optimal, your code
│
└── Path B — Prefix Sums + Binary Search
    └── Prefix sums monotonic (positives only) -> binary search for the
        smallest valid end index per start index
        └── O(n log n) time, O(n) space  <-- valid but strictly worse here
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Shortest subarray satisfying a sum condition + all positive elements ->
  variable-size sliding window, greedy shrink whenever valid."
- "Greedy shrink is safe here because BOTH growing and shrinking move the
  sum in one predictable direction — no need to 're-grow' after shrinking
  too far, since we stop shrinking the moment it becomes invalid."
- "Positive-only array -> prefix sums are strictly increasing -> binary
  search becomes an option, but it's a fallback pattern, not the first
  choice when sliding window applies."
- "This is a VARIABLE-size window (like 'longest substring without
  repeating chars'), not a FIXED-size window (like 'max sum subarray of
  size k') — the growth/shrink logic is driven by a condition, not a
  fixed k."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                        | Core Idea                                           | TC         | SC   | Pros                                    | Cons                                         | When to Use                          |
|-------------------------------------|----------------------------------------------------------|------------|------|---------------------------------------------|--------------------------------------------------|-------------------------------------------|
| Brute Force                         | For each start, extend right until sum >= target            | O(n^2)     | O(1) | Trivial to write/verify                      | Redoes running-sum work for every start           | Baseline / correctness check only         |
| Prefix Sums + Binary Search         | Binary search smallest valid end per start on sorted prefix | O(n log n) | O(n) | Generalizes to problems 2-pointer can't solve | Strictly worse here than sliding window            | When two-pointer monotonicity breaks down |
| Variable-Size Sliding Window        | Grow with end, greedily shrink from start while valid       | O(n)       | O(1) | Optimal time AND space                       | Only valid when all elements are positive          | Default optimal choice (your code)        |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Variable-Size Sliding Window (same family as "longest substring
  without repeating characters," but here we're minimizing length under a
  sum condition instead of maximizing it under a distinctness condition).
- Go-to answer: "Since all elements are positive, the running sum is
  monotonic as the window grows or shrinks. Expand the window with `end`;
  every time the sum reaches target, greedily shrink from `start` while it
  stays valid, tracking the minimum length seen. O(n) time, O(1) space."
- Mention prefix-sum + binary search only as a fallback pattern for
  variants where positivity/monotonicity doesn't hold cleanly for a
  two-pointer approach — shows range of technique, but flag it as
  strictly worse for THIS exact problem.
- Common follow-up: "What if negative numbers were allowed?" -> The
  sliding window breaks (sum isn't monotonic anymore); you'd typically
  need a different technique (e.g. a monotonic deque on prefix sums for
  the related "shortest subarray with sum at least K" — LC 862).
"""