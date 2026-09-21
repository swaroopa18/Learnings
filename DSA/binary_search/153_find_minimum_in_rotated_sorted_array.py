"""
================================================================================
 PROBLEM: Find Minimum in Rotated Sorted Array (LeetCode 153)
================================================================================
Given: an array of DISTINCT integers, originally sorted ascending, then
rotated at some unknown pivot (e.g. [0,1,2,4,5,6,7] rotated 4 times
becomes [4,5,6,7,0,1,2]). Return the MINIMUM element. Must run in
O(log n) time.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Are all elements distinct? (Yes for LC 153 — LC 154 is the "with
  duplicates" variant, which needs different handling)
- Could the array be un-rotated (rotated by 0, or the same as rotating by
  n)? (Yes — must return nums[0] correctly in that case too)
- Is O(log n) required, or would O(n) be acceptable? (O(log n) is the
  whole point — this is a warm-up / building block for "Search in
  Rotated Sorted Array," LC 33)
"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR ROTATED SORTED ARRAY PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Compare nums[mid] to nums[r] — NEVER nums[l].                    │
    │   nums[mid] > nums[r]  -> the seam is still AHEAD -> l = mid + 1   │
    │   nums[mid] <= nums[r] -> mid is already past the seam -> r = mid  │
    │                            (NOT mid - 1 — mid could BE the answer) │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

Memorize these as REFLEXES for any rotated-sorted-array problem:

1. **Rotation = exactly ONE seam.** A big value immediately followed by a
   smaller one, exactly once in the whole array. Every rotated-array
   binary search is really just "figure out which side of that seam
   you're on."

2. **Compare to nums[r], not nums[l].** `nums[mid] > nums[r]` is an
   unambiguous signal that the seam is still to the right — values can
   only "reset downward" once, so if mid is bigger than the rightmost
   value, the reset hasn't happened yet within [mid, r].

3. **`r = mid`, never `mid - 1`, when nums[mid] <= nums[r].** mid itself
   might BE the minimum — shrinking with `mid - 1` risks throwing away
   the correct answer. Contrast this with mySqrt's `r = mid - 1`, which
   was safe there because mid had already been PROVEN wrong (too big).

4. **Loop condition `l < r`, not `l <= r`.** This is a CONVERGING-pointer
   search — l and r walk toward each other and MEET exactly at the
   answer, rather than CROSSING past each other the way mySqrt/
   searchInsert's l and r do. Recognize this as a different binary-search
   template: "search for one special index" vs. "search for a boundary
   where l and r cross."
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
The most obvious approach: just scan the whole array and track the
smallest value seen — that's what `min(nums)` does under the hood. It
works, but it's O(n), and the problem tells us we can do better because
the array has special structure (sorted, then rotated).

### The key insight: compare nums[mid] to nums[r], not nums[l]
Here's the trick: at any `mid`, compare `nums[mid]` to `nums[r]` (the
RIGHTMOST element of the current search range):
- If `nums[mid] > nums[r]`: the rotation "seam" (where a big number is
  followed by a small number) must be somewhere to the RIGHT of mid —
  because if nums[mid] is bigger than the rightmost element, the array
  must "drop down" somewhere between mid and r. So the minimum is
  strictly to the right of mid -> `l = mid + 1`.
- If `nums[mid] <= nums[r]`: the segment from mid to r is ALREADY
  normally sorted (no seam in it) — so the minimum can't be strictly to
  the right of mid; it's either AT mid or somewhere to its LEFT ->
  `r = mid` (note: NOT `mid - 1`, since mid itself could BE the minimum).

### Why compare to nums[r] and not nums[l]?
Comparing to `nums[l]` doesn't reliably tell you which half contains the
seam — but comparing to `nums[r]` does. If `nums[mid] > nums[r]`, that's
an unambiguous signal: values only "reset downward" once (the rotation
seam), so if the current middle value is bigger than the rightmost value,
that reset must still be ahead of us (to the right). This one-directional
comparison is the key that makes the binary search always safely halve
the space toward the true minimum.

### Step-by-step trace: findMin([4,5,6,7,0,1,2])
```
l=0, r=6

Step 1: mid = 3 -> nums[mid]=7, nums[r]=nums[6]=2
        Is 7 > 2? YES -> seam is to the right of mid -> l = mid+1 = 4

Step 2: l=4, r=6 -> mid = 5 -> nums[mid]=1, nums[r]=nums[6]=2
        Is 1 > 2? NO -> seam is at mid or to the left -> r = mid = 5

Step 3: l=4, r=5 -> mid = 4 -> nums[mid]=0, nums[r]=nums[5]=1
        Is 0 > 1? NO -> seam is at mid or to the left -> r = mid = 4

Step 4: l=4, r=4 -> l == r, loop condition `l < r` is False, loop ends!

Return nums[l] = nums[4] = 0.  Correct! ✅
```

### Building strong intuition: "chasing the seam from the right"
Picture the array as two normally-sorted runs glued together at one seam
(e.g. [4,5,6,7] glued to [0,1,2]). Comparing `nums[mid]` to `nums[r]`
tells you whether mid is still in the FIRST (high) run or already in the
SECOND (low) run. If mid is still in the high run, the seam (and the
minimum) must be further right, so you chase rightward. If mid is
already in the low run, the minimum is at mid or somewhere before it
within that same low run, so you pull `r` inward to mid — never past it,
since mid itself might already BE the minimum.

### The "aha" moment to remember 🎯
This is "converging pointer" binary search, not "crossing pointer" binary
search: `l` and `r` walk TOWARD each other and STOP the moment they meet
(`l < r` as the loop condition, not `l <= r`), rather than crossing past
one another. This pattern shows up whenever you're searching for a single
special INDEX (like a boundary point or a minimum) rather than searching
for a threshold where you check "was the last comparison valid or
invalid" after the fact.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (linear scan for minimum)
# ================================================================================
"""
### Thought Process 🧠
Ignore the rotation structure entirely — just track the smallest value
seen while scanning the whole array once. This is literally what Python's
built-in `min()` does.

### Complexity
- TC: O(n) — must look at every element
- SC: O(1)
"""


def find_min_brute(nums: list[int]) -> int:
    return min(nums)


# ================================================================================
# ALTERNATIVE APPROACH — Tracking Minimum (compare to nums[l], keep a running min)
# ================================================================================
"""
### Thought Process 🧠
A slightly different framing: instead of narrowing the search range until
`l` and `r` converge exactly ON the minimum, explicitly track a running
`minimum` variable as you go, comparing `nums[l]` (the LEFT boundary,
not nums[r]) to `nums[mid]` to decide which half is sorted, and folding
a CANDIDATE minimum into `minimum` from whichever half you're about to
discard.

### Idea
At each step: if `nums[l] <= nums[mid]`, the LEFT half [l..mid] is
normally sorted, so its smallest element is `nums[l]` — record that as a
candidate, then move `l` past this whole sorted chunk (`l = mid + 1`),
since the true minimum can't be hiding in an already-fully-sorted
ascending run (its own first element already IS its minimum). Otherwise,
the left half must contain the seam, so `nums[mid]` becomes the new best
candidate, and `r = mid - 1` shrinks from the right.

### Why does it work?
Whenever a half is confirmed normally sorted, you already KNOW its
minimum without searching further — it's just the leftmost element of
that sorted run. So instead of continuing to narrow toward a single
index, this version opportunistically captures that "free" minimum
information every time a sorted half is identified, and simply keeps the
best one seen across the whole search.

### Complexity
- TC: O(log n) — same halving behavior as the optimal approach
- SC: O(1) — just a few scalar variables

### Pros
- Conceptually intuitive if you're comfortable with "which half is
  sorted?" reasoning from "Search in Rotated Sorted Array" (LC 33) — this
  uses the SAME `nums[l]` vs `nums[mid]` comparison as that problem.

### Cons
- Slightly more bookkeeping than the optimal approach — you're
  maintaining an extra `minimum` variable and comparing against it every
  iteration, versus letting `l` and `r` converge directly onto the answer.
- Uses `l <= r` with `r = mid - 1` in the "seam" branch — this SKIPS
  `mid` from future consideration, relying on `minimum` having already
  captured it as a candidate this iteration. This is subtly different
  from the optimal approach's `r = mid` (which never skips mid without
  first re-checking it) — correct here, but easier to get wrong if
  you forget to update `minimum` before shrinking past mid.

### DSA Buddy Point 🧠
"This version front-loads the 'which half is sorted?' question from
nums[l] (like LC 33's search does) rather than nums[r] (like the optimal
find-min approach does) — same problem, different comparison anchor,
each requiring slightly different bookkeeping to stay correct."
"""


def find_min_tracking(nums: list[int]) -> int:
    l, r = 0, len(nums) - 1
    minimum = float("inf")

    while l <= r:
        mid = (l + r) // 2

        if nums[l] <= nums[mid]:            # left half [l..mid] is sorted
            minimum = min(minimum, nums[l])
            l = mid + 1
        else:                                  # seam is in the left half
            minimum = min(minimum, nums[mid])
            r = mid - 1

    return minimum


# ================================================================================
# ALTERNATIVE APPROACH — Early-Exit "Already Sorted" Optimization
# ================================================================================
"""
### Thought Process 🧠
A practical, real-world-flavored optimization layered on top of the
optimal converging-pointer approach: at the START of every iteration,
check "is the CURRENT search range already fully sorted (no rotation
seam left in it at all)?" If so, you can stop immediately — the minimum
of an already-sorted range is trivially its first element — instead of
continuing to binary-search down to a single index.

### Idea
Before computing `mid` at all, check `nums[l] < nums[r]`. If true, the
current range [l..r] has no seam in it whatsoever (a rotated range would
have its left boundary LARGER than its right boundary), so return
`nums[l]` immediately. Otherwise, proceed with the same `nums[mid]` vs
`nums[l]` comparison logic to narrow the range, same as the tracking
approach.

### Why does it work?
A sub-range with no rotation seam is, by definition, in plain ascending
order — its leftmost element MUST be its smallest. This early check can
short-circuit the search the moment the "still rotated" region has
shrunk down to something fully resolved, without needing to narrow all
the way to a single index via further mid-comparisons.

### Complexity
- TC: O(log n) — same asymptotic behavior as the other binary search
  versions; the early exit doesn't change the worst case, but can save a
  constant number of iterations in practice
- SC: O(1)

### Pros
- Can terminate slightly earlier in practice once the remaining range
  becomes seam-free, rather than always narrowing all the way to `l == r`.
- The "is this chunk already sorted?" check is a genuinely useful mental
  habit for rotated-array problems in general — recognizing you can stop
  early whenever you've localized a rotation-free segment.

### Cons
- Adds an extra comparison (`nums[l] < nums[r]`) every iteration, which
  in the worst case (never triggers until the very last step) is pure
  overhead — no asymptotic benefit, just a possible constant-factor win.
- Slightly more code paths to verify correct than the minimal optimal
  version — more surface area for an off-by-one mistake.

### DSA Buddy Point 🧠
"'Check if I can already answer trivially before doing more work' is a
generally good instinct — but confirm it's not costing you more than it
saves. Here it's a nice-to-have, not a complexity-class improvement."
"""


def find_min_sorted_check(nums: list[int]) -> int:
    l, r = 0, len(nums) - 1

    while l < r:
        if nums[l] < nums[r]:          # current range has no seam - already sorted
            return nums[l]

        mid = (l + r) // 2

        if nums[mid] >= nums[l]:        # left half [l..mid] is sorted
            l = mid + 1
        else:                              # seam is in the left half
            r = mid

    return nums[l]


# ================================================================================
# MY APPROACH — Binary Search (converging pointers, compare to nums[r])
# ================================================================================
"""
### Idea
Compare `nums[mid]` to `nums[r]` at each step. If `nums[mid] > nums[r]`,
the minimum is strictly to the right (`l = mid + 1`). Otherwise, the
minimum is at `mid` or to its left (`r = mid`). Loop while `l < r`; when
they converge (`l == r`), that shared index IS the minimum.

### Complexity
- TC: O(log n) — search range halves each iteration
- SC: O(1) — just pointer variables

### Pros
- Optimal time complexity, minimal and clean.
- This EXACT logic is the pivot-finding "Phase 1" used in the two-phase
  solution to "Search in Rotated Sorted Array" (LC 33) — mastering this
  problem directly unlocks that one.

### DSA Buddy Point 🧠
"Find minimum in rotated array -> compare nums[mid] to nums[r] (NOT
nums[l]). Bigger than the rightmost value means the seam (and minimum)
is still ahead; not bigger means you're already in the low run, so pull
the right boundary inward to mid."

### What can be improved?
Nothing — O(log n) is optimal, since finding a single distinguished value
via halving comparisons cannot be done faster than logarithmic time for
this kind of problem. This is the accepted optimal solution.
"""


def find_min(nums: list[int]) -> int:
    l, r = 0, len(nums) - 1

    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[r]:
            l = mid + 1
        else:
            r = mid
    return nums[l]


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
FIND MINIMUM IN ROTATED SORTED ARRAY
│
├── Brute Force
│   └── Scan the whole array, track the smallest value -> O(n)
│
├── Bottleneck
│   └── Ignores the sorted-then-rotated structure entirely
│
├── Key Observation
│   └── Rotation creates exactly ONE seam (big value directly followed
│       by a smaller one) — comparing nums[mid] to nums[r] reveals
│       whether mid is still in the "high" run or already the "low" run
│
├── Path A — Tracking Minimum (compare to nums[l], keep running min)
│   └── Whenever a half is confirmed sorted, its first element is a free
│       candidate minimum — track the best one seen across the search
│       └── O(log n) time, O(1) space (uses l <= r, r = mid - 1)
│
├── Path B — Early-Exit "Already Sorted" Check
│   └── Before narrowing further, check if current range has no seam at
│       all (nums[l] < nums[r]) — if so, nums[l] is trivially the answer
│       └── O(log n) time, O(1) space (same worst case, saves iterations in practice)
│
└── Path C — Optimal: Converging-Pointer Binary Search (compare to nums[r])
    ├── nums[mid] > nums[r]  -> seam still ahead -> l = mid + 1
    ├── nums[mid] <= nums[r] -> seam at/behind mid -> r = mid (not mid-1!)
    ├── Loop while l < r (pointers CONVERGE, don't cross)
    └── When l == r, that index is the minimum
        └── O(log n) time, O(1) space  <-- cleanest, your code
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Find minimum in rotated array -> compare nums[mid] to nums[r], never
  nums[l] — the rightward comparison is what reliably reveals which side
  the rotation seam is on."
- "r = mid, NOT mid - 1, when nums[mid] <= nums[r] — mid itself could BE
  the minimum, so you must never exclude it from the search range."
- "This uses `l < r` as the loop condition (converging pointers that
  MEET), not `l <= r` (crossing pointers) — a different binary-search
  template than mySqrt/searchInsert, worth recognizing as its own
  pattern: 'search for a single special index.'"
- "This exact logic IS Phase 1 of solving 'Search in Rotated Sorted
  Array' (LC 33) via the two-phase approach — nail this problem and
  you've already built half of that one's optimal solution."
- "Comparing to nums[l] (tracking/sorted-check versions) vs. nums[r]
  (optimal version) are BOTH valid anchors — just remember each demands
  different shrink logic (mid-1 vs mid) to stay correct, and don't mix
  them up mid-solution."
- "An early 'is this range already fully sorted?' check is a good
  instinct for rotated-array problems generally, even when it doesn't
  change the worst-case complexity — it's a legitimate constant-factor
  optimization, not just a style choice."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                  | Core Idea                                          | TC       | SC   | Pros                                    | Cons                                             | When to Use                        |
|-------------------------------|-----------------------------------------------------------|----------|------|------------------------------------------------|-------------------------------------------------------|------------------------------------------|
| Brute Force                    | Linear scan, track smallest value seen                        | O(n)     | O(1) | Trivial, always correct                          | Ignores the O(log n) requirement entirely              | Baseline / correctness check only        |
| Tracking Minimum (nums[l])     | Compare to nums[l]; capture free candidate min per sorted half | O(log n) | O(1) | Mirrors LC 33's "which half sorted?" comparison   | Extra running-min bookkeeping; r=mid-1 needs care      | If you're anchoring on nums[l] already   |
| Early-Exit Sorted Check        | Check "already sorted?" before each narrowing step             | O(log n) | O(1) | Can terminate early once seam-free in practice     | Extra comparison every iteration; more code paths      | Good general instinct, minor practical win|
| Optimal (compare to nums[r])   | Converging pointers, halve based on nums[mid] vs nums[r]        | O(log n) | O(1) | Cleanest, minimal code, fewest edge cases          | None significant                                        | Default optimal choice (your code)       |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Converging-Pointer Binary Search on a Rotated Array (a building
  block for "Search in Rotated Sorted Array," LC 33 — this problem's
  logic IS that problem's pivot-finding phase).
- Go-to answer: "Compare nums[mid] to nums[r]. If nums[mid] is bigger,
  the rotation seam (and the minimum) is still to the right, so move l
  past mid. Otherwise, mid is already in the low run, so pull r in to
  mid (not mid-1, since mid itself might be the answer). Loop while
  l < r; when they converge, that's the minimum. O(log n) time, O(1) space."
- Good to mention this is a converging-pointer template, distinct from
  the crossing-pointer template used in mySqrt/searchInsert — shows
  awareness that "binary search" isn't a single monolithic pattern.
- If you naturally reach for comparing to nums[l] instead of nums[r]
  (e.g. because you're already thinking in LC 33's "which half is
  sorted?" terms), that's a valid alternative too — just remember it
  needs a running `minimum` variable and `r = mid - 1` instead of the
  cleaner `r = mid` the nums[r]-anchored version allows.
- Common follow-up: "What if there could be duplicates?" -> That's LC
  154; when `nums[mid] == nums[r]`, you can't tell which side the seam is
  on, so you fall back to shrinking `r` by one and retrying — this
  degrades worst-case time to O(n).
"""

# ================================================================================
# STRONG UNDERSTANDING CHECK 💪
# ================================================================================
"""
If you can confidently answer these without looking back up, you've truly
internalized this problem (not just memorized the code):

1. Q: Why compare nums[mid] to nums[r] instead of nums[l]?
   A: Comparing to nums[r] gives an UNAMBIGUOUS signal about which side
      the rotation seam is on: nums[mid] > nums[r] can ONLY happen if the
      seam lies between mid and r (values must "drop" somewhere in that
      range to end up smaller than nums[mid] by the time we reach r).
      Comparing to nums[l] doesn't give this same guarantee in all cases.

2. Q: Why is it `r = mid` and not `r = mid - 1` in the "else" branch?
   A: Because when `nums[mid] <= nums[r]`, mid itself might already BE
      the minimum value — excluding it with `mid - 1` could throw away
      the correct answer. Compare this to mySqrt, where `r = mid - 1` was
      safe because we'd already confirmed mid's square was TOO BIG (never
      the answer) — here, mid is never disqualified, just possibly not
      yet proven to be the true minimum.

3. Q: Why does the loop condition use `l < r` instead of `l <= r`?
   A: Because `l` and `r` are converging onto the SAME final index (the
      minimum's position) rather than crossing past each other to signal
      "search exhausted." Once `l == r`, we've found that index — there's
      no need (or correctness) in continuing to loop past that point.

4. Q: What does this function return if the array is NOT rotated at all
      (e.g. [1,2,3,4,5])?
   A: nums[0], i.e. 1. Every comparison finds `nums[mid] <= nums[r]`
      (since the whole array is already sorted, nothing is ever bigger
      than nums[r]), so `r` keeps shrinking toward `l` until they meet at
      index 0 — correctly identifying the first element as the minimum
      when there's no rotation.

5. Q: If you had to explain this to someone who's never seen this problem
      before, in one sentence, what would you say?
   A: "I keep checking whether the middle element is still part of the
      'big numbers' run or has already crossed into the 'small numbers'
      run by comparing it to the rightmost element, and I narrow my
      search toward whichever side the transition point must be on,
      until both ends of my search meet exactly at the minimum."
"""