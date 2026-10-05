"""
================================================================================
 PROBLEM: Next Greater Element II (LeetCode 503)
================================================================================
Given a CIRCULAR integer array `nums` (the next element of `nums[n-1]` is
`nums[0]`), return an array `ans` where `ans[i]` is the next greater number
for `nums[i]`. The next greater number of `x` is the first number strictly
greater than `x` found by traversing the array circularly starting from the
element after `x`. If none exists, `ans[i] = -1`.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is "greater" STRICT? (Yes — equal values do NOT count. This decides whether
  the stack pops on `<` or `<=` and is the #1 off-by-one-style bug here.)
- Is the array truly circular, so we may wrap around past the end to find the
  answer? (Yes — this is the only difference from LC 496 / "Next Greater
  Element I"; it is what forces the 2n traversal trick.)
- Can there be duplicates / a single element / all-equal elements? (Yes to
  all — a single element or all-equal array gives all -1, because an element
  never counts as its own "next greater" even after a full lap.)
- Do I return values or indices? (Values — but the stack should hold INDICES
  so we know which `ans` slot to fill.)

"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "NEXT GREATER ELEMENT" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   "Next greater to the right" = MONOTONIC (decreasing) STACK.       │
    │   Elements WAITING for their answer sit on the stack. The moment    │
    │   a bigger value arrives, it is the answer for every smaller        │
    │   waiting element on top — pop them all and fill their answers.     │
    │   CIRCULAR? Just walk the array TWICE (2n steps, index = i % n).    │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

This is the classic monotonic-stack pattern (same family as Daily
Temperatures, Next Greater Element I, Stock Span, Largest Rectangle in
Histogram) with ONE twist for circularity. Key ideas:

1. **The stack holds indices of elements that have NOT found their answer
   yet, and their values are non-increasing from bottom to top.** Any new
   value that is bigger than the top resolves the top; keep popping until the
   top is >= the new value (strict "greater" => pop only on `<`).

2. **Each index is pushed once and popped at most once => O(n) total,** even
   though there is a `while` inside the `for`. Amortized analysis, not
   O(n^2).

3. **Circular trick: loop `i` from 0 to 2n-1 and use `idx = i % n`.** The
   first lap handles "greater element to the right"; the second lap lets
   still-unresolved elements see everything that sits to their LEFT (which is
   to their right after wrapping). Two laps are always enough: after one full
   wrap every element has been compared against every other element.

4. **Only PUSH during the first lap (`i < n`).** In the second lap we only
   want to resolve leftovers. Pushing again would just add duplicate stack
   entries that can never produce a new answer.

5. **Anything left on the stack after 2n steps keeps `-1`** — those are the
   maximum value(s) of the array: nothing strictly greater exists anywhere.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
For each element, walk forward up to n-1 steps (wrapping around with `%`)
until you find something bigger. Easy, but each element may scan the whole
array -> O(n^2).

### The key insight: share work between neighbours
If `5` is waiting for something bigger and `3` is also waiting right after
it, then whatever finally beats `5` ALSO beats `3`. So waiting elements form
a stack where the smallest/newest is on top; one big arrival can settle many
of them at once. That is why we never re-scan.

### Step-by-step trace: nextGreaterElements([1, 2, 1])   (n = 3)
```
i=0 idx=0 val=1 : stack empty                 -> push 0         stack=[0]
i=1 idx=1 val=2 : nums[0]=1 < 2 -> pop 0, ans[0]=2
                                              -> push 1         stack=[1]
i=2 idx=2 val=1 : nums[1]=2 < 1? no           -> push 2         stack=[1,2]
--- second lap (no pushes) ---
i=3 idx=0 val=1 : nums[2]=1 < 1? no (STRICT)  -> nothing
i=4 idx=1 val=2 : nums[2]=1 < 2 -> pop 2, ans[2]=2   (wrapped around!)
                  nums[1]=2 < 2? no           -> stop
i=5 idx=2 val=1 : nums[1]=2 < 1? no           -> nothing
leftover stack=[1] -> ans[1] stays -1 (2 is the max)
ans = [2, -1, 2] ✅
```

### The "aha" moment to remember 🎯
"Next greater / next smaller / span / temperature wait-days" => think
MONOTONIC STACK of unresolved indices. Circular => iterate 2n with `% n` and
only push in the first lap. Decide strict vs non-strict by re-reading the
problem statement every time.
"""

# ================================================================================
# ALTERNATIVE APPROACH 1 — Brute Force (circular scan per element)
# ================================================================================
"""
### Thought Process 🧠
For each i, check j = i+1, i+2, ..., i+n-1 (mod n) and take the first
`nums[j] > nums[i]`.

### Complexity
- TC: O(n^2) — worst case (e.g. strictly decreasing, or all equal) scans
  n-1 elements for each of n positions
- SC: O(1) extra (ignoring output)

### Pros
- Trivially correct; perfect baseline for validating the fast solution.

### Cons
- n up to 10^4 -> ~10^8 steps worst case; too slow in an interview setting
  and wastes the overlap between neighbours' searches.

### Bottleneck
Each element re-searches from scratch even though neighbouring searches
overlap heavily. Ask: "can one big value settle many earlier elements at
once?" -> Yes: monotonic stack.
"""


def next_greater_elements_brute(nums: list[int]) -> list[int]:
    n = len(nums)
    ans = [-1] * n
    for i in range(n):
        for step in range(1, n):
            j = (i + step) % n
            if nums[j] > nums[i]:
                ans[i] = nums[j]
                break
    return ans


# ================================================================================
# ALTERNATIVE APPROACH 2 — Physically Double the Array + Monotonic Stack
# ================================================================================
"""
### Thought Process 🧠
Build `doubled = nums + nums`, run the standard (non-circular) next-greater
stack over it, then keep only the first n answers. The wrap-around is now
"just" elements further to the right in a longer array.

### Complexity
- TC: O(n) — 2n elements, each pushed/popped once
- SC: O(n) — extra 2n-length array + stack + answer array

### Pros
- Conceptually the easiest to explain: "circular -> linearize by doubling".
- Reuses the exact non-circular template with zero modifications.

### Cons
- Allocates a copy of the input (2x memory) for no real benefit; the
  `i % n` trick gives the same effect without copying.
- Must remember to truncate the result to the first n entries.

### DSA Buddy Point 🧠
"Circular array => either double it physically or double it virtually with
`% n`. Prefer the virtual version once you are comfortable — same logic,
less memory."
"""


def next_greater_elements_doubled(nums: list[int]) -> list[int]:
    n = len(nums)
    doubled = nums + nums
    ans = [-1] * (2 * n)
    stack = []
    for i, v in enumerate(doubled):
        while stack and doubled[stack[-1]] < v:
            ans[stack.pop()] = v
        stack.append(i)
    return ans[:n]


# ================================================================================
# MY APPROACH — Monotonic Stack over 2n Virtual Steps (optimal)
# ================================================================================
"""
### Idea
Walk `i` from 0 to 2n-1 with `idx = i % n`. The stack stores indices of
elements still waiting for a strictly greater value. For each `nums[idx]`,
pop and answer every waiting index whose value is smaller. Push `idx` only
during the first lap so the second lap just resolves leftovers.

### Complexity
- TC: O(n) — each index is pushed once and popped at most once; the loop
  runs 2n times
- SC: O(n) — stack (up to n entries) + answer array

### Pros
- Optimal time, no copy of the input, tiny code.
- Stack of INDICES lets us write directly into `ans[...]` without a
  value->index lookup.
- Handles duplicates correctly because the pop condition is STRICT `<`.

### Cons
- The wrap-around logic (`i % n`, push only when `i < n`) is easy to get
  subtly wrong; forgetting the "push only in lap 1" guard won't break the
  output but silently wastes stack space and confuses the reasoning.
- Amortized (not per-step) O(1) — the inner `while` can pop many at once,
  which sometimes looks like O(n^2) to a reader at first glance.

### DSA Buddy Point 🧠
"Whenever a problem asks 'first element to the right that is bigger/smaller',
reach for a monotonic stack of unresolved indices. Circular => iterate 2n
with modulo."

### What can be improved?
Complexity-wise nothing — O(n) time is optimal (must read every element).
One small code fix to the version you wrote: the guard `if idx < n:` is
ALWAYS true (idx = i % n is always < n), so it never skips a push. It should
be `if i < n:`. The output is still correct (the extra second-lap pushes are
harmless, since they can only be popped by the same elements that already
answered them), but the intended behaviour — "push only in the first lap" —
needs `i < n`. The fixed version is the one below.
"""


class Solution:
    def nextGreaterElements(self, nums: list[int]) -> list[int]:
        n = len(nums)
        stack = []
        ans = [-1] * n

        for i in range(2 * n):
            idx = i % n
            while stack and nums[stack[-1]] < nums[idx]:
                ans[stack.pop()] = nums[idx]
            if i < n:  # push only during the first lap
                stack.append(idx)

        return ans


# ================================================================================
# ALTERNATIVE APPROACH 3 — Traverse Right-to-Left over 2n-1..0 (Stack of Values)
# ================================================================================
"""
### Thought Process 🧠
Go backwards. The stack holds CANDIDATE answers (values) for the elements to
the left. For each element, pop every candidate that is `<= nums[idx]`
(they can never be a "next greater" for anything further left, since the
current element is at least as big AND closer). After popping, the top of the
stack (if any) is the answer. Then push the current value. Start at i = 2n-1
so the stack is pre-warmed with the circular "right side", but only record
answers when `i < n`.

### Complexity
- TC: O(n) — each value pushed/popped at most once across 2n steps
- SC: O(n) — stack + answer array

### Pros
- Answer is read straight off the stack top — no write-back into earlier
  slots, no "leftover" cleanup; unresolved elements naturally get -1.
- Same pattern as the "previous greater" / "span" problems when mirrored.

### Cons
- Pop condition is `<=` here (candidates equal to the current value are
  useless) but `<` in the forward version — easy to mix the two up.
- Backward + circular is harder to reason about than forward + circular
  for most people.

### DSA Buddy Point 🧠
"Forward stack = waiting ELEMENTS that get resolved later. Backward stack =
surviving CANDIDATES that answer the current element immediately. Same
complexity, mirrored bookkeeping and mirrored strictness (`<` vs `<=`)."
"""


def next_greater_elements_backward(nums: list[int]) -> list[int]:
    n = len(nums)
    ans = [-1] * n
    stack = []  # candidate values, decreasing from bottom to top
    for i in range(2 * n - 1, -1, -1):
        idx = i % n
        while stack and stack[-1] <= nums[idx]:
            stack.pop()
        if i < n:
            ans[idx] = stack[-1] if stack else -1
        stack.append(nums[idx])
    return ans


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
NEXT GREATER ELEMENT II (CIRCULAR)
│
├── Brute Force
│   └── For each i, scan up to n-1 elements circularly -> O(n^2)
│
├── Bottleneck
│   └── Neighbouring scans overlap; the same bigger value settles many
│       earlier elements, but brute force finds it again and again
│
├── Key Insight
│   └── Keep a MONOTONIC stack of unresolved indices; one larger value pops
│       and answers all smaller waiting ones. Circular => walk 2n with % n
│
├── Doubled Array + Stack
│   └── nums + nums, standard stack, truncate to n -> O(n) time, O(n) extra
│
├── My Approach — Virtual 2n Pass + Forward Stack (BEST)
│   └── idx = i % n, pop while nums[top] < nums[idx], push only if i < n
│       -> O(n) time, O(n) space, no input copy
│       -> STRICT `<` because "greater" is strict
│
└── Backward Pass + Candidate-Value Stack
    └── i from 2n-1 down to 0, pop while top <= cur, answer = top or -1
        -> O(n) time, O(n) space, `<=` pop (mirror of forward strictness)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'Next greater/smaller element' is a monotonic-stack problem: the stack
  holds elements still WAITING for an answer, and each new element settles
  every smaller one on top."
- "Circular array => iterate 2n times with `i % n` (virtual doubling). Two
  laps are enough because after a full wrap every element has been compared
  with every other."
- "Push only in the FIRST lap (`i < n`), NOT `idx < n` — `idx` is always
  < n, so that guard would be a silent no-op."
- "Strict vs non-strict matters: forward stack pops on `<` (equal values do
  not count as greater), backward stack pops on `<=`. Re-derive it from the
  problem statement each time."
- "Total work is O(n) despite the nested loop: every index is pushed once and
  popped at most once (amortized analysis)."
- "Whatever remains on the stack at the end are the array's maximum
  value(s) -> their answer stays -1."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                         | Core Idea                                            | TC     | SC   | Pros                                         | Cons                                              | When to Use                         |
|----------------------------------|------------------------------------------------------|--------|------|----------------------------------------------|---------------------------------------------------|-------------------------------------|
| Brute Force                      | For each i, scan circularly until a bigger value      | O(n^2) | O(1) | Trivial, great for validating                | Too slow, repeats overlapping work                | Baseline / correctness check        |
| Doubled Array + Stack            | Build nums+nums, run standard next-greater stack      | O(n)   | O(n) | Easiest to explain; reuses non-circular code | Copies input (2x memory), must truncate           | Teaching / first working solution   |
| Virtual 2n Pass + Forward Stack  | i in [0,2n), idx=i%n, push only when i<n              | O(n)   | O(n) | Optimal, no copy, tiny code                  | Wrap/guard logic easy to get subtly wrong         | Default optimal choice (your code)  |
| Backward Pass + Value Stack      | i from 2n-1 to 0, pop <=, answer = stack top          | O(n)   | O(n) | Answer read directly, no leftover cleanup    | `<=` vs `<` mirror is error-prone, harder to reason| Alternative when asked "other way?" |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Monotonic Stack (Next Greater Element family) + circular
  traversal via doubled/modulo indexing — same family as LC 496, LC 739
  (Daily Temperatures), LC 901 (Stock Span), LC 84 (Largest Rectangle).
- Go-to answer: "Use a monotonic decreasing stack of indices. Iterate i from
  0 to 2n-1 with idx = i % n; while the stack top's value is strictly less
  than nums[idx], pop it and set its answer to nums[idx]. Push idx only in
  the first lap. Leftovers stay -1. O(n) time, O(n) space."
- Good to call out: why 2n is enough, why the pop is strict `<`, and why
  the push is guarded by `i < n` (not `idx < n`).
- Common follow-up: "Can you do it without a stack?" -> Brute force
  O(n^2) or a jump-pointer trick (follow `ans` chains: `j = ans_index[j]`
  to skip already-known smaller elements) — but the stack is the intended
  and cleanest O(n) answer. Another: "Return INDICES / distances instead of
  values?" -> store `idx` (or `(j - i) % n`) in `ans` instead of the value.
"""