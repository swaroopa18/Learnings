"""
================================================================================
 PROBLEM: Find Peak Element (LeetCode 162)
================================================================================
Given: an array `nums` where `nums[i] != nums[i+1]` for all adjacent
elements (no equal neighbors). A "peak" is an element strictly greater
than both its neighbors (treat out-of-bounds neighbors as -infinity, so
the first/last element only needs to beat its one real neighbor).
Task: return the INDEX of any one peak. Multiple peaks may exist — any
valid one is an acceptable answer. Must run in O(log n) time.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is any valid peak acceptable, or does it need to be the GLOBAL maximum?
  (Any local peak is fine — this is explicitly NOT "find the maximum")
- Are adjacent elements guaranteed distinct? (Yes — this is what makes
  "always increasing or always decreasing across a comparison" possible,
  with no equal-neighbor edge case to worry about)
- Can the array have just one element? (Yes — trivially a peak, since
  both its "neighbors" are treated as -infinity)
- Is O(log n) required? (Yes — a linear scan works but defeats the point;
  the constraint is the whole reason this is a binary-search problem)
"""

# ================================================================================
# 🔑🔑🔑  STRONG POINTS FOR "FIND A PEAK" PROBLEMS  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   You don't need to know BOTH neighbors to decide which way to     │
    │   go — comparing nums[mid] to just ONE neighbor (nums[mid+1]) is   │
    │   enough to guarantee a peak exists on the side you move toward.   │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

Memorize these as REFLEXES for "find a peak / local max" problems:

1. **"Any peak is fine" is what unlocks binary search.** If the problem
   demanded the GLOBAL maximum, you'd be stuck with O(n) — there's no way
   to discard half the array without risking throwing away the true max.
   But since ANY local peak counts, a much weaker, purely LOCAL signal
   (comparing two adjacent elements) is enough to safely discard a half.

2. **If nums[mid] < nums[mid+1], a peak MUST exist to the right.** The
   sequence is "climbing" at mid, and it has to eventually stop climbing
   somewhere (even if that's just the last element, which counts as a
   peak against -infinity on its far side) — that stopping point is a
   peak, guaranteed to exist in the right half.

3. **If nums[mid] > nums[mid+1], a peak MUST exist at or before mid.**
   Symmetric logic — the sequence is "descending" at mid, meaning
   something to its left (possibly mid itself) must have been a local
   high point for the descent to have started.

4. **Out-of-bounds neighbors = -infinity.** This cleanly handles the
   first/last element being a peak without special-casing them — they
   automatically "win" against a neighbor that doesn't exist.

5. **This is a converging-pointer search (`l < r` or careful `l <= r`
   handling), same family as "Find Minimum in Rotated Sorted Array"** —
   you're hunting for ONE special index where a local property holds, not
   a boundary where l/r cross past each other.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
Just walk through the array left to right, and at each index check "is
this bigger than both neighbors?" The first one you find is a valid
peak. That's the brute force approach — completely correct, but O(n).

### The key insight: you don't need to scan everything
Here's the surprising part: this problem does NOT require the array to
be sorted, or have any global structure at all — yet it's STILL
binary-searchable. Why? Because the problem only asks for ANY peak, not
THE (unique) maximum. That relaxation is exactly what makes a purely
LOCAL comparison (just look at nums[mid] vs. its immediate neighbor)
enough information to know which half to search next.

### Why does comparing to just ONE neighbor work?
Imagine standing at position `mid` and looking one step to your right.
- If the value goes UP (nums[mid] < nums[mid+1]): you're on an "uphill"
  slope. No matter what happens further right, EITHER it keeps going up
  until it hits the end (and the last element is a peak, since its
  "right neighbor" is -infinity), OR it eventually turns around and
  starts going down (and the turning point is a peak). Either way,
  SOME peak is guaranteed to exist somewhere to your right.
- If the value goes DOWN (nums[mid] > nums[mid+1]): you're on a
  "downhill" slope, which means something before this point must have
  been a local high — either mid itself, or something earlier. A peak
  is guaranteed to exist at index mid or somewhere to its left.

### Step-by-step trace: findPeakElement([1,2,1,3,5,6,4])
```
l=0, r=6

Step 1: mid=3 -> nums[3]=3, nums[4]=5.  3 < 5 (going up)
        -> peak guaranteed to the right -> l = mid+1 = 4

Step 2: l=4, r=6 -> mid=5 -> nums[5]=6, nums[6]=4.  6 > 4 (going down)
        -> peak guaranteed at mid or left -> r = mid = 5

Step 3: l=4, r=5 -> mid=4 -> nums[4]=5, nums[5]=6.  5 < 6 (going up)
        -> peak guaranteed to the right -> l = mid+1 = 5

Step 4: l=5, r=5 -> l == r, loop ends (using the simple `l < r` template)

Return index 5.  Check: nums[5]=6, neighbors are nums[4]=5 and nums[6]=4.
5 < 6 > 4 -> valid peak! ✅
```

### Building strong intuition: "walking uphill always leads to a peak"
Picture the array as a mountain range profile. If you're walking and the
ground is rising in front of you, common sense says: keep walking that
direction, you're heading toward higher ground, and mountains (by
definition) have to stop rising SOMEWHERE — that stopping point is a
peak. If the ground is falling in front of you, that means you already
passed a peak (or you're standing on one right now) — so look backward
or stay put. This "always chase uphill, or stay near a downhill start"
intuition is EXACTLY the binary search decision rule, just described in
plain English.

### The "aha" moment to remember 🎯
Binary search doesn't require GLOBAL sortedness — it only requires that,
at every step, a single LOCAL comparison gives you a GUARANTEE about
which half still contains a valid answer. "Any local peak" is a weak
enough requirement that a single neighbor comparison is always enough to
make that guarantee, even though the array itself could be completely
unsorted and jagged everywhere else.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (linear scan)
# ================================================================================
"""
### Thought Process 🧠
Check every index directly: is it bigger than both its (possibly
out-of-bounds, treated as -infinity) neighbors?

### Complexity
- TC: O(n) — must potentially check every element
- SC: O(1)

### Pros
- Trivial, obviously correct, no cleverness required.

### Cons
- Ignores the O(log n) requirement and the "any local comparison
  guarantees a direction" structure that makes this binary-searchable.

### Bottleneck
Checking every index one at a time throws away the fact that a single
uphill/downhill comparison at ANY point already guarantees a peak exists
on one specific side. Ask: "can one comparison eliminate half the
remaining search space with a guarantee, not just a probability?" -> Yes:
the slope-direction binary search (main approach below).
"""


def find_peak_brute(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        left = float("-inf") if i == 0 else nums[i - 1]
        right = float("-inf") if i == n - 1 else nums[i + 1]
        if left < nums[i] > right:
            return i
    return -1


# ================================================================================
# MY APPROACH — Binary Search (check both neighbors explicitly, l <= r)
# ================================================================================
"""
### Idea
At each `mid`, explicitly compute BOTH neighbors (treating out-of-bounds
as -infinity), and directly check if `mid` is already a peak. If not,
compare `nums[mid]` to the RIGHT neighbor: if `nums[mid] > higher` (i.e.
descending to the right), the peak must be at mid or to the left, so
`r = mid - 1`. Otherwise (ascending or equal-ish going right, though
equality can't actually happen given distinct neighbors), search right
with `l = mid + 1`.

### Complexity
- TC: O(log n) — search range halves each iteration
- SC: O(1)

### Pros
- Directly checks the peak condition every iteration, which some find
  more intuitive to verify correct (you're explicitly looking at "is
  this THE answer?" before deciding which way to move).

### DSA Buddy Point 🧠
"Computing both neighbors explicitly (with -infinity padding for
out-of-bounds) and checking the exact peak condition inline is a very
readable way to write this — it costs a couple of extra comparisons per
iteration, but nothing that changes the O(log n) complexity."

### What can be improved?
Nothing complexity-wise — O(log n) is optimal. There IS a slightly
leaner way to write the same algorithm that skips the explicit "is this
already a peak?" check and the LEFT-neighbor computation entirely, since
a single comparison to just the right neighbor is enough on its own to
guide the search all the way to a peak without ever needing to verify it
mid-loop (see the simplified version below).
"""


def find_peak(nums: list[int]) -> int:
    l, r = 0, len(nums) - 1

    while l <= r:
        mid = (l + r) // 2
        lower = float("-inf") if mid - 1 < 0 else nums[mid - 1]
        higher = float("-inf") if mid + 1 > len(nums) - 1 else nums[mid + 1]
        if lower < nums[mid] > higher:
            return mid
        if nums[mid] > higher:
            r = mid - 1
        else:
            l = mid + 1
    return -1


# ================================================================================
# ALTERNATIVE APPROACH — Simplified Binary Search (compare only to the right neighbor)
# ================================================================================
"""
### Thought Process 🧠
A leaner version of the same idea: you don't actually need to check the
LEFT neighbor or explicitly verify "is mid already a peak?" at all. Just
compare `nums[mid]` to `nums[mid+1]` (always safe to access, since the
loop condition `l < r` guarantees `mid < r <= len(nums)-1`, so `mid+1` is
always a valid in-bounds index during the loop). If ascending, go right;
if descending, stay at-or-left. The moment `l` and `r` converge, that
index is GUARANTEED to be a peak — no separate verification step needed,
because the loop invariant itself proves it.

### Idea
`while l < r`: compare `nums[mid]` to `nums[mid+1]`. If
`nums[mid] > nums[mid+1]` (descending), the peak is at mid or to the
left, so `r = mid` (not `mid - 1` — mid could BE the peak). Otherwise
(ascending), the peak is strictly to the right, so `l = mid + 1`. When
`l == r`, return that index directly — no final peak-condition check
required.

### Why no explicit peak check is needed
This is the same "converging pointers, trust the invariant" pattern as
"Find Minimum in Rotated Sorted Array": by construction, every step
either confirms "a peak exists strictly to my right" or "a peak exists
at or to my left" — the search space NEVER loses the guarantee of
containing at least one peak. When `l` and `r` finally converge, the
single remaining index is, by that invariant, necessarily a peak — you
don't need to re-verify it against both neighbors after the fact.

### Complexity
- TC: O(log n) — same as the main approach
- SC: O(1)

### Pros
- Fewer comparisons per iteration (one, instead of computing both
  padded neighbors and checking a three-way condition).
- Never needs -infinity padding logic at all — `mid+1` is always safely
  in-bounds under the `l < r` loop condition.
- Shorter, and arguably easier to prove correct via the loop invariant
  alone, without needing a separate "did I find it?" branch.

### Cons
- The correctness argument (why no final check is needed) is less
  immediately obvious than the main approach's "just check the condition
  directly" style — requires trusting the invariant rather than seeing
  the peak check happen explicitly in the code.

### DSA Buddy Point 🧠
"Once you trust that 'peak guaranteed to exist in the current range' is
an INVARIANT maintained every step (not something you re-derive each
time), you can drop the explicit peak-condition check entirely and just
trust convergence — same trick as findMin's converging-pointer approach."
"""


def find_peak_simple(nums: list[int]) -> int:
    l, r = 0, len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[mid + 1]:      # descending -> peak at mid or left
            r = mid
        else:                                  # ascending -> peak strictly right
            l = mid + 1
    return l


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
FIND PEAK ELEMENT
│
├── Brute Force
│   └── Check every index against both (padded) neighbors -> O(n)
│
├── Bottleneck
│   └── Throws away the fact that "any peak is fine" makes a single
│       LOCAL comparison enough to guarantee a direction
│
├── Key Observation
│   └── nums[mid] < nums[mid+1] (ascending) -> peak guaranteed to the right
│       nums[mid] > nums[mid+1] (descending) -> peak guaranteed at/left of mid
│
├── Path A — Explicit Check (both neighbors, l <= r)
│   └── Computes both padded neighbors, checks peak condition directly
│       └── O(log n) time, O(1) space  <-- your code, very explicit/readable
│
└── Path B — Simplified (only right neighbor, l < r, trust the invariant)
    └── One comparison per step; convergence itself proves the answer
        └── O(log n) time, O(1) space  <-- leaner, same complexity
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'Any peak is fine' (not the global max) is EXACTLY what makes this
  binary-searchable — a purely local, single-neighbor comparison is
  enough to guarantee a direction, with no need for global sortedness."
- "Ascending at mid (nums[mid] < nums[mid+1]) -> peak guaranteed to the
  right. Descending at mid -> peak guaranteed at mid or to the left.
  Memorize this pair as a reflex."
- "Out-of-bounds neighbors as -infinity elegantly handles first/last
  element edge cases without special-case branches."
- "You can trust the loop invariant to converge onto a valid peak without
  a final explicit check (simplified version) — same 'converging
  pointers, trust the invariant' pattern as Find Minimum in Rotated
  Sorted Array."
- "This problem needs NO sorting or rotation structure at all — it works
  on ANY array with distinct adjacent elements, which is a good contrast
  to keep in mind against the rotated-array family."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                     | Core Idea                                             | TC       | SC   | Pros                                     | Cons                                        | When to Use                          |
|----------------------------------|----------------------------------------------------------------|----------|------|------------------------------------------------|--------------------------------------------------|-------------------------------------------|
| Brute Force                       | Check every index against both padded neighbors                   | O(n)     | O(1) | Trivial, always correct                          | Ignores the O(log n) requirement entirely           | Baseline / correctness check only         |
| Explicit Check (both neighbors)   | Compute both padded neighbors, verify peak condition directly     | O(log n) | O(1) | Very readable, explicit correctness at each step   | A couple extra comparisons per iteration            | Default choice for clarity (your code)    |
| Simplified (right neighbor only)  | One comparison, converging pointers, trust the invariant           | O(log n) | O(1) | Leaner, fewer comparisons, no padding needed        | Correctness argument less immediately visible in code | If prioritizing minimal, elegant code     |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Binary Search via Local Slope Direction (a "weaker guarantee"
  binary search — works on unsorted arrays because "any peak" is a much
  easier target than "the true maximum").
- Go-to answer: "Compare nums[mid] to nums[mid+1]. If ascending, a peak
  is guaranteed somewhere to the right, so search right. If descending, a
  peak is guaranteed at mid or to its left, so search there. Converging
  pointers guarantee the final index is a peak. O(log n) time, O(1) space."
- Good to explicitly call out WHY this works despite no sortedness
  requirement — that's the single most important insight interviewers
  want articulated clearly for this problem.
- Common follow-up: "What if the array could have duplicate adjacent
  values?" -> The problem's distinctness guarantee is what avoids a
  "flat plateau" ambiguity (nums[mid] == nums[mid+1] would give no
  directional information) — with duplicates allowed, you'd need
  different handling, similar to how rotated-array problems with
  duplicates degrade toward O(n) in the worst case.
"""


if __name__ == "__main__":
    tests = [
        [1, 2, 3, 1],
        [1, 2, 1, 3, 5, 6, 4],
        [1],
        [1, 2],
        [2, 1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [1, 3, 2, 4, 1, 5, 1],
    ]

    def is_valid_peak(nums, idx):
        n = len(nums)
        left = float("-inf") if idx == 0 else nums[idx - 1]
        right = float("-inf") if idx == n - 1 else nums[idx + 1]
        return left < nums[idx] > right

    for nums in tests:
        a = find_peak(nums)
        b = find_peak_brute(nums)
        c = find_peak_simple(nums)
        assert is_valid_peak(nums, a), f"find_peak invalid on {nums}: {a}"
        assert is_valid_peak(nums, b), f"find_peak_brute invalid on {nums}: {b}"
        assert is_valid_peak(nums, c), f"find_peak_simple invalid on {nums}: {c}"
        print(f"nums={nums} -> explicit={a}, brute={b}, simplified={c} (all valid peaks)")