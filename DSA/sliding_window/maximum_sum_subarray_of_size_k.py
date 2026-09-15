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

from collections import deque  # needed for the deque-based alternative below

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
# ALTERNATIVE APPROACH — Deque as the Window (looks like sliding window, isn't)
# ================================================================================
"""
### Thought Process 🧠
A very common instinct: "sliding window -> use a deque to represent the
window." It's the right data structure *family*, but here it's used to
just hold the elements rather than to track a running aggregate — so we
still end up re-summing the window every time it's full.

### Idea
Push each new element onto a deque. Once the deque reaches size k, take
`sum(queue)` to get the current window's total, compare against `max_sum`,
then pop the oldest element off the left before continuing.

### Why it's tempting
- `deque` gives O(1) appendleft/append/popleft, so it *feels* efficient.
- It visually mirrors the sliding window shape (grow right, shrink left).

### Where it goes wrong
`sum(queue)` is NOT O(1) — it's O(k), because it re-iterates over every
element currently in the deque. That call happens once per window, and
there are roughly (n - k + 1) windows, so total work is O(n*k) — no better
than the brute-force "recompute each window from scratch" approach. The
deque's O(1) push/pop is wasted because the sum is recomputed anyway.

### Complexity
- TC: O(n*k) — `sum(queue)` costs O(k), called ~n times
- SC: O(k) — the deque holds up to k elements

### Pros
- Structurally very close to the optimal solution — easy to fix (see below).
- Deque handles the "drop oldest / add newest" bookkeeping cleanly.

### Cons
- No better than brute force time-wise, despite "looking" optimized.
- Extra O(k) space for the deque, vs O(1) for the running-sum version.

### The Fix 🔧
Keep the deque's add/drop bookkeeping, but ALSO maintain a running
`curr_sum`, exactly like the running-sum version — add `num` to `curr_sum`
on push, subtract the popped value from `curr_sum` on pop. Then `max_sum`
comparisons become O(1) instead of O(k). That turns this exact structure
into the optimal O(n) solution — the queue becomes bookkeeping only, not
the thing being summed each time.

### DSA Buddy Point 🧠
"A deque makes push/pop O(1), but if you still call sum() on it every
time, you've only moved the O(k) cost around — not eliminated it. The
data structure isn't the optimization; tracking a running total is."
"""


def max_subarray_sum_deque(arr: list[int], k: int) -> int:
    max_sum, curr_sum = 0, 0
    queue = deque()

    for end, num in enumerate(arr):
        queue.append(num)
        if len(queue) == k:
            max_sum = max(max_sum, sum(queue))
            queue.popleft()
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
├── Tempting Detour
│   └── Deque holding the window elements, call sum(queue) each time
│       └── O(1) push/pop, but sum(queue) is O(k) -> still O(n*k) overall
│       └── Data structure changed, but the recompute-per-window cost didn't
│
├── Optimization
│   └── Sliding Window: add new element on the right, drop oldest on the
│       left once window size == k, using a RUNNING SUM (not re-summing)
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
- "O(1) push/pop on a deque doesn't save you if you still sum() it every
  time — check what happens INSIDE the loop body, not just the structure."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                  | Core Idea                                  | TC     | SC   | Pros                              | Cons                                  | When to Use                       |
|-----------------------------|-----------------------------------------------|--------|------|------------------------------------|------------------------------------------|--------------------------------------|
| Deque + sum(queue)          | Deque holds window, re-sum it each time         | O(n*k) | O(k) | Clean add/drop bookkeeping         | Re-sums window every time — no better than brute force | Only if you stop halfway and forget the running total |
| Sliding Window (running sum)| Running sum, add on entry, subtract on exit    | O(n)   | O(1) | Optimal time AND space             | None significant                          | Default optimal choice (your code)   |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Fixed-Size Sliding Window (same family as "average of subarrays
  of size k", "max/min of every window of size k").
- Go-to answer: "Maintain a running window sum — add the incoming element,
  and once the window reaches size k, record the sum and subtract the
  outgoing element before sliding forward. O(n) time, O(1) space."
- If you reach for a deque first, that's fine as a starting structure — just
  make sure you're tracking a running sum alongside it, not calling sum()
  on the whole window every iteration, or you've quietly regressed to O(n*k).
- Common follow-up: "What if k varies, or it's 'at most k' instead of
  exactly k?" -> That shifts to a *variable-size* sliding window (two
  pointers where both can move independently based on a condition), a
  related but distinct pattern.
"""