# ================================================================================
# PROBLEM: Find First and Last Position of Element in Sorted Array (LeetCode 34)
# ================================================================================
"""
Given: a sorted array `nums` of integers and an integer `target`.

Task: return the starting and ending position of `target` in `nums`.
If `target` is not present, return `[-1, -1]`.

The solution must run in O(log n) time.

Example:
    nums = [5, 7, 7, 8, 8, 10]
    target = 8
    output = [3, 4]
"""

# --------------------------------------------------------------------------------
# INTERVIEW CLARIFYING QUESTIONS
# --------------------------------------------------------------------------------
"""
- Is `nums` guaranteed to be sorted? (Yes, in non-decreasing order.)
- Can duplicate values exist? (Yes — that is the main challenge.)
- What should be returned if the target is absent? ([-1, -1].)
- Is O(log n) required? (Yes — a linear scan would not satisfy the requirement.)
- Should we return indices or values? (Indices.)
"""

# ================================================================================
# 🔑🔑🔑 STRONG POINTS FOR "SEARCH RANGE" PROBLEMS 🔑🔑🔑
# ================================================================================
"""
1. Standard binary search finds ANY occurrence, but that is not enough.
   We need the FIRST and LAST occurrence.

2. Once we find one valid occurrence at `mid`, we can search:
   - Left side: find the earliest index containing `target`.
   - Right side: find the latest index containing `target`.

3. The left-boundary search uses a normal midpoint:
       middle = (lower + upper) // 2

4. The right-boundary search uses an upper-biased midpoint:
       middle = (lower + upper + 1) // 2

   The upper bias is essential when assigning:
       lower = middle

   Without it, the loop can get stuck when `lower` and `upper`
   are adjacent.

5. Because the array is sorted:
   - Values smaller than target are always to the left.
   - Values greater than target are always to the right.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea

We could scan the entire array and record every index where:
    nums[i] == target

That works, but it takes O(n) time.

The problem asks for O(log n), so we need binary search.

### Key insight

First, use binary search to find any occurrence of `target`.

Suppose:
    nums = [5, 7, 7, 8, 8, 10]
    target = 8

After finding an occurrence at index 3 or 4:

- Search between the original left boundary and `mid` to find
  the first occurrence.
- Search between `mid` and the original right boundary to find
  the last occurrence.

### Why the left search works

If `nums[middle] == target`, the target might appear earlier,
so move the upper boundary left:

    upper = middle

Otherwise, `nums[middle] < target` within this search range,
so move right:

    lower = middle + 1

When the loop ends, `lower == upper`, and that index is the
first occurrence.

### Why the right search works

If `nums[middle] == target`, the target might appear later,
so move the lower boundary right:

    lower = middle

Otherwise, the target cannot be at `middle` or to its right
within the current range, so move left:

    upper = middle - 1

Use an upper-biased midpoint:

    middle = (lower + upper + 1) // 2

This guarantees progress when only two candidates remain.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Linear Scan
# ================================================================================
"""
### Thought Process

Walk through the array and record the first and last index where
`nums[i] == target`.

### Complexity
- TC: O(n)
- SC: O(1), excluding the output

### Pros
- Very easy to understand.
- Straightforward to implement.

### Cons
- Does not satisfy the required O(log n) time complexity.
- Does not use the sorted property of the array.
"""

def search_range_linear(nums: list[int], target: int) -> list[int]:
    first = -1
    last = -1

    for i, value in enumerate(nums):
        if value == target:
            if first == -1:
                first = i
            last = i

    return [first, last]


# ================================================================================
# MY APPROACH — Find Any Occurrence, Then Search Both Boundaries
# ================================================================================
"""
### Idea

1. Run a normal binary search.
2. When `nums[mid] == target`, call:
   - `find_first(l, mid)`
   - `find_last(mid, r)`
3. If the target is never found, return [-1, -1].

### Complexity
- TC: O(log n)
  - Initial binary search: O(log n)
  - First-boundary search: O(log n)
  - Last-boundary search: O(log n)
  - Total remains O(log n)
- SC: O(1) auxiliary space

### Why this approach is valid

The first and last searches operate only on ranges that contain
at least one known occurrence of the target: `mid`.

That means:
- `find_first(l, mid)` has a target at its right boundary.
- `find_last(mid, r)` has a target at its left boundary.
"""

def search_range(nums: list[int], target: int) -> list[int]:
    l, r = 0, len(nums) - 1

    def find_first(lower: int, upper: int) -> int:
        while lower < upper:
            middle = (lower + upper) // 2

            if nums[middle] == target:
                upper = middle
            else:
                lower = middle + 1

        return lower

    def find_last(lower: int, upper: int) -> int:
        while lower < upper:
            middle = (lower + upper + 1) // 2

            if nums[middle] == target:
                lower = middle
            else:
                upper = middle - 1

        return lower

    while l <= r:
        mid = (l + r) // 2

        if nums[mid] == target:
            return [
                find_first(l, mid),
                find_last(mid, r),
            ]
        elif nums[mid] > target:
            r = mid - 1
        else:
            l = mid + 1

    return [-1, -1]


# ================================================================================
# ALTERNATIVE APPROACH — Two Independent Boundary Searches
# ================================================================================
"""
### Thought Process

Instead of first finding any occurrence, perform two complete binary
searches:

1. Find the first occurrence:
   - When target is found, save `mid` and continue left.
2. Find the last occurrence:
   - When target is found, save `mid` and continue right.

This approach is often easier to explain because each helper has
one clear responsibility.

### Complexity
- TC: O(log n)
- SC: O(1)
"""

def search_range_two_searches(nums: list[int], target: int) -> list[int]:
    def find_first() -> int:
        l, r = 0, len(nums) - 1
        answer = -1

        while l <= r:
            mid = (l + r) // 2

            if nums[mid] == target:
                answer = mid
                r = mid - 1
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1

        return answer

    def find_last() -> int:
        l, r = 0, len(nums) - 1
        answer = -1

        while l <= r:
            mid = (l + r) // 2

            if nums[mid] == target:
                answer = mid
                l = mid + 1
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1

        return answer

    return [find_first(), find_last()]


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
SEARCH RANGE
│
├── Brute Force
│   └── Scan every element and track first/last matching index
│       └── O(n) time, O(1) auxiliary space
│
├── Key Observation
│   └── Sorted array allows us to discard half the search space
│
├── Path A — Find Any Match First
│   ├── Initial binary search finds one target occurrence
│   ├── Search left for first occurrence
│   ├── Search right for last occurrence
│   └── O(log n) time, O(1) space
│
└── Path B — Two Independent Searches
    ├── One binary search for the first occurrence
    ├── One binary search for the last occurrence
    └── O(log n) time, O(1) space
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- Finding any target occurrence is not the final goal.
  We need the leftmost and rightmost matching indices.

- When moving the lower pointer to `middle`, use an upper-biased midpoint:
      (lower + upper + 1) // 2

- When moving the upper pointer to `middle`, a normal midpoint is enough:
      (lower + upper) // 2

- The array must be sorted for binary search to work.

- If the target does not exist, return [-1, -1].

- Both the "find any match first" and "two independent searches"
  approaches run in O(log n) time and O(1) auxiliary space.
"""

# ================================================================================
# APPROACH COMPARISON
# ================================================================================
"""
| Approach                    | Core Idea                              | TC       | SC   |
|----------------------------|----------------------------------------|----------|------|
| Linear Scan               | Check every element                    | O(n)     | O(1) |
| Find Any + Boundaries     | Find one match, then search both ends  | O(log n) | O(1) |
| Two Independent Searches  | Search first and last separately       | O(log n) | O(1) |

### Interview recommendation

The current "find any match, then search both boundaries" approach
is efficient and valid.

The two-independent-searches approach is also excellent because
the boundary logic is isolated and easy to reason about.
"""

# ================================================================================
# INTERVIEW SNAPSHOT
# ================================================================================
"""
- Pattern: Binary Search for Boundaries
- Main challenge: Finding the first and last occurrence, not just
  any occurrence.
- Critical detail: Use an upper-biased midpoint when moving
  `lower = middle`.
- Complexity: O(log n) time, O(1) auxiliary space.
- Common bug: Using `(lower + upper) // 2` in the right-boundary
  search can cause an infinite loop when lower and upper are adjacent.
"""