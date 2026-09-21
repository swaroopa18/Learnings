"""
================================================================================
 PROBLEM: Search in Rotated Sorted Array (LeetCode 33)
================================================================================
Given: an array of DISTINCT integers that was originally sorted in
ascending order, then ROTATED at some unknown pivot (e.g. [0,1,2,4,5,6,7]
rotated becomes [4,5,6,7,0,1,2]). Given a `target`, return its index, or
-1 if it's not present. Must run in O(log n) time.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Are all elements distinct? (Yes for LC 33 — LC 81 is the "with
  duplicates" variant, which needs different handling)
- Could the array be un-rotated (i.e. rotated by 0)? (Yes — must handle
  the "already fully sorted" case correctly, not just genuinely rotated ones)
- Is O(log n) a hard requirement? (Yes — a plain linear scan technically
  works but defeats the point of the problem)
"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR ROTATED SORTED ARRAY PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   At ANY mid, at least ONE half is normally sorted (no seam in it) │
    │   — because rotation creates exactly ONE seam, which can only      │
    │   live in ONE of the two halves.                                   │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

Memorize these as REFLEXES for any rotated-sorted-array problem:

1. **Rotation = exactly ONE seam.** A big value immediately followed by a
   smaller one, exactly once in the whole array. Every rotated-array
   binary search is really just "figure out which side of that seam
   you're on" before doing anything else.

2. **Per step, ask ONE question: which half is normally sorted?** Compare
   `nums[mid]` to `nums[l]` (as this solution does) — if
   `nums[mid] >= nums[l]`, the LEFT half [l..mid] is seam-free and
   normally sorted; otherwise the RIGHT half [mid..r] is.

3. **Once you know the sorted half, check if target's VALUE fits its
   range.** If yes, search inside it with ordinary binary search
   reasoning. If no, target must be hiding in the OTHER (still rotated)
   half — move there and repeat the same one question.

4. **This is "find an exact match," not "find a boundary."** Unlike
   mySqrt/searchInsert, you return the match's index the instant you find
   it (or -1 if the range is exhausted) — there's no l/r crossing-point
   convention to apply here.

5. **The "which half is sorted?" check (comparing to nums[r] instead of
   nums[l]) is EXACTLY the logic behind LC 153** ("Find Minimum in
   Rotated Sorted Array"). That problem's binary search IS this
   problem's pivot-finding building block, isolated on its own.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
If the array weren't rotated, you'd just do plain binary search — compare
target to the middle, go left or right. The rotation is what messes
things up: after rotating, you can't just say "everything left of mid is
smaller" anymore, because the rotation point creates a "jump" somewhere
in the array (e.g. in [4,5,6,7,0,1,2], the jump from 7 down to 0 happens
between indices 3 and 4).

### The key insight: AT LEAST ONE HALF is always normally sorted
Here's the trick that makes this solvable in O(log n): no matter where
you split a rotated sorted array at any `mid`, at least ONE of the two
halves [l..mid] or [mid..r] is guaranteed to be a NORMAL, un-rotated,
sorted run — because the rotation "jump" can only exist in ONE of the two
halves, never both. So the algorithm becomes:
1. Figure out WHICH half is normally sorted (compare nums[l] to nums[mid]).
2. Check if target falls within THAT sorted half's value range.
3. If yes, recurse/search only in that half (standard binary search).
4. If no, target must be in the OTHER half (even though it's rotated) —
   search there instead, and repeat the same logic on the smaller range.

### Why must one half always be sorted?
Picture the rotation as a single "seam" where the array wraps around
(the point where a big number is immediately followed by a small number).
That seam can only occur at ONE location in the whole array. When you
split the array at `mid`, that single seam is either in the left half or
the right half — it literally cannot be in BOTH halves, since there's
only one seam. So whichever half DOESN'T contain the seam is guaranteed
to be normally sorted, ascending, no rotation weirdness at all.

### Step-by-step trace: search([4,5,6,7,0,1,2], target=0)
```
l=0, r=6

Step 1: mid = 3  -> nums[mid]=7
        Is nums[mid] >= nums[l]? nums[3]=7 >= nums[0]=4 -> YES
        -> LEFT half [l..mid] = [4,5,6,7] is the normally sorted one
        Is target(0) in range [nums[l]=4, nums[mid]=7]? NO (0 < 4)
        -> target must be in the OTHER half -> l = mid+1 = 4

Step 2: l=4, r=6 -> mid = 5  -> nums[mid]=1
        Is nums[mid] >= nums[l]? nums[5]=1 >= nums[4]=0 -> YES
        -> LEFT half [l..mid] = [0,1] is the normally sorted one
        Is target(0) in range [nums[l]=0, nums[mid]=1]? YES (0 is in [0,1])
        -> search inside this sorted half with plain binary search: bs(4, 5)
           bs(4,5): mid=4, nums[4]=0 == target(0) -> return 4!

Return 4.  Check: nums[4] = 0. Correct! ✅
```

### Building strong intuition: "which half is the normal one?"
Every step, ask yourself just ONE question: "is the left half
[l..mid] sorted normally, or is the right half [mid..r] sorted
normally?" You answer this with a single comparison (`nums[mid] >=
nums[l]`). Once you know which half is "boring and normal," you can use
totally ordinary reasoning ("is target within this range?") to decide
whether to dive into that normal half, or whether you must be dealing
with target hiding in the still-rotated other half — in which case you
just repeat the exact same question on that smaller half next.

### The "aha" moment to remember 🎯
Rotation only breaks GLOBAL sortedness, not LOCAL sortedness — any
contiguous half you pick is either fully normal-sorted, or itself
contains the rotation seam (and is thus still effectively "half rotated,"
which you resolve by splitting again). This is why the algorithm
naturally terminates in O(log n): every split guarantees you learn
which side is "safe" to reason about normally, shrinking the "still
messy" region by half every time, just like ordinary binary search.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (linear scan)
# ================================================================================
"""
### Thought Process 🧠
Ignore the rotation and sortedness entirely — just walk the array and
check each element against target.

### Complexity
- TC: O(n) — worst case, scans the whole array
- SC: O(1)

### Pros
- Trivial to write, always correct regardless of rotation.

### Cons
- Completely ignores the problem's explicit O(log n) requirement and the
  sorted-with-rotation structure that makes a faster solution possible.

### Bottleneck
A linear scan throws away ALL the ordering information the problem gives
us for free. Ask: "even though rotation breaks GLOBAL order, is there
still SOME local order I can exploit?" -> Yes: at least one half is
always normally sorted (see main approach above).
"""


def search_brute(nums: list[int], target: int) -> int:
    for i, n in enumerate(nums):
        if n == target:
            return i
    return -1


# ================================================================================
# MY APPROACH — Modified Binary Search (recursive inner search)
# ================================================================================
"""
### Idea
Outer `while` loop narrows down to a range where one side is confirmed
normally sorted and target's value falls within it, then hands off to a
small recursive helper `bs(l, r)` that does plain textbook binary search
within that confirmed-sorted sub-range.

### Complexity
- TC: O(log n) — the outer loop halves the search space each iteration
  (just like standard binary search), and the inner `bs` helper is also
  O(log (sub-range size)) once invoked
- SC: O(log n) — due to the recursive call stack of the `bs` helper
  (each level of recursion halves its own range, so recursion depth is
  bounded by log of the sub-range size)

### Pros
- Clearly separates "which half is sorted?" reasoning (outer loop) from
  "plain binary search within a known-sorted range" (inner recursive
  helper) — can make the logic easier to reason about in pieces.

### DSA Buddy Point 🧠
"Rotated sorted array search = 'figure out which half is a normal sorted
array, then binary search inside it' — repeated until you either find
target directly, or run out of range."

### What can be improved?
The recursion in the `bs` helper adds O(log n) auxiliary space for the
call stack — a fully iterative version (below) achieves the exact same
O(log n) time with O(1) space instead, by folding the "search within the
sorted half" logic directly into the main loop rather than delegating to
a separate recursive call.
"""


def search_hybrid(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1

    def bs(l, r):
        if l > r:
            return -1
        mid = (l + r) // 2

        if nums[mid] == target:
            return mid
        if nums[mid] > target:
            return bs(l, mid - 1)
        else:
            return bs(mid + 1, r)

    while l <= r:
        mid = (l + r) // 2
        if nums[mid] >= nums[l]:
            if nums[l] <= target and target <= nums[mid]:
                return bs(l, mid)
            else:
                l = mid + 1
        else:
            if nums[mid] <= target and target <= nums[r]:
                return bs(mid, r)
            else:
                r = mid - 1
    return -1


# ================================================================================
# ALTERNATIVE APPROACH — Fully Iterative (no recursion, O(1) space)
# ================================================================================
"""
### Thought Process 🧠
Same "which half is sorted?" logic as the main approach, but instead of
delegating the "search within the sorted half" step to a separate
recursive helper, fold that decision directly into the SAME loop that's
already running — every iteration either finds target, or moves `l`/`r`
one step closer, all within a single `while` loop.

### Idea
At each `mid`: determine which half is normally sorted. If the left half
is sorted and target falls strictly within `[nums[l], nums[mid])`, shrink
`r = mid - 1` (search left). If the right half is sorted and target falls
strictly within `(nums[mid], nums[r]]`, shrink `l = mid + 1` (search
right). Otherwise, target must be in the OTHER (still rotated) half, so
move the pointer that direction and let the next iteration re-evaluate.

### Complexity
- TC: O(log n) — same as the recursive-hybrid version
- SC: O(1) — no recursive call stack, just a few pointer variables

### Pros
- Strictly better space complexity than the recursive-hybrid version, for
  the exact same time complexity.
- Everything happens in one loop — some find this easier to trust there's
  no subtle bug in a separate recursive helper's base case.

### Cons
- The boundary conditions (`<` vs `<=`) need careful attention to avoid
  off-by-one errors — slightly more fiddly to get exactly right on the
  first attempt than delegating to a clean recursive `bs` helper.

### DSA Buddy Point 🧠
"Any recursive 'binary search within a known sub-range' can usually be
inlined into the outer loop directly — recursion here is a convenience,
not a necessity, and folding it in trades a small bit of readability for
O(1) space instead of O(log n)."
"""


def search_pure_iterative(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        if nums[l] <= nums[mid]:               # left half is normally sorted
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        else:                                    # right half is normally sorted
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1


# ================================================================================
# ALTERNATIVE APPROACH — Two-Phase: Find Pivot First, Then Plain Binary Search
# ================================================================================
"""
### Thought Process 🧠
A conceptually different way to split the problem into two SEPARATE, much
simpler subproblems, instead of interleaving "which half is sorted?" logic
into every step of a single search:

**Phase 1:** Find the rotation pivot — the index of the minimum element
(equivalently, the one place where `nums[i] > nums[i+1]`, i.e. where the
"seam" is). This is itself a classic binary search: compare `nums[mid]`
to `nums[r]`; if `nums[mid] > nums[r]`, the minimum must be to the RIGHT
of mid (the seam hasn't been crossed yet), so `l = mid + 1`; otherwise the
minimum is at mid or to the LEFT, so `r = mid`.

**Phase 2:** Once you know the pivot index, you know EXACTLY which of the
two segments `[0, pivot-1]` and `[pivot, n-1]` is sorted and could
contain target's value range — pick the right one and run completely
standard, textbook binary search on it (no rotation-awareness needed
anymore, since you've already "unrotated" your understanding of the array).

### Why does it work?
This decouples two different concerns that the other approaches solve
simultaneously: "where is the rotation?" and "where is target?" By
answering the first question completely first, the second question
becomes a totally ordinary binary search on a normal sorted subarray —
arguably easier to convince yourself is correct, since each phase only
has to reason about ONE thing at a time.

### Complexity
- TC: O(log n) — Phase 1 is O(log n) (finding the minimum), Phase 2 is
  O(log n) (standard binary search on the correct segment); two
  sequential O(log n) phases is still O(log n) overall
- SC: O(1) — just a few pointer variables across both phases

### Pros
- Conceptually cleaner separation of concerns — some find "find the
  pivot, THEN search" easier to reason about than juggling both decisions
  in a single combined loop.
- The pivot-finding phase is independently useful — it's the exact
  solution to a related problem, "Find Minimum in Rotated Sorted Array"
  (LC 153), so this approach doubles as practice for that problem too.

### Cons
- Two separate binary search passes instead of one combined pass — same
  Big-O, but more total code and two things to get right instead of one.
- If you only need target's presence (not the pivot itself), this does
  slightly more conceptual "setup" work than strictly necessary compared
  to the single-pass approaches.

### DSA Buddy Point 🧠
"When a rotated-array problem feels tangled, it's often worth asking:
'can I separate FINDING THE ROTATION from SEARCHING WITHIN IT?' Splitting
into two clean binary searches (find pivot, then search the right normal
segment) is a totally valid, sometimes clearer, alternative to combining
both concerns into a single pass."
"""


def search_find_pivot(nums: list[int], target: int) -> int:
    n = len(nums)

    # Phase 1: binary search for the rotation pivot (index of the minimum)
    l, r = 0, n - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[r]:      # seam is still ahead -> min is to the right
            l = mid + 1
        else:                          # seam already crossed or at mid -> min is here or left
            r = mid
    pivot = l

    # Phase 2: plain binary search on whichever segment could hold target
    def bsearch(lo, hi):
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    if nums[pivot] <= target <= nums[n - 1]:
        return bsearch(pivot, n - 1)
    else:
        return bsearch(0, pivot - 1)


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
SEARCH IN ROTATED SORTED ARRAY
│
├── Brute Force
│   └── Linear scan, ignore rotation entirely -> O(n)
│
├── Bottleneck
│   └── Throws away all the ordering structure the rotation preserves
│
├── Key Observation
│   └── Rotation creates exactly ONE "seam" -> splitting at any mid means
│       AT LEAST ONE half is guaranteed normally sorted (no seam inside it)
│
├── Per-Step Decision (same in both optimal versions)
│   ├── Which half is normally sorted? (compare nums[l] vs nums[mid])
│   ├── Does target's value fall within that sorted half's range?
│   │   ├── YES -> search inside that sorted half (plain binary search)
│   │   └── NO  -> target must be in the OTHER (still rotated) half
│   └── Repeat on the shrunk range
│
├── Path A — Recursive Hybrid (outer loop + inner bs() helper)
│   └── O(log n) time, O(log n) space (recursive call stack)  <-- your code
│
├── Path B — Fully Iterative (logic inlined into one loop)
│   └── O(log n) time, O(1) space  <-- space-optimal variant
│
└── Path C — Two-Phase: Find Pivot, Then Plain Binary Search
    ├── Phase 1: binary search for the rotation pivot (min element index)
    │   [same technique as LC 153 "Find Minimum in Rotated Sorted Array"]
    └── Phase 2: standard binary search on whichever segment fits target
        └── O(log n) time, O(1) space  <-- separates concerns into 2 clean passes
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "Rotated sorted array -> exactly ONE rotation 'seam' exists -> any split
  guarantees at least one half is normally, boringly sorted."
- "Per step: figure out WHICH half is normal, check if target's value
  fits in that half's range, then either search there or flip to the
  other half."
- "This problem is 'find an exact match,' not 'find a boundary' — so the
  l/r-return-convention rule from mySqrt/searchInsert doesn't directly
  apply here; instead, you return the match's index the moment you find
  it, or -1 if the loop exhausts."
- "A recursive 'search within a known sorted sub-range' step can almost
  always be inlined into the outer loop for O(1) space instead of
  O(log n) — recursion there is convenience, not necessity."
- "Distinct elements matter: with duplicates (LC 81), `nums[mid] >=
  nums[l]` can no longer reliably tell you which half is sorted when
  nums[mid] == nums[l] == nums[r], requiring an extra fallback step."
- "'Find the pivot, then search' is a valid alternative to combining both
  decisions into one pass — same O(log n) overall, and the pivot-finding
  phase alone solves LC 153 (Find Minimum in Rotated Sorted Array)."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                           | TC       | SC       | Pros                                    | Cons                                        | When to Use                       |
|----------------------------------|------------------------------------------------------------|----------|----------|------------------------------------------------|--------------------------------------------------|-----------------------------------------|
| Brute Force                       | Linear scan, ignore rotation                                   | O(n)     | O(1)     | Trivial, always correct                          | Ignores the O(log n) requirement entirely           | Baseline / correctness check only       |
| Recursive Hybrid                  | Outer loop picks sorted half; inner bs() searches it            | O(log n) | O(log n) | Clean separation of "which half" vs "search it"  | Extra O(log n) call-stack space                     | If readability > raw space efficiency   |
| Fully Iterative                   | Same logic, folded into a single loop, no recursion             | O(log n) | O(1)     | Space-optimal, single self-contained loop         | Slightly more fiddly boundary (< vs <=) conditions  | Default optimal choice (space-conscious)|
| Two-Phase (Find Pivot, Then Search)| Locate rotation point first, then plain binary search           | O(log n) | O(1)     | Cleanest separation of concerns, doubles as LC 153 | Two passes / more total code for the same Big-O      | When reasoning clarity matters most     |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Modified Binary Search on a Rotated Array (distinct from
  boundary-search problems like mySqrt/searchInsert — this is "find an
  exact match," using an extra "which half is sorted?" decision per step).
- Go-to answer: "At any midpoint, one half of a rotated sorted array is
  always normally sorted, since there's only one rotation point. Check
  which half that is, see if target's value falls in its range, and
  search there — otherwise search the other (still rotated) half. Repeat
  until found or the range is exhausted. O(log n) time."
- Good to mention the recursive-hybrid vs. fully-iterative trade-off
  (same logic, O(log n) vs O(1) space) if asked to optimize further.
- Common follow-up: "What if there could be duplicates?" -> That's LC 81;
  when `nums[l] == nums[mid] == nums[r]`, you can't tell which half is
  sorted from that comparison alone, so you fall back to shrinking both
  `l` and `r` by one and retrying — this degrades worst-case time to O(n).
"""