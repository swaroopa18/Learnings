"""
================================================================================
 PROBLEM: Maximum Sum Subarray of Size K
================================================================================
Given: an array `arr` and an integer `k`.
Task: find the maximum sum of any contiguous subarray of exactly size k.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can arr contain negative numbers? (If yes, `max_sum` should NOT start at 0
  — see "Edge Case" note below)
- Is k guaranteed to be <= len(arr)? (If not, need a length check up front)
- Exactly size k, or "at most k" / "at least k"? (This problem: exactly k)
- What should be returned if arr is empty or k <= 0? (Usually 0 or invalid input)
"""

# ================================================================================
# MY APPROACH — Fixed-Size Sliding Window
# ================================================================================
"""
### Idea
Instead of recomputing the sum of every k-length window from scratch, keep a
running `curr_sum` for the current window. As the window slides forward by
one element (`end` moves right), add the new element and, once the window
has grown to size k, subtract the element that's falling out of the window
on the left (`start`) before advancing `start`.

### Why does it work?
Each element enters the window exactly once (added at `curr_sum += num`) and
leaves exactly once (subtracted at `curr_sum -= arr[start]`). So instead of
paying O(k) to sum each window separately, each element is touched O(1)
times total across the whole scan — classic sliding window amortization.

### Complexity
- TC: O(n) — each element added once and removed once, single pass
- SC: O(1) — only a few running scalars, no extra array

### Pros
- Optimal time and space — can't do better than O(n) since every element
  must be looked at at least once.
- Clean incremental update — no recomputation of sums.

### DSA Buddy Point 🧠
"Fixed-size window -> maintain a running sum, add on the right, drop on the
left once the window is 'full' (size == k)."

### Edge Case ⚠️
`max_sum` is initialized to 0. This is only safe if all array elements are
guaranteed non-negative (so the true max subarray sum is never negative).
If negative numbers are allowed, initialize `max_sum = float('-inf')`
instead, or seed it with the sum of the first window — otherwise a valid
but negative-sum window could be masked by the default 0.

### What can be improved?
Nothing algorithmically — O(n) time / O(1) space is optimal for this
problem, since a naive approach (recompute each window's sum from scratch)
would cost O(n*k). The only real refinement is hardening the edge case
above for negative-number inputs.
"""


def max_subarray_sum(arr: list[int], k: int) -> int:
    start = 0
    max_sum, curr_sum = 0, 0

    for end, num in enumerate(arr):
        curr_sum += num
        if end - start + 1 == k:
            max_sum = max(max_sum, curr_sum)
            curr_sum -= arr[start]
            start += 1
    return max_sum


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MAX SUM SUBARRAY OF SIZE K
│
├── Naive Idea
│   └── For each window start, sum k elements from scratch
│       └── O(n*k) time — wasteful re-summing of overlapping elements
│
├── Observation
│   └── Consecutive windows overlap in (k-1) elements — no need to re-add them
│
├── Optimization
│   └── Sliding Window: add new element on the right, drop oldest on the
│       left once window size == k
│       └── O(n) time, O(1) space
│
└── Watch Out
    └── max_sum init value matters if negatives are allowed
        (use float('-inf') or seed with first window's sum)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Fixed window size -> sliding window with a running sum, not recomputation."
- "Add on entry (right), subtract on exit (left) — each element touched once."
- "O(n*k) naive -> O(n) sliding window whenever overlapping work is being
  redone across shifts."
- "Default max_sum = 0 is a trap if negative numbers are allowed — use
  -infinity or seed with the first window instead."
"""

# ================================================================================
# INTERVIEW SNAPSHOT
# ================================================================================
"""
- Pattern: Fixed-Size Sliding Window (same family as "average of subarrays
  of size k", "max/min of every window of size k").
- Go-to answer: "Maintain a running window sum — add the incoming element,
  and once the window reaches size k, record the sum and subtract the
  outgoing element before sliding forward. O(n) time, O(1) space."
- Common follow-up: "What if k varies, or it's 'at most k' instead of
  exactly k?" -> That shifts to a *variable-size* sliding window (two
  pointers where both can move independently based on a condition), a
  related but distinct pattern.
"""