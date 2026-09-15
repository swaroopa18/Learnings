# ============================================================
# LC 713 - Subarray Product Less Than K
# ALL VARIANTS SIDE BY SIDE
# ============================================================
# Problem:
#   Count the number of contiguous subarrays whose product
#   is strictly less than k.
#
# Assumption:
#   nums contains POSITIVE integers.
#
# Main progression:
#
#   V1 → Brute Force
#   V2 → Sliding Window
#
# Complexity:
#
#   V1 → O(n²) time, O(1) space
#   V2 → O(n)  time, O(1) space
#
# ============================================================


from typing import List


# ============================================================
# VARIANT 1: Brute Force
# ============================================================
# STYLE:
#   Fix the starting point and expand the ending point.
#
# MENTAL MODEL:
#   "For every possible start, keep multiplying elements
#    until the product becomes too large."
#
# KEY INSIGHT:
#   Because all nums are POSITIVE:
#
#       Once product >= k,
#       adding another number can never make it smaller.
#
#   Therefore we can safely `break`.
#
# ============================================================

class V1_BruteForce:
    def numSubarrayProductLessThanK(
        self,
        nums: List[int],
        k: int
    ) -> int:

        count = 0

        for i in range(len(nums)):

            mult = 1

            for j in range(i, len(nums)):

                mult *= nums[j]

                if mult < k:
                    count += 1

                else:
                    # Product can only stay the same or increase
                    # because nums contains positive integers.
                    break

        return count


# ============================================================
# V1 COMPLEXITY
# ============================================================
#
# Time:
#   O(n²)
#
# Space:
#   O(1)
#
# Why O(n²)?
#
#   In the worst case, every starting position expands almost
#   all the way to the end.
#
# Example:
#
#   nums = [1, 1, 1, 1, 1]
#
#   We examine:
#
#       i=0 → 5 elements
#       i=1 → 4 elements
#       i=2 → 3 elements
#       i=3 → 2 elements
#       i=4 → 1 element
#
#   Total ≈ n² / 2
#
# ============================================================


# ============================================================
# VARIANT 2: Sliding Window
# ============================================================
# STYLE:
#   Maintain a valid window using TWO POINTERS.
#
# POINTERS:
#
#       start → left side of window
#       end   → right side of window
#
# STATE:
#
#       mult  = product of current window
#       count = number of valid subarrays
#
# MENTAL MODEL:
#
#   "Expand the window by adding nums[end].
#
#    If the product becomes too large,
#    shrink from the left until it becomes valid again.
#
#    Once the window is valid, count ALL valid subarrays
#    ending at `end`."
#
# ============================================================

class V2_SlidingWindow:
    def numSubarrayProductLessThanK(
        self,
        nums: List[int],
        k: int
    ) -> int:

        # Every positive integer is >= 1.
        # Therefore if k <= 1, no product can be < k.
        if k <= 1:
            return 0

        count, start, mult = 0, 0, 1

        for end, num in enumerate(nums):

            # ------------------------------------------------
            # STEP 1: Expand
            # ------------------------------------------------
            mult *= num

            # ------------------------------------------------
            # STEP 2: Shrink while invalid
            # ------------------------------------------------
            while mult >= k:
                mult //= nums[start]
                start += 1

            # ------------------------------------------------
            # STEP 3: Count ALL valid subarrays ending at end
            # ------------------------------------------------
            count += end - start + 1

        return count


# ============================================================
# WHY `while mult >= k`?
# ============================================================
#
# We need:
#
#       product < k
#
# So whenever:
#
#       product >= k
#
# the window is invalid.
#
# Keep removing elements from the left until:
#
#       product < k
#
# ============================================================


# ============================================================
# THE MOST IMPORTANT LINE
# ============================================================
#
#       count += end - start + 1
#
# This is the key sliding-window trick.
#
# Once the current window is valid:
#
#       [start ........ end]
#
# Every subarray ending at `end` and starting anywhere
# from `start` to `end` is also valid.
#
#
# Example:
#
#       nums = [10, 5, 2]
#       k = 100
#
# Current window:
#
#       [10, 5, 2]
#        ^       ^
#      start    end
#
# Valid subarrays ending at end:
#
#       [10, 5, 2]
#       [5, 2]
#       [2]
#
# Number of them:
#
#       end - start + 1
#       = 2 - 0 + 1
#       = 3
#
# So:
#
#       count += 3
#
# ============================================================


# ============================================================
# WHY DOES THIS WORK?
# ============================================================
#
# nums contains POSITIVE integers.
#
# If:
#
#       product(nums[start ... end]) < k
#
# then removing elements from the LEFT can only make the
# product smaller.
#
# Therefore:
#
#       nums[start ... end]       valid
#       nums[start+1 ... end]     valid
#       nums[start+2 ... end]     valid
#       ...
#       nums[end ... end]         valid
#
# So there are exactly:
#
#       end - start + 1
#
# valid subarrays ending at `end`.
#
# ============================================================

# ============================================================
# COMPARISON TABLE
# ============================================================
#
#  Variant          Technique          Time      Space
#  ───────────────  ─────────────────  ────────  ───────
#  V1 Brute Force   Nested loops       O(n²)     O(1)
#  V2 Sliding       Two pointers       O(n)      O(1)
#
#
# BEST FOR:
#
#   V1 → First solution / understanding the problem
#
#   V2 → Interview / optimal solution
#
# ============================================================


# ============================================================
# PATTERN RECOGNITION
# ============================================================
#
# This problem is a classic:
#
#       POSITIVE NUMBERS + CONTIGUOUS SUBARRAY
#       + MONOTONIC CONDITION
#
# Think:
#
#       → Sliding Window
#
#
# Why does positive matter?
#
# Because when we expand:
#
#       product *= nums[end]
#
# the product cannot decrease.
#
# And when we shrink:
#
#       product //= nums[start]
#
# the product cannot increase.
#
# This monotonic behavior allows the two-pointer technique.
#
# ============================================================


# ============================================================
# IMPORTANT EDGE CASE
# ============================================================
#
#       if k <= 1:
#           return 0
#
# Why?
#
# nums contains positive integers.
#
# Minimum possible subarray product = 1.
#
# We need:
#
#       product < k
#
# If:
#
#       k = 1
#
# then we need:
#
#       product < 1
#
# impossible.
#
# Same for k < 1.
#
# ============================================================

# ============================================================
# FINAL TAKEAWAY
# ============================================================
#
# V1 BRUTE FORCE:
#
#   "Try every start and expand the end.
#    Stop when product >= k."
#
#
# V2 SLIDING WINDOW:
#
#   "Expand right.
#    If product becomes too large, shrink left.
#    Once valid, every subarray ending at right is valid."
#
#
# THE CORE TEMPLATE:
#
#       if k <= 1:
#           return 0
#
#       start = 0
#       product = 1
#       count = 0
#
#       for end, num in enumerate(nums):
#
#           product *= num
#
#           while product >= k:
#               product //= nums[start]
#               start += 1
#
#           count += end - start + 1
#
#
# ============================================================
# ONE-LINE INTERVIEW EXPLANATION
# ============================================================
#
# "I maintain a sliding window whose product is always less
# than k; whenever it becomes invalid I shrink from the left,
# and once valid, there are end - start + 1 valid subarrays
# ending at end."
#
# For each end, every start from start to end forms one unique
# valid subarray—including the single element [nums[end]],
# so there are exactly end - start + 1 of them.
# ============================================================