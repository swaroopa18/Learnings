"""
================================================================================
 PROBLEM: Search Insert Position (LeetCode 35)
================================================================================
Given: a SORTED array `nums` of distinct integers, and a `target` value.
Task: return the index of `target` if it exists in `nums`. If it doesn't
exist, return the index where it WOULD be inserted to keep the array
sorted.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Is nums guaranteed sorted and distinct? (Yes — both are required for
  binary search to work cleanly here)
- What if target is smaller than every element, or larger than every
  element? (Insert at index 0, or at index len(nums), respectively)
- Can nums be empty? (Then the only valid answer is index 0)
"""

# ================================================================================
# 🔑🔑🔑  THE #1 RULE FOR BINARY-SEARCH BOUNDARIES  🔑🔑🔑
# ================================================================================
"""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   If your answer is the FIRST INVALID / first position AFTER       │
    │   the boundary  ──────────────────────────────────>  return `l`    │
    │                                                                     │
    │   If your answer is the LAST VALID / position BEFORE               │
    │   the boundary  ──────────────────────────────────>  return `r`    │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

THIS PROBLEM (searchInsert): we want the FIRST index where
`nums[index] >= target` — that's the FIRST position AFTER the "too
small" boundary is crossed -> return `l`.

Compare directly with mySqrt: there, the answer was the LAST VALID value
BEFORE the boundary -> `r`. Here, it's the FIRST position AFTER the
boundary -> `l`. Same rule, opposite side — this contrast is exactly why
memorizing the rule (instead of re-deriving it per problem) saves you
real time and avoids off-by-one panic in an interview.
"""

# ================================================================================
# BEGINNER-FRIENDLY WALKTHROUGH 🌱
# ================================================================================
"""
### Start with the simplest possible idea
If someone handed you the sorted list [1, 3, 5, 6] and asked "where does
5 go, or where WOULD 5 go?", the most natural approach is to just walk
through the list left to right: "Is 1 >= 5? No. Is 3 >= 5? No. Is 5 >= 5?
Yes! It belongs right here, at index 2." That's Linear Scan — walk until
you find the first element that's >= target; that position is your
answer (whether target is actually there or would be inserted there).

### Why binary search instead of scanning left to right?
Scanning works, but it's O(n) — for a huge sorted array, you might check
thousands of elements before finding the spot. Since the array is SORTED,
there's a much smarter way: you don't need to check every element in
order, because once you know `nums[mid] < target`, you also know
EVERYTHING to the left of mid is also less than target (sorted order
guarantees it) — so you can skip checking all of them individually.

### The key reframe: "find target" AND "find insert position" are the
    SAME search
Here's the beautiful trick in this specific problem: standard binary
search for "does target exist, and where" naturally ALSO tells you where
to insert it if it doesn't exist. Watch what happens when target isn't
found: `l` and `r` cross each other, and at that exact moment, `l` is
sitting EXACTLY where target would need to be inserted to keep the array
sorted. You don't need a separate "insert position" calculation — regular
binary search already computes it as a side effect of not finding a match.

### Step-by-step trace: searchInsert([1,3,5,6], target=2)
```
l=0, r=3   (searching indices 0..3)

Step 1: mid = (0+3)//2 = 1   -> nums[1]=3.  3 > 2 (target)
        target must be to the LEFT of index 1 -> r = mid-1 = 0

Step 2: l=0, r=0  -> mid = (0+0)//2 = 0   -> nums[0]=1.  1 < 2 (target)
        target must be to the RIGHT of index 0 -> l = mid+1 = 1

Step 3: l=1, r=0  -> l > r, loop ends!

Return l = 1.
Check: nums = [1, 3, 5, 6] -> inserting 2 at index 1 gives [1, 2, 3, 5, 6]
       which is still sorted. Correct! ✅
```

### Why does `l` end up being the answer, not `r`?
This is the MIRROR IMAGE of mySqrt's logic (where `r` was the answer).
Here, `l` only ever moves when we've PROVEN `nums[mid] < target` — so `l`
is always chasing "the first position where target COULD fit without
violating sorted order from the left." `r` only moves when
`nums[mid] > target` — ruling out mid and everything to its right. When
the loop ends, `l` has landed exactly on the first index where
`nums[index] >= target` — which is precisely the correct insert position
(or the index of target itself, if it's present).

### Building strong intuition: "which post lands on the gap?"
Same two-fence-post mental model as binary search on a range of numbers,
but now the "gap" we're looking for is a GAP BETWEEN ARRAY SLOTS, not a
single number. `l` creeps rightward past every element proven too small;
`r` creeps leftward past every element proven too big. They meet at the
exact gap where target belongs. Because `l` is the one that always
advances PAST "too small" elements, it naturally lands ON the first
"big enough" slot — which is exactly the insertion point.

### The "aha" moment to remember 🎯
"Find target, or the position to insert it" is really just "find the
first index where nums[index] >= target" — a single unified search. You
never need an if/else split between "found" and "not found" logic; plain
binary search, returning `l` at the end, answers both questions at once.
"""

# ================================================================================
# ALTERNATIVE APPROACH — Linear Scan
# ================================================================================
"""
### Idea
Walk through nums left to right; return the index of the first element
that is `>= target`. If no such element exists (target is bigger than
everything), the answer is `len(nums)` (insert at the very end).

### Complexity
- TC: O(n) — worst case, scan the entire array
- SC: O(1)

### Pros
- Very intuitive, no binary search bookkeeping required.

### Cons
- Doesn't exploit the fact that nums is SORTED — throws away the one
  piece of structure that makes this problem binary-searchable.

### Bottleneck
Once `nums[i] < target`, sorted order guarantees `nums[0..i]` are ALL
less than target too — checking each of them individually is redundant
information we already had for free. Ask: "can I discard a whole chunk of
candidates at once, instead of ruling out one element per check?" -> Yes:
binary search (the main approach above).
"""


def search_insert_linear(nums: list[int], target: int) -> int:
    for i, num in enumerate(nums):
        if num >= target:
            return i
    return len(nums)


# ================================================================================
# MY APPROACH — Binary Search (find first index where nums[i] >= target)
# ================================================================================
"""
### Idea
Standard binary search for `target`. If found, return its index directly.
If the loop ends without finding it, `l` has naturally converged to the
correct insert position (see the walkthrough above for exactly why).

### Complexity
- TC: O(log n) — search range halves every iteration
- SC: O(1)

### Pros
- Optimal time complexity for a sorted-array search.
- One unified piece of logic handles BOTH "found" and "not found" cases —
  no extra post-processing needed for the insert-position case.

### DSA Buddy Point 🧠
"Search Insert Position is just binary search where the 'not found' exit
condition already IS the answer you want — no separate insert-position
calculation required."

### What can be improved?
Nothing — O(log n) is optimal for search over a sorted array, since any
algorithm must be able to distinguish between at least n+1 possible
outcomes (insert at any of n+1 gaps, or match one of n elements), which
requires at least log2(n+1) comparisons in the worst case.
"""


def search_insert(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1

    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            l = mid + 1
        else:
            r = mid - 1
    return l


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
SEARCH INSERT POSITION
│
├── Linear Scan
│   └── Walk left to right, return first index with nums[i] >= target
│       └── O(n) time
│
├── Bottleneck
│   └── Sorted order already tells us "everything left of a too-small
│       element is also too small" — scanning one at a time ignores this
│
├── Key Reframe
│   └── "Find target OR its insert position" = "find first index where
│       nums[index] >= target" — ONE unified search, not two separate cases
│
└── Optimization — Binary Search
    ├── Standard binary search for target
    ├── If found: return mid directly
    └── If not found: l naturally lands on the correct insert position
        └── O(log n) time, O(1) space  <-- optimal, your code
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "'Insert into a sorted array to keep it sorted' -> binary search for the
  first index where nums[index] >= target. Found or not-found is the same
  search."
- "This is the MIRROR of mySqrt's boundary logic: there, `r` held the
  answer on 'not found' (largest value still valid). Here, `l` holds the
  answer on 'not found' (first index big enough) — know which one your
  problem needs based on whether you're bounding from below or above."
- "No post-processing needed after the loop — the natural resting point
  of `l` when the loop ends IS the insert position, by construction."
- "Distinct sorted elements + 'find target or nearest valid position' is
  the classic binary-search-for-boundary pattern (same family as
  'first/last occurrence of target in sorted array with duplicates')."
"""

# ================================================================================
# STRONG UNDERSTANDING CHECK 💪
# ================================================================================
"""
If you can confidently answer these without looking back up, you've truly
internalized this problem (not just memorized the code):

1. Q: Why does `l` hold the answer here, but `r` held the answer in
      mySqrt?
   A: It depends on which direction you're "chasing." In mySqrt, we
      wanted the LARGEST value still satisfying a <= condition, so `r`
      (which only shrinks when something is proven TOO BIG) ends up
      resting on the last valid value. Here, we want the FIRST index
      satisfying a >= condition, so `l` (which only grows when something
      is proven TOO SMALL) ends up resting on the first valid index.
      🔑 Rule check: our answer is the FIRST position AFTER the boundary
      -> the rule says return `l`. This IS that rule in action.

2. Q: What would go wrong if nums contained DUPLICATE values equal to
      target?
   A: Nothing breaks for THIS problem (returning any index where
      nums[index] == target is acceptable), but if the problem instead
      asked for "the FIRST occurrence of target," you'd need to keep
      searching left even after finding a match (move `r = mid - 1`
      instead of returning immediately) to make sure you land on the
      leftmost equal element.

3. Q: Why is nums required to be sorted and distinct for this exact
      solution to work?
   A: Sorted order is what makes "nums[mid] < target implies everything
      left of mid is also < target" TRUE — without sorting, eliminating
      half the array based on one comparison would be invalid. Distinct
      values simplify the "found" case (only one possible index to
      return) but aren't strictly required for the insert-position logic
      to still make sense.

4. Q: If target is smaller than nums[0], what index does this code
      return, and why?
   A: Index 0. Every comparison will find `nums[mid] > target`, so `r`
      keeps shrinking (r = mid-1) every step until it goes below 0, while
      `l` never moves from 0. The loop ends with `l = 0`, correctly
      indicating "insert at the very front."

5. Q: If you had to explain this to someone who's never seen binary
      search before, in one sentence, what would you say?
   A: "I keep guessing the middle of the remaining sorted range, and
      whether my guess is too big or too small tells me which half still
      might contain (or should contain) the target — I throw away the
      other half every time, until there's nowhere left to look, and
      wherever I land is exactly where the target belongs."
"""


if __name__ == "__main__":
    tests = [
        ([1, 3, 5, 6], 5, 2),
        ([1, 3, 5, 6], 2, 1),
        ([1, 3, 5, 6], 7, 4),
        ([1, 3, 5, 6], 0, 0),
        ([], 5, 0),
        ([1], 1, 0),
    ]
    for nums, target, expected in tests:
        a = search_insert(nums, target)
        b = search_insert_linear(nums, target)
        assert a == expected == b, f"Mismatch on nums={nums}, target={target}: {a} vs {b}"
        print(f"nums={nums}, target={target} -> {a}")