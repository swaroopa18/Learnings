"""
================================================================================
 PROBLEM: Move Zeroes (LeetCode 283)
================================================================================
Given: an integer array nums.
Task: move all 0's to the end while maintaining the relative order of the
      non-zero elements. Must be done in-place, without making a copy of
      the array.

--------------------------------------------------------------------------------
INTERVIEW CLARIFYING QUESTIONS
--------------------------------------------------------------------------------
- Must this be done in-place with O(1) extra space? (Yes — that's the point)
- Do we need to minimize the total number of writes/swaps? (Nice-to-have,
  not required — this solution already keeps it low)
- Can nums be empty or have no zeros / all zeros? (Yes, handle both)
- Does relative order of non-zero elements matter? (Yes — must be preserved)
"""

# ================================================================================
# MY APPROACH — Two Pointers (Slow/Fast), Swap-in-place
# ================================================================================
"""
### Idea
Use two pointers:
- `first`  -> marks the next position where a non-zero element should land.
- `second` -> scans through the array looking for non-zero elements.

Whenever `second` finds a non-zero value, swap it into position `first`, then
advance `first`. `second` always advances every iteration regardless.

### Why does it work?
`first` never moves ahead of `second`, so it always points to either:
- the next zero waiting to be overwritten, or
- a spot already holding a non-zero value (in which case swapping with
  itself is a harmless no-op).
Because every non-zero found gets slotted in left-to-right, relative order
of non-zero elements is automatically preserved. Zeros just get pushed
rightward as a byproduct of the swaps.

### Complexity
- TC: O(n) — single pass, `second` visits every index once
- SC: O(1) — in-place swaps, no extra data structure

### Pros
- Single pass, optimal time and space.
- Very few swaps compared to naive "shift everything" approaches.
- No extra array/list needed at all.

### DSA Buddy Point 🧠
"`first` is your 'next non-zero slot', `second` is your scanner — classic
slow/fast pointer partition, same family as the Dutch National Flag /
partition-in-place pattern (like in quicksort's partition step)."

### What can be improved?
Nothing algorithmically — O(n) time / O(1) space is optimal (you must touch
every element at least once, and no extra space is allowed). This is the
gold-standard answer.
"""

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:

        # Two pointers:
        #
        # first  -> position where the next non-zero element
        #           should be placed.
        #
        # second -> scans through the entire array.
        #
        # At any point:
        #
        # [0 ... first-1]       -> all non-zero elements
        # [first ... second-1]  -> zeros / processed elements
        # [second ... end]      -> not processed yet
        first = 0
        second = 0

        # second scans every element in the array.
        while second < len(nums):

            # If we find a non-zero element,
            # it belongs at position 'first'.
            if nums[second] != 0:

                # Swap the non-zero element into the
                # next available position.
                #
                # If first == second, this is simply
                # swapping the element with itself.
                nums[first], nums[second] = nums[second], nums[first]

                # We have placed one non-zero element,
                # so move first to the next position.
                first += 1

                # Move second forward because this element
                # has now been processed.
                second += 1

            else:
                # nums[second] is zero.
                #
                # We don't need to do anything with it.
                # Just continue scanning for the next
                # non-zero element.
                second += 1


# ================================================================================
# MIND MAP 🧠
# ================================================================================
"""
MOVE ZEROES
│
├── Constraint
│   └── In-place, O(1) space, preserve order of non-zeros
│
├── Naive Idea
│   └── Copy non-zeros to a new array, then fill rest with zeros
│       └── O(n) time but O(n) EXTRA space — violates in-place constraint
│
├── Observation
│   └── We just need a "write pointer" for the next non-zero slot
│
├── Optimization
│   └── Two Pointers (first = write slot, second = scanner) -> O(n) time, O(1) space
│
└── Pattern Family
    └── Partition-in-place (same spirit as quicksort partition,
        Dutch National Flag, remove-duplicates-from-sorted-array)
"""

# ================================================================================
# STRONG POINTS TO REMEMBER 🧠
# ================================================================================
"""
- "In-place + preserve order -> two pointers: one writes, one scans."
- "Swap instead of overwrite -> zeros drift to the end for free."
- "This is the same partitioning idea as quicksort's partition step."
- "O(n) time / O(1) space is optimal — you can't do better than touching
  each element once with no extra memory."
"""

# ================================================================================
# INTERVIEW SNAPSHOT
# ================================================================================
"""
- Pattern: Two Pointers — write pointer + scan pointer, in-place partition.
- Go-to answer: "Walk the array with a scan pointer; every time I find a
  non-zero, swap it into the next 'write' slot and advance both — zeros
  naturally end up pushed to the back, in O(n) time and O(1) space."
- Common follow-up: "Can you do it with fewer writes when there are very
  few zeros?" -> Yes, this swap-based version already only writes when
  needed (skips no-op swaps in spirit, though it still executes the swap
  statement — a micro-optimization would check `first != second` before
  swapping to avoid a redundant assignment).
"""