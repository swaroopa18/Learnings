"""
================================================================================
 PROBLEM: 3Sum (LeetCode 15)
================================================================================
Given: an integer array nums.
Find: all unique triplets [nums[i], nums[j], nums[k]] such that i != j != k
      and nums[i] + nums[j] + nums[k] == 0.
Constraints to keep in mind: duplicates in input are common, output triplets
must be unique (no duplicate triplets), order inside a triplet / between
triplets usually doesn't matter for correctness checks.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Can nums contain duplicates? (Yes -> must dedupe triplets)
- Can we sort / mutate the input array? (Usually yes, and it's the key enabler)
- What if len(nums) < 3? (Return empty list)
- Does the order of triplets or elements inside a triplet matter? (No)
- Are we optimizing for time or space? (Time -> O(n^2) is the expected bar)
"""

# ================================================================================
# MY APPROACH (as given) — Sort + Two Pointers, target = -nums[i]
# ================================================================================
"""
### Idea
Sort the array first. Fix one element nums[i] as the "anchor". Now finding two
other numbers that sum to -nums[i] is just the classic sorted-array 2Sum,
solved with two pointers (l, r) closing in from both ends.

### Why does it work?
Once sorted:
- If the 3 numbers sum too high -> the right pointer (largest) must shrink.
- If the sum is too low -> the left pointer (smallest) must grow.
This monotonic property is exactly what lets two pointers scan in O(n) instead
of checking every pair (which would be O(n^2) per anchor).

### Complexity
- TC: O(n^2)  -> O(n log n) for sort + O(n) anchors * O(n) two-pointer scan
- SC: O(1) extra (ignoring the output list; sort is in-place, some
      languages' sort uses O(log n) internally)

### Pros
- Optimal known complexity for this problem.
- No extra hash structures — very memory-light.
- Naturally handles duplicate skipping via sorted order.

### DSA Buddy Point 🧠
"3Sum is just 2Sum wearing a trench coat — fix one number, sorted-two-pointer
the rest."

### What can be improved?
Nothing algorithmically — O(n^2) is the accepted optimal for 3Sum (no
sub-quadratic general solution is known). The only real gains left are
*readability* and *micro-cleanliness* of the code, which is exactly what the
second version below does.
"""


def three_sum_v1(nums: list[int]) -> list[list[int]]:
    result = []
    nums.sort()
    for i in range(len(nums)):
        if nums[i] > 0:                       # smallest number positive -> no triplet can sum to 0
            break
        if i > 0 and nums[i] == nums[i - 1]:  # skip duplicate anchors
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            curr = nums[l] + nums[r] + nums[i]
            if curr == 0:
                result.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:   # skip dup left
                    l += 1
                while l < r and nums[r] == nums[r + 1]:   # skip dup right
                    r -= 1
            elif curr < 0:
                l += 1
            else:
                r -= 1
    return result


# ================================================================================
# CLEANER VARIANT (your second version) — same algorithm, tighter bookkeeping
# ================================================================================
"""
### What actually changed?
This is NOT a new approach or a complexity improvement — it's the same
sort + two-pointer algorithm, refactored:
1. `enumerate(nums)` instead of indexing `nums[i]` repeatedly.
2. Precomputes `target = -num` once per anchor, so the inner loop compares
   `nums[l] + nums[r] == target` instead of recomputing `nums[l]+nums[r]+num`
   every iteration (saves one addition per step — negligible in Big-O, but a
   nice micro-optimization / readability win).

### Complexity — unchanged
- TC: O(n^2)
- SC: O(1) extra

### Pros
- Slightly more readable (named `target`).
- Marginally fewer redundant additions in the hot loop.

### Cons
- Same as v1: still O(n^2), duplicate-skip logic must be written carefully
  or it silently produces duplicate triplets / misses cases.

### DSA Buddy Point 🧠
"When two versions have identical Big-O, the only honest comparison left is
readability and constant-factor cleanliness — don't confuse a refactor with
an optimization."
"""


def three_sum_v2(nums: list[int]) -> list[list[int]]:
    nums.sort()
    output = []
    for idx, num in enumerate(nums):
        if num > 0:
            break
        if idx != 0 and nums[idx] == nums[idx - 1]:
            continue
        l, r = idx + 1, len(nums) - 1
        target = -num
        while l < r:
            if nums[l] + nums[r] == target:
                output.append([nums[l], num, nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                while l < r and nums[r] == nums[r + 1]:
                    r -= 1
            elif nums[l] + nums[r] < target:
                l += 1
            else:
                r -= 1
    return output


# ================================================================================
# ALTERNATIVE APPROACH — Brute Force (for contrast only, not recommended)
# ================================================================================
"""
### Thought Process 🧠
The most naive idea: just try every triplet of indices and check the sum.
No sorting, no cleverness — pure brute force.

### Idea
Three nested loops over i < j < k, check nums[i]+nums[j]+nums[k] == 0,
dedupe using a set of sorted tuples (since we have no sorted-order trick
to skip duplicates cheaply).

### Complexity
- TC: O(n^3) — three nested loops
- SC: O(n) to O(n^2) — for the dedup set of triplets

### Pros
- Extremely simple to write, easy to explain from first principles.

### Cons
- Way too slow for n up to 3000-10000 (typical constraints) — TLE territory.
- Dedup logic without sorting is clunky (need a set of tuples).

### Bottleneck
Repeated work: for each anchor i, we re-scan all pairs (j, k) from scratch
with no ordering info to prune the search. Ask: "can we avoid rechecking
every pair once we fix one number?" -> Yes: sort + two pointers (our main
approach above).
"""


def three_sum_brute_force(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    seen = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    seen.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in seen]


# ================================================================================
# ALTERNATIVE APPROACH — Hashing (fix one, use a set for the other two)
# ================================================================================
"""
### Thought Process 🧠
Instead of two pointers, fix i, then walk j from i+1 to end and check if
`-(nums[i]+nums[j])` has been seen before in a hash set for this anchor.
This avoids sorting-based pointer movement but needs careful dedup.

### Approach
1. Sort nums (still needed for easy duplicate-triplet skipping).
2. For each i (skip duplicate anchors):
   - Use a local set `seen` for the inner loop.
   - For each j > i: complement = -(nums[i] + nums[j]).
     If complement in seen -> found a triplet. Skip duplicate j's.
     Add nums[j] to seen.

### Complexity
- TC: O(n^2) — same as two pointers
- SC: O(n) — extra hash set per anchor (worse space than two pointers' O(1))

### Pros
- Doesn't rely on two-pointer "monotonic shrink" reasoning — some find it
  more intuitive coming from 2Sum-with-hashmap.

### Cons
- Extra O(n) space per anchor vs O(1) for two pointers.
- Duplicate handling is a bit fiddlier without pointer symmetry.

### Remember 🧠
"Two-pointer and hash-set are two doors into the same O(n^2) room — pick
two-pointer when you want O(1) space, hash-set when the array isn't sorted
and you don't want to sort it."
"""


def three_sum_hashset(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    n = len(nums)
    for i in range(n):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        seen = set()
        for j in range(i + 1, n):
            complement = -(nums[i] + nums[j])
            if complement in seen:
                result.append([nums[i], complement, nums[j]])
                while j + 1 < n and nums[j] == nums[j + 1]:  # skip dup j
                    j += 1
            seen.add(nums[j])
    return result


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
3SUM
│
├── Start
│   └── Try every triplet (brute force)
│       └── O(n^3)
│
├── Bottleneck
│   └── Repeated pair search per anchor, no ordering to prune
│
├── Observation
│   └── Fix one number -> remaining problem is just 2SUM
│
├── Two Doors Out of 2SUM
│   ├── Sort + Two Pointers -> O(n^2) time, O(1) space   <-- your solution
│   └── Hash Set per anchor -> O(n^2) time, O(n) space
│
└── Duplicate Handling
    ├── Skip duplicate anchors (i > 0 and nums[i] == nums[i-1])
    └── Skip duplicate l/r (or j) after a match is found
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "3SUM -> Fix one -> solve 2SUM."
- "Sorted array + pair target -> Two Pointers."
- "Duplicates + sorted data -> skip neighbors, and skip AFTER a match too."
- "O(n^2) is the accepted optimal for 3Sum — don't hunt for O(n log n)."
- "Same Big-O, different code -> that's a refactor, not an optimization."
- "Two-pointer trades a hash set's O(n) space for O(1) space, same time."
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach              | Core Idea                          | TC     | SC   | Pros                          | Cons                              | When to Use                       |
|------------------------|-------------------------------------|--------|------|-------------------------------|-------------------------------------|-------------------------------------|
| Brute Force            | Check every triplet                 | O(n^3) | O(n) | Trivial to write               | Way too slow, clunky dedup          | Never in interview, only baseline   |
| Hash Set per anchor    | Fix i, hash j/k pair                 | O(n^2) | O(n) | Intuitive from 2Sum-hashmap    | Extra space, fiddly dup handling    | Array not sortable / order matters  |
| Sort + Two Pointers    | Fix i, two-pointer sorted 2Sum       | O(n^2) | O(1) | Optimal, O(1) space, clean dedup | Requires sorting (mutates/copies)  | Default/optimal choice (your code)  |

--------------------------------------------------------------------------------
INTERVIEW SNAPSHOT
--------------------------------------------------------------------------------
- Pattern: Fix one element -> reduce k-Sum to (k-1)-Sum.
- Go-to answer: "Sort, then for each i use two pointers to solve the 2Sum
  subproblem in O(n), giving O(n^2) overall with O(1) extra space."
- Mention brute force only to show you know the O(n^3) baseline and why we
  move past it (repeated work with no pruning).
- Always call out duplicate handling explicitly — it's the #1 place
  interviewers probe for bugs.
"""


if __name__ == "__main__":
    tests = [
        [-1, 0, 1, 2, -1, -4],
        [0, 1, 1],
        [0, 0, 0],
        [],
        [0, 0, 0, 0],
    ]
    for t in tests:
        print(t, "->", sorted(three_sum_v2(t.copy())))