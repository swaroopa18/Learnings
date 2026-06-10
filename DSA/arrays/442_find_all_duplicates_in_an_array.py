"""
LeetCode 442 - Find All Duplicates in an Array
https://leetcode.com/problems/find-all-duplicates-in-an-array/

Problem:
    Given an integer array nums of length n where all integers are in range [1, n]
    and each integer appears once or twice, return all integers that appear twice.
    Must run in O(n) time. Follow-up: without extra space (O(1)).
"""

from typing import List


# =============================================================================
# APPROACH 1: Frequency Array (Counter)
# =============================================================================
# Intuition:
#   Build a frequency table indexed by value. Since values are in [1, n],
#   a list of size n+1 works as a direct-address count array.
#
# Time Complexity:  O(n) — two linear passes over nums and frequencies
# Space Complexity: O(n) — extra list of size n+1
#
# Pros: Simple, easy to read
# Cons: Uses O(n) extra space — fails the follow-up constraint
# =============================================================================

class SolutionFrequency:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        frequencies = [0] * (len(nums) + 1)

        for num in nums:
            frequencies[num] += 1

        output = []
        for idx, frequency in enumerate(frequencies):
            if frequency == 2:
                output.append(idx)
        return output


# =============================================================================
# APPROACH 2: Cyclic Sort (In-place)
# =============================================================================
# Intuition:
#   Since values are in [1, n], each value v ideally sits at index v-1.
#   Use cyclic sort to place every number at its "home" index.
#   After sorting, any index i where nums[i] != i+1 holds a duplicate.
#
# Time Complexity:  O(n) — each element is swapped at most once
# Space Complexity: O(1) — sorting is done in-place (output list excluded)
#
# Pros: Meets the O(1) extra-space follow-up constraint
# Cons: Mutates the input array
# =============================================================================

class SolutionCyclicSort:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        i, n = 0, len(nums)
        output = set()  # set for O(1) duplicate-add safety during traversal

        while i < n:
            correct_idx = nums[i] - 1  # where nums[i] belongs

            if i == correct_idx:
                # Element is already at its home index — move on
                i += 1
            elif nums[i] == nums[correct_idx]:
                # Home index already has the same value → duplicate found
                output.add(nums[i])
                i += 1
            else:
                # Swap nums[i] to its correct position
                nums[i], nums[correct_idx] = nums[correct_idx], nums[i]

        return list(output)


# =============================================================================
# APPROACH 3: Index Negation (Optimal — O(n) time, O(1) space, read-friendly)
# =============================================================================
# Intuition:
#   Use the sign of nums[abs(v)-1] as a visited flag for value v.
#   First visit → negate. Second visit → already negative → duplicate.
#
# Time Complexity:  O(n) — single pass
# Space Complexity: O(1) — no extra data structures (output list excluded)
#
# Pros: Clean single-pass, no mutation of positions (only signs), very common
#       interview answer for this problem
# Cons: Also mutates the input array (sign bits)
# =============================================================================

class SolutionIndexNegation:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        output = []

        for v in nums:
            idx = abs(v) - 1          # map value to 0-based index
            if nums[idx] < 0:         # already flipped → seen before
                output.append(idx + 1)
            else:
                nums[idx] = -nums[idx]  # mark as visited

        return output


# =============================================================================
# APPROACH COMPARISON
# =============================================================================
#
# Approach             Time    Space   Mutates Input   Notes
# -------------------  ------  ------  --------------  --------------------------
# Frequency Array      O(n)    O(n)    No              Simplest; fails follow-up
# Cyclic Sort          O(n)    O(1)    Yes (swaps)     Good for understanding sort
# Index Negation       O(n)    O(1)    Yes (signs)     Best interview answer
#
# Recommended: Index Negation for interviews (clean single-pass O(1) space).
#              Frequency Array for clarity when space isn't constrained.
# =============================================================================