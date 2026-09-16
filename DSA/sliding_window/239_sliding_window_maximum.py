"""
================================================================================
 PROBLEM: Sliding Window Maximum (LeetCode 239)
================================================================================
Given: an array `nums` and a window size `k`.
Task: return an array of the maximum value in each contiguous window of
size k as it slides from left to right across `nums`.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is k guaranteed to be <= len(nums) and >= 1? (Confirm before coding)
- Can nums contain negative numbers or duplicates? (Yes to both — the
  monotonic deque approach handles this fine)
- Output length should be len(nums) - k + 1 — good sanity check to mention.
"""

from collections import deque

# ================================================================================
# MY APPROACH — Monotonic Decreasing Deque (store indices)
# ================================================================================
"""
### Idea
Keep a deque of INDICES (not values) such that the values at those indices
are always in decreasing order from front to back. The front of the deque
is therefore always the index of the current window's maximum.

As `end` advances:
1. Pop from the BACK any index whose value is <= nums[end] — those values
   can never be the max again once a bigger (or equal) number has shown up
   to their right, since nums[end] will outlive them in every future
   window they're both part of. This keeps the deque strictly decreasing.
2. Push `end` onto the back.
3. Once the window has grown to size k, the front of the deque is the
   current max — record `nums[queue[0]]`.
4. If the front index is about to fall OUTSIDE the window (i.e. it equals
   `start`), pop it from the front before sliding `start` forward.

### Why does it work?
Any index whose value is smaller than a later index's value, and which
appears earlier in the array, can NEVER be the answer for any future
window — the larger, later value will always be in the window whenever
the smaller one still is (until the smaller one ages out), and it's
bigger. So it's safe to permanently discard such indices. This pruning is
what keeps the deque small and the front always correct.

### Complexity
- TC: O(n) — each index is pushed onto the deque exactly once and popped
  at most once (either from the back during pruning, or from the front
  when it ages out of the window) — amortized O(1) per element
- SC: O(k) — the deque holds at most k indices at any time (strictly
  decreasing values, all within the current window)

### Pros
- Optimal time — each element does O(1) amortized work.
- No recomputation of the window's max from scratch on each slide.

### DSA Buddy Point 🧠
"Monotonic deque = 'keep only the candidates that could still win.' Any
index whose value loses to something appearing later and staying in the
window longer is permanently useless — throw it away immediately."

### What can be improved?
Nothing algorithmically — O(n) time is optimal since every element must be
looked at at least once, and a monotonic deque is the standard optimal
structure for this "sliding window max/min" family of problems.
"""


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    start, end = 0, 0
    queue = deque([])
    output = []
    while end < len(nums):
        while queue and nums[end] >= nums[queue[-1]]:
            queue.pop()
        queue.append(end)

        if end - start + 1 == k:
            max_ = queue[0]
            output.append(nums[max_])
            if start == queue[0]:
                queue.popleft()
            start += 1
        end += 1
    return output


# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (recompute max per window)
# ================================================================================
"""
### Thought Process 🧠
The most direct reading: for every window position, just scan its k
elements and take the max.

### Idea
For each start index i where a full window fits, compute
`max(nums[i:i+k])` directly and append it to the output.

### Complexity
- TC: O(n*k) — n-k+1 windows, each scanned in O(k)
- SC: O(1) extra (ignoring the output list)

### Pros
- Trivial to write and reason about — good baseline / sanity check.

### Cons
- Re-scans overlapping elements across windows — wasted work whenever
  windows share most of their elements.

### Bottleneck
Each window overlaps its neighbor in (k-1) elements, but we throw away
all knowledge of "who was the max" between slides. Ask: "can I maintain a
small set of 'still could be the max' candidates instead of rescanning
everything?" -> Yes: the monotonic deque above, which discards elements
that can never win again.
"""


def max_sliding_window_brute(nums: list[int], k: int) -> list[int]:
    n = len(nums)
    output = []
    for i in range(n - k + 1):
        output.append(max(nums[i:i + k]))
    return output

class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        start = 0
        end = start + k
        output = []
        while end <= len(nums):
            output.append(max(nums[start:end]))
            start += 1
            end = start + k
        return output

class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        start = 0
        queue = deque([])
        output = []
        for start in range(len(nums)):
            queue.append(nums[start])
            if len(queue) == k:
                output.append(max(queue))
                queue.popleft()
        return output


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
SLIDING WINDOW MAXIMUM
│
├── Brute Force
│   └── Rescan k elements per window -> O(n*k)
│
├── Bottleneck
│   └── Overlapping windows share (k-1) elements, but max is recomputed
│       from scratch every time
│
├── Key Observation
│   └── A smaller value that appears BEFORE a bigger value can never be
│       the max again — it's permanently "beaten" once outlived
│
├── Optimization
│   └── Monotonic Decreasing Deque (store indices)
│       ├── Pop from back while new value >= deque's back value (prune losers)
│       ├── Push new index to back
│       ├── Front of deque = current window's max
│       └── Pop from front when it ages out of the window (index == start)
│
└── Complexity
    └── O(n) time (amortized — each index pushed & popped at most once)
    └── O(k) space (deque holds at most k indices)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Sliding window MAX/MIN -> think monotonic deque, not a heap or a
  fresh scan per window."
- "Store INDICES in the deque, not values — you need the index to know
  when an element ages out of the window."
- "Prune from the back: anything smaller than (or equal to) the incoming
  value can never win again — discard it immediately, permanently."
- "Evict from the front: only when the front index equals the window's
  leaving edge (start) — that's the only reason to pop from the front."
- "Amortized O(n): even though there are two inner operations (pop back,
  pop front), each index is added once and removed at most once total."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                  | Core Idea                                    | TC     | SC   | Pros                          | Cons                                | When to Use                       |
|-----------------------------|--------------------------------------------------|--------|------|---------------------------------|----------------------------------------|---------------------------------------|
| Brute Force                 | Rescan k elements, take max, per window            | O(n*k) | O(1) | Trivial to write/verify          | Redoes overlapping work every window   | Baseline / correctness check only    |
| Monotonic Decreasing Deque  | Maintain only "still could win" candidates         | O(n)   | O(k) | Optimal time, amortized O(1)/elem | Requires careful index-based bookkeeping | Default optimal choice (your code)   |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Monotonic Deque (same family as "next greater element,"
  "longest subarray with max - min <= limit").
- Go-to answer: "Maintain a deque of indices with strictly decreasing
  values. On each step, prune the back while the new value is >= the
  back's value, push the new index, and pop the front if it's aged out of
  the window. The front is always the current window's max. O(n) time,
  O(k) space."
- Good to mention brute force (O(n*k)) first if asked to think out loud,
  then explain WHY it's wasteful (rescanning shared elements) before
  introducing the deque as the fix.
- Common follow-up: "What about sliding window MINIMUM?" -> Same idea,
  just flip to a monotonic INCREASING deque (prune back while new value
  <= back's value).
"""